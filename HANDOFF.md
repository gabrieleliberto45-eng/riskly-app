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
