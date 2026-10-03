# Revisione del corso «Risk Management Avanzato» (Riskly)

Materiale esaminato: `Riskly_Corso_Completo.zip` — 175 slide con copione (30 lezioni, 8 moduli), 3 file Excel, 5 grafici.
Ho letto tutte le slide e tutti i copioni, ricalcolato i numeri con simulazioni (200.000 percorsi per i casi principali), verificato i fogli Excel con un motore di calcolo e confrontato le affermazioni sui bot con la pagina prodotti del sito.

**Come leggere i numeri di slide:** sono le posizioni nel file «COMPLETO» (1–175).

---

## In sintesi

Il corso ha una buona spina dorsale (da «misuro» a «dimensiono», «simulo», «automatizzo» fino al piano scritto), un tono onesto e formule giuste quasi dappertutto. Ma **così com'è non lo venderei**: ha errori di matematica proprio sugli argomenti che insegna, due fogli Excel che non funzionano, affermazioni sui bot che non corrispondono al prodotto e nessun avviso di rischio. Sono tutte cose sistemabili in pochi giorni.

| Priorità | Quante | Cosa |
|---|---|---|
| 🔴 Da correggere prima di vendere | 9 | errori che fanno perdere credibilità o creano problemi legali |
| 🟠 Da sistemare | 10 | incoerenze interne e numeri da allineare |
| 🟡 Migliorie | 8 | qualità, ritmo, grafica |

---

## 🔴 Da correggere prima di vendere

### 1. Due fogli Excel su tre non funzionano
Verificato ricalcolando i fogli:

| Foglio | Cella | Formula attuale | Risultato attuale | Dovrebbe dare |
|---|---|---|---|---|
| 1 Calcolatore R | B11 Expectancy | `=B6*B7-(1-B6)*B8` | **1,8 R** | 0,26 R |
| | B12 Expectancy in € | `=B10*B9` | 0 € | 26 € |
| | B13 Profit factor | `=B6*B7/((1-B6)*B8)` | **#DIV/0!** | 1,47 |
| | B14/B15 su 100/200 trade | `=B11*100` | 180 / 360 | 2.600 € / 5.200 € |
| 2 Kelly + ATR | B5 Kelly pieno | `=B4-(1-B4)/B5` (si cita da sola) | 0 (riferimento circolare) | 14,4% |
| | B6 ¼ Kelly | `=B6/4` (circolare) | 0 | 3,6% |
| | B15 Stop in pip | `=B13*B14` (usa il valore del pip) | 20 | 40 |
| | B16 Rischio in € | `=B11*B12` (usa l'ATR) | 0,2 | 100 |
| | B17 Lotti | `=B16/(B15*B17)` (circolare) | 0 | 0,25 |

Le formule puntano alle righe sbagliate (spostate di una o due). Il foglio 3 (piano operativo) è un modulo senza formule e va bene.
**Fatto:** copie corrette in `marketing/corso-corretto/…_CORRETTO.xlsx`, ricalcolate: danno esattamente i numeri del corso (0,26 R, 100 €, PF 1,47, 2.600 €/5.200 €; Kelly 14,4%, ¼ Kelly 3,6%, stop 40 pip, 0,25 lotti). Gli originali non sono stati toccati.

### 2. Mancano materiali che le lezioni promettono
- **Slide 92:** «Il foglio Excel allegato al corso fa lo stesso (Monte Carlo) sul tuo computer». Non c'è nessun foglio Monte Carlo.
- **Slide 159:** «15 minuti con il foglio Excel del corso: expectancy, profit factor, **max drawdown, R realizzato contro previsto, percentuale checklist**». Il foglio 1 calcola solo expectancy e PF.
- **Slide 113:** «trovi il template [della checklist] nei materiali». Non c'è.
- **Slide 92** dice che la calcolatrice del sito dà anche la «forbice dei risultati» (10°–90° percentile): oggi dà probabilità di rovina, expectancy, risultato mediano e drawdown mediano, non la forbice.

Scelta: o si creano i tre file (posso farlo), o si tolgono le frasi.

### 3. La storia dei due trader (lezione 1.1 e 1.5) non regge
È la prima cosa che vede chi compra, e contraddice sé stessa:
- Slide 8 dice «media +1,5R a trade»; dalla 1.3 lo stesso sistema è «vincita media +1,8R, expectancy +0,26R». Slide 35 dice persino che i 5.200 € sono «gli stessi numeri della Lezione 1.1», ma lì non lo sono.
- **Il grafico (slide 9) smentisce il copione.** Il Trader A, definito «fuori mercato», finisce a **+18%** sopra il capitale iniziale. Il Trader B, che «recupera in due settimane», alla fine è ancora **19% sotto il suo massimo**. Il grafico è un percorso costruito a mano, non una simulazione.
- **Con numeri veri il racconto cambia.** Stesso sistema, 200 trade (45%, +1,8R / −1R):

| | Rischio 4% (A) | Rischio 1% (B) |
|---|---|---|
| Drawdown massimo mediano | **−35%** | −10% |
| Capitale finale mediano | 6,9× (+585%) | 1,65× (+65%) |
| Casi con drawdown oltre −50% | **10%** | ~0% |
| Casi in cui tocca −30% dal capitale iniziale | **10%** | 0% |
| Casi in cui finisce sotto l'inizio | 0,9% | 0,6% |

  «Il Trader A è fuori mercato» riguarda circa il 2% dei casi. Il vero messaggio, più forte e onesto, è: **A guadagna di più sulla carta, ma attraversa un −35% tipico (uno su dieci supera il −50%): quanti lo sopportano senza cambiare il piano?** Il rischio per trade decide quanto male si sta, non solo se si sopravvive.
- **Fatto:** nuovo grafico `equity_1_1_corretto.png` (stessa serie di trade, percorso tipico, più la distribuzione dei drawdown su 40.000 simulazioni).

### 4. Errori di matematica
Sono quelli che un lettore esperto nota e usa per non fidarsi del resto.

| Slide | Cosa dice | Cosa è giusto |
|---|---|---|
| **56** | «Cinque perdite di fila e il tuo rischio fisso è diventato il doppio in percentuale» | Con lotto fisso, dopo 5 perdite dell'1% il conto è al 95%: il rischio è 1,05%, non il doppio. Raddoppia solo dopo un −50%. |
| **58** | «…momenti in cui la probabilità di una serie avversa è più alta: dopo una serie» | È la fallacia del giocatore: se i trade sono indipendenti, la probabilità della perdita successiva non cambia. Il vero motivo: dopo una serie hai meno capitale e decidi male (emozione). |
| **63–64** | A ¼ di Kelly «la crescita è quasi identica al picco» | A ¼ Kelly la crescita è il **45%** del massimo; a ½ Kelly il 76%. Il messaggio resta valido (si perde poco rischiando molto meno), ma «quasi identica» è falso. |
| **84** | Drawdown mediano: 1% / 2% / 4% / 7% / 10% (rischio 0,5 / 1 / 2 / 3 / 5%) | Con la stessa simulazione: **5% / 10% / 19% / 28% / 43%**. I valori della tabella sono circa 1/5 di quelli veri; contraddicono le slide 29 e 97 (1% → ~12%) e il calcolatore del sito. |
| **91 e 103** | 8 perdite × 5% = −40%; × 3% = −24%; «−40% richiede +60%» | Le perdite si compongono: 8 × 5% = **−33,7%**; 8 × 3% = **−21,6%**; −40% richiede **+66,7%**. Strano dirlo proprio dopo la lezione 1.5. |
| **57** | «Al 2%… drawdown del 30–40%» | Al 2%: mediano 19%, 9 casi su 10 sotto il 28%. |
| **138** | Trailing drawdown: «all'inizio spazio 10%; dopo +5% di profitto, spazio 5%» | Con il limite che segue il massimo, a +5% lo spazio resta di 10 punti, non 5. Il pericolo vero: i profitti **non aperti** alzano il pavimento e un ritracciamento consuma lo spazio. Va riscritto con un esempio numerico corretto. |
| **82–84** | «Rovina = −30%» | Nella tabella 84 è −30% **dal capitale iniziale**. Come drawdown dal massimo darebbe: 2% → 7%, 3% → 38%, 5% → 94%. Va dichiarata la definizione (il calcolatore del sito usa quella dal capitale iniziale). |

### 5. Affermazioni sui bot che non corrispondono al prodotto
- **Slide 155:** «TradeManager replica l'esecuzione su MT4/MT5 su tutti i conti». **Non è vero.** TradeManager gestisce stop, break-even e trailing. Chi «replica la posizione in N scaglioni» è **ScaleIn**, e sullo stesso conto, non su più conti. Il testo promette una funzione che non esiste.
- **Slide 118:** «controllo esposizione correlata per cluster» non è una funzione: Riskly Pro calcola il rischio sull'insieme delle posizioni.
- **Modulo 6 «Scale-in»** parla di aggiungere a una posizione vincente (piramide), mentre il prodotto **ScaleIn** divide l'uscita in più take profit. Stesso nome, cose opposte: chi compra si confonde. Rinominare il modulo («Piramide e gestione a scaglioni»).
- **Lezione 6.3** parla di 2–5 conti; la licenza copre **2 conti**. E molte prop firm vietano o limitano la copia dei trade tra conti: va detto.
- Confermate: RiskGuard (pausa dopo perdita, stop dopo N perdite, limite giornaliero, chiusura al target, blocco di MetaTrader) corrisponde al sito.

### 6. Nessun avviso di rischio in 175 slide
La parola «consulenza» non compare mai. Il corso dà indicazioni numeriche precise («mai oltre il 2%», «challenge 0,5–1%», «stop −3R») e in tre lezioni (4.2, 4.4, 6.3) promuove i bot senza dire che sono **un prodotto dell'autore**.
Le linee guida CONSOB/ESMA sui «finfluencer» (gennaio 2026) chiedono, per forex e CFD, di ricordare che si può perdere tutto il capitale e di dichiarare gli interessi. Proposta:
- slide 2 e ultima slide: «Contenuto educativo, non consulenza finanziaria. Il trading con leva comporta un alto rischio: puoi perdere tutto il capitale. I numeri sono esempi, non promesse»;
- nelle lezioni con i bot: «Riskly è un mio prodotto».
Da far rileggere a un legale.

### 7. Statistiche e affermazioni senza fonte
Da togliere o sostituire con fatti verificabili:

| Slide | Frase |
|---|---|
| 21 | «su cui si gioca il 90 per cento dei conti» |
| 42 | «spiega il novanta per cento dei conti bruciati» |
| 54 | titolo «Il sizing che il 90% dei trader sbaglia» e «il novanta per cento… lo applica male» |
| 156 | «butta via il novanta per cento di quello che traccia la gente» |
| 43 | «…a quasi chiunque» (perdere il 90%) |
| 120 | «la stragrande maggioranza fallisce per le stesse due regole»; «sono scritte per farti fallire» (accusa a terzi) |
| 126 | «distrugge più challenge di qualsiasi drawdown» |
| 131 | «sei nel 10 per cento» |
| 132 | «statisticamente, entro i primi tre mesi» |
| 113 | «la metrica più predittiva di sopravvivenza che esista» |
| 166 | «la lezione più redditizia del corso» (promessa di guadagno) |
| 169 | «ho visto replicarsi decine di volte su journal reali»; «quattromila euro al mese che vanno dal tuo conto al tuo comportamento» |
| 36 | «commissioni e slippage mangiano 0,02–0,05R» (dipende dallo stop) |

### 8. La durata non è quella dichiarata
Il sito dice «trenta lezioni video… circa tre ore». Il copione ha **12.493 parole**: a 130–150 parole al minuto sono **83–96 minuti**, circa 1h40–2h con le pause degli esercizi. Le lezioni 1.1 (593 parole) e 1.2 (970 parole) sono 2–3 volte le altre (300–430 parole, circa 3 minuti l'una): la profondità è sbilanciata e solo le prime due hanno esercizi e anteprima della lezione successiva.
Due strade: dire «circa un'ora e mezza» sul sito, oppure allungare le lezioni 1.3–8.1 con esempi svolti sullo schermo (consigliato, vedi sotto). Con un prezzo di 199 € è meglio promettere meno e consegnare di più.

### 9. La lezione 8.2 è nel posto sbagliato
«Stress test del piano» (slide 25–29) è inserita tra la 1.2 e la 1.3, ma richiede Monte Carlo, losing streak e prop firm, che arrivano molto dopo. Va spostata dopo la 8.1 (slide 171–175).

---

## 🟠 Da sistemare (incoerenze)

1. **Aggiunte alla posizione:** slide 145 «dopo 2 add la piramide è fatta», slide 148 «max 1 add per ogni trade», slide 143 «rischio aggiuntivo max +0,5R». Scegliere una regola.
2. **Serie di perdite attese** (slide 102 e Excel): win rate 35% → «~12», 40% → «~10». Simulazione: **~10** e **~9** (mediana su 200 trade; 45–60% giusti). Corretti nell'Excel 1.
3. **Slide 52:** il copione dice «sei punti e mezzo», la slide 6,3.
4. **Slide 64:** «un quindicesimo di Kelly»: 14,4 → «circa un quattordicesimo».
5. **Slide 39:** la slide dice «PF > 2 sospetto», il copione «PF da 3».
6. **Slide 41 e 36:** «il giorno che E scende sotto zero, smetti» vs «20 trade sono rumore». Aggiungere «su un campione di almeno 100 trade».
7. **Valore del pip «10 €/lotto» (slide 73):** vale per un conto in dollari su EURUSD; in euro è circa 8,5–9 €. Scrivere «circa 10 $».
8. **ATR:** il corso usa 2×; i nostri video (z09, 7/10) usano 1,5×: allineare (si può dire «1,5–2×»).
9. **Regole delle prop (modulo 5):** presentare tutto come «esempi, rilevati a [mese anno]». Sulla consistency rule «squalificato» non è sempre vero: spesso il payout viene rifiutato o la challenge non si valida finché il rapporto non rientra.
10. **Refusi:** slide 111 «Lo setup», «nè»; 174 «mezogiorno»; 154 «si nascondo»; 93 «un scommettitore»; 150 «Alléggerisci»; 99 «incazzato» (tono).

---

## 🟡 Migliorie

1. **Grafica.** Sfondo nero, testo piccolo, molte slide con tre righe in basso e il resto vuoto; i grafici delle slide 44, 63 e 89 coprono il piè di pagina. La palette (corallo, azzurro, giallo) non è quella del brand (nero + lime #B6D84F).
2. **Più grafici.** Solo 5 slide su 175 hanno un grafico. Servono per: expectancy A contro B, win rate di pareggio, ATR, losing streak, trailing drawdown, heat del portafoglio.
3. **Esercizi.** Ce ne sono solo nelle lezioni 1.1 e 1.2. Un esercizio con soluzione per modulo e 3 domande di verifica alla fine di ogni modulo.
4. **Esempi sullo schermo.** Dimostrare il Monte Carlo con il calcolatore del sito, l'R previsto contro realizzato con il journal (ora ha la scheda dell'operazione e gli scaglioni) e il piano operativo compilato. Più credibile e allunga le lezioni in modo utile.
5. **Anteprima della lezione successiva** (slide 12 e 24) solo nelle prime due lezioni: estenderla a tutte.
6. **Frasi in prima persona** («nella mia esperienza», «per me il sabato mattina», «soglia mia»): confermare che sono vere, perché le dirai tu a voce.
7. **Materiali:** checklist stampabile, riepilogo dei numeri, glossario, tabella prop aggiornata.
8. **Chiusura del corso:** non c'è una slide finale (solo la firma del piano). Aggiungere riepilogo, avviso di rischio e dove chiedere supporto.

---

## Cosa è già buono (da non toccare)

- La **regola n.1** («valuta il trade dal rischio, non dal risultato») e il concetto **R previsto contro R realizzato**: sono il cuore e funzionano.
- Formule corrette: expectancy, profit factor, tabella del recupero, win rate di pareggio, Kelly, sizing con ATR, tabella delle serie di perdite (a meno dei due valori sopra), win rate/RR.
- Il **ventaglio Monte Carlo** (`mc_fan_3_2.png`) è accurato: mediana +65%, 10° percentile +27%, 90° +113%, in linea con la mia simulazione (+65 / +28 / +112).
- Il grafico del **drawdown aritmetico/geometrico** è corretto.
- La **tabella di rovina** (slide 84), a parte la colonna del drawdown, è confermata (3% → ~4%, 5% → ~17%).
- Le slide «limiti del modello» (74, 86, 119) sono oneste e vanno tenute: costruiscono fiducia.
- La struttura in 8 moduli e il **piano operativo in sette sezioni**.

---

## File consegnati (cartella `marketing/corso-corretto/`)

| File | Contenuto |
|---|---|
| `Riskly_Excel_1_Calcolatore_R_Expectancy_CORRETTO.xlsx` | formule sistemate; tabella delle serie aggiornata (35% → ~10, 40% → ~9) |
| `Riskly_Excel_2_Kelly_Sizing_ATR_CORRETTO.xlsx` | formule sistemate |
| `equity_1_1_corretto.png` | sostituisce `equity_1_1.png` (slide 9) |
| `kelly_2_2_corretto.png` | sostituisce `kelly_2_2.png` (slide 63): l'originale ha l'asse fino a 360% e l'etichetta del ¼ Kelly punta nel vuoto |

## Decisioni che spettano a te
1. Durata: dichiarare «circa un'ora e mezza» o allungare le lezioni?
2. Storia dei due trader: riscrivere con il messaggio del drawdown mediano (consigliato)?
3. Modulo 6: rinominarlo e togliere la replica multi-conto da TradeManager?
4. Vuoi che crei i tre materiali mancanti (Excel Monte Carlo, Excel metriche mensili, checklist)?
5. Vuoi che applichi tutte le correzioni di testo alle slide e ti restituisca il file PowerPoint corretto?

*Metodo: simulazioni Monte Carlo con win rate 45%, vincita +1,8R, perdita −1R, 200 trade, rischio costante sul capitale corrente; stessa definizione di rovina del sito (capitale sotto −30% dall'inizio). I fogli sono stati ricalcolati con un motore di calcolo e confrontati con i risultati attesi.*
