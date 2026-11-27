# HANDOFF · Riskly News, gli articoli giornalieri (come funzionano)

Aggiornato il 27 novembre 2026. Questo file parla SOLO degli articoli di Riskly News: cosa sono, chi li scrive, a che ora escono, dove stanno, come si pubblicano, quali regole valgono e cosa può andare storto. Non contiene chiavi né testi di articoli.
(Per tutto il resto del progetto vedi `HANDOFF.md`; per i social vedi la sezione «SOCIAL FERMI» lì dentro: i social NON c'entrano con gli articoli.)

---

## 1. Cos'è Riskly News

- Servizio di notizie e analisi su **USA, Fed, dollaro, oro** (news.riskly.trade), con abbonamento a parte: **6,99 €/mese**.
- **Pubblico:** titolo, sommario e copertina di ogni articolo (anteprima).
- **Solo abbonati:** il testo completo, le tabelle, i grafici, le fonti. Chi ha un acquisto attivo «Riskly News…» (funzione `ha_news()`, tabella `acquisti`, stato `attivo`) legge tutto.
- Ogni articolo pubblicato manda una **notifica push** agli iscritti (parte da sola all'inserimento nel database).
- Temi ammessi: Fed (decisioni, verbali, discorsi), aspettative sui tassi (FedWatch), lavoro USA, inflazione USA (CPI, PCE, PPI), PIL, vendite al dettaglio, ISM, dollaro, Treasury, oro. La BCE solo nei giorni di decisione. **Niente** Banca d'Inghilterra, Giappone, Svizzera o altre banche centrali.
- Lingua: italiano, semplice e diretto. Segno meno «−», numeri all'italiana (3.649,7 $, 3,8%), orari in **ora italiana**.

## 2. Dove vive tutto

| Cosa | Dove |
|---|---|
| Articoli | Supabase, progetto `swlztverwfgdgchgpudt`, tabella `public.notizie` |
| Anteprima pubblica | vista `public.notizie_anteprima` (solo SELECT per tutti) |
| Copertine e grafici | bucket pubblico `copertine` di Supabase Storage (si caricano con `notizie/carica_copertina.py`) |
| Sito | news.riskly.trade → file `nuovo/news/index.html` (Netlify, sito `abca6d6e-64d8-40cb-a0c5-776d787d16ac`) |
| Codice e script | repository GitHub `gabrieleliberto45-eng/riskly-app`, branch `claude/come-ti-sembra-nmri8v` (pubblico) |
| Copia di sicurezza di copertine e grafici | nella cartella `nuovo/news/copertine/` del repository |
| Testi degli articoli | **SOLO nel database.** Mai nel repository (bozze solo nella cartella temporanea) |
| Schema e permessi | `supabase/news.sql` (+ migrazioni successive) |

Il sito NON si deve rifare (deploy Netlify) per pubblicare un articolo: legge tutto dal database e dal bucket. Un deploy serve solo se si cambia il sito stesso (costa 15 crediti Netlify su 300 al mese; il periodo parte il giorno 20; controllare i crediti prima e raggruppare le modifiche).

### Struttura di una riga in `notizie`

| Campo | Contenuto |
|---|---|
| `id` | `AAAA-MM-GG-slug` (il Setup è `AAAA-MM-GG-setup-xau`, l'articolo dei dati `AAAA-MM-GG-scenari-dati-slug`) |
| `data` | data dell'articolo |
| `categoria` | `oro`, `dollaro`, `fed`, `tassi`, `straordinarie`, `settimana`, `setup`, `dati` |
| `titolo` | con il fatto e i numeri |
| `sommario` | 2 frasi (è la parte gratuita) |
| `corpo` | JSON: elenco di righe di testo. Una riga TUTTA MAIUSCOLA e corta è un **titolo di sezione**. Una riga `GRAFICO\|<url del bucket copertine>\|didascalia` è un'immagine (il sito la mostra come figura) |
| `da_guardare` | elenco di 2–4 punti con orari italiani |
| `fonti` | elenco di **oggetti** `{nome, url}` (mai stringhe: errore fatto il 25/11 e corretto) |
| `tabella` | elenco di coppie `[etichetta, valore]`; **mai null** (se non serve, `[]`) |
| `copertina` | indirizzo completo `https://swlztverwfgdgchgpudt.supabase.co/storage/v1/object/public/copertine/ID.jpg` |
| `creato` | automatico |

## 3. La giornata degli articoli (ora italiana)

| Ora | Cosa | Giorni | Chi lo fa |
|---|---|---|---|
| 07:37 | **Articolo del giorno** (cosa è successo nelle ultime 24 ore; la domenica «La settimana che arriva», categoria `settimana`). Programma anche le sessioni per i dati delle 14:30 | ogni giorno | compito `trig_015vzb2URdCQk9ipHhLwrtyH`, in questa sessione |
| 10:49 → esce ~11:00 | **Setup XAU** (livelli, volume profile, dollaro e rendimenti con grafici, scenari). La domenica «Setup XAU della settimana» | domenica–venerdì | compito `trig_017Ms7gu1XRiLaaf4UxAZvBw`, in questa sessione |
| 11:12 → esce ~11:30 | **Articolo dei dati** («scenari-dati»): solo nei giorni con dati USA importanti. Cosa esce, stime delle banche (in tabella), «sopra/in linea/sotto le attese», livelli dell'oro | lun–ven | compito `trig_01DqC42a6zUgpefkSZnZDmgq`, in questa sessione |
| 25 min prima del dato (es. 14:05 per le 14:30) | **Articolo istantaneo del dato**: pubblicato appena escono i numeri, poi aggiornato 16 minuti dopo con la reazione di oro, dollaro, decennale, EUR/USD | solo giorni con dati | sessione separata una tantum, creata dal compito delle 07:37 |
| 17:49 → ~18:00 | **Aggiornamento delle 18:00 del Setup XAU**: si aggiunge IN CODA allo stesso articolo (nessuna seconda notifica). Si fa solo se l'oro si è mosso ≥0,4% dalle 11:00 o ci sono notizie rilevanti | lun–ven | compito `trig_016aKYv4FJPHcarvMNqqXK2V`, in questa sessione |
| ogni ora al minuto 12, dalle 9 alle 22 | **Controllo straordinarie**: se oro, dollaro, petrolio, decennale o future S&P/Nasdaq superano le soglie, scrive e pubblica un articolo «straordinarie» | lun–ven | compito `trig_01HdS7FYDWMCDxTMYPdS8gNt`, sessione separata, modello Sonnet |

**27/11/2026, sera:** gli articoli sono passati a una chat dedicata. I 4 compiti «in questa sessione» (`trig_015vzb2URdCQk9ipHhLwrtyH`, `trig_017Ms7gu1XRiLaaf4UxAZvBw`, `trig_01DqC42a6zUgpefkSZnZDmgq`, `trig_016aKYv4FJPHcarvMNqqXK2V`) sono stati **spenti** nella vecchia chat e ricreati nella nuova, con gli stessi orari. Gli identificativi sopra sono quindi quelli vecchi: per i nuovi guardare `list_triggers`.

Compiti spenti (non cancellati): `trig_018DfoT8aPFuH8k4fypsDbid` (vecchio controllo con Haiku), `trig_01HEdkvCEiG17hjg86Yt1P6A` (controllo dentro questa chat).

Regola d'oro di Gabriele (13/11): **«Gli articoli non devono mai fermarsi.»** Se manca un articolo, lo si recupera subito; si scrive a Gabriele solo se qualcosa non funziona o serve una sua decisione (mai per mandargli gli articoli: «sprechi solo token», 8/11).

## 4. Come si scrive e si pubblica un articolo (procedura)

1. **Accessi.** Le chiavi sono variabili d'ambiente: `SUPABASE_ACCESS_TOKEN` (e `NETLIFY_AUTH_TOKEN` solo per il sito). Si usano togliendo gli spazi (`"${VAR// /}"`), **mai stampate, mai scritte in file o commit**. Verifica: `GET https://api.supabase.com/v1/projects/swlztverwfgdgchgpudt` deve dare 200. Se non dà 200 non si pubblica.
2. `cd /home/user/riskly-app && git pull` (se il repository manca: `git clone -b claude/come-ti-sembra-nmri8v https://github.com/gabrieleliberto45-eng/riskly-app`). Leggere `HANDOFF.md` (regola fonti, regole in cima).
3. **Controllare gli articoli già usciti** (select degli ultimi `id`, `categoria`, `titolo`) per non ripetersi né contraddirsi.
4. **Raccogliere i fatti** (sezione 7): almeno due fonti per ogni fatto, prezzi da Yahoo, calendario da TradingView.
5. **Scrivere l'articolo** nel formato del tipo (sezione 5). Bozze fuori dal repository.
6. **Copertina** (sezione 6): crearla, guardarla, poi `python3 notizie/carica_copertina.py ID` (stampa l'indirizzo completo). **La copertina va caricata PRIMA dell'insert.**
7. **Insert** in `public.notizie` con `POST https://api.supabase.com/v1/projects/swlztverwfgdgchgpudt/database/query` (header `Authorization: Bearer <token>` e `User-Agent: Mozilla/5.0`, body `{"query": "..."}` fatto con `json.dumps`; apici raddoppiati, `::jsonb` sui campi JSON, `on conflict (id) do nothing`). **L'insert manda subito la notifica push.**
8. **Verificare** con una select (id, numero di righe del corpo, copertina).
9. `git add` della copertina (e dei grafici `ID-*.jpg`, e di `notizie/higgsfield_registro.json`), commit e push (copia di sicurezza). Niente deploy Netlify.
10. Se qualcosa fallisce: riprovare fino a 3 volte, poi avvisare Gabriele. Se il controllo automatico dei comandi non risponde, programmare un nuovo tentativo tra 10 minuti.

Un **update** (aggiornamento in coda) NON manda notifiche: si usa per l'aggiornamento delle 18:00 e per la reazione dei primi 15 minuti. Si concatena: `corpo = corpo || nuovo::jsonb` (idem per `tabella`, `da_guardare`, `fonti`), senza toccare il resto. Dopo l'update verificare che il testo e le fonti di prima ci siano ancora tutti.

## 5. I formati

Principio generale (Gabriele 11/11 e 23/11): ogni parte ha un **titolo in MAIUSCOLO** e un paragrafo breve; articoli **completi ma non pesanti** («le cose che non servono toglile»). Niente numeri ripetuti, niente elenchi inutili. L'ultima riga è sempre: «Contenuto informativo ed educativo, non è consulenza finanziaria né un'indicazione di acquisto o vendita.» (nel Setup si aggiunge «Il trading con leva comporta un alto rischio di perdita del capitale.»).

### 5.1 Articolo del giorno (07:37)
Sezioni: la notizia (cosa è successo), reazione dei mercati, perché l'oro si muove così, **ASPETTATIVE SUI TASSI** (sempre: probabilità FedWatch per la prossima riunione Fed, confronto con i giorni prima, frasi dei membri Fed delle ultime 24 ore con nome, ruolo e se vota quest'anno), **COSA SIGNIFICA PER L'ORO E IL DOLLARO** (sempre: perché si muovono rendimenti e dollaro, per paura o per attese sulla Fed, se è un giorno o una tendenza, cosa significa per l'oro anche quando la teoria non funziona, due soglie con i numeri), cosa guardare. Nei dati USA si spiega sempre che i mercati reagiscono alla **sorpresa rispetto alle attese**, non al confronto col mese prima. 1 articolo (2 solo per un fatto grosso). Votanti Fed 2026: presidenti di New York, Cleveland, Philadelphia, Dallas, Minneapolis; i governatori votano sempre. Citazioni brevi e verificate col testo dell'agenzia.
I **grafici di dollaro e rendimenti NON vanno qui**: stanno nel Setup (Gabriele 22/11).

### 5.2 Setup XAU (11:00) e aggiornamento 18:00
Circa 14–16 paragrafi, categoria `setup`, titolo «Setup XAU: …» **senza dati economici** (Gabriele 25/11). Sezioni:
1. **COSA HA FATTO L'ORO** (2–3 frasi; RSI/ATR/medie solo se estremi).
2. **I LIVELLI DI OGGI**: pivot e volume profile sono livelli osservati, non segnali; massimo 3 livelli sopra e 3 sotto con cosa ci si sovrappone; vuoto volumetrico solo se il prezzo è dentro o vicino; la nota sul cambio di contratto solo a fine mese; riga `GRAFICO` del volume profile.
3. **DOLLARO E RENDIMENTI: COSA DICONO** (dove vanno, giorno o tendenza, perché: paura o Fed, cosa significa per l'oro, due soglie con i numeri) + le due righe `GRAFICO` (dollaro 6 mesi con media a 50 giorni; rendimenti a 5 e 10 anni).
4. **COSA MUOVE IL MERCATO**: Fed/FedWatch più UN altro motivo (non un dato economico).
5. **SCENARI**: 3 frasi «se… allora…» legate ai livelli; non sono previsioni né consigli.
6. **ORARI E LOTTI**: l'orario delicato e un esempio di lotto marcato come ESEMPIO (conto 10.000 $, rischio 1%, stop di 1 ATR).
Tabella di massimo 8 righe (prezzo, ultima seduta, 2 livelli sopra e 2 sotto, POC/VAH/VAL del giorno prima, dollaro, decennale), `da_guardare` solo sui livelli. Se ci sono dati importanti, UNA frase che rimanda all'articolo dei dati.
**Aggiornamento 18:00** (in coda, senza notifica): AGGIORNAMENTO DELLE 18:00 (cosa è cambiato dalle 11: prezzo, Fed, borse, geopolitica) · COME SONO ANDATI I LIVELLI E GLI SCENARI (quale scenario del mattino si è verificato, senza correggere il passato) · COSA GUARDARE PER LA SERA; 2–3 righe in coda alla tabella.
La domenica: «Setup XAU della settimana».

### 5.3 Articolo dei dati delle 11:30 («scenari-dati»)
Solo nei giorni con dati USA importanti (importance 1 su TradingView: payrolls, disoccupazione, CPI, PCE, PPI, PIL, vendite al dettaglio, ISM, JOLTS, fiducia Michigan, ADP; più decisione/verbali Fed e discorsi di Powell/Warsh; i sussidi da soli NO). Sezioni: COSA ESCE OGGI · PREVISIONI DELLE BANCHE · PERCHÉ CONTA LA SORPRESA · SE ESCE SOPRA / IN LINEA / SOTTO LE ATTESE (effetto su FedWatch, rendimenti, dollaro, oro, come scenari condizionali) · I LIVELLI DELL'ORO · DOPO I DATI.
**Previsioni delle banche (Gabriele 25/11):** una **tabella per ogni dato** (PCE, PIL, CPI, payrolls…), mai un paragrafo che mescola banche e dati. Si crea con `python3 notizie/tabella_banche.py ID NOME spec.json` (immagine nella paletta del sito, caricata nel bucket; stampa la riga `GRAFICO|…`). Righe fisse e nello stesso ordine: consenso (evidenziato), Goldman Sachs, Morgan Stanley, U.S. Bank, Citigroup, poi le altre molto influenti (Bank of America, JPMorgan; Wells Fargo/Deutsche Bank/UBS solo se hanno una cifra pubblica). Niente RBC, società di ricerca o Fed regionali. **Mai inventare una cifra**: dove la banca non ha pubblicato il numero c'è «—»; se una stima viene da una sola fonte lo si scrive nella nota.

### 5.4 Articolo istantaneo del dato (all'uscita)
Pubblicato in pochi minuti dall'uscita: titolo col numero contro le attese, sezioni COSA È USCITO · PREVISIONI DELLE BANCHE (confronto con le tabelle delle 11:30: chi ci è andato vicino) · PERCHÉ I MERCATI REAGISCONO ALLA SORPRESA · COME HANNO REAGITO ORO, DOLLARO E RENDIMENTI · ASPETTATIVE SUI TASSI · COSA SIGNIFICA PER L'ORO E IL DOLLARO · COSA GUARDARE ORA. Categoria `dati` o `fed`. **16 minuti dopo** si aggiunge in coda «LA REAZIONE NEI PRIMI 15 MINUTI» con numeri verificati. La copertina qui è quella disegnata (`illustra.py`): la velocità conta più della copertina IA. Se il valore non esce in 10 minuti o fallisce dopo 3 tentativi: fermarsi senza inventare. Per i discorsi Fed: sessione 20 minuti dopo l'inizio, solo citazioni verificate, se non parla di tassi o economia non si pubblica.

### 5.5 Straordinarie
Sezioni: COSA È SUCCESSO · LA REAZIONE DEI MERCATI · PERCHÉ L'ORO SI MUOVE COSÌ (anche quando la teoria non funziona) · ASPETTATIVE SUI TASSI · COSA GUARDARE ORA. Categoria `straordinarie`, titolo con fatto e numeri.
**Quando partono** (script `notizie/controlla_movimenti.py`, una riga di risposta: `STOP: …` oppure `SERVE: …`): soglie sul giorno / nell'ultima ora: petrolio WTI ±4% / ±2,5%; oro ±1,5% / ±1%; indice del dollaro ±0,6%; decennale ±8 punti base; future S&P 500 e Nasdaq ±1,5% / ±1%. Niente Brent (salti finti al cambio contratto). **Stop** se: nessuna soglia superata; già 2 straordinarie oggi; movimento solo sul giorno già spiegato da un dato/Fed/tassi recente; già una straordinaria oggi e nessun nuovo scatto nell'ultima ora. La causa va verificata con almeno 2 fonti: se non è chiara o è una voce non confermata, **non si pubblica**.

## 6. Copertine

- **Preferita (Higgsfield):** `generate_image`, modello `gpt_image_2_6`, 16:9, 1 immagine (0,75 crediti), prompt in inglese per un'illustrazione editoriale sul tema, palette carta `#F6F6F3`, blu notte `#12263F`, oro `#D4AE5A`, terzo inferiore scuro, angoli in alto liberi, sempre «NO text, NO letters, NO numbers, NO logos, NO people, NO real brands». Poi `python3 notizie/copertina_ia.py ID URL "CATEGORIA" "TITOLO" "NUMERO"` aggiunge logo, categoria, titolo e numero e salva `nuovo/news/copertine/ID.jpg`. **Guardare sempre l'immagine** (titolo leggibile, numero esatto, niente scritte/persone/loghi); se non va, rigenerare UNA volta, poi ripiegare sul disegnato. Categorie scritte: Oro, Dollaro, Fed, Tassi e banche centrali, Straordinarie, Dati USA, La settimana.
- **Budget:** massimo **100 crediti Higgsfield al mese** in tutto, circa 35 per gli articoli; leggere `notizie/higgsfield_registro.json` (lo script lo aggiorna) e **fermarsi a 90–95**. Usati a fine novembre: ~9,75.
- **Riserva (disegnata):** `python3 notizie/illustra.py ID SCENA "CATEGORIA" "TITOLO" "NUMERO"` (scene: fed, bce, lingotti, setup, petroliera, fabbrica, lavoro, capitol, dollaro, borsa, calendario con `GIORNO=0…4`; evitare «inflazione»; richiede `NODE_PATH=/opt/node22/lib/node_modules`). Si usa se Higgsfield non c'è (le sessioni separate non lo hanno), se i crediti sono finiti o dopo due tentativi falliti.
- **Setup:** la copertina è il grafico del prezzo (`setup_xau.py` crea un PNG 1600×900 da convertire in JPG).
- Mai foto né persone reali, mai opere protette di terzi.

## 7. Dati e fonti

- **Prezzi (Yahoo, v8 chart):** oro `GC=F`, argento `SI=F`, dollaro `DX-Y.NYB`, decennale `^TNX`, 5 anni `^FVX` (non usare `2YY=F`), Treasury 10 anni `ZN=F` (se sale, i rendimenti scendono), future `ES=F` e `NQ=F`, indici `^GSPC` e `^IXIC`, `NVDA`, petrolio `CL=F`, `EURUSD=X`. Chiamata: `https://query1.finance.yahoo.com/v8/finance/chart/<SIMBOLO>?range=1d&interval=5m` con `User-Agent: Mozilla/5.0`. `^TNX` è in % (4,86 = 4,86%).
- **Calendario:** `GET https://economic-calendar.tradingview.com/events?from=…Z&to=…Z&countries=US` con header `Origin: https://www.tradingview.com`. Date in UTC: **+1 ora per l'Italia fino a marzo**. Campo `actual` per il valore uscito.
- **FedWatch:** probabilità per la riunione Fed successiva (confrontare con i giorni prima). Prossima riunione: 8–9 dicembre 2026.
- **Script del Setup:** `notizie/setup_xau.py` (dati e grafico), `notizie/setup_xau_extra.py` (pivot, zone di confluenza, ore più mosse, lotti), `notizie/volume_profilo.py ID` (volume profile a intervallo fisso sul future COMEX: ultima settimana e giorno precedente; POC oro, VAH rosso, VAL verde, vuoti volumetrici in grigio; crea e carica `ID-vp.jpg`), `notizie/grafici_macro.py ID` (crea e carica `ID-dxy.jpg` e `ID-tassi.jpg`). Nota: nei giorni dopo festività USA il volume del giorno prima è basso e va detto. A fine mese il cambio di contratto può spostare i livelli.
- **Regola fonti (23/11, Gabriele: «usa anche qualche altra fonte»):** per TUTTI gli articoli: almeno **3 fonti diverse**, al massimo **UNA** di Investing.com (e mai come unica fonte di un fatto); ordine di preferenza: 1) ufficiali (federalreserve.gov, BLS, BEA, Census, Treasury, CME FedWatch), 2) agenzie e grandi testate (Reuters, Bloomberg, AP, CNBC, WSJ, MarketWatch, Kitco, Il Sole 24 Ore, ANSA), 3) siti di analisi (FXStreet, InvestingLive) solo come complemento. Per i dati USA si cita sempre il comunicato ufficiale; per le frasi dei membri Fed il testo su federalreserve.gov o l'agenzia. Ogni fatto con almeno 2 fonti.

## 8. Regole fisse (non negoziabili)

- **Niente segnali, previsioni certe, compra/vendi, ingressi, stop o obiettivi reali.** Solo fatti e scenari condizionali «se… allora…». Gli esempi di numeri sono marcati come ESEMPIO.
- Le previsioni delle banche sono previsioni **del dato** attribuite alla banca, non previsioni nostre.
- **Mai inventare** cifre, citazioni o fonti. Se non si trova, si scrive «—» o si omette.
- Non mandare a Gabriele gli articoli.
- Chiavi mai in chiaro; articoli mai nel repository.
- Le modifiche allo schema del database di produzione richiedono l'approvazione esplicita di Gabriele.
- Niente deploy Netlify per pubblicare articoli.
- La palette A del sito: carta `#F6F6F3`, blu notte `#12263F`, oro `#D4AE5A`.

## 9. Dove girano i compiti (e perché conta)

- I compiti segnati «in questa sessione» (07:37, Setup, dati 11:30, aggiornamento 18:00) parlano nella **sessione principale** (`session_01Rox5Y82H3wuFvLiNNm8L9A`): hanno Higgsfield, Metricool, Supabase. Se la sessione è ferma o si riavvia, i compiti restano in coda e partono tutti insieme appena torna attiva: **è successo tra il 26 e il 27 novembre** (vedi sezione 10).
- Le sessioni **separate** (controllo straordinarie, articoli istantanei dei dati) partono da zero a ogni giro, **non hanno** strumenti per avviare altri compiti (`fire_trigger`, `send_message`), **non hanno** Higgsfield né Metricool, non hanno il repository clonato (devono clonare quello pubblico in `/tmp/r`). Per questo usano `illustra.py` e scrivono e pubblicano da sole. Non possono avere connettori dai compiti creati da qui: per averli bisogna crearli/modificarli dalla pagina Routine di claude.ai.
- Il modello delle sessioni separate: Sonnet 5.5 per il controllo straordinarie (richiesta di Gabriele il 24/11 per avere articoli più solidi); le altre sessioni usano il modello predefinito. Cambiare il modello di un compito richiede la richiesta esplicita di Gabriele.
- Le sessioni separate in passato si sono fermate per il limite di utilizzo: per questo il Setup, l'articolo del giorno e l'aggiornamento 18:00 sono stati riportati nella sessione principale.

## 10. Cosa è andato storto (e cosa si fa)

| Quando | Problema | Cosa si fa |
|---|---|---|
| 23/11 e 24/11 | Il controllo orario vedeva il movimento ma non poteva far partire la straordinaria (nessun `fire_trigger`/`send_message` nelle sue sessioni) | Ora il controllo scrive e pubblica da solo. Articoli di quei giorni scritti a mano |
| 25/11 | Per un errore, nell'aggiornamento 18:00 le fonti del mattino furono sovrascritte (erano oggetti, io ho filtrato come stringhe) | Ripristinate dal registro della sessione. **Le fonti sono sempre oggetti `{nome,url}` e in un update si concatenano** |
| 26–27/11 | La sessione principale si è riavviata più volte: nessun articolo del giorno né Setup giovedì 26 e venerdì mattina 27, notifiche in ritardo | Recuperati alle 17:16–17:40 del 27. Il giovedì era festa USA, quindi nessun dato perso. Se si ripete: **prima cosa, controllare con una select cosa manca** e recuperare nell'ordine: articolo del giorno → Setup → dato importante |
| ogni tanto | Il controllo automatico dei comandi non risponde | Riprovare; programmare un nuovo tentativo tra 10 minuti |

**Controllo di sicurezza ogni mattina (compito delle 07:37, punto G):** se ieri mancava un articolo o un dato USA importante, recuperarlo; controllare che le sessioni separate di ieri abbiano pubblicato.

## 11. Comandi utili

Elenco ultimi articoli (in Python, con la chiave dall'ambiente senza spazi):
```python
import os, json, urllib.request
tok = os.environ['SUPABASE_ACCESS_TOKEN'].replace(' ', '')
def q(s):
    r = urllib.request.Request('https://api.supabase.com/v1/projects/swlztverwfgdgchgpudt/database/query',
        data=json.dumps({'query': s}).encode(),
        headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r, timeout=30))
for a in q("select id,categoria,left(titolo,90) t,creato from notizie order by creato desc limit 12"): print(a)
```
Insert (schema): `insert into public.notizie (id,data,categoria,titolo,sommario,corpo,da_guardare,fonti,tabella,copertina) values ('…','AAAA-MM-GG','oro','…','…','[...]'::jsonb,'[...]'::jsonb,'[...]'::jsonb,'[...]'::jsonb,'https://…/copertine/ID.jpg') on conflict (id) do nothing`.
Aggiornamento in coda: `update notizie set corpo = corpo || '[...]'::jsonb, tabella = tabella || '[...]'::jsonb where id = '…'`.

Script da `/home/user/riskly-app`:
```bash
python3 notizie/controlla_movimenti.py        # STOP o SERVE per le straordinarie
python3 notizie/setup_xau.py /percorso/s.png  # dati e grafico del Setup
python3 notizie/setup_xau_extra.py            # pivot, zone, ore, lotti
python3 notizie/volume_profilo.py ID          # volume profile (crea e carica ID-vp.jpg)
python3 notizie/grafici_macro.py ID           # dollaro e rendimenti (crea e carica 2 immagini)
python3 notizie/tabella_banche.py ID NOME spec.json   # tabella delle stime per un dato
python3 notizie/copertina_ia.py ID URL "Oro" "Titolo" "NUMERO"
python3 notizie/illustra.py ID SCENA "Oro" "Titolo" "NUMERO"   # copertina disegnata (NODE_PATH=/opt/node22/lib/node_modules)
python3 notizie/carica_copertina.py ID        # carica nel bucket e stampa l'indirizzo
```

## 12. Lista di controllo prima di premere «pubblica»

- [ ] Titolo col fatto e i numeri; sommario di 2 frasi.
- [ ] Ogni parte ha il suo titolo in MAIUSCOLO; l'ultima riga è l'avviso.
- [ ] Almeno 3 fonti diverse, al massimo una Investing.com, comunicato ufficiale citato nei dati USA.
- [ ] `fonti` = oggetti `{nome,url}`; `tabella` mai null.
- [ ] Nessun segnale, compra/vendi, previsione certa; numeri all'italiana, segno «−».
- [ ] Orari in ora italiana, controllati sul calendario.
- [ ] Copertina guardata e già caricata; l'indirizzo nel campo `copertina`.
- [ ] Dopo l'insert: select di verifica, poi commit e push di copertina e grafici.
