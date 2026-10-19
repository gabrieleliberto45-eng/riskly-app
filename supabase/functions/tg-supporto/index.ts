// Riskly · bot di supporto su Telegram
//
// Chi scrive al bot non vede mai l'account personale di Gabriele:
//   cliente → bot  : il messaggio viene inoltrato a Gabriele (TG_SUPPORTO_ADMIN), con nome e @ del cliente
//   Gabriele → bot : se RISPONDE a un messaggio inoltrato, la risposta arriva al cliente a nome del bot
// Telegram chiama questa funzione (webhook) con l'intestazione segreta TG_SUPPORTO_SEGRETO.
// Pubblicata SENZA verifica JWT. Tabelle: tg_supporto_msg, tg_supporto_utenti (vedi supabase/tg-supporto.sql).

import { createClient } from "npm:@supabase/supabase-js@2";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const TOKEN = Deno.env.get("TG_SUPPORTO_TOKEN")!;
const ADMIN = Number(Deno.env.get("TG_SUPPORTO_ADMIN") || 0);
const SEGRETO = Deno.env.get("TG_SUPPORTO_SEGRETO") || "";

const BENVENUTO =
  "Ciao, sei nel supporto di Riskly 👋\n\n" +
  "Scrivi qui la tua domanda su bot, corsi, journal o acquisti: ti rispondiamo in questa chat, di solito in giornata.\n\n" +
  "Se riguarda un acquisto, indica l'email che hai usato.\n\n" +
  "Riskly non dà segnali né consigli su cosa comprare o vendere.";
const RICEVUTO = "Ricevuto ✅ Ti rispondiamo qui il prima possibile.";

async function tg(metodo: string, corpo: Record<string, unknown>) {
  const r = await fetch(`https://api.telegram.org/bot${TOKEN}/${metodo}`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo),
  });
  return r.json();
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("ok");
  if (!SEGRETO || req.headers.get("x-telegram-bot-api-secret-token") !== SEGRETO) return new Response("no", { status: 401 });
  let u: any;
  try { u = await req.json(); } catch { return new Response("ok"); }
  const m = u.message;
  if (!m || !m.chat || m.chat.type !== "private") return new Response("ok");
  const chat = m.chat.id;

  try {
    // Gabriele: si dà l'ID con /id (serve solo per configurare); risponde ai clienti rispondendo ai messaggi inoltrati
    if (m.text === "/id") { await tg("sendMessage", { chat_id: chat, text: "Il tuo ID Telegram: " + chat }); return new Response("ok"); }

    if (chat === ADMIN) {
      const orig = m.reply_to_message;
      if (!orig) {
        await tg("sendMessage", { chat_id: chat, text: "Per rispondere a un cliente tieni premuto il suo messaggio e scegli «Rispondi»." });
        return new Response("ok");
      }
      const { data } = await db.from("tg_supporto_msg").select("utente_chat").eq("admin_msg", orig.message_id).maybeSingle();
      if (!data) {
        await tg("sendMessage", { chat_id: chat, text: "Non trovo il cliente di questo messaggio: rispondi al messaggio inoltrato, non all'intestazione." });
        return new Response("ok");
      }
      const r = await tg("copyMessage", { chat_id: data.utente_chat, from_chat_id: chat, message_id: m.message_id });
      await tg("sendMessage", { chat_id: chat, text: r.ok ? "Inviato ✓" : "Non inviato: il cliente potrebbe aver bloccato il bot.", reply_to_message_id: m.message_id });
      return new Response("ok");
    }

    // cliente
    if (m.text === "/start") { await tg("sendMessage", { chat_id: chat, text: BENVENUTO }); return new Response("ok"); }
    if (!ADMIN) return new Response("ok");

    const f = m.from || {};
    const chi = [f.first_name, f.last_name].filter(Boolean).join(" ") + (f.username ? " (@" + f.username + ")" : "") + " · id " + chat;
    const testa = await tg("sendMessage", { chat_id: ADMIN, text: "💬 " + chi });
    const copia = await tg("copyMessage", { chat_id: ADMIN, from_chat_id: chat, message_id: m.message_id });
    const righe = [testa, copia].filter((x: any) => x.ok).map((x: any) => ({ admin_msg: x.result.message_id, utente_chat: chat }));
    if (righe.length) await db.from("tg_supporto_msg").insert(righe);

    // conferma al cliente, al massimo una volta ogni 6 ore
    const { data: ut } = await db.from("tg_supporto_utenti").select("ultima_conferma").eq("chat", chat).maybeSingle();
    if (!ut || Date.now() - new Date(ut.ultima_conferma).getTime() > 6 * 3600 * 1000) {
      await tg("sendMessage", { chat_id: chat, text: RICEVUTO });
      await db.from("tg_supporto_utenti").upsert({ chat, ultima_conferma: new Date().toISOString() });
    }
  } catch (e) {
    console.error(e);
  }
  return new Response("ok");
});
