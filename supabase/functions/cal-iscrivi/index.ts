// Riskly · iscrizione agli avvisi del calendario
//
// La chiama strumenti.riskly.trade quando l'utente attiva gli avvisi o cambia i preferiti.
//   POST   { sub: PushSubscription JSON, preferiti: { id: { d, t, c } } }  → salva
//   DELETE { endpoint }                                                  → toglie
// Pubblicata SENZA verifica JWT (la chiama il browser senza account).

import { createClient } from "npm:@supabase/supabase-js@2";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const ORIGINI = ["https://strumenti.riskly.trade", "https://riskly.trade"];
const SERVIZI = /^https:\/\/([a-z0-9-]+\.)*(push\.apple\.com|fcm\.googleapis\.com|googleapis\.com|push\.services\.mozilla\.com|notify\.windows\.com)\//;

function cors(req: Request) {
  const o = req.headers.get("origin") || "";
  return {
    "Access-Control-Allow-Origin": ORIGINI.includes(o) ? o : ORIGINI[0],
    "Access-Control-Allow-Methods": "POST, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    "Vary": "Origin",
  };
}
const risposta = (req: Request, s: number, b: unknown) =>
  new Response(JSON.stringify(b), { status: s, headers: { ...cors(req), "Content-Type": "application/json" } });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors(req) });
  let j: any;
  try { j = await req.json(); } catch { return risposta(req, 400, { errore: "json" }); }

  if (req.method === "DELETE") {
    if (typeof j?.endpoint !== "string") return risposta(req, 400, { errore: "endpoint" });
    await db.from("cal_iscrizioni").delete().eq("endpoint", j.endpoint);
    return risposta(req, 200, { ok: true });
  }
  if (req.method !== "POST") return risposta(req, 405, { errore: "metodo" });

  const s = j?.sub;
  if (typeof s?.endpoint !== "string" || !SERVIZI.test(s.endpoint) || s.endpoint.length > 1000 ||
      typeof s?.keys?.p256dh !== "string" || typeof s?.keys?.auth !== "string") return risposta(req, 400, { errore: "iscrizione" });

  // al massimo 60 preferiti, solo i campi che servono, testi corti
  const pref: Record<string, { d: string; t: string; c: string }> = {};
  for (const [id, x] of Object.entries(j?.preferiti || {}).slice(0, 60) as [string, any][]) {
    if (!/^[\w-]{1,40}$/.test(id) || isNaN(Date.parse(x?.d))) continue;
    pref[id] = { d: new Date(x.d).toISOString(), t: String(x?.t || "").slice(0, 120), c: String(x?.c || "").slice(0, 4) };
  }
  const { error } = await db.from("cal_iscrizioni").upsert({
    endpoint: s.endpoint, p256dh: s.keys.p256dh.slice(0, 200), auth: s.keys.auth.slice(0, 100),
    preferiti: pref, aggiornato: new Date().toISOString(),
  });
  if (error) return risposta(req, 500, { errore: "salvataggio" });
  return risposta(req, 200, { ok: true, preferiti: Object.keys(pref).length });
});
