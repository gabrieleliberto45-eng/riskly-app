# Rotazione dei formati (da ottobre 2026)

Problema: tutti i post avevano lo stesso schema (scritta + numeri + "link in bio"). L'algoritmo e il pubblico smettono di notarli.
Regola: mai lo stesso formato due giorni di fila sullo stesso social; stile grafico cambiato ogni 2 settimane.

## 6 formati a rotazione (TikTok e Instagram)
| Formato | Cosa | Frequenza |
|---|---|---|
| A · Attualità | "La settimana dei mercati": dati e date della settimana, notizie (Fed, petrolio, geopolitica) e cosa cambiano per il rischio | 1 a settimana, domenica |
| B · Notizia del giorno | un fatto uscito oggi (es. CPI) spiegato in 30 secondi, con cosa fare con il rischio | dopo i dati importanti |
| C · Carosello educativo | numeri e formule (lotto, winrate, prop) | 2 a settimana |
| D · Domanda / sondaggio | una sola domanda forte, video corto | 1–2 a settimana |
| E · Dietro le quinte | test dei bot su MT4/MT5, schermo reale, girato col telefono | 1 a settimana (lo gira Gabriele) |
| F · Prodotto | un solo post promozionale ogni 4–5 contenuti | fino al lancio |

Stili grafici: bianco "foglio" · scuro marchio · rosso "notiziario" (attualità). Si alternano, non si ripetono due giorni di fila.

## YouTube: solo video lunghi (8–12 min), 2 a settimana
- Domenica: "La settimana dei mercati" (attualità + calendario + gestione del rischio)
- Mercoledì: guida pratica (position sizing, piano di rischio giornaliero, prop firm, journal…)

## Regole per l'attualità
- Solo fatti verificati, con data; niente previsioni di prezzo, niente "compra/vendi".
- Ogni notizia chiude con cosa significa per il rischio (lotto, stop, orari).
- Orari sempre in ora italiana (attenzione al cambio d'ora: Italia 25 ottobre, USA 1° novembre).

## Alternanza decisa il 9 ottobre (TikTok e Instagram)
- Giorni pari dal 10: **Storie di rischio** (reel cinematografico, crolli e disastri veri), ore 18:00. Ogni storia chiude collegandosi a uno strumento Riskly.
- Giorni dispari dall'11: **Gestione del rischio** (carosello), ore 13:00.
- In più, quando esce un video lungo su YouTube: 2 clip verticali che portano al canale.
- Attualità ("La settimana dei mercati") il lunedì mattina prima dei dati importanti.
- I vecchi reel/video promozionali programmati sono in bozza: non escono.

## Calendario TikTok + Instagram (programmato il 9 ottobre)
| Data | Ora | Contenuto |
|---|---|---|
| 9 ott | 18:30 / 19:30 | YouTube v02 + teaser t1 |
| 10 ott | 18:00 | Storia s01 · franco svizzero |
| 11 ott | 10:00 / 13:00 | teaser t2 · carosello c02 breakeven |
| 12 ott | 09:00 / 18:00 | n01 settimana dei mercati · Storia s02 · Barings |
| 13 ott | 13:00 / 18:00 | carosello c04 winrate · **Oggi no.** p02 il minuto prima del dato |
| 14 ott | 09:00 / 12:00 / 18:00 | YouTube v03 inflazione USA · clip v03-t1 · Storia s03 · Archegos |
| 15 ott | 13:00 / 18:00 | carosello c01 lotto · **Oggi no.** p01 la quarta operazione |
| 16 ott | 18:00 | Storia s04 · LTCM |
| 17 ott | 13:00 / 18:00 | carosello c03 prop firm · **Oggi no.** p05 scaglioni (ScaleIn) |
| 18 ott | 18:00 | Storia s05 · Knight Capital |
| 19 ott | 13:00 / 18:00 | carosello c05 frasi · **Oggi no.** p03 lo stop spostato |
| 20 ott | 13:00 / 18:00 | conto alla rovescia "Mancano 3 giorni" (IG / TikTok) |
| 21 ott | 13:00 / 18:00 | carosello c06 operazioni al giorno (bianco: dal 15 ottobre i caroselli sono bianchi come il sito) · **Oggi no.** p06 copia tra conti (RisklyCopy) |
| 22 ott | 13:00 / 18:00 | "Domani escono i bot" (IG / TikTok) |
| 23 ott | 13:00 / 18:00 | lancio bot (IG + YouTube / TikTok) |

Video "come funziona" dei bot, alle 20:30 (anticipati il 13 ottobre su richiesta di Gabriele): 13 ott Riskly Pro · 14 RiskGuard · 15 TradeManager · 16 ScaleIn · 21 RisklyCopy (dopo la pubblicazione del sito con la sua scheda).
Video dei bot: social/oggino/b-*.mp4 (demo.html + demo-bot.json + genera-demo.js), TikTok + Instagram Reel, contenuto commerciale del proprio marchio. Copertine con il nome del bot: social/oggino/copertine/ (copertina.html + genera-copertine.js).
Sponsorizzate pronte (le avvia Gabriele dal 23): social/oggino/ad01-inizia.mp4 (con grafico) e ad02-pulito.mp4 (senza grafico, per la verifica).

In bozza (non escono): tutti i vecchi reel/video promo dal 10 al 22 e tutti gli Shorts promo YouTube dal 9 al 22 (compresi quelli del 9 e 10 alle 16:00).

Aggiornato il 9 ottobre sera: tutto il calendario fino al 22 è programmato. Dal 16 ottobre la routine del venerdì segue questo piano (storie/caroselli alternati, YouTube solo video lunghi + clip).

## Format "Oggi no." (deciso il 13 ottobre)
Schermo di MetaTrader ricostruito, pensieri del trader scritti (niente voce sintetica, niente personaggio), il sistema che blocca il pulsante, "OGGI NO." e un referto di 3 righe con i numeri, chiusura Riskly. 15-17 s, funziona anche senza audio.
Si produce con social/oggino/sistema.html + sistema-puntate.json + genera-sistema.js (azioni: buy, stop, dialogo; avviso del dato opzionale).
Ritmo: giorni dispari alle 18:00 (dopo il carosello delle 13:00). Il weekend (p04) è montato ma scartato: a Gabriele non piace. Idee per le prossime: l'ottava operazione del giorno, il lotto "a occhio", la challenge all'ultimo giorno, il trade fuori orario, il segnale del gruppo Telegram.

## Versione con margini su TikTok e Instagram (deciso il 13 ottobre)
A schermo intero, sui telefoni più alti (19,5:9), sia TikTok sia Instagram ingrandiscono i video 9:16 e tagliano i lati; icone e descrizione coprono i bordi.
Regola: sui social si pubblica sempre la versione in social/oggino/tiktok/ (contenuto all'80%, margini neri:
ffmpeg -vf "scale=864:1536,pad=1080:1920:95:110:color=0x000000"), anche negli annunci. Gli originali restano per il sito.
Post Instagram e TikTok separati alla stessa ora. Già fatto per tutti i video dal 13 al 21 ottobre.

## YouTube dal 14 ottobre: due serie fisse (decise da Gabriele)
**Autonomia piena (Gabriele, 14 ottobre): le puntate si scrivono, montano e programmano senza chiedere conferma; a Gabriele solo una riga a cose fatte.**
Formato: **con la voce** dei video YouTube (edge-tts aggiornato, funziona di nuovo dal 14 ottobre): `python3 social/youtube/voce.py vNN` poi `node social/youtube/genera.js vNN`.
Se la voce non va: versione senza voce con sottotitoli, `MUTO=1 node social/youtube/genera.js vNN`.
(server: python3 -m http.server 8790 nella cartella social/youtube). Ogni video chiude portando al corso **Riskly · Analisi fondamentale** (in arrivo): fino al 21 ottobre "iscriviti al canale per sapere quando esce", dal 21 "lista d'attesa su riskly.trade, pagina Corso".

1. **"Domani esce"**: il giorno prima di ogni dato ad alto impatto USA o eurozona (importanza alta nel calendario), alle 18:30.
   2–3 minuti: cosa esce e a che ora italiana, il contesto, il consenso (precedente → atteso), come può reagire di solito il mercato,
   il rischio (prima, se resti dentro, dopo), chiusura sul corso. Niente previsioni. Fonte consensi: calendario economico TradingView.
   Modello: social/youtube/v04.json. Titolo: "Domani alle HH:MM: <dato> (<data>)".
2. **"La settimana dell'oro"**: ogni sabato alle 11:00. Numeri e grafico da `python3 social/youtube/oro/settimana.py <lunedì>`
   (oro future COMEX, indice del dollaro, decennale USA), più le notizie della settimana verificate con fonti.
   Scene: titolo con la variazione della settimana · grafico · i numeri (oro, dollaro, decennale) · cosa l'ha mosso · i dati della settimana prossima · rischio · chiusura sul corso.
   Niente previsioni di prezzo.
Attenzione agli orari: dal 25 ottobre al 1° novembre i dati USA delle 8:30 di New York escono alle 13:30 italiane e la Fed del 28 ottobre alle 19:00.

## Turno del 16 ottobre (settimana 19–25 ottobre)
Dati Metricool 8–16 ottobre (TikTok, visualizzazioni): storie 259–417 (franco 417, Barings 294), clip attualità 257–343, "Oggi no." 260–264,
caroselli 219–241 ma con più like (9–10). Instagram: reel 3–43 visualizzazioni, caroselli 16–29 di copertura. Follower quasi fermi, 0 salvataggi.
Cosa ho cambiato: chiusure con parola chiave nei commenti (DATI, ROVINA) e link corto in tutti i nuovi post; storia più "sorprendente" (mercato chiuso, operazioni cancellate).

| Data | Ora | Contenuto |
|---|---|---|
| 19 ott | 09:00 | n02 La settimana dei mercati (19–25 ott, cambio dell'ora, Fed e BCE della settimana dopo) · IG + TikTok · riskly.trade/dati |
| 24 ott | 18:00 | Storia s06 · nichel al London Metal Exchange (8 marzo 2022) · IG + TikTok separati · riskly.trade/rovina |
| 25 ott | 13:00 | carosello c07 La leva non è il rischio (bianco) · IG + TikTok · riskly.trade/rovina |
Il resto della settimana era già programmato (conto alla rovescia, lancio del 23, Oggi no., RisklyCopy).
YouTube: in questo turno nessun nuovo video lungo; restano le routine "Domani esce" e "La settimana dell'oro".

## Regola dal 19 ottobre 2026 (decisa da Gabriele)
- Al massimo **un contenuto al giorno per social** (Instagram, TikTok, YouTube; X se verrà collegato). Niente più 2–4 uscite nello stesso giorno.
- Riorganizzazione fatta il 17/10: in bozza i reel pre-lancio superati (bot 19/10 e 21/10, carosello overtrading); spostati "Oggi no · stop" al 26/10, "Oggi no · copia tra conti" al 27/10 (testo aggiornato: RisklyCopy disponibile ora), carosello "5 frasi" al 28/10, video YouTube sul lotto dell'oro al 24/10.

## YouTube dal 20 ottobre: grafica del sito e formati diversi (richiesta di Gabriele)
Problema: quasi solo "Domani esce", sempre uguale → poche visualizzazioni. Dal 20 ottobre:

**Grafica** (social/youtube/modello.html): stile dell'apertura di riskly.trade. Fondo nero, candele che scorrono con la linea
dello stop ambra, ambra #F2B83A solo su ciò che conta, Archivo stretto, schede scure come le tile del sito, capitolo nella pillola ambra
e nome della serie accanto (campo "serie" del json). Le candele si muovono sempre: il montaggio rende ogni fotogramma
(circa 0,18 s a fotogramma: 3 minuti ≈ 13 minuti di montaggio; FERMO=1 per la versione veloce senza movimento).

**Tipi di scena** (oltre a titolo, punti, numeri, grafico, formula, chiusura):
- `cifra`: {titolo?, cifra:"-35,2%", etichetta, nota?}: numero enorme che conta da zero.
- `confronto`: {titolo, no:{titolo, righe[]}, si:{titolo, righe[]}, nota?}: due schede, sbagliato e giusto.
- `domanda`: {titolo, opzioni[2-4], giusta:indice, spiegazione}: quiz; la voce fa la domanda, lascia un attimo
  ("metti in pausa e rispondi nei commenti"), poi si accende la risposta giusta.
Regola: in ogni video almeno 3 tipi di scena diversi, mai due scene di fila dello stesso tipo, almeno una `domanda` o `cifra`.

**Calendario YouTube** (massimo un'uscita al giorno):
| Giorno | Ora | Serie |
|---|---|---|
| Martedì | 18:30 | **Casi veri** (6–8 min): un crollo o un caso vero raccontato come una storia (Archegos, franco svizzero 2015, LTCM, Barings, Knight Capital, Amaranth, nichel LME 2022, Melvin/GameStop, Credit Suisse, petrolio negativo 2020…). Struttura: gancio con la cifra · chi erano · la decisione sbagliata · il giorno del crollo (cifre verificate) · domanda "tu cosa avresti fatto?" · confronto senza piano / con piano · cosa porti nel tuo conto. Chiusura riskly.trade/rovina. |
| Giovedì | 18:30 | **Rispondi tu** (5–7 min): guida pratica a quiz, 4–5 domande con risposta e spiegazione (lotto, leva, stop, prop firm, serie di perdite, orari dei dati). Chiusura con lo strumento del tema (riskly.trade/lotto, /prop, /rovina). |
| Sabato | 11:00 | **La settimana dell'oro** (come prima, con la nuova grafica). |
| Giorno prima di un dato | 18:30 | **Domani esce**: solo per i dati più forti (decisioni Fed e BCE, inflazione CPI e PCE USA, occupazione USA, PIL USA). Al massimo 2 a settimana e mai nei giorni che hanno già un video. |
Gli altri giorni: YouTube Short (la clip verticale del video uscito prima), se c'è.

## Casi veri · puntate
| Data | Video | Caso |
|---|---|---|
| 20 ott 18:30 | v09 | Petrolio a −37,63 $ (20 aprile 2020): Bank of China «Yuan You Bao», clienti di Interactive Brokers. Fonti: CFTC, Caixin. |
Prossimi casi non ancora usati su YouTube: Amaranth (2006), Melvin Capital e GameStop (2021), Credit Suisse (2023), e in versione lunga quelli già raccontati nelle storie brevi (franco svizzero, Barings, Archegos, LTCM, Knight Capital, nichel).

## Dal 26 ottobre: grafiche del sito ovunque e video educativi (decisi con Gabriele il 23 ottobre)
Dati 9–23 ottobre: TikTok 210–270 visualizzazioni a video (picchi 740–765 per "come funziona" dei bot e storia LTCM), Instagram reel 11–48,
YouTube video lunghi 1–36 ma Shorts educativi di inizio ottobre 30–146. Dal sito quasi zero visite dai social, nessuna vendita al lancio (23 ott, ore 18:25).

**Grafiche**: tutto nello stile di riskly.trade (nero con candele e linea dello stop, ambra #F2B83A, Archivo stretto, frasi normali, niente maiuscolo).
- Caroselli: social/caroselli/modello.html (predefinito chiaro come le pagine del sito, `--scuro` come l'apertura; usare **scuro**). "notizie" = scuro con la pillola "Mercati · la settimana".
- Video verticali educativi (TikTok, Reels, Shorts): stesso motore dei video YouTube, `VERT=1 node social/youtube/genera.js tNN` (1080×1920, sottotitoli grandi, niente 3D). File social/youtube/tNN.json, serie "Rischio in 1 minuto" o "Fondamentale in 1 minuto", 45–70 s, 4 scene, almeno una "domanda" o "cifra".
- Storie di rischio e "Oggi no." restano, con l'ambra al posto del verde.

**Settimana tipo** (massimo un contenuto al giorno per social):
| Giorno | Instagram + TikTok | YouTube |
|---|---|---|
| Lun | carosello "La settimana dei mercati" (scuro) | Short tNN |
| Mar | video educativo tNN | Casi veri (lungo) |
| Mer | video educativo tNN | Short tNN |
| Gio | carosello di rischio | Rispondi tu (lungo) |
| Ven | Oggi no. / storia di rischio | Short tNN |
| Sab | video educativo tNN | La settimana dell'oro |
| Dom | storia di rischio o Oggi no. | — |
TikTok: 3 video educativi a settimana su rischio e analisi fondamentale (richiesta di Gabriele). Gli stessi video vanno su Reels e come Shorts su YouTube.

**Programmata su Metricool, 25 ottobre – 1 novembre** (immagini e video da raw GitHub, commit 4f026f5):
| Giorno | Instagram + TikTok | YouTube |
|---|---|---|
| Dom 25 13:00 | carosello c07 leva (scuro) | — |
| Lun 26 | 09:00 carosello n03 "Fed e BCE nella stessa settimana" | 18:00 Short t01 |
| Mar 27 | 13:00 t01 dati USA alle 13:30 | Casi veri (routine) |
| Mer 28 | 13:00 t02 Fed/BCE, 3 regole | 10:00 Short t02 (prima della Fed delle 19:00) |
| Gio 29 | 13:00 carosello c05 5 frasi (scuro) | Rispondi tu (routine) |
| Ven 30 | 18:00 Oggi no · stop | 18:00 Short t03 |
| Sab 31 | 13:00 t03 quanti lotti con 1.000 € | La settimana dell'oro (routine) |
| Dom 1 | 18:00 Oggi no · copia | — |
