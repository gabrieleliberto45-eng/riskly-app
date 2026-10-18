// Riskly · manda gli avvisi push del calendario
//
// La chiama pg_cron ogni minuto (vedi supabase/calendario-avvisi.sql), con l'intestazione x-cron.
// Per ogni iscritto e ogni dato preferito:
//   - 5 minuti prima       → "Tra 5 min: …"
//   - appena esce il valore → "Uscito: … effettivo / previsto / precedente"
// I dati arrivano dal calendario di TradingView, gli stessi che vede il sito.
//
// Segreti richiesti (Supabase → Edge Functions → Secrets):
//   VAPID_PUBLIC, VAPID_PRIVATE  (chiavi delle notifiche push)
//   CRON_SECRET                  (lo stesso scritto nel job di pg_cron)
// Pubblicata SENZA verifica JWT.

import { createClient } from "npm:@supabase/supabase-js@2";
import webpush from "npm:web-push@3.6.7";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
webpush.setVapidDetails("mailto:info@riskly.trade", Deno.env.get("VAPID_PUBLIC")!, Deno.env.get("VAPID_PRIVATE")!);

const BANDIERE: Record<string, string> = { us: "🇺🇸", eu: "🇪🇺", it: "🇮🇹", de: "🇩🇪", gb: "🇬🇧", jp: "🇯🇵", ch: "🇨🇭", ca: "🇨🇦", au: "🇦🇺", nz: "🇳🇿", cn: "🇨🇳" };
const MIN = 60_000;

function num(v: unknown, u?: string) {
  if (v === null || v === undefined || v === "") return "—";
  const n = Number(v);
  const t = isNaN(n) ? String(v) : n.toLocaleString("it-IT", { maximumFractionDigits: 2 });
  return t + (u === "%" ? "%" : u ? " " + u : "");
}
const ora = (d: Date) => d.toLocaleTimeString("it-IT", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/Rome" });

Deno.serve(async (req) => {
  if (req.headers.get("x-cron") !== Deno.env.get("CRON_SECRET")) return new Response("no", { status: 401 });
  const adesso = Date.now();
  const { data: righe, error } = await db.from("cal_iscrizioni").select("*");
  if (error) return new Response("db", { status: 500 });

  // quali preferiti sono vicini: 5 minuti prima, oppure usciti nelle ultime 3 ore
  const vicino = (d: string) => { const t = Date.parse(d); return t > adesso - 180 * MIN && t < adesso + 6 * MIN; };
  const servono = righe!.some((r) => Object.values(r.preferiti as Record<string, any>).some((x) => vicino(x.d)));
  let eventi: Record<string, any> = {};
  if (servono) {
    try {
      const u = `https://economic-calendar.tradingview.com/events?from=${new Date(adesso - 180 * MIN).toISOString()}&to=${new Date(adesso + 10 * MIN).toISOString()}&countries=US,EU,IT,DE,GB,JP,CH,CA,AU,NZ,CN`;
      const r = await fetch(u, { headers: { Origin: "https://www.tradingview.com" } });
      const j = await r.json();
      for (const e of j.result || []) eventi[e.id] = e;
    } catch { eventi = {}; }
  }

  let mandati = 0;
  for (const r of righe!) {
    const pref = r.preferiti as Record<string, { d: string; t: string; c: string }>;
    const inviati = { ...(r.inviati as Record<string, number>) };
    const nuovi: { tit: string; testo: string; tag: string }[] = [];
    let cambiato = false;

    for (const [id, x] of Object.entries(pref)) {
      const t = Date.parse(x.d), b = BANDIERE[x.c] || "";
      if (t > adesso && t - adesso <= 5 * MIN && !inviati[id + ":p"]) {
        inviati[id + ":p"] = adesso; cambiato = true;
        nuovi.push({ tit: `Tra ${Math.max(1, Math.round((t - adesso) / MIN))} min: ${x.t}`, testo: `${b} esce alle ${ora(new Date(t))}. Occhio a spread e stop stretti.`, tag: id + ":p" });
      }
      const e = eventi[id];
      if (e && e.actual !== null && e.actual !== undefined && e.actual !== "" && !inviati[id + ":u"] && t <= adesso + MIN) {
        inviati[id + ":u"] = adesso; cambiato = true;
        nuovi.push({ tit: `Uscito: ${x.t}`, testo: `${b} Effettivo ${num(e.actual, e.unit)} · previsto ${num(e.forecast, e.unit)} · precedente ${num(e.previous, e.unit)}`, tag: id + ":u" });
      }
    }
    // pulizia: via i preferiti e gli avvisi più vecchi di 2 giorni
    for (const [id, x] of Object.entries(pref)) if (Date.parse(x.d) < adesso - 2 * 1440 * MIN) { delete pref[id]; cambiato = true; }
    for (const k of Object.keys(inviati)) if (inviati[k] < adesso - 9 * 1440 * MIN) { delete inviati[k]; cambiato = true; }

    let morto = false;
    for (const n of nuovi) {
      try {
        await webpush.sendNotification({ endpoint: r.endpoint, keys: { p256dh: r.p256dh, auth: r.auth } },
          JSON.stringify({ titolo: n.tit, testo: n.testo, tag: n.tag }), { TTL: 600, urgency: "high" });
        mandati++;
      } catch (err: any) { if (err?.statusCode === 404 || err?.statusCode === 410) { morto = true; break; } }
    }
    if (morto) await db.from("cal_iscrizioni").delete().eq("endpoint", r.endpoint);
    else if (cambiato) await db.from("cal_iscrizioni").update({ preferiti: pref, inviati }).eq("endpoint", r.endpoint);
  }
  return new Response(JSON.stringify({ iscritti: righe!.length, mandati }), { headers: { "Content-Type": "application/json" } });
});
