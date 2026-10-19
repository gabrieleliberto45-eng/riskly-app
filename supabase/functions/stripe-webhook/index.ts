// Riskly · conferma automatica dei pagamenti Stripe
//
// Stripe chiama questa funzione dopo ogni pagamento. La funzione:
//  - checkout.session.completed → trova l'ordine "in_attesa" del cliente
//    (client_reference_id = id dell'account), lo mette "attivo" e,
//    se è un piano del journal, assegna il piano al profilo
//  - checkout.session.expired   → il cliente non ha pagato: ordine "rifiutato"
//  - customer.subscription.deleted → abbonamento al journal finito: piano tolto
//
// Segreti richiesti (Supabase → Edge Functions → Secrets):
//   STRIPE_WEBHOOK_SECRET  (whsec_..., dall'endpoint creato su Stripe)
// SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY ci sono già.
// La funzione va pubblicata SENZA verifica JWT (la chiama Stripe).

import { createClient } from "npm:@supabase/supabase-js@2";

const db = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);
const SEGRETO = Deno.env.get("STRIPE_WEBHOOK_SECRET") ?? "";

/* verifica la firma di Stripe (header Stripe-Signature: t=...,v1=...) */
async function firmaValida(corpo: string, header: string): Promise<boolean> {
  const parti = Object.fromEntries(
    header.split(",").map((p) => p.split("=") as [string, string]),
  );
  const t = parti["t"];
  const firme = header.split(",").filter((p) => p.startsWith("v1=")).map((p) => p.slice(3));
  if (!t || !firme.length || !SEGRETO) return false;
  if (Math.abs(Date.now() / 1000 - Number(t)) > 600) return false; // più di 10 minuti
  const chiave = await crypto.subtle.importKey(
    "raw", new TextEncoder().encode(SEGRETO),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"],
  );
  const mac = await crypto.subtle.sign("HMAC", chiave, new TextEncoder().encode(`${t}.${corpo}`));
  const atteso = [...new Uint8Array(mac)].map((b) => b.toString(16).padStart(2, "0")).join("");
  return firme.some((f) => f.length === atteso.length &&
    [...f].reduce((d, c, i) => d | (c.charCodeAt(0) ^ atteso.charCodeAt(i)), 0) === 0);
}

/* "Journal Pro annuale" → "pro" */
function pianoDa(prodotto: string): string | null {
  const m = /^journal\s+(base|pro|premium)\b/i.exec(prodotto || "");
  return m ? m[1].toLowerCase() : null;
}

/* Quale prodotto è stato pagato lo dice Stripe (il link di pagamento usato), mai l'ordine
   scritto dal sito: così nessuno può registrare un ordine "Pacchetto corsi" e poi pagare un
   prodotto più economico. Se si aggiunge un link di pagamento nuovo, va aggiunto qui. */
const PRODOTTO_DEL_LINK: Record<string, string> = {
  "plink_1UKhOcC4UovOoFaViANPN5Mb": "RiskGuard",
  "plink_1UNIISC4UovOoFaVZXl81nzK": "TradeManager",
  "plink_1UNIIUC4UovOoFaV9ay6TNvd": "ScaleIn",
  "plink_1UNIIVC4UovOoFaVKuWKL9K8": "Riskly Pro",
  "plink_1US1auC4UovOoFaVpeOX0XvC": "RisklyCopy",
  "plink_1UMnafC4UovOoFaVmg2vfWjr": "Videocorso",
  "plink_1US0PWC4UovOoFaVtAXaxLlA": "Corso Analisi fondamentale",
  "plink_1US0PXC4UovOoFaVpYdUys4l": "Pacchetto corsi",
  "plink_1UKhSEC4UovOoFaV0BuMbyu5": "Journal Base mensile",
  "plink_1UKhSFC4UovOoFaVxE2MhVGY": "Journal Base annuale",
  "plink_1UKhSHC4UovOoFaVrMoqepFq": "Journal Base a vita",
  "plink_1UKhSKC4UovOoFaVadAY1pUv": "Journal Pro mensile",
  "plink_1UKhSMC4UovOoFaVZ3qDfCCj": "Journal Pro annuale",
  "plink_1UKhSOC4UovOoFaVnGMgu50o": "Journal Pro a vita",
  "plink_1UKhSpC4UovOoFaV1rsuVXYt": "Journal Premium mensile",
  "plink_1UKhSqC4UovOoFaVUwcAf1SB": "Journal Premium annuale",
  "plink_1UKhSsC4UovOoFaVMKHFTaLQ": "Journal Premium a vita",
};

/* l'ordine in attesa dello stesso cliente e dello stesso prodotto, il più recente */
async function ordineDi(utente: string, prodotto: string) {
  const { data } = await db.from("acquisti").select("*")
    .eq("utente", utente).eq("stato", "in_attesa").eq("prodotto", prodotto)
    .order("creato", { ascending: false }).limit(1);
  return data && data.length ? data[0] : null;
}

async function pagato(s: any) {
  const utente = s.client_reference_id;
  if (!utente) return "nessun client_reference_id";
  const prodotto = PRODOTTO_DEL_LINK[s.payment_link];
  if (!prodotto) return "link di pagamento sconosciuto: " + s.payment_link + " (nessun prodotto attivato)";
  const importo = s.amount_subtotal != null ? s.amount_subtotal / 100 : null;

  /* Stripe può mandare lo stesso evento più volte: una sessione attiva un solo acquisto */
  const { data: gia } = await db.from("acquisti").select("id").eq("stripe_sessione", s.id).limit(1);
  if (gia && gia.length) return "sessione già registrata";

  const o = await ordineDi(utente, prodotto);
  if (o) {
    const { error } = await db.from("acquisti").update({ stato: "attivo", prezzo: importo ?? o.prezzo, stripe_sessione: s.id }).eq("id", o.id);
    if (error) throw new Error(error.message);
  } else {
    /* pagato senza ordine sul sito (es. link aperto da un'altra scheda): lo registriamo noi */
    const { error } = await db.from("acquisti").insert({ utente, prodotto, prezzo: importo, stato: "attivo", stripe_sessione: s.id });
    if (error) throw new Error(error.message);
  }

  const piano = pianoDa(prodotto);
  if (piano) {
    const agg: Record<string, unknown> = { piano };
    if (s.customer) agg.stripe_cliente = s.customer;
    let { error } = await db.from("profili").update(agg).eq("id", utente);
    if (error && agg.stripe_cliente) {           // colonna non ancora creata
      ({ error } = await db.from("profili").update({ piano }).eq("id", utente));
    }
    if (error) return "piano non assegnato: " + error.message;
  }
  return prodotto + " attivo";
}

async function scaduto(s: any) {
  const utente = s.client_reference_id;
  if (!utente) return "nessun client_reference_id";
  const prodotto = PRODOTTO_DEL_LINK[s.payment_link];
  if (!prodotto) return "link di pagamento sconosciuto";
  const o = await ordineDi(utente, prodotto);
  if (!o) return "nessun ordine in attesa";
  await db.from("acquisti").update({ stato: "rifiutato" }).eq("id", o.id);
  return "ordine " + o.id + " rifiutato";
}

async function abbonamentoFinito(sub: any) {
  if (!sub.customer) return "nessun cliente";
  const { error } = await db.from("profili")
    .update({ piano: "prova", scadenza: new Date().toISOString() })
    .eq("stripe_cliente", sub.customer);
  return error ? error.message : "piano tolto";
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("ok");
  const corpo = await req.text();
  if (!(await firmaValida(corpo, req.headers.get("stripe-signature") ?? ""))) {
    return new Response("firma non valida", { status: 400 });
  }
  const evento = JSON.parse(corpo);
  let esito = "ignorato";
  try {
    if (evento.type === "checkout.session.completed" ||
        evento.type === "checkout.session.async_payment_succeeded") {
      const s = evento.data.object;
      /* "paid" = pagato; "no_payment_required" = totale 0 € con un codice al 100%; "unpaid" = non ancora */
      esito = (s.payment_status === "paid" || s.payment_status === "no_payment_required") ? await pagato(s) : "pagamento in sospeso";
    } else if (evento.type === "checkout.session.expired") {
      esito = await scaduto(evento.data.object);
    } else if (evento.type === "customer.subscription.deleted") {
      esito = await abbonamentoFinito(evento.data.object);
    }
  } catch (e) {
    console.error(e);
    return new Response("errore: " + (e as Error).message, { status: 500 });
  }
  console.log(evento.type, esito);
  return new Response(JSON.stringify({ ricevuto: true, esito }), {
    headers: { "Content-Type": "application/json" },
  });
});
