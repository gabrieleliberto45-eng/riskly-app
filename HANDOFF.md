# Passaggio di consegne (8 novembre 2026)

## REGOLA FISSA (15/11/2026, Gabriele: "non deve mai essere mandata in nessun caso con la mia personale")
- Le email verso clienti, utenti o contatti partono SEMPRE e SOLO da Riskly: Resend, mittente "Riskly <noreply@mail.riskly.trade>", reply_to info@riskly.trade, firma "Il team Riskly".
- MAI usare il Gmail personale di Gabriele (strumenti mcp__Gmail__send_message / create_draft) per scrivere a clienti, utenti o contatti esterni, in nessun caso. Se Resend non funziona: non mandare, dirlo a Gabriele.

Sessione precedente: "Riskly · News, social e app (principale)" (session_01CZRW5kRhjiWo9ejMQNFKL6).
Gabriele scrive in italiano: rispondi in italiano semplice, frasi brevi.

## Regole fisse di Gabriele
- NON mandare in chat articoli o post pubblicati (8 novembre: "sprechi solo token"). Scrivere solo per errori o decisioni.
- Chiavi mai nel repository né nei commit, mai stampate. Il testo degli articoli MAI nel repository (solo Supabase o scratchpad); le copertine sì.
- Articoli di Riskly News (10 novembre, richiesta di Gabriele): ogni parte dell'articolo ha un TITOLO, scritto come paragrafo breve in MAIUSCOLO subito prima del paragrafo (es. IL DATO · LA REAZIONE DEI MERCATI · PERCHÉ L'ORO SCENDE · ASPETTATIVE SUI TASSI; per il Setup XAU: COSA HA FATTO L'ORO · IL TREND SULLE MEDIE · LE ZONE OSSERVATE · QUANTO SI MUOVE (ATR) E RSI). Il sito non ha ancora uno stile per i titoli (servirebbe un deploy Netlify, bloccato per i crediti): per ora sono righe in maiuscolo. Non ripetere il titolo come prima frase del paragrafo. Nei dati USA spiega sempre perché i mercati reagiscono alla SORPRESA rispetto alle attese e non al confronto col mese prima.
- Autorizzazione di Gabriele (9 novembre): tutte le uscite automatiche già previste (Riskly News, social, setup XAU, ecc.) si pubblicano senza chiedere permesso; in chat solo errori o decisioni.
- Niente segnali, previsioni, "compra/vendi"; i numeri di esempio vanno segnati come esempio.
- Riskly News: solo USA/Fed/oro/dollaro (niente Banca d'Inghilterra o altre banche centrali; BCE solo nei giorni di decisione).

## Progetti e dove stanno
- Branch di lavoro: `claude/come-ti-sembra-nmri8v` (news, social, strumenti). Il journal (app.riskly.trade) si modifica su branch `claude/journal-*` → PR → merge su main.
- Supabase: progetto `swlztverwfgdgchgpudt` (Management API `/database/query`). Tabelle principali: `notizie` (+ vista `notizie_anteprima`), `acquisti`, `visite`, `news_iscrizioni`. L'insert in `notizie` manda da solo la notifica push.
- Netlify: news `abca6d6e-64d8-40cb-a0c5-776d787d16ac` (deploy a zip di `nuovo/news` senza *.py), strumenti `0f4adbce-96a2-4a3f-ba7c-e500a0f3f4ad`.
- PRIMA di ogni deploy della news: `python3 notizie/copertine_mancanti.py` deve dire 0 (il deploy cancella le copertine che non sono nella cartella).
- Copertine: `python3 notizie/illustra.py ID SCENA "CATEGORIA" "TITOLO" "NUMERO"`. Setup oro: `python3 notizie/setup_xau.py <png>`.
- Metricool: brand 7104502, Europe/Rome. Media dai raw GitHub fissati al commit.
- Chiavi: nella vecchia sessione stanno in file della sua scratchpad (non copiate). Nelle sessioni nuove usare le variabili d'ambiente `SUPABASE_ACCESS_TOKEN` e `NETLIFY_AUTH_TOKEN` togliendo gli spazi (`"${VAR// /}"`); se rispondono 401, chiedere a Gabriele di ricontrollarle nelle impostazioni dell'ambiente.

## Uscite automatiche attive (girano ancora nella vecchia sessione)
- Articolo del giorno 7:37 (trig_01HunTjpVqFkU1ybwBA2wfGm) · notizie straordinarie alle :12, 9–22 lun–ven (trig_012AhxnWVLbNCR1LEYw9iFMo) · Setup XAU pomeriggio 16:47 (trig_016v5GMFy89zuLVoMwN5d4mE) · social del venerdì 10:50 (trig_01E9G9VqyXFVe2wboP5RGRV9) · La settimana dell'oro sabato 8:47 (trig_01TU4i6jdcjpjtr5RmAGTiWa).
- In pausa dal 7 novembre (1–5 visualizzazioni): YouTube Casi veri, Rispondi tu, Domani esce.
- Ogni dato USA importante: l'articolo del giorno crea una sessione separata una tantum 20 minuti prima dell'uscita. Il 4 novembre ADP e ISM sono falliti per limite di utilizzo dell'account.

## Prossimi appuntamenti
- Martedì 10 novembre 14:30: CPI di ottobre (core atteso +0,2% m/m, 2,8% a/a; totale 3,9% a/a). Venerdì 13 14:30: PPI. Mercoledì 18: verbali Fed. Fed 8–9 dicembre (rialzo stimato ~78% secondo Reuters dopo i payrolls).
- Social 9–15 novembre già programmati (8 caroselli: n05 + c14–c20; c14, c17, c20 con prodotto SOLO su Instagram).
- Reel "Il punto" r14–r20 (9–15 novembre) programmati l'8 novembre: IG + TikTok alle 13:00 (martedì 10 e venerdì 13 alle 09:30) e Short YouTube alle 18:00. Voce: Marco di ElevenLabs (ID `13Cuh3NuYvWOVQtLbRN8`, variabile `ELEVEN_VOCE`; chiave in `ELEVEN_API_KEY`, solo come variabile, mai nei file). La chiave data da Gabriele non può leggere voci né crediti, solo sintetizzare; è comparsa in chat: consigliato rigenerarla. Hook già usati fino a r20; ripartire dalla rotazione.

## Cose aperte con Gabriele
- TikTok gli ha dato un AVVISO il 7 novembre: aspettiamo lo screenshot di "Vedi azioni coercitive". Finché non è chiaro, niente prodotto nei post TikTok.
- Acquisto RiskGuard 99 € "in_attesa" del 6 novembre: deve controllare su Stripe.
- ElevenLabs: l'8 novembre nuova chiave (solo sintesi) con voce Marco; funziona. Da rigenerare perché è stata scritta in chat.
- Assistente AI di Riskly News (`supabase/functions/news-ai`): pronto ma senza chiave; Gabriele non vuole pagare: da scegliere Haiku (pochi centesimi) o Gemini gratuito.
- Pubblicità a pagamento (~50 €, vedi `social/piano/pubblicita.md`): decide e paga lui.
- Plugin ECC installato: consigliato spegnere gli hook o mettere il profilo "minimal" (pesa sui token). OmniRoute sconsigliato (non funziona nel cloud, manda i dati a terzi; zip da cancellare).
- Chat riordinate con prefissi (Riskly · / Aste · / Ceramiche · / Altro ·); da archiviare se vuole: Indicatore correlazioni, Collegamento TradingView, Controllo perizie case, Idea canale YouTube. Ambienti: "Default" doppione di "Predefinito"; "Immobiliare" doppione di "Aste".

## Documenti da leggere
- `social/piano/pubblicita.md` (sezione "Revisione del 7 novembre": cosa funziona e cosa no sui social).
- `social/piano/rotazione.md`, `social/piano/conversione.md`.

## Aggiornamento del 9 novembre 2026 (sessione "come ti sembra")
- Autorizzazione di Gabriele: le uscite automatiche (Riskly News, social, setup XAU, ecc.) si pubblicano da sole, senza chiedere e SENZA scrivere in chat cosa è uscito; in chat solo errori o decisioni.
- Orari: ora italiana = UTC+1 fino a marzo (errore corretto il 9 novembre: scrivere sempre l'ora italiana, non UTC).
- Voce reel: Marco di ElevenLabs, ID `13Cuh3NuYvWOVQtLbRN8`, variabili `ELEVEN_API_KEY` e `ELEVEN_VOCE` (la chiave ha solo il permesso di sintesi; è stata scritta in chat: da rigenerare). Reel r14–r20 (9–15 novembre) programmati su Metricool (IG+TikTok 13:00, martedì 10 e venerdì 13 alle 9:30; Short YouTube 18:00). Strumenti per rifarli: `python3 social/youtube/voce.py rNN`, `python3 social/reel/parole.py rNN`, `node social/reel/punto.js rNN` (serve `pip install edge-tts faster-whisper "av<17"`, certificati in /root/.ccr/ca-bundle.crt).
- Notifiche Riskly News: il server funziona (news-avvisi); il sito ora riallinea da solo l'iscrizione a ogni apertura. Se un telefono non le riceve: aprire l'app dall'icona Home e riprovare.
- Aspetto "serio" (blu notte e bianco, Instrument Serif/Sans): file `serio.css` in nuovo/riskly, nuovo/strumenti, nuovo/news e nella radice (journal). Vale solo col tema chiaro (`html:not([data-tema="scuro"])`); il tema scuro resta quello vecchio, cambiano solo i caratteri. Per tornare indietro basta togliere il `<link>` a serio.css.
- Riskly News su computer: pagina a tutto schermo con elenco a destra (blocco @media in nuovo/news/serio.css).
- Journal: i file stanno su main; il ramo di lavoro NON ha la versione aggiornata di index.html/demo.html. Modificare solo da un ramo `claude/journal-*` creato da main, poi PR e merge.
- Ordini: nuova `registraOrdine()` (niente doppioni "in attesa"); stato "scaduto" visibile in Gestione e Account. Oggi in `acquisti` non c'è nessun ordine (quello RiskGuard del 6 novembre non c'è più).
- Calendario (strumenti): la stella segue l'INDICATORE (chiave = ticker + paese, colonna `serie` in `cal_iscrizioni`); funzioni `cal-iscrivi` e `cal-avvisi` aggiornate (versione 2). I dati "effettivo" arrivano da TradingView: possono tardare per i dati minori. Il sito si aggiorna ogni 30 s e al ritorno sulla pagina.
- Deploy funzioni Supabase senza CLI: `POST https://api.supabase.com/v1/projects/swlztverwfgdgchgpudt/functions/deploy?slug=NOME` con file multipart `index.ts` e metadata `{"entrypoint_path":"index.ts","name":"NOME","verify_jwt":false}`. Il controllo di sicurezza può bloccare deploy e modifiche al database di produzione: serve l'ok esplicito di Gabriele ("metti online" / "approvo"), poi si riesegue.
- Netlify siti: riskly `44a1076d-45d2-4c1e-a702-541fbc7a3010`, strumenti `0f4adbce-96a2-4a3f-ba7c-e500a0f3f4ad`, news `abca6d6e-64d8-40cb-a0c5-776d787d16ac`.
- Da fare: video dei bot e copertina del corso hanno ancora nero/giallo acceso (andrebbero rifatti nello stile nuovo); rigenerare la chiave ElevenLabs; mercoledì 18 verbali Fed.

## Aggiornamento del 10 novembre 2026 (copertine senza Netlify)
- Il 10 novembre Netlify ha bloccato i nuovi deploy ("Account credit usage exceeded"): ogni nuova copertina obbligava a rifare il deploy del sito news.
- Soluzione (approvata da Gabriele): le copertine stanno nell'archivio pubblico `copertine` di Supabase. `python3 notizie/carica_copertina.py ID` carica `nuovo/news/copertine/ID.jpg` (tramite la funzione `supabase/functions/copertina-carica`, che legge il codice di caricamento dalla tabella privata `config_interna`) e stampa l'indirizzo completo da mettere nel campo `copertina` dell'articolo. NIENTE più deploy Netlify per gli articoli (Netlify serve solo per modifiche al sito). Tutte le copertine esistenti sono state caricate e i campi `copertina` aggiornati.
- Le routine (articolo del giorno, straordinarie, Setup XAU pomeriggio) sono già aggiornate a questo metodo. Per i dati USA il prompt della sessione separata ora parte 25 minuti prima e dice di clonare il repository (il 10 novembre la sessione per il CPI è partita 8 minuti in ritardo, senza repository, e ha chiuso senza pubblicare: l'articolo del CPI l'ha scritto questa sessione).
- Da fare: Gabriele deve aggiungere crediti Netlify per poter di nuovo pubblicare modifiche ai siti (riskly.trade, strumenti, news).
- Lezione: l'insert in `notizie` manda subito la notifica: caricare la copertina PRIMA dell'insert.
- Reel sponsor: social/sponsor (4 versioni: prodotti, news, calc, journal; `node social/sponsor/rendi.js <versione>`; voce Marco con `ELEVEN_API_KEY` senza spazi). Programmati su Metricool dal 10 al 14 novembre, tutti su Instagram, TikTok e YouTube.
- Journal: corretto (PR #62) il bug per cui non si potevano selezionare «P.B./B.O. EMA200 + Alligator».
- COPERTINE DEI VIDEO (10 novembre, richiesta di Gabriele: "occhio sempre alle copertine"): TikTok, Instagram e YouTube usano il PRIMO fotogramma, che nei reel "Il punto" (punto.js) e nei reel sponsor è sfocato o in dissolvenza. Prima di programmare un video: `python3 social/reel/copertina.py ingresso.mp4 uscita.mp4 [secondo]` aggiunge 0,2 s con un fotogramma nitido (secondo 2.0 per i reel "Il punto", 2.4 per gli sponsor) e si programma il file in `cover/`. Guardare sempre la copertina (primo fotogramma) prima di programmare. Le copertine dei video già pubblicati su TikTok (r14, r15 e il reel di Riskly News del 10 novembre) non si possono cambiare da qui. Tutti i reel ancora programmati al 10 novembre (r16–r20 e i reel sponsor su prodotti, calcolatori, journal) sono già stati aggiornati.
- STILE DEI VIDEO (10 novembre, scelta di Gabriele: "usa questo stile"): da adesso tutti i reel nuovi si fanno nello stile di social/sponsor (sfondo blu notte con griglia, oro e blu, Instrument Serif/Sans, tanti effetti: colpo e lampo di apertura, raggi di luce, onde d'urto, crepe, schede che entrano di lato, quadranti e barre animate, battito rosso, barra di avanzamento, effetti sonori e voce di Marco). Renderer: `node social/sponsor/rendi.js <versione>`; voce e testi in `social/sponsor/varianti.json` + `python3 social/sponsor/voce.py <versione>`. Il formato "pre-news" (versione `prenews`, oro e dollaro protagonisti, tre scenari + effetto sui tassi + esempio vero) si rifà prima di ogni dato USA cambiando il blocco `PRE` in sponsor.html (nome, ora, atteso, precedente) e i testi in varianti.json; aggiornare la probabilità FedWatch la mattina dell'uscita. Poi `copertina.py` e Metricool (Instagram+TikTok e YouTube). I reel "Il punto" già programmati (r16–r20) restano nel vecchio stile.
- Pre-news n.1 (PPI di venerdì 13 novembre, 14:30) programmato venerdì 13 alle 11:45 (Instagram+TikTok) e 12:15 (YouTube). Controllare che l'84% FedWatch sia ancora valido la mattina del 13.

## Aggiornamento dell'11 novembre 2026 (articoli di valore e meno token)
- Gabriele (11 novembre): gli articoli devono restare COMPLETI e di valore; si risparmia solo sui compiti leggeri (modelli più economici ammessi lì). Il Setup XAU va arricchito con valore tecnico e operativo.
- SETUP XAU, nuova struttura (ogni parte con titolo in MAIUSCOLO): COSA HA FATTO L'ORO · IL TREND SULLE MEDIE · LE ZONE OSSERVATE · I PIVOT DEL GIORNO E DELLA SETTIMANA · STRUTTURA SETTIMANALE E VOLATILITÀ (Bollinger, distanza dalle medie, ATR in % ) · ORE E SESSIONI: QUANDO SI MUOVE DI PIÙ · CORRELAZIONI A 20 SEDUTE · LOTTI E STOP: TABELLA D'ESEMPIO · QUANTO SI MUOVE (ATR) E RSI. I numeri delle sezioni nuove vengono da `python3 notizie/setup_xau_extra.py` (pivot classici giornalieri e settimanali, struttura settimanale, Bollinger 20/2, correlazioni, ore più mosse in ora italiana, mappa delle sessioni, tabella dei lotti con rischio 1%); i numeri di base da `python3 notizie/setup_xau.py <png>`. Tabella dell'articolo con righe aggiuntive (pivot, Bollinger, correlazioni, ore più mosse). Sempre solo livelli e statistiche: MAI segnali, ingressi, obiettivi o previsioni; i lotti sono esempi.
- CONTROLLO ORARIO (notizie straordinarie): ora lo fa lo script `notizie/controlla_movimenti.py` (soglie, max 2 al giorno, "già spiegato da un dato"): stampa STOP o SERVE. Routine leggera "Riskly News · controllo movimenti (leggero)" (trig_018DfoT8aPFuH8k4fypsDbid, sessione separata, modello Haiku, alle :12 dalle 9 alle 22 lun–ven): se STOP risponde una riga; se SERVE lancia con fire_trigger la routine "Riskly News · scrivi notizia straordinaria (su richiesta)" (trig_01NQAvFXKfx4QJCYByfSRpZ9, modello predefinito) che scrive e pubblica l'articolo completo. La vecchia routine oraria dentro la sessione principale (trig_01Ux3gvJynUhmPmsHyWFx4e3) è disattivata.
- SETUP XAU, FORMATO DEFINITIVO (11 novembre, indicazioni di Gabriele; sostituisce l'elenco delle sezioni scritto sopra): piaceva la parte sui PIVOT e sulle ZONE IMPORTANTI DI POSSIBILE INVERSIONE e sugli ORARI PER OPERARE; via Bollinger, distanze dalle medie in %, correlazioni statistiche e altri tecnicismi: servono cose concrete. Va aggiunta la parte GEOPOLITICA E MACRO (come sta influenzando e come può influenzare il mercato di oggi e della settimana) con SCENARI INTRADAY (direzionalità possibile, scritta come scenari condizionali «se… allora…» legati a livelli e catalizzatori, non come previsioni: MAI ingressi, stop, obiettivi o compra/vendi). Sezioni, ognuna con titolo in MAIUSCOLO: COSA HA FATTO L'ORO · ZONE IMPORTANTI DI POSSIBILE INVERSIONE (da `zone_di_confluenza`) · I PIVOT DEL GIORNO E DELLA SETTIMANA · GEOPOLITICA E MACRO: COSA STA MUOVENDO IL MERCATO · COSA PUÒ MUOVERLO OGGI E QUESTA SETTIMANA (calendario in ora italiana) · SCENARI PER LA GIORNATA · ORARI IMPORTANTI PER OPERARE · LOTTI E STOP: TABELLA D'ESEMPIO. Dati: `notizie/setup_xau.py` (base e grafico) e `notizie/setup_xau_extra.py` (pivot, zone di confluenza, ore, sessioni, calendario, lotti).
- ORARI: il Setup XAU esce alle 11:00 ora italiana (routine "Setup XAU · articolo delle 11", parte alle 10:47, lun–ven e domenica "della settimana"). Alle 18:00 (parte alle 17:47) la routine di aggiornamento AGGIUNGE IN CODA all'articolo senza sostituire niente e senza nuova notifica (sezioni: AGGIORNAMENTO DELLE HH:MM · COME SONO ANDATI I LIVELLI E GLI SCENARI · COSA GUARDARE DOMANI) solo se serve (oro mosso più dello 0,4% dalle 11, o dati/notizie nuove). L'articolo del giorno (Fed, dati, macro) resta alle 7:37 e non include più il Setup.

## 13 novembre 2026: audit e piano di crescita
- Documento con audit, priorità, formule del journal, piano social di 30 giorni e roadmap: https://claude.ai/artifact/JXwnKmgY5HbZ439zM8vgVB
- Prototipo cliccabile del nuovo sito (non pubblicato): nuovo/prototipo/riskly.html (https://claude.ai/artifact/WLKCmtdmKY7mWfNU6zSH1k).
- Dati veri del 13/11: 0 acquisti nel database, 6 account, 7 in lista d'attesa, 3 notifiche News, ~210 aperture home in 30 giorni.
- Pagina nuovo/riskly/grazie.html (riskly.trade/grazie.html?p=NomeProdotto): da impostare su ogni link di pagamento Stripe (Dopo il pagamento → reindirizza). Traccia 'grazie' e, dal clic su Acquista, 'stripe-<prodotto>'.
- Lingua del sito: italiano (il brief proponeva titoli in inglese: sconsigliato). Vendita con Stripe sul sito, non MQL5.

## 13 novembre 2026: GLI ARTICOLI NON SI FERMANO MAI (ha la precedenza sul testo delle routine)
Gabriele: "Non bloccare mai gli articoli… non devono mai fermarsi, anche gli straordinari o quelli delle soglie dei rendimenti, petrolio ecc".
- Il 12 e il 13 novembre le SESSIONI SEPARATE (create_new_session_on_fire) sono fallite tutte con USAGE_LIMIT_REACHED: Setup XAU delle 11 e delle 18, PPI. Le routine legate a QUESTA sessione hanno sempre funzionato.
- Quindi ogni articolo parte in QUESTA sessione:
  - Setup XAU delle 11: trig_014V7M3YgjQMnfKaF6peQFc2 (10:49, dom–ven). Aggiornamento delle 18: trig_01FjJaP73CrMFvHgmktC9ZEc (17:49, lun–ven); se l'articolo del giorno manca, lo pubblica.
  - Straordinarie (soglie su petrolio, oro, dollaro, decennale, indici): il controllo orario (Haiku, trig_018DfoT8aPFuH8k4fypsDbid) chiama trig_016teaKetUaGHtWcAw89ep33, che arriva qui.
  - Dati USA e discorsi Fed (punto F della routine del mattino): NON creare più sessioni separate. Per ogni uscita crea un promemoria una tantum IN QUESTA SESSIONE (create_trigger senza create_new_session_on_fire, oppure send_later) 5 minuti prima dell'uscita, con dato, ora, attese e precedente. All'arrivo: valore dal calendario TradingView, articolo, copertina, insert, poi la reazione dopo 16 minuti.
  - Vecchie routine a sessione separata: spente (trig_016ebCnjLxqzhFjao5tU6Ag8, trig_017FUpk5kyF4aUCKvUSHRk6k). trig_01NQAvFXKfx4QJCYByfSRpZ9 resta come riserva.
- Un messaggio di una routine ha la precedenza sul lavoro in corso: se arriva mentre si lavora ad altro, prima l'articolo, poi si riprende.
- Durante lavori lunghi (più di 30 minuti) controllare l'orologio: se è passata l'ora di un articolo (7:37, 11:00, 18:00, dati USA) e manca in public.notizie, pubblicarlo subito.
- Controllo del mattino (punto G): select degli articoli di ieri; se manca il Setup XAU o un dato USA importante, recuperarlo.

## 14 novembre 2026: partner e affiliazioni
- Pagina nuovo/riskly/partner.html (riskly.trade/partner): si compila dall'array PARTNER in fondo al file (nome, tipo, descrizione, punti verificabili, link di affiliazione https, codice, vantaggio, logo in /img/partner/). Con la lista vuota mostra "Stiamo selezionando i partner" ed è noindex; con almeno un partner attivo toglie il noindex da sola. Link con rel="sponsored", scritta "Link di affiliazione" su ogni scheda, avviso in alto. Non è nel menu: aggiungerla al menu e al piè di pagina quando c'è il primo partner.
- MAI mettere un partner senza accordo firmato e link vero di Gabriele. Niente broker (CONSOB/ESMA): solo prop firm e servizi.
- Concorrente di riferimento: riskguardmanagement.com (Montorio Michele, Sossano VI, dal 2021). ATTENZIONE: il loro prodotto si chiama RiskGuard come il nostro software: proposto a Gabriele di rinominare il nostro.
- Banner dei cookie: nuovo/cookie.js copiato in ogni sito (riskly, strumenti, news, journal) con <script src="/cookie.js" defer>. Consenso in localStorage riskly-consenso; "Contenuti esterni" = calendario TradingView (riskly-tv-ok).

## 14 novembre 2026: software venduti su MQL5 (decisione di Gabriele: "tutti e due", poi "abbassa")
- Profilo venditore: https://www.mql5.com/it/users/riskly/seller. 6 prodotti, MT5/MT4: RisklyPro 205282/205462 (99 $), RiskGuard 205467/205470 (69 $), RisklyCopy 205472/205475 (79 $), RisklyTrailing 205477/205479 (49 $), RisklyScalen=ScaleIn 205481/205483 (49 $), RisklyManager=TradeManager 205484/205486 (49 $).
- Sul sito i prezzi dei software sono uguali a MQL5, in dollari. I pulsanti portano a MQL5. Stripe per i software è SPENTO finché Gabriele non crea 6 link Stripe con i nuovi prezzi (i vecchi hanno i prezzi di lancio): azioneProdotto() manda alla pagina /software/<nome>.
- Pagine prodotto generate da nuovo/riskly/pagine_software.py (dizionari P, MQL5, MQL5_NOME). Modifica lì e rilancia, poi deploy.
- Tolto lo sconto 30% Premium sui software (non applicabile su MQL5). Lo sconto 50% sul videocorso per chi compra un software resta: si dà a mano con la ricevuta MQL5.
- Da fare su MQL5 (Gabriele): correggere RisklyScalen in RisklyScaleIn; scegliere un solo nome tra TradeManager e RisklyManager.

## Copertine con vidIQ (14 novembre 2026, Gabriele: "ora sì che mi piace", "anche per le copertine dei reel utilizzalo")
- vidIQ (MCP `mcp__vidIQ__*`) fa le copertine: `vidiq_generate_thumbnail` (22 crediti) poi `vidiq_job_poll`; `vidiq_score_title` (5 crediti) per scegliere il titolo YouTube tra 2 varianti.
- Crediti: 150 AL MESE (si ricaricano il 9 di ogni mese), controlla con `vidiq_balance` (gratis). Bastano per circa 6 copertine al mese. Ordine: 1) miniatura del video del sabato "La settimana dell'oro"; 2) copertine dei reel migliori della settimana (attualità/pre-news). Quando restano meno di 22 crediti: copertina nostra (copertina.py) come prima.
- Prompt copertina: stile blu notte e oro, cifra grande vera e verificata (es. "ORO −4,9%"), al massimo 2 scritte, niente persone, niente marchi altrui, niente "compra/vendi", niente previsioni. Reel: orientation "portrait"; YouTube: "landscape". Controlla SEMPRE che numeri e testo siano giusti prima di usarla.
- Salva la copertina nel repository (es. social/youtube/vNN-miniatura-vidiq.png o social/reel/cover/rNN-vidiq.png) e passala a Metricool come videoThumbnailUrl. Su TikTok la copertina personalizzata vale solo con account Business; il primo fotogramma nitido (copertina.py) resta comunque.

## Instagram: griglia "vetrina" (14 novembre 2026, Gabriele: "chiaro ma basta, non voglio avere 100 post, devono esserci pochi post che rappresentano l'azienda"; scelta: "zero caroselli")
- La griglia Instagram ha SOLO i 9 post vetrina chiari v01–v09 (social/caroselli/caroselli.json, anteprima in social/caroselli/anteprima-vetrina.jpg), pubblicati il 14/11 dalle 11:12 alle 11:20 (v09 per primo, v01 "Cos'è Riskly" in alto a sinistra).
- MAI più caroselli o post nella griglia di Instagram. I caroselli vanno solo su TikTok.
- Reel su Instagram: sempre instagramData.showReelOnFeed = false (escono nella sezione Reel, non nella griglia).
- I vecchi post li archivia Gabriele dall'app (l'API non può archiviare). Se un prodotto o un prezzo cambia, si rifà il post vetrina corrispondente (stesso stile chiaro) e Gabriele archivia il vecchio.
- Il 14/11 sono stati tolti da Instagram i caroselli programmati (restano su TikTok) e messi in bozza quelli solo Instagram (15, 18, 20 novembre).
- REEL INSTAGRAM SCURI (14/11, Gabriele: "No quello scuro"): tutti i reel, anche su Instagram, restano nello stile scuro di social/sponsor (blu notte e oro), uguali tra loro; un solo file per Instagram, TikTok e YouTube. Copertine vidIQ dei reel: scure (blu notte e oro). Il tema chiaro (`rendi.js <versione> --chiaro`) esiste ma NON si usa.
- STILE DEI REEL "FUMETTO" (14/11, Gabriele: "No intendo bianco e nero"): da ora TUTTI i reel (Instagram, TikTok, YouTube) si fanno in bianco e nero stile fumetto: `node social/sponsor/rendi.js <versione> --fumetto` (carta bianca, inchiostro nero, titoli Bangers, testi Comic Neue, retino a puntini, cornice nera). Prova: social/sponsor/sponsor-prodotti-fumetto.mp4. Copertine vidIQ dei reel nello stesso stile (bianco e nero, fumetto, retino, niente colori). Gli stili --arancio, --giornale e --chiaro restano solo come prove.

## 15 novembre 2026: blocco email usa e getta (approvato da Gabriele)
- Database: tabella public.domini_usa_e_getta (10.233 domini, lista disposable-email-domains), funzione public.email_ammessa(e) (anon e authenticated), trigger blocca_email_usa_e_getta BEFORE INSERT su auth.users che solleva 'email_usa_e_getta'. SQL in supabase/email_usa_e_getta.sql. Per sbloccare un dominio: delete from public.domini_usa_e_getta where dominio = '...'.
- Siti (riskly.trade, strumenti, news, journal): rEmailAmmessa() prima di signUp + messaggio "Le email temporanee (usa e getta) non sono accettate". Provato dal vivo il 15/11: signup con @mailinator.com rifiutato, nessun account creato.
- La conferma dell'email era già attiva (confirmation_sent_at su tutti gli account dal 23/9).

## 15 novembre 2026: calendario economico sul database
- Tabella `cal_eventi` (stessi campi di TradingView, paese in minuscolo) e `cal_stato` (fonte attiva, errori, ultimo aggiornamento). Lettura pubblica, scrittura solo dalla funzione. SQL: supabase/calendario-dati.sql.
- Funzione `cal-aggiorna` (pg_cron ogni minuto, stessa intestazione x-cron di cal-avvisi): ogni minuto finestra vicina (−6 h → +36 h), ogni 30 minuti finestra larga (−10 g → +35 g) e pulizia oltre 60 giorni.
- Fonte: TradingView (scelta di Gabriele: "lasciamo TradingView"; nessuna licenza, rischio di blocco). Dopo 30 minuti di errori passa da sola a biquote.io (gratis, uso commerciale permesso, dati MQL5, righe doppie tolte) e torna a TradingView appena risponde. Una sola fonte alla volta in tabella.
- Strumenti legge da `cal_eventi` (calDalDatabase); la vecchia lettura /api/calendario resta come riserva. I bot useranno il calendario interno di MetaTrader 5.
- Sezione "Calendario economico" (15/11): strumenti.riskly.trade/calendario (redirect 200 su index.html, classe html.cal-solo: menu laterale Dashboard/Journal/News/Calendario economico/Strumenti, scura se l'utente non ha scelto). Stesso calendario anche nella scheda Calendario di Strumenti. Tabella (ora, valuta, evento, impatto, effettivo, previsto, precedente, stella), filtri a pillole impatto e valuta (calStato.valute; se scegli valute ignora i paesi), paesi nel pannello "Paesi", periodi Oggi/Domani/Settimana/Prossimi 14 giorni/Preferiti. Dettaglio: effettivo, previsto, precedente, scostamento (effettivo − previsto, o − precedente se manca il previsto), spiegazione, notizie collegate da notizie_anteprima (parole chiave in CAL_NEWS_PAROLE, altrimenti le ultime). CSS in fondo al blocco style, classi ce-*.
- Riskly News (15/11): riquadro "Calendario economico" nella home (prossimi 5 dati ad alto impatto di us, eu, gb, jp, de da cal_eventi, aggiornato ogni minuto; link a strumenti.riskly.trade/calendario). Nomi italiani in nuovo/news/cal-nomi.js, copia del blocco CAL_NOMI…calRifinisci di strumenti: se cambia lì, ricopiarlo. Bandiere copiate in nuovo/news/bandiere. Voce "Calendario economico" del menu Altro → /calendario.

## 15 novembre 2026: prove scadute, lista d'attesa, email da Riskly
- Regola dei 30 giorni (approvata): account journal in prova scaduta senza abbonamento → avviso via email, eliminazione 30 giorni dopo la scadenza. Testi aggiornati in FAQ (riskly.trade) e informativa privacy (online).
- Lista d'attesa: svuotata (7 iscritti eliminati il 15/11).
- Email di servizio: Resend, team "gabrieleliberto45", dominio verificato mail.riskly.trade (DNS su Netlify: TXT resend._domainkey.mail, CNAME rsend.mail, CNAME send.mail). Mittente Riskly <noreply@mail.riskly.trade>, reply_to info@riskly.trade. Chiave Resend (solo invio) salvata come network secret dell'ambiente per api.resend.com: si usa "Authorization: Bearer proxy-injected". Script: supabase/email-avviso-prova.py manda "Nome:email" … MAI dal Gmail personale (errore del 15/11: email promozionale da Gmail a andrea e Valentina senza consenso né disiscrizione).
- Il vecchio account Resend che manda le email di conferma (dominio riskly.trade) non è accessibile a Gabriele: non toccare quei record DNS.
- Prove scadute: avvisi → andrea e Valentina avvisati il 15/11 (eliminazione dal 15/12, promemoria trig_01TRTonutrkFSKKE2iXinKV3; l'eliminazione chiede conferma a Gabriele). Damiano (lib…@icloud): non scrivere (Gabriele). Le eliminazioni automatiche ricorrenti sono state bloccate dal controllo di sicurezza: si fanno a mano, con conferma.

## 16 novembre 2026: passaggio a una sessione nuova (consumo token)
- Questa sessione (session_01Rox5Y5v2hULn9FEaTyuG55) era diventata lunghissima: i compiti programmati vengono ricreati nella sessione nuova e quelli vecchi SPENTI (non cancellati).
- Helper SQL: /tmp/q.py non esiste nei container nuovi. Ricrealo: funzione q(sql) che fa POST https://api.supabase.com/v1/projects/swlztverwfgdgchgpudt/database/query con Authorization Bearer ${SUPABASE_ACCESS_TOKEN// /}, Content-Type application/json, User-Agent Mozilla/5.0, body {"query": sql}.
- Controllo movimenti (trig_018DfoT8aPFuH8k4fypsDbid, Haiku, ogni ora 9–22 lun–ven): script dentro il prompt (non clona GitHub), niente Brent. Quando trova SERVE chiama fire_trigger sul compito "notizia straordinaria" della sessione principale.
- 16/11 pubblicati: 2026-11-16-oro-sotto-3860-warsh (7:37), 2026-11-16-setup-xau (11:00 + aggiornamento 18:00 con Empire State 7,8 vs 18), 2026-11-16-warsh-super-intelligenza-politica-monetaria (sessione separata).
- Riskly News su computer: articolo a tutta larghezza con colonna destra (calendario + ultimi articoli), classe #vista.v-articolo.
- Account: "Esci" su tutti i siti usa signOut({ scope: 'local' }) (prima scollegava tutti i siti e dispositivi).

## TRASLOCO DEI COMPITI PROGRAMMATI (16/11/2026, da fare nella sessione principale nuova)
Una sessione può legare a sé i compiti solo creandoli lei. Nella sessione nuova, per OGNI id qui sotto: get_trigger(id) → create_trigger con lo STESSO name, la STESSA cron_expression o run_once_at e lo STESSO prompt copiato parola per parola (initiation human_request, senza persistent_session_id: così fira in questa sessione); poi update_trigger(id vecchio, enabled=false) (spegnere, NON cancellare).
- trig_012rxjXzAKQwTK2ioAY1Luu6 · articolo del giorno (CRON_TZ=Europe/Rome 37 7 * * *)
- trig_014V7M3YgjQMnfKaF6peQFc2 · Setup XAU delle 11 (CRON_TZ=Europe/Rome 49 10 * * 0-5)
- trig_01FjJaP73CrMFvHgmktC9ZEc · Setup XAU aggiornamento delle 18 (CRON_TZ=Europe/Rome 49 17 * * 1-5)
- trig_016teaKetUaGHtWcAw89ep33 · notizia straordinaria su richiesta (nessun orario: create_trigger senza cron né run_once_at)
- trig_017R7vovVrevt6fbBmJw9TTa · Riskly social settimanale (CRON_TZ=Europe/Rome 50 10 * * 5)
- trig_01VUvYbBN939a7pRZpi4Nhxb · YouTube La settimana dell'oro (CRON_TZ=Europe/Rome 47 8 * * 6)
- trig_01ML9tmvZ2TUsGggN4gYXJDQ · vendite al dettaglio (run_once_at 2026-11-17T13:05:00Z) — solo se non è già passato
- trig_01FVvmAwHhbc3Y7jMdKaW8s3 · verbali Fed (run_once_at 2026-11-18T18:35:00Z)
- trig_01TRTonutrkFSKKE2iXinKV3 · prove scadute andrea e Valentina (run_once_at 2026-12-15T09:07:00Z)
Poi nel controllo orario trig_018DfoT8aPFuH8k4fypsDbid (update_trigger, solo prompt): sostituisci trig_016teaKetUaGHtWcAw89ep33 con l'id del NUOVO compito "notizia straordinaria". Lascia invariato trig_01NQAvFXKfx4QJCYByfSRpZ9 (riserva).
Alla fine: list_triggers per verificare che i nuovi siano enabled e legati a questa sessione, e messaggio a Gabriele di una riga.

## 16 novembre 2026 (sera): compiti spostati nella sessione nuova (session_01Rox5Y82H3wuFvLiNNm8L9A)
- NUOVI (in questa sessione): aggiornamento Setup 18:00 trig_016aKYv4FJPHcarvMNqqXK2V · notizia straordinaria su richiesta trig_01XxTbrBMgDqoN8h3sihZRGD (il controllo orario trig_018DfoT8aPFuH8k4fypsDbid ora chiama questo) · vendite al dettaglio 17/11 trig_01L31GabBwWQdjDzgPRdMpvB · verbali Fed 18/11 trig_01VG7wvXaLcN8Mso2dQuh9r6 · prove scadute 15/12 trig_01SzBDu7nreHFSXGpbswdmNg · YouTube sabato trig_019J5Wdry7NJHTfb6qwsRBjP · social venerdì trig_018hEFGpXyEY2c8tgdRnZe7Q.
- VECCHI GIÀ SPENTI: trig_016teaKetUaGHtWcAw89ep33, trig_01ML9tmvZ2TUsGggN4gYXJDQ, trig_01TRTonutrkFSKKE2iXinKV3, trig_01VUvYbBN939a7pRZpi4Nhxb.
- COMPLETATO (16/11 sera): creati qui anche articolo del giorno trig_015vzb2URdCQk9ipHhLwrtyH (7:37) e Setup XAU delle 11 trig_017Ms7gu1XRiLaaf4UxAZvBw (10:49). Spenti tutti i vecchi della sessione session_01Rox5Y5v2hULn9FEaTyuG55 (articolo del giorno, Setup 11, Setup 18, verbali, social, oltre a quelli sopra). Restano accesi a parte: controllo orario Haiku trig_018DfoT8aPFuH8k4fypsDbid e riserva trig_01NQAvFXKfx4QJCYByfSRpZ9.

## 16 novembre 2026: controllo sicurezza (dopo il reel VibeCodingLab)
- Corretto (approvato da Gabriele): la vista notizie_anteprima (gira come postgres) dava a anon/authenticated INSERT/UPDATE/DELETE → chiunque poteva modificare/cancellare/creare articoli (e far partire le push). Ora solo SELECT. Il trigger proteggi_piano blocca anche stripe_cliente. SQL: supabase/sicurezza-16-novembre.sql. Verificato: lettura anteprime 200, modifica anonima 401.
- Ok: nessuna chiave segreta nella storia git; HTTPS+HSTS su tutti i siti; RLS su tutte le tabelle; firma Stripe con tolleranza 10 min; funzioni con token (copertine, cron, Telegram); esc() su tutti i campi delle news.
- Da fare (Gabriele): attivare "Leaked password protection" in Supabase → Authentication → Passwords; rigenerare la chiave ElevenLabs. Header mancanti (nosniff/X-Frame-Options su strumenti, X-Frame-Options su news) al prossimo deploy Netlify.
- Reel "10 controlli prima di usare un EA sul conto reale": versione `ea` di social/sponsor (rendi.js ea --fumetto), file social/sponsor/cover/sponsor-ea-fumetto.mp4. Programmato martedì 17/11: Instagram+TikTok 13:00 (Metricool 430585145), Short YouTube 18:00 (430585253).

## 17 novembre 2026: Netlify, paletta 60-30-10, News su computer
- ERRORE MIO (16/11 sera): tre deploy per togliere "Powered by Netlify" hanno esaurito i crediti Netlify (1.000/mese, ricarica automatica SPENTA) → tutti i siti (riskly, strumenti, news, app) offline dalle 20:58 del 16/11 al mattino del 17/11, finché Gabriele ha aggiunto crediti. REGOLA: prima di ogni deploy chiedere/controllare i crediti (l'API non mostra il saldo; accounts → usages_exceeded), raggruppare le modifiche in un solo giro. Periodo nuovo dal 20 di ogni mese.
- "Powered by Netlify": nascosto via cookie.js (stile #nl-badge-frame,#nl-hud-frame) in tutti i siti.
- Paletta 60-30-10 scelta da Gabriele (versione A): 60% base carta #F6F6F3/#FFF, 30% contrasto blu notte #12263F/#1B3A5C (menu, barre, aperture delle pagine, fasce, piè di pagina, intestazioni tabelle), 10% scintilla oro #D4AE5A (pulsanti principali, prezzi, icone, fascia "frase"), testo oro su chiaro #8A6420, su blu #F1D58F. File unico nuovo/paletta.css copiato in nuovo/riskly, nuovo/strumenti, nuovo/news (collegato dopo serio.css; pagine software tramite pagine_software.py). Se si modifica: cambiare nuovo/paletta.css e ricopiarlo nei tre siti. Escluse per ora: privacy, quiz, partner, download, journal (main).
- News su computer: la fascia "Oggi" a tutta larghezza scivolava sotto l'elenco di destra e lasciava vuota la colonna sinistra; corretto in nuovo/news/serio.css (:has(> .lista) → grid-column:1).
