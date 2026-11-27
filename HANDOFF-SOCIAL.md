# HANDOFF · Social di Riskly (TikTok, Instagram, YouTube)

Aggiornato il 27 novembre 2026. Questo file serve a una chat nuova che si occupa SOLO dei social. Non parla degli articoli di Riskly News (vedi `HANDOFF-RISKLY-NEWS.md`) e non contiene chiavi.
Per il resto del progetto vedi `HANDOFF.md`. Dove i due si contraddicono sui social, **vale questo file** (le istruzioni di Gabriele del 27/11 sostituiscono quelle vecchie).

---

## 1. La nuova linea (Gabriele, 27/11/2026)

Parole di Gabriele:
- «Dobbiamo fermare tutti i post e i Reel perché dobbiamo rimodulare un po' i social: vorrei dei social puliti che spiegano con delle immagini quello che facciamo, non un video ogni giorno. Deve essere un canale serio dove spieghiamo i prodotti che offriamo e basta.»
- «Dobbiamo dividere in due. **YouTube Short e TikTok devono portare traffico, tanto traffico al sito web.** Per **Instagram** deve essere una pagina pulita con 4–5 immagini, caroselli che spiegano tutto l'ecosistema di Riskly, ma non fatti con le foto che abbiamo messo adesso: con delle immagini, non in quello stile, ma in uno stile **serio**.»

Tradotto in due compiti separati:

| Canale | Ruolo | Cosa pubblicare |
|---|---|---|
| **YouTube Short** e **TikTok** | **Portare traffico al sito** (riskly.trade e gli strumenti gratuiti) | Contenuti brevi che spingono verso un link preciso. Qui si può pubblicare con più continuità |
| **Instagram** | **Vetrina seria e pulita** | Una pagina con solo 4–5 caroselli di immagini che spiegano **tutto l'ecosistema Riskly**, in stile serio. Niente flusso quotidiano |

Punti ancora da confermare con Gabriele (non decidere da soli):
1. **Instagram: i reel.** Il vecchio piano li pubblicava (fuori dalla griglia). «Pagina pulita» fa pensare che i reel su Instagram si fermino: **chiedere conferma**.
2. **Quali prodotti** mostrare e in che ordine; **quanto spesso** pubblicare su TikTok e YouTube.
3. **Stile serio di Instagram:** non è ancora definito. Prima di produrre, preparare **2 proposte con anteprima** (non produrre tutta la serie al buio).

## 2. Stato di oggi (27/11, sera)

- **Tutto fermo.** Il turno settimanale automatico del venerdì «Riskly social settimanale» (`trig_018hEFGpXyEY2c8tgdRnZe7Q`) è **spento**. Non programmare niente su Metricool finché Gabriele non approva il piano.
- **Metricool** (brand `7104502`, fuso `Europe/Rome`): i **13 post programmati sono in BOZZA** (non cancellati): Tappa 1 (quiz 27/11, riepilogo 29/11 su Instagram+TikTok e Short YouTube) e tutta la Tappa 2 (carosello «settimana dei mercati» n08, reel t2a/t2b/t2c, caroselli p2-lezione, p2-errori, p2-quiz, più i 3 Short). I file sono nel repository. Si possono ripubblicare o eliminare dall'app Metricool.
- **Percorso a 8 tappe** («Dal caso al piano», `social/piano/percorso.md`): **in pausa** (idea di fondo: una tappa a settimana, ogni contenuto con l'etichetta «Percorso Riskly · Tappa N di 8»). Non va buttato: può diventare un filone per TikTok/YouTube.
- **Instagram oggi:** la griglia ha i **9 post «vetrina» v01–v09** (stile chiaro, pubblicati il 14/11; definizioni in `social/caroselli/caroselli.json`, anteprima `social/caroselli/anteprima-vetrina.jpg`). Gabriele dice che **quelle immagini non vanno bene**: vanno **sostituite** da 4–5 caroselli nuovi in stile serio. **L'API non può archiviare i post:** i vecchi li archivia Gabriele dall'app Instagram.
- **Post già pubblicati** su TikTok/Instagram/YouTube: non toccati.
- Il lavoro di Svelarium (Short giornalieri) **non è di Riskly**: non toccarlo.

## 3. I canali e gli strumenti di Metricool

- Instagram: account **@riskly.trade** (nel vecchio piano). TikTok e YouTube: collegati a Metricool, brand `7104502`.
- Tool disponibili nella chat (collegare **Metricool** e **Higgsfield**): `getScheduledPosts`, `createScheduledPost`, `updateScheduledPost` (per mettere in bozza: stesso contenuto con `draft: true`; l'`id` cambia a ogni update), `getAnalyticsDataByMetrics`, `getBestTimeToPostByNetwork`.
- Programmazione: media come **URL raw GitHub fissati al commit** (`https://raw.githubusercontent.com/gabrieleliberto45-eng/riskly-app/<commit>/…`); fare commit e push PRIMA di programmare; video sotto ~40 MB. Metricool ricarica i file e restituisce i propri indirizzi `static.metricool.com`.
- Regole tecniche per rete:
  - **Instagram reel:** `instagramData: {type: "REEL", showReelOnFeed: false, isAiGenerated: true se voce o immagini IA}`. Instagram richiede un'immagine o un video.
  - **Instagram carosello (nuova linea):** `instagramData: {type: "POST"}`, più immagini in `media`, JPG 1080×1350.
  - **TikTok:** `tiktokData: {privacyOption: "PUBLIC_TO_EVERYONE", title, isAigc: true per voce sintetica}`; i caroselli (foto) usano `photoCoverIndex`. La copertina personalizzata vale solo con account Business; la copertina è il primo fotogramma, che deve essere nitido.
  - **YouTube:** solo `type: "short"`, `privacy: "public"`, `category: "EDUCATION"`, `madeForKids: false`, `isAiGeneratedContent: true se voce IA`, titolo con `#shorts`, descrizione con il link in https. **MAI video lunghi** (Gabriele 20/11: «niente video lunghi, solo Short»).
- Analisi: metriche Data Studio, es. TikTok `TKPO01/05/07/08/09/10`, reel Instagram `IGRE01/03/23/11/12/21`. **I numeri vecchi (15/9–15/10: Instagram 14 follower, TikTok 70, poche centinaia di visualizzazioni al giorno)** sono da rifare: ripartire da una misura nuova.

## 4. Mettere traffico sul sito (YouTube Short e TikTok)

Regola di conversione (`social/piano/conversione.md`): **ogni contenuto chiude con UNA sola cosa da fare** e il suo link corto, scritto nel testo e detto a voce. Niente «link in bio» generico.

| Tema | Chiusura | Link |
|---|---|---|
| lotto, stop, rischio per trade | calcola il lotto giusto, gratis | `riskly.trade/lotto` |
| serie di perdite, rovina, drawdown | simula le tue perdite di fila | `riskly.trade/rovina` |
| prop firm, challenge | tieni sotto controllo la challenge | `riskly.trade/prop` |
| dati, Fed, CPI, notizie | i dati di domani, gratis | `riskly.trade/dati` |
| journal, disciplina | prova il journal | `riskly.trade/prova` (7 giorni di prova) |
| corsi | programma completo | `riskly.trade/corsi` |
| software (bot) | i software | `riskly.trade/bot` |
| tutto | pagina con tutti i canali | `riskly.trade/link` |

Ogni link corto registra la provenienza: nel **pannello Gestione di riskly.trade** (account admin → Visite: «Visite per sito», «Cosa fanno», «Da dove arrivano») si vede quale contenuto porta visite e quali azioni seguono. **È la misura principale di successo: le visite al sito, non le visualizzazioni.**

Altre note:
- **TikTok:** un avviso ricevuto il 7 novembre non è stato chiarito. **Finché non lo è: niente prodotto a pagamento nei contenuti TikTok, solo strumenti gratuiti**, e **mai** «commenta X e ti mando…». (Si può chiedere a Gabriele lo screenshot di «Vedi azioni coercitive».)
- I prodotti a pagamento si mostrano su Instagram (vetrina) e, dove consentito, su YouTube, sempre con la dicitura «Comunicazione promozionale».
- Un «schermo vero» girato da Gabriele (registrazione dello schermo mentre usa i prodotti) è il tipo di contenuto che funziona meglio per spiegare i prodotti: chiederglielo, non inventarlo.
- Un reel con una **storia personale vera** è stato il più visto nelle analisi dei concorrenti (va girato da Gabriele).
- Evitare doppioni: lo stesso contenuto pubblicato più volte lo stesso giorno prende molto meno.

## 5. Instagram: la nuova pagina (4–5 caroselli seri)

Obiettivo: chi apre il profilo capisce **tutto l'ecosistema Riskly** guardando 4–5 caroselli, in uno stile serio, con immagini (non nello stile delle vetrine v01–v09 né in quello dei reel).

Ecosistema da spiegare (da `HANDOFF.md` e `social/piano/piano-instagram.md`; **verificare prezzi e disponibilità sul sito prima di scriverli**):
- **Cos'è Riskly:** gestione del rischio per trader, **niente segnali**; il nemico è il comportamento, non il mercato.
- **Software per MetaTrader 4/5** (bot): RiskGuard, TradeManager, ScaleIn, Riskly Pro (e relativi servizi).
- **Journal** (app.riskly.trade, 7 giorni di prova): diario di trading, statistiche.
- **Riskly News** (news.riskly.trade, 6,99 €/mese): notizie e analisi su USA, Fed, dollaro, oro.
- **Strumenti gratuiti** (strumenti.riskly.trade): calcolatori di lotto, rovina, recupero, prop e calendario dati.
- **Corsi** (riskly.trade/corsi).

Idea di scaletta (da confermare): 1) «Cos'è Riskly e come funziona l'ecosistema» · 2) Software · 3) Journal · 4) Riskly News · 5) Strumenti gratuiti e corsi. Ogni carosello 5–8 immagini, ultima slide con un solo invito e il link.

Regole per questa pagina:
- **Stile serio**: nessuna grafica «da social», niente emoji, niente fumetto o motion. Immagini sobrie e coerenti; palette del sito: carta `#F6F6F3`, blu notte `#12263F`, oro `#D4AE5A`. Le immagini possono essere illustrazioni di Higgsfield (senza testo, persone o loghi), schermate vere dei prodotti, schemi puliti. **Preparare 2 proposte con anteprima per Gabriele prima di produrre tutta la serie.**
- **Pochi post, che restano**: la griglia ha SOLO questi 4–5 caroselli. Se un prodotto o un prezzo cambia, si rifà il post corrispondente e Gabriele archivia il vecchio.
- Questa regola **sostituisce** quella del 14/11 («MAI caroselli nella griglia di Instagram, solo i 9 post vetrina»).
- Su Instagram si può nominare il prodotto con «Comunicazione promozionale: Riskly è un mio prodotto».
- Bio e link in bio: vedi `social/piano/piano-instagram.md` (nome «Riskly | Rischio nel trading», link `riskly.trade/link`); aggiornare quando la pagina nuova è pronta.

## 6. Cosa c'è già pronto nel repository

| Cosa | Dove |
|---|---|
| Motore dei **caroselli** (1080×1350 JPG) | `social/caroselli/`: `caroselli.json` (46+ caroselli: `id`, `stile`, `slide[]` di tipo `copertina`, `testo`, `numeri`, `domanda`), `modello.html`, `rendi.js` (`node social/caroselli/rendi.js <id> [--scuro]`). Uscita: cartella `<id>/01.jpg…`. Campo `immagine` opzionale sulla slide copertina (`img/NOME.jpg`) |
| Motore dei **reel** (1080×1920, MP4 con voce) | `social/sponsor/`: `sponsor.html`, `varianti.json` (testi per scena), `voce.py` (voce di sintesi ElevenLabs, «Marco»), `rendi.js` (`node social/sponsor/rendi.js <versione> --motion`; `prova 2 9 17` per i fotogrammi) |
| Copertine dei reel con titolo | `python3 notizie/copertina_ia.py ID URL "Etichetta" "TITOLO" "NUMERO" --verticale` → `social/reel/cover/ID.jpg` |
| Immagini Higgsfield per i caroselli | `python3 notizie/higgsfield_scarica.py ID URL social/caroselli/img/NOME.jpg` |
| Contenuti della Tappa 1 e 2 (in bozza) | `social/sponsor/sponsor-t2a/t2b/t2c-motion.mp4`, `social/caroselli/{n08-settimana-scuro,p2-lezione,p2-errori,p2-quiz}`, `social/reel/cover/t2a-c.jpg` |
| Piani e regole | `social/piano/` (`percorso.md`, `conversione.md`, `pubblicita.md` con la «Revisione del 7 novembre», `rotazione.md`, `piano-instagram.md`, `script-30-giorni.md`) |

Voce dei reel: **ElevenLabs** (voce «Marco»), chiave in `ELEVEN_API_KEY` (variabile d'ambiente, senza spazi, mai scritta nei file). **Higgsfield**: modello `gpt_image_2_6`, 0,75 crediti a immagine, solo illustrazioni senza scritte/persone/loghi; **budget totale 100 crediti al mese**, quota social circa 45; leggere `notizie/higgsfield_registro.json` e fermarsi a 95 nel mese. vidIQ: crediti quasi finiti (ricarica 9 dicembre).

## 7. Regole che restano (non negoziabili)

- **Niente segnali, previsioni certe, promesse di guadagno**, niente «compra/vendi». Numeri verificati.
- **Avvisi sul rischio**: chiusura dei contenuti educativi: «Contenuto educativo, non è consulenza finanziaria. Il trading con leva (forex, CFD) comporta un alto rischio: puoi perdere tutto il capitale.» Se si parla di un prodotto Riskly: **«Comunicazione promozionale: Riskly è un mio prodotto.»** davanti all'avviso (regole CONSOB/ESMA sui finfluencer).
- **Voce o immagini IA**: dichiararlo (`isAiGenerated` su Instagram, `isAigc` su TikTok, `isAiGeneratedContent` su YouTube).
- **Niente opere o immagini protette di terzi.** Niente «compatibile con le prop firm X» senza aver letto e archiviato le loro regole. Niente affermazioni forti non provabili («resiste ai riavvii»…): vedi gli 8 punti deboli in `piano-instagram.md`.
- **Email e comunicazioni promozionali** ai clienti: solo con consenso (la privacy policy lo richiede); mai dalla mail personale di Gabriele (solo Resend, mittente «Riskly <noreply@mail.riskly.trade>»). Non c'entra con i social ma non va dimenticato.
- Palette A ovunque (carta, blu notte, oro).
- **Non programmare nulla** finché Gabriele non approva il piano.
- Non mandare a Gabriele l'elenco di ciò che programmi («sprechi solo token»): messaggio finale breve con ciò che serve da lui. Per le proposte di stile, invece, mostrare le anteprime.

## 8. Cosa fare per primo (ordine consigliato)

1. Verificare con `list_triggers` che nessun compito social vecchio sia ancora acceso (il turno settimanale è spento; controllare anche gli eventuali compiti YouTube del sabato).
2. Chiedere a Gabriele le tre conferme del punto 1 (reel su Instagram, prodotti e ordine, frequenza su TikTok/YouTube).
3. **Instagram:** scegliere gli argomenti dei 4–5 caroselli, preparare 2 proposte di stile con anteprima (una slide ciascuna), farsi approvare, poi produrre la serie, programmarla e dire a Gabriele quali post vecchi archiviare.
4. **TikTok e YouTube Short:** proporre un piano di contenuti brevi, ciascuno con UN link a uno strumento gratuito, e un modo per misurare le visite (pannello Gestione). Produrre solo dopo l'approvazione.
5. Aggiornare questo file con ciò che si decide.
