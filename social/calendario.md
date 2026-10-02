# Calendario social Riskly · 27 settembre → 23 ottobre (lancio)

**Due post al giorno per rete** (dal 29 settembre): uno di **trading** e uno di **finanza**, sempre collegati a Riskly.
Colori dei video: quelli del sito (nero e lime, sfumature), già nel modello `social/generatore/modello.html`.

| Serie | TikTok | Instagram Reel | YouTube Shorts |
|---|---|---|---|
| Trading (gNN · yNN) | 18:00 feriali, 10:00 weekend | 10:00 | 16:00 |
| Finanza (fNN · zNN) | 12:00 feriali, 18:00 weekend | 18:00 | 10:00 |

Orari da Metricool (getBestTimeToPostByNetwork), aggiornati ogni settimana in base ai risultati.

Tutti i video partono con il titolo già visibile (`"subito": true`): TikTok usa il primo fotogramma come copertina.

Stato: collegati TikTok (@riskly63), Instagram (@riskly.trade) e YouTube; settimana 1 programmata su tutti e tre, due post al giorno.

Regole per tutti i contenuti:
- niente segnali, niente setup, niente promesse di guadagno;
- ogni didascalia chiude con: *Contenuto educativo, non è consulenza finanziaria.*;
- i video hanno una base lo-fi originale (social/generatore/musica.py): niente diritti di terzi, quindi va bene anche per un account di brand;

Hashtag base (Instagram e TikTok, massimo 5): `#trading #gestionedelrischio #forex #tradingitalia #propfirm`
Su YouTube Shorts: `#shorts #trading #gestionedelrischio`

---

## Settimana 1 · programmata su TikTok (video g08–g14)

I primi 7 video (g01–g07, in `video/scartati/`) ripetevano temi già pubblicati sul profilo e sono stati sostituiti.
Dal profilo: rendono di più i contenuti in cui il trader si riconosce e quelli contro i "guru"
(1.000+ visualizzazioni) rispetto ai tutorial puri (200–300). Temi GIÀ TRATTATI, da non ripetere:
drawdown e recupero, calcolo dei lotti, formula del rischio per trade, revenge trading, challenge prop firm,
rischio per operazione, simulazioni di conti / ordine dei risultati, bias e journal, segnali venduti,
tipi di trader nei gruppi Telegram, crolli storici, checklist prima del trade, 500 € vs 5.000 €,
"raddoppio e recupero", break-even (in bozza), "3 numeri a memoria", "quanto perdo se va male", "decidi la perdita prima".

| Data | Ora | Video | Tema |
|---|---|---|---|
| Dom 27/9 | 10:00 | g08 | Frasi che ogni trader ha detto almeno una volta |
| Lun 28/9 | 18:00 | g09 | Il corso da 997 € in 20 secondi |
| Mar 29/9 | 18:00 | g10 | Winrate minimo per andare in pari (0,5R–3R) |
| Mer 30/9 | 18:00 | g11 | La giornata di un trader in 4 frasi |
| Gio 1/10 | 18:00 | g12 | Overtrading: 1.400 $ di commissioni al mese |
| Ven 2/10 | 18:00 | g13 | Un bot che non apre mai un'operazione (RiskGuard) |
| Sab 3/10 | 10:00 | g14 | Weekend: 20 minuti, tre domande |

## YouTube Shorts · contenuti diversi, pensati per YouTube (video y01–y07, ore 16:00)

Su YouTube Shorts conta soprattutto quanto del video viene visto (circa 70%+), quanti scorrono via nei primi 2 secondi
e le ripetizioni (ogni loop conta come visualizzazione). Quindi: testo già visibile dal primo fotogramma (`"subito": true`),
15–18 secondi, nessuna scheda finale col logo, ultima frase che si ricollega all'inizio (`"loop": true`), un bot citato in ogni video.
Picco del pubblico YouTube: 16:00 tutti i giorni.

| Data | Video | Tema | Bot |
|---|---|---|---|
| Dom 27/9 | y01 | Tra il 74% e l'89% dei conti retail su CFD perde (analisi ESMA) | RiskGuard |
| Lun 28/9 | y02 | Leva 1:500: il margine cambia, il rischio no | RiskGuard |
| Mar 29/9 | y03 | Con 100 $ non puoi rischiare l'1% (lotto minimo) | calcolatore |
| Mer 30/9 | y04 | Un Expert Advisor che non fa trading | RiskGuard |
| Gio 1/10 | y05 | Trailing stop in 15 secondi | TradeManager |
| Ven 2/10 | y06 | Quanto vale un pip su EURUSD | RiskGuard |
| Sab 3/10 | y07 | Lo stop loss mentale | RiskGuard |

## Cosa funziona (ricerca del 28/9, da rifare ogni mese)

- **Primi 1,5–2 secondi**: se su YouTube più del 70% scorre via subito, il gancio è da rifare. Testo già visibile dal primo fotogramma (`subito`).
- **YouTube Shorts**: sotto i 30 s serve circa il 65% di visione media per essere spinti; le ripetizioni contano come visualizzazioni, quindi finale che si ricollega all'inizio (`loop`).
- **Instagram**: dopo tempo di visione e completamento conta soprattutto quante volte il Reel viene **inviato in DM** (pesa più dei like), poi i salvataggi. Didascalie con "Mandalo a chi…" o "Salvalo". I contenuti originali sono premiati, i ripost penalizzati: i nostri video sono generati da noi, niente watermark.
- **Finanza**: rendono di più spiegazioni rapide, sfatare miti e "cosa avrei voluto sapere prima" rispetto ai contenuti promozionali. Durata con più interazioni: circa 20–35 s.
- **Musica**: 11 basi originali in 5 stili (lo-fi, trap, deep house, cinematico, pluck), scelte in base alla serie: video vicini e dello stesso giorno hanno basi diverse.

Fonti: vidiq.com/blog/post/youtube-shorts-algorithm, shortimize.com/blog/youtube-shorts-retention-rate, sproutsocial.com/insights/instagram-algorithm, creatorlanehq.com/blog/instagram-sends-per-reach-2026, fullyvested.com/insights/tik-tok-for-finance-brands, kapwing.com (statistiche short-form 2026).

## Settimana 1 · serie finanza (dal 29/9)

| Data | TikTok / IG | Tema | YouTube | Tema |
|---|---|---|---|---|
| Mar 29/9 | f01 | Inflazione: 10.000 € fermi valgono 7.441 € tra 10 anni | z01 | Lo spread (bid/ask) · Riskly Pro |
| Mer 30/9 | f02 | Regola del 72 e il "10% al mese" | z02 | Interesse composto: 1.000 € al 10% per 30 anni |
| Gio 1/10 | f03 | Prima del trading: fondo di emergenza | z03 | Stop out e livello di margine · RiskGuard |
| Ven 2/10 | f05 | NFP del primo venerdì · Riskly Pro filtro notizie | z04 | Lo swap overnight |
| Sab 3/10 | f04 | Correlazione: tre operazioni, un solo rischio · Riskly Pro | z05 | Sessioni di mercato in orario italiano · RiskGuard |

Temi di FINANZA GIÀ TRATTATI, da non ripetere: inflazione, regola del 72, fondo di emergenza, correlazione tra coppie,
NFP e calendario economico, spread, interesse composto, stop out/margine, swap, sessioni di mercato.

## Settimana 2 · 4–10 ottobre · PROGRAMMATA (28 video, 42 post)

Orari invariati (TikTok trading 18:00 / weekend 10:00, finanza 12:00 / weekend 18:00; Instagram 10:00 e 18:00; YouTube y 16:00, z 10:00).
Video: `g15–g21`, `f06–f12`, `y08–y14`, `z06–z12`. Raw GitHub fissato al commit 72fb974.

| Data | Trading (g) | Finanza (f) | YouTube trading (y) | YouTube finanza (z) |
|---|---|---|---|---|
| Dom 4/10 | g15 Disciplina = regola scritta | f06 1,5% di costi in 30 anni | y08 Cos'è una prop firm | z06 Leva 1:30 |
| Lun 5/10 | g16 Senza stop non rischi l'1% | f07 Capitale per vivere di trading | y09 MT4 o MT5 | z07 Cos'è un CFD |
| Mar 6/10 | g17 Winrate 70% e conto in perdita | f08 100 €/mese per 20 anni | y10 Profit factor | z08 Tassi e valute |
| Mer 7/10 | g18 Dopo una perdita (pausa) | f09 Broker: 4 controlli | y11 Slippage | z09 Stop e ATR |
| Gio 8/10 | g19 Limite giornaliero vs prop firm | f10 10 perdite di fila (1/2/5%) | y12 Demo o reale | z10 Valute rifugio |
| Ven 9/10 | g20 Break-even troppo presto | f11 Gap del weekend | y13 Balance ed equity | z11 ECN o standard |
| Sab 10/10 | g21 Presentazione TradeManager | f12 Trader A o B? (commenti) | y14 Cosa scrivere nel journal | z12 Forex aperto 24 ore? |

Temi GIÀ TRATTATI aggiunti (da non ripetere): disciplina e regole scritte, stop loss obbligatorio, aspettativa (winrate vs R), pausa dopo una perdita,
limite giornaliero vs prop firm, break-even troppo presto, TradeManager; costi dei fondi, capitale per vivere di trading, PAC 100 €/mese,
scelta del broker, serie di perdite (1/2/5%), gap del weekend, rendimento/drawdown; prop firm, MT4 vs MT5, profit factor, slippage,
demo vs reale, balance/equity, journal, leva 1:30, CFD, tassi e valute, ATR, valute rifugio, ECN vs standard, orari del forex.

## Lezioni dai numeri (analisi del 2/10)

- **TikTok**: 6 video trading/finanza ≈ 250–330 visualizzazioni ciascuno (la finanza "inflazione" 327, "corso da 997 €" 316 con 8 like e 1 invio). Un video (g11) è rimasto a 6 visualizzazioni: TikTok non lo ha distribuito, non si sa perché. Commenti: 0 su tutti i video generati → da questa settimana CTA a scelta binaria (A o B, 1/2/3) e domande su cosa fa chi guarda.
- **Instagram**: reach 10–20 per Reel; tempo di visione medio 3–8 secondi. I due post pubblicati a mano da Gabriele (screenshot reali: "Test finali", "Jurnal collegato") hanno avuto più like e più reach (28/19 e 21/12) dei video generati (10–14). → Più materiale reale (schermate dei bot, journal) nei video: serve da Gabriele, anche 1 al giorno.
- **YouTube**: Metricool non restituisce ancora visualizzazioni né tempo di visione (campi vuoti): serve riguardare dopo 48 ore o da YouTube Studio.
- **Cambi fatti**: gancio in 2,6–3 s con numero o domanda nella prima riga, video più corti (14–17 s), più tabelle e meno liste, titoli TikTok con la domanda, "Mandalo a chi…" su ogni Reel.
- Video di presentazione (`social/promo/riskly-presentazione.mp4`, 67 s) pubblicato il 30/9: 251 visualizzazioni su TikTok, 14 su Instagram (tempo medio 4 s su 67): troppo lungo per i social, meglio tagli da 15 s con lo stesso materiale.

Nota per la settimana 4: dal 25/10 l'Europa torna all'ora solare, gli USA il 1/11. Per una settimana i dati USA (NFP, CPI) escono alle 13:30 italiane invece che alle 14:30. Tema pronto per un video.

## Settimana 3 · prop firm e strumenti (video da generare)

| Data | Tema | Gancio |
|---|---|---|
| Dom 11/10 | Drawdown giornaliero vs totale | "Due limiti, due modi diversi di perdere la challenge." |
| Lun 12/10 | Rischio di rovina | "Una strategia vincente può comunque azzerarti il conto." |
| Mar 13/10 | Scale-in: una posizione diventa quattro | "Chiudere a pezzi senza farlo a mano." |
| Mer 14/10 | Presentazione ScaleIn | "TP scaglionati in pip, rischio calcolato sul totale." |
| Gio 15/10 | Il costo di una challenge fallita | "Una giornata storta costa 100–500 €. Una regola costa meno." |
| Ven 16/10 | Presentazione RiskGuard | "Ti ferma dopo N perdite di fila, quando il conto è ancora sano." |
| Sab 17/10 | Dietro le quinte: test su conto demo | Screenshot datati dei test (serve materiale tuo) |

## Settimana 4 · verso il lancio (video da generare)

| Data | Tema | Gancio |
|---|---|---|
| Dom 18/10 | Perché non vendiamo segnali | "Chi ti promette rendimenti ti sta mentendo." |
| Lun 19/10 | Le 7 regole di rischio (guida PDF) | "Sette regole che salvano un conto. Gratis." |
| Mar 20/10 | Riskly Pro: tutto insieme | "Rischio calcolato sull'insieme delle posizioni, non su ognuna." |
| Mer 21/10 | Domande frequenti (licenza, conti, demo) | "Si paga una volta. Funziona su 2 conti. Si prova su demo." |
| Gio 22/10 | Domani si parte | "Domani escono i bot. I primi 10 bloccano il prezzo di lancio." |
| Ven 23/10 | **Lancio** | "Da oggi RiskGuard, TradeManager, ScaleIn e Riskly Pro." |

---

## Come si generano i video

```bash
pip install imageio-ffmpeg          # solo la prima volta, se ffmpeg non c'è
node social/generatore/genera.js g08    # oppure senza argomenti: li rigenera tutti
```

Ogni video è un file `social/video/gNN.json` con le scene (tipi: `hook`, `frase`, `numero`, `barre`, `lista`, `conto`, `chiusura`).
Il generatore crea `gNN.mp4` (1080×1920, 30 fps) e `gNN-copertina.jpg`.
