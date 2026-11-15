// Riskly · copia il calendario economico sul database (tabella cal_eventi)
//
// La chiama pg_cron ogni minuto (vedi supabase/calendario-dati.sql), con l'intestazione x-cron.
//   - ogni minuto:     finestra vicina (6 ore fa → 36 ore avanti), per avere subito il dato effettivo
//   - ogni 30 minuti:  finestra larga (10 giorni fa → 35 giorni avanti) e pulizia dei dati più vecchi di 60 giorni
// Fonte principale TradingView. Se non risponde per 30 minuti di fila passa da sola a biquote.io
// (riserva gratuita) e torna a TradingView appena risponde. In tabella resta una sola fonte alla volta.
//
// Segreti: CRON_SECRET (lo stesso del job pg_cron). Pubblicata SENZA verifica JWT.

import { createClient } from "npm:@supabase/supabase-js@2";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const PAESI = ["US", "EU", "IT", "DE", "GB", "JP", "CH", "CA", "AU", "NZ", "CN"];
const MIN = 60_000, ORA = 60 * MIN, GIORNO = 24 * ORA;
const LIMITE_ERRORI = 30; // minuti di fila senza TradingView prima di passare alla riserva

type Riga = Record<string, unknown>;
const n = (v: unknown) => (v === null || v === undefined || v === "" || isNaN(Number(v)) ? null : Number(v));

async function daTradingView(da: Date, a: Date): Promise<Riga[]> {
  const u = `https://economic-calendar.tradingview.com/events?from=${da.toISOString()}&to=${a.toISOString()}&countries=${PAESI.join(",")}`;
  const r = await fetch(u, { headers: { Origin: "https://www.tradingview.com" }, signal: AbortSignal.timeout(15_000) });
  if (!r.ok) throw new Error("tradingview " + r.status);
  const j = await r.json();
  if (!Array.isArray(j.result)) throw new Error("tradingview risposta");
  return j.result.map((e: any) => ({
    id: String(e.id), date: e.date, country: String(e.country || "").toLowerCase(), currency: e.currency || null,
    title: e.title, indicator: e.indicator || null, ticker: e.ticker || null, period: e.period || null,
    importance: Number(e.importance ?? 0), actual: n(e.actual), forecast: n(e.forecast), previous: n(e.previous),
    unit: e.unit || null, scale: e.scale || null, comment: e.comment || null, source: e.source || null,
    source_url: e.source_url || null, fonte: "tradingview",
  }));
}

const IMP: Record<string, number> = { high: 1, medium: 0, low: -1 };
async function daBiquote(da: Date, a: Date): Promise<Riga[]> {
  const fuori: Riga[] = [], visti = new Set<string>();
  let dal = da.toISOString();
  for (let giro = 0; giro < 20; giro++) {
    const r = await fetch(`https://biquote.io/api/calendar?from=${dal}&to=${a.toISOString()}&limit=500`, { signal: AbortSignal.timeout(15_000) });
    if (!r.ok) throw new Error("biquote " + r.status);
    const j = await r.json();
    if (!Array.isArray(j)) throw new Error("biquote risposta");
    for (const e of j) {
      if (!PAESI.includes(String(e.countryCode)) || e.type === "holiday" && !e.name) continue;
      const id = "bq:" + e.id;
      if (visti.has(id)) continue;
      // il feed ripete lo stesso dato più volte (stesso evento, stessa ora): ne tengo uno, quello con più valori
      const doppio = "k:" + e.eventId + "|" + e.time;
      if (visti.has(doppio)) continue;
      visti.add(id); visti.add(doppio);
      fuori.push({
        id, date: e.time, country: String(e.countryCode).toLowerCase(), currency: e.currency || null,
        title: e.name, indicator: e.name, ticker: null, period: null, importance: IMP[e.importance] ?? 0,
        actual: n(e.actual), forecast: n(e.forecast), previous: n(e.revisedPrevious ?? e.previous),
        unit: e.unit === "percent" ? "%" : null, scale: null, comment: null, source: null,
        source_url: e.sourceUrl || null, fonte: "biquote",
      });
    }
    if (j.length < 500) break;
    const ultimo = j[j.length - 1].time;
    if (!ultimo || ultimo === dal) break;
    dal = ultimo;
  }
  return fuori;
}

async function salva(righe: Riga[]) {
  const ora = new Date().toISOString();
  for (let i = 0; i < righe.length; i += 500) {
    const pezzo = righe.slice(i, i + 500).map((r) => ({ ...r, aggiornato: ora }));
    const { error } = await db.from("cal_eventi").upsert(pezzo, { onConflict: "id" });
    if (error) throw new Error("db " + error.message);
  }
}

Deno.serve(async (req) => {
  if (req.headers.get("x-cron") !== Deno.env.get("CRON_SECRET")) return new Response("no", { status: 401 });
  const adesso = Date.now();
  const { data: st } = await db.from("cal_stato").select("*").eq("id", 1).maybeSingle();
  const stato = st || { fonte: "tradingview", errori_tv: 0, ultimo_largo: null };
  const largo = !stato.ultimo_largo || adesso - Date.parse(stato.ultimo_largo) >= 30 * MIN;
  const da = new Date(adesso - (largo ? 10 * GIORNO : 6 * ORA)), a = new Date(adesso + (largo ? 35 * GIORNO : 36 * ORA));

  let righe: Riga[] = [], fonte = stato.fonte, errori = stato.errori_tv, errore: string | null = null;
  try {
    righe = await daTradingView(da, a);
    errori = 0;
    if (fonte !== "tradingview") {
      // TradingView è tornato: tolgo la riserva e ricarico tutto da TradingView
      await db.from("cal_eventi").delete().eq("fonte", "biquote");
      fonte = "tradingview";
      if (!largo) righe = await daTradingView(new Date(adesso - 10 * GIORNO), new Date(adesso + 35 * GIORNO));
    }
  } catch (e) {
    errori++; errore = String(e);
    if (errori >= LIMITE_ERRORI) {
      try {
        const passo = fonte !== "biquote";
        righe = await daBiquote(passo ? new Date(adesso - 10 * GIORNO) : da, passo ? new Date(adesso + 35 * GIORNO) : a);
        if (passo && righe.length) { await db.from("cal_eventi").delete().gte("date", new Date(adesso - 10 * GIORNO).toISOString()).eq("fonte", "tradingview"); fonte = "biquote"; }
        if (!passo || fonte === "biquote") errore += " · riserva biquote attiva";
      } catch (e2) { errore += " · riserva: " + String(e2); righe = []; }
    }
  }

  try { if (righe.length && (fonte === "tradingview" ? righe[0].fonte === "tradingview" : true)) await salva(righe.filter((r) => r.fonte === fonte)); }
  catch (e) { errore = (errore ? errore + " · " : "") + String(e); }

  if (largo && !errore) await db.from("cal_eventi").delete().lt("date", new Date(adesso - 60 * GIORNO).toISOString());

  await db.from("cal_stato").upsert({
    id: 1, fonte, errori_tv: errori, ultimo_errore: errore,
    ...(errore ? {} : { ultimo_ok: new Date().toISOString() }),
    ...(largo && !errore ? { ultimo_largo: new Date().toISOString() } : {}),
    aggiornato: new Date().toISOString(),
  });
  return Response.json({ fonte, righe: righe.length, largo, errore });
});
