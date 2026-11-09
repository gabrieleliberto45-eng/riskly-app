# Passaggio di consegne (8 novembre 2026)

Sessione precedente: "Riskly · News, social e app (principale)" (session_01CZRW5kRhjiWo9ejMQNFKL6).
Gabriele scrive in italiano: rispondi in italiano semplice, frasi brevi.

## Regole fisse di Gabriele
- NON mandare in chat articoli o post pubblicati (8 novembre: "sprechi solo token"). Scrivere solo per errori o decisioni.
- Chiavi mai nel repository né nei commit, mai stampate. Il testo degli articoli MAI nel repository (solo Supabase o scratchpad); le copertine sì.
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
