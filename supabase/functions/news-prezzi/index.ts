// Riskly News · quotazioni per la barra in alto del sito e prossimi dati USA di oggi
// GET → { prezzi: [{ s, nome, p, v, vp }], eventi: [{ ora, titolo, attese, precedente, effettivo }] }
// Prezzi da Yahoo Finance (ritardati di qualche minuto), eventi dal calendario di TradingView.
// Cache di 60 secondi in memoria per non chiamare le fonti a ogni visita. Pubblicata SENZA verifica JWT.

const SIMBOLI: [string, string, number][] = [
  ["GC=F", "XAU/USD", 1], ["EURUSD=X", "EUR/USD", 4], ["DX-Y.NYB", "DXY", 2],
  ["^TNX", "US 10A", 2], ["BZ=F", "BRENT", 2], ["^GSPC", "S&P 500", 0], ["BTC-USD", "BTC/USD", 0],
];
const IMPORTANTI = /(Nonfarm|Payroll|Unemployment Rate|CPI|PCE|PPI|GDP|Retail Sales|ISM|JOLT|Jobless Claims|ADP|Michigan|Fed Interest Rate|FOMC|Powell)/i;
let cache: { t: number; corpo: string } | null = null;

const cors = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, OPTIONS", "Content-Type": "application/json", "Cache-Control": "public, max-age=60" };

async function prezzo([s, nome, dec]: [string, string, number]) {
  try {
    const r = await fetch(`https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(s)}?range=1d&interval=5m`, { headers: { "User-Agent": "Mozilla/5.0" } });
    const m = (await r.json()).chart.result[0].meta;
    const p = m.regularMarketPrice, prec = m.chartPreviousClose;
    return { s, nome, dec, p, v: p - prec, vp: (p / prec - 1) * 100 };
  } catch { return null; }
}
async function eventi() {
  try {
    const oggi = new Date().toISOString().slice(0, 10);
    const r = await fetch(`https://economic-calendar.tradingview.com/events?from=${oggi}T00:00:00.000Z&to=${oggi}T23:59:00.000Z&countries=US`, { headers: { Origin: "https://www.tradingview.com" } });
    const j = await r.json();
    return (j.result || []).filter((e: any) => e.importance >= 1 && IMPORTANTI.test(e.title))
      .map((e: any) => ({ ora: e.date, titolo: e.title, attese: e.forecast, precedente: e.previous, effettivo: e.actual, unita: e.unit || "" }));
  } catch { return []; }
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });
  if (cache && Date.now() - cache.t < 60_000) return new Response(cache.corpo, { headers: cors });
  const [prezzi, ev] = await Promise.all([Promise.all(SIMBOLI.map(prezzo)), eventi()]);
  const corpo = JSON.stringify({ aggiornato: new Date().toISOString(), prezzi: prezzi.filter(Boolean), eventi: ev });
  cache = { t: Date.now(), corpo };
  return new Response(corpo, { headers: cors });
});
