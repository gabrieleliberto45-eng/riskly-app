// Riskly News · manda la notifica quando esce un articolo
//
// La chiama il database (trigger su public.notizie, vedi supabase/news-avvisi.sql) con { id }.
// Non serve un segreto: manda solo per un articolo pubblicato che non ha ancora avvisato
// (colonna avvisato), e la segna prima di mandare, quindi ogni articolo avvisa una volta sola.
// Nella notifica ci sono solo titolo e sommario, che sono già pubblici.
// Segreti: VAPID_PUBLIC, VAPID_PRIVATE (gli stessi degli avvisi del calendario).
// Pubblicata SENZA verifica JWT.

import { createClient } from "npm:@supabase/supabase-js@2";
import webpush from "npm:web-push@3.6.7";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
webpush.setVapidDetails("mailto:info@riskly.trade", Deno.env.get("VAPID_PUBLIC")!, Deno.env.get("VAPID_PRIVATE")!);

const ETICHETTA: Record<string, string> = {
  dati: "Dato appena uscito", fed: "Fed", tassi: "Tassi", oro: "Oro", dollaro: "Dollaro",
  setup: "Setup XAU", straordinarie: "Straordinaria", settimana: "La settimana",
};

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("no", { status: 405 });
  let id = "";
  try { id = String((await req.json())?.id || ""); } catch { return new Response("json", { status: 400 }); }
  if (!/^[\w-]{1,120}$/.test(id)) return new Response("id", { status: 400 });

  // la segno subito: se arriva una seconda chiamata per lo stesso articolo non trova niente
  const { data: a } = await db.from("notizie").update({ avvisato: new Date().toISOString() })
    .eq("id", id).eq("pubblicato", true).is("avvisato", null).select("id, categoria, titolo, sommario").maybeSingle();
  if (!a) return new Response(JSON.stringify({ mandati: 0, motivo: "già avvisato o non pubblicato" }), { headers: { "Content-Type": "application/json" } });

  const { data: righe } = await db.from("news_iscrizioni").select("*");
  const corpo = JSON.stringify({
    titolo: `${ETICHETTA[a.categoria] || "Riskly News"} · ${a.titolo}`.slice(0, 140),
    testo: String(a.sommario || "").slice(0, 220),
    url: "/#/" + a.id, tag: "news-" + a.id,
  });
  let mandati = 0; const morti: string[] = [];
  const lista = righe || [];
  for (let i = 0; i < lista.length; i += 50) {
    await Promise.all(lista.slice(i, i + 50).map(async (r) => {
      try {
        await webpush.sendNotification({ endpoint: r.endpoint, keys: { p256dh: r.p256dh, auth: r.auth } }, corpo, { TTL: 6 * 3600, urgency: "high" });
        mandati++;
      } catch (err: any) { if (err?.statusCode === 404 || err?.statusCode === 410) morti.push(r.endpoint); }
    }));
  }
  if (morti.length) await db.from("news_iscrizioni").delete().in("endpoint", morti);
  return new Response(JSON.stringify({ iscritti: lista.length, mandati, tolti: morti.length }), { headers: { "Content-Type": "application/json" } });
});
