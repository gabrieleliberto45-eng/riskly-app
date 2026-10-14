from h import *
LEZIONE = L('1.4', 'Modulo 1', 'Come il mercato reagisce alle notizie', 'Spread, slippage e gap nei minuti del dato', [
 T('MODULO 1 · LEZIONE 4', 'Nei minuti del dato, **le regole cambiano**', 'Spread più larghi, ordini eseguiti a prezzi diversi, salti di prezzo.',
   "Finora abbiamo parlato di direzione: dove può andare il prezzo dopo un dato. Ora parliamo di una cosa che riguarda tutti, anche chi non vuole fare trading sulle notizie: nei minuti intorno a un dato importante, il mercato funziona in modo diverso dal solito. E se non lo sai, puoi perdere più di quanto avevi deciso di rischiare."),
 TB('Cosa cambia', ['Fenomeno', 'Cosa succede'], [
   ['Spread', 'la differenza tra prezzo di acquisto e di vendita si allarga, anche di molte volte'],
   ['Liquidità', "pochi ordini disponibili: chi fornisce prezzi si ritira finché il dato non esce"],
   ['Slippage', "lo stop diventa un ordine a mercato ed è eseguito al primo prezzo disponibile"],
   ['Gap', "il prezzo salta da un livello all'altro senza passare per quelli in mezzo"]],
   ["Vediamo cosa cambia, e soprattutto perché.",
    "Lo spread, cioè la differenza tra il prezzo a cui puoi comprare e quello a cui puoi vendere. Normalmente sull'euro dollaro è di una frazione di pip. Nei secondi del dato può diventare di diversi pip. Il motivo è che chi fornisce i prezzi, banche e intermediari, non sa dove andrà il mercato e si protegge allargando la differenza.",
    "La liquidità, cioè la quantità di ordini pronti a essere eseguiti. Prima di un dato molti operatori ritirano i loro ordini e aspettano di vedere il numero. Il mercato si svuota, e bastano pochi ordini per spostare il prezzo di molto.",
    "Lo slippage, la parte che fa più male. Lo stop loss non è una garanzia di prezzo: quando il prezzo lo tocca, lo stop diventa un ordine a mercato, ed è eseguito al primo prezzo disponibile. In un mercato normale è praticamente lo stesso prezzo. In un mercato vuoto, il primo prezzo disponibile può essere molto più lontano.",
    "E il gap: il prezzo può saltare da un livello all'altro senza passare per quelli in mezzo. Se il tuo stop era proprio in mezzo, verrà eseguito al primo prezzo dopo il salto."]),
 EX('Esempio illustrativo: lo stop che salta', [
   ['Posizione', 'EURUSD, 0,50 lotti, stop a 20 pip'],
   ['Rischio previsto', '20 pip × 5 € (valore del pip arrotondato) = 100 €'],
   ['Al dato', 'il prezzo salta di 35 pip in un secondo'],
   ['Stop eseguito', 'a 35 pip invece di 20']],
   ["Facciamo i conti con un esempio, numeri inventati e arrotondati. Hai una posizione su euro dollaro di mezzo lotto, con lo stop a venti pip dal prezzo di entrata.",
    "Con mezzo lotto, ogni pip vale circa cinque euro. Quindi hai deciso di rischiare venti pip per cinque euro: cento euro. È il rischio che hai calcolato, magari l'uno per cento del conto.",
    "Esce il dato, ed è una sorpresa contro di te. In un secondo il prezzo salta di trentacinque pip, senza fermarsi nei livelli intermedi.",
    "Lo stop viene eseguito al primo prezzo disponibile, a trentacinque pip invece che a venti. La perdita è di centosettantacinque euro: quasi il doppio di quella che avevi deciso. Non hai sbagliato il calcolo; è il mercato che, in quei secondi, non ti ha dato il prezzo."],
   risultato='Perdita 175 € invece di 100 €', k=[1, 2, 3, 5]),
 P('Cosa fare', [
   ('Chiudere o ridurre prima', 'se non vuoi essere esposto al dato'),
   ('Niente ordini a ridosso', 'pendenti e stop vicini al prezzo sono i più esposti'),
   ('Lotto più piccolo', "se resti dentro, calcola il rischio con uno slippage possibile"),
   ('Aspettare', 'dopo qualche minuto spread e liquidità tornano normali')],
   ["Cosa puoi fare, in concreto? Hai quattro strade.",
    "La prima: chiudere, o ridurre, la posizione qualche minuto prima del dato. Se non vuoi scommettere sul numero, non c'è motivo di restare esposto.",
    "La seconda: evitare ordini piazzati a ridosso dell'orario. Un ordine pendente vicino al prezzo, o uno stop molto stretto, è il primo a essere colpito nel salto, e con lo slippage peggiore.",
    "La terza, se decidi di restare in posizione: usa un lotto più piccolo, e calcola il rischio come se lo stop potesse essere eseguito più lontano. Nell'esempio di prima, se avessi messo un quarto di lotto, anche con trentacinque pip di slippage avresti perso meno di novanta euro.",
    "La quarta: aspettare. Dopo cinque o dieci minuti, spread e liquidità tornano normali, e puoi valutare il mercato con calma."]),
 P('Uno strumento che ti aiuta', [
   ('Riskly Pro', 'filtro notizie: non apre operazioni nei minuti vicini ai dati importanti (prodotto mio)')],
   ["Lo dichiaro, perché è un mio prodotto: Riskly Pro ha un filtro notizie, che impedisce di aprire operazioni nei minuti vicini ai dati importanti. Non è l'unico modo di proteggersi: lo stesso risultato lo ottieni con il calendario, una sveglia sul telefono e un po' di disciplina. L'importante è che la decisione la prendi prima, non nel momento del dato."]),
])
