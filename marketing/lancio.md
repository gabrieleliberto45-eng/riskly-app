# Lancio Riskly · 23 ottobre

## Il percorso di chi arriva dai social

TikTok / Instagram / YouTube → link in bio **riskly.trade/tt** (o /ig, /yt: così nel pannello Gestione vedi da dove arriva)
→ sito: guida PDF gratis o lista d'attesa (email salvata nel database)
→ email di lancio (sotto) → pagamento con Stripe → conferma in Gestione → gruppo Telegram clienti.

## Da fare prima del 23 ottobre

- [ ] **Link in bio**: `riskly.trade/tt` su TikTok, `riskly.trade/ig` su Instagram, `riskly.trade/yt` su YouTube.
- [ ] **Stripe**: crea un Payment Link per RiskGuard (99 €), TradeManager (99 €), ScaleIn (129 €), Riskly Pro (249 €), Videocorso (199 €).
      In ogni link: "Dopo il pagamento" → reindirizza a `https://riskly.trade/download.html`.
- [ ] Incolla i link in `site/index.html` (costante `STRIPE`) e metti `VENDITA_ATTIVA = true` **la mattina del 23**, poi ripubblica il sito.
- [ ] Prova un acquisto vero da 1 € (link di test) fino all'area clienti, poi rimborsalo.
- [ ] Dal 23 ottobre, i "10 posti" vanno aggiornati a mano (`POSTI_USATI` in index.html) a ogni vendita.

## Come confermare un ordine

1. Il cliente clicca "Acquista": l'ordine compare in **Gestione → Ordini** come "da confermare".
2. Su Stripe vedi il pagamento con la stessa email (e il codice cliente in "client_reference_id").
3. In Gestione premi **Conferma**: il cliente vede subito il pulsante del gruppo Telegram in `download.html`.

## Email alla lista d'attesa

Si mandano da info@riskly.trade: in **Gestione → Lista d'attesa → Copia email**, incollale in **Ccn** (mai in "A").
Solo a chi si è iscritto: la guida PDF e la lista d'attesa danno il consenso a ricevere le notizie sul lancio.

### 1 · Giovedì 16 ottobre, una settimana prima

**Oggetto:** Tra 7 giorni escono i bot di Riskly

Ciao,

ti sei iscritto alla lista d'attesa di Riskly: giovedì 23 ottobre escono i quattro software per MetaTrader.

Un promemoria su cosa fanno, perché non è quello che fanno quasi tutti i bot:
**non aprono operazioni e non danno segnali.** Fanno rispettare le regole che decidi tu a mente fredda:
ti fermano dopo N perdite di fila, bloccano la perdita giornaliera prima del limite della tua prop firm,
rendono obbligatorio lo stop loss.

I primi 10 che acquistano tengono il prezzo di lancio per sempre: RiskGuard e TradeManager 99 €, ScaleIn 129 €, Riskly Pro 249 €.
Si paga una volta, niente abbonamento, e si prova prima su conto demo.

Ti scrivo di nuovo il giorno prima.

Gabriele — Riskly
riskly.trade

*Contenuto informativo, non è consulenza finanziaria. Per non ricevere altre email rispondi "stop".*

### 2 · Mercoledì 22 ottobre, il giorno prima

**Oggetto:** Domani alle 10:00

Ciao,

domani, giovedì 23 ottobre alle 10:00, apre la vendita dei bot di Riskly su riskly.trade.

I posti al prezzo di lancio sono 10 in tutto, e il prezzo resta bloccato a vita, aggiornamenti compresi.
Se sai già quale ti serve:
- **RiskGuard** se il problema è fermarti (perdite di fila, limite giornaliero, prop firm);
- **TradeManager** se il problema è gestire la posizione aperta (break-even, trailing stop);
- **Riskly Pro** se vuoi tutto, con il rischio calcolato sull'insieme delle posizioni.

Per acquistare serve un account sul sito: se vuoi, crealo già oggi, così domani ci metti un minuto.

Gabriele — Riskly

*Contenuto informativo, non è consulenza finanziaria. Per non ricevere altre email rispondi "stop".*

### 3 · Giovedì 23 ottobre, ore 10:00

**Oggetto:** È aperto

Ciao,

da adesso RiskGuard, TradeManager, ScaleIn e Riskly Pro sono disponibili su **riskly.trade**.

Dopo il pagamento entri nel gruppo Telegram dei clienti e ricevi i file abilitati per il tuo conto MetaTrader entro 24 ore lavorative.
Se il software non funziona sul tuo broker e non riusciamo a risolvere, ti rimborsiamo.

Gabriele — Riskly

*Contenuto informativo, non è consulenza finanziaria. Per non ricevere altre email rispondi "stop".*
