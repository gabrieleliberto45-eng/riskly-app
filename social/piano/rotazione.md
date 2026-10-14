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
| 21 ott | 13:00 / 18:00 | carosello c06 operazioni al giorno (scuro) · **Oggi no.** p06 copia tra conti (RisklyCopy) |
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
Formato: senza voce (la voce sintetica da qui non funziona), sottotitoli a schermo e musica: `MUTO=1 node social/youtube/genera.js vNN`
(server: python3 -m http.server 8790 nella cartella social/youtube). Ogni video chiude portando al corso **Riskly · Analisi fondamentale** (in arrivo).

1. **"Domani esce"**: il giorno prima di ogni dato ad alto impatto USA o eurozona (importanza alta nel calendario), alle 18:30.
   2–3 minuti: cosa esce e a che ora italiana, il contesto, il consenso (precedente → atteso), come può reagire di solito il mercato,
   il rischio (prima, se resti dentro, dopo), chiusura sul corso. Niente previsioni. Fonte consensi: calendario economico TradingView.
   Modello: social/youtube/v04.json. Titolo: "Domani alle HH:MM: <dato> (<data>)".
2. **"La settimana dell'oro"**: ogni sabato alle 11:00. Numeri e grafico da `python3 social/youtube/oro/settimana.py <lunedì>`
   (oro future COMEX, indice del dollaro, decennale USA), più le notizie della settimana verificate con fonti.
   Scene: titolo con la variazione della settimana · grafico · i numeri (oro, dollaro, decennale) · cosa l'ha mosso · i dati della settimana prossima · rischio · chiusura sul corso.
   Niente previsioni di prezzo.
Attenzione agli orari: dal 25 ottobre al 1° novembre i dati USA delle 8:30 di New York escono alle 13:30 italiane e la Fed del 28 ottobre alle 19:00.
