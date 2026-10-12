# RisklyCopy — copiatore di operazioni tra conti (MT4 e MT5)

Stato: prima versione, **non ancora compilata né provata**. Da compilare in MetaEditor (`RisklyCopy.mq5` per MT5, `RisklyCopy.mq4` per MT4) e provare su conti demo prima di venderla.

## Come funziona
- Sul conto principale: RisklyCopy in modalità **Invia** (su un grafico qualsiasi; un solo grafico basta per tutto il conto).
- Sugli altri conti: RisklyCopy in modalità **Ricevi**, stesso **Nome del canale**.
- I conti si parlano dalla cartella comune di MetaTrader (`%APPDATA%\MetaQuotes\Terminal\Common\Files\RisklyCopy`): funziona tra MT4 e MT5 **sullo stesso computer o VPS**. Conti su computer diversi: versione futura via journal.
- Si può usare insieme a Riskly Pro: ogni bot sul suo grafico (MT5 permette un bot per grafico, non uno per terminale).

## Il lotto sul conto che riceve
| Modo | Cosa fa |
|---|---|
| In proporzione al saldo (predefinito) | lotto principale × saldo di questo conto ÷ saldo del principale: **stessa % di rischio** |
| Rischio % sullo stop loss | lotto calcolato perché, se tocca lo stop, perdi la % scelta (senza stop usa il saldo) |
| Moltiplicatore | stesso lotto × moltiplicatore |
| Lotto fisso | sempre lo stesso lotto |

**Conti piccoli.** Esempio: principale da 10.000 € con 0,50 lotti, secondario da 100 €: il lotto giusto sarebbe 0,005, sotto il minimo del broker (0,01).
Con *"Conto piccolo: copia al lotto minimo e raggruppa"* attivo (predefinito):
- la prima operazione si copia al lotto minimo 0,01;
- le successive sullo stesso simbolo e direzione si aprono solo quando la somma dei lotti giusti delle posizioni aperte sul principale supera quello già aperto sul secondario.
- Esempio: 10 operazioni da 0,50 sul principale → sul secondario 5 posizioni da 0,01 (alle operazioni 1, 4, 6, 8, 10): stessa esposizione totale (0,05).
- La prima operazione da sola rischia il doppio (0,01 invece di 0,005): è il prezzo del lotto minimo. Se vuoi un tetto, imposta *"rischio massimo con il lotto minimo (%)"*.
Con il raggruppamento spento, le operazioni sotto il minimo non vengono copiate.

## Cosa copia
Apertura di posizioni a mercato, chiusura, chiusura parziale (in proporzione), modifica di stop loss e take profit. **Non** copia ordini pendenti (copia la posizione quando si attivano).

## Sicurezze
- Il conto principale non manda la lista finché non è collegato al broker (e per 5 s dopo l'avvio): così una lista vuota all'apertura di MetaTrader non fa chiudere tutto ai conti che ricevono.
- Una copia si chiude solo se la posizione manca dal principale per 3 letture di fila.
- Chiusura parziale su un principale MT4: la posizione resta la stessa (il nuovo ordine "from #" eredita il numero), quindi il secondario chiude in proporzione invece che tutto.
- Modifica di stop/take profit rifiutata dal broker: un solo tentativo per ogni cambiamento, niente richieste a raffica.
- Se il conto principale non aggiorna da 15 s (MetaTrader chiuso, PC spento) il secondario **non fa nulla**: non chiude niente per sbaglio.
- Non copia posizioni aperte da più di 60 s o con prezzo spostato di oltre 30 pip.
- Lotto massimo e numero massimo di posizioni.
- Se una copia fallisce riprova al massimo 5 volte.
- Le posizioni chiuse a mano sul secondario non vengono riaperte.

## Da fare prima della vendita
- Compilare e provare su demo: MT5→MT5, MT4→MT5, MT5→MT4, chiusure parziali, simboli con suffisso.
- Aggiungere lo stesso controllo della licenza degli altri bot.
- Conto MT5 in modalità netting: non supportato (avviso all'avvio).
- Conti in valute diverse (EUR e USD): in modalità "saldo" il rapporto usa i saldi così come sono; meglio usare "rischio %".
