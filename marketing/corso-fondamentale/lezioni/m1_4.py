from h import *
LEZIONE = L('1.4', 'Modulo 1', 'Come il mercato reagisce alle notizie', 'Spread, slippage e gap nei minuti del dato', [
 T('MODULO 1 · LEZIONE 4', 'Nei minuti del dato, **le regole cambiano**', 'Spread più larghi, ordini eseguiti a prezzi diversi, salti di prezzo.',
   "Nei minuti intorno a un dato importante, il mercato funziona in modo diverso dal solito. Gli spread si allargano, gli ordini vengono eseguiti a prezzi diversi da quelli impostati, e il prezzo può saltare. Vediamo cosa succede e perché."),
 TB('Cosa cambia', ['Fenomeno', 'Cosa succede'], [
   ['Spread', 'la differenza tra prezzo di acquisto e di vendita si allarga, anche di molte volte'],
   ['Liquidità', "pochi ordini disponibili: chi fornisce prezzi si ritira finché il dato non esce"],
   ['Slippage', "lo stop diventa un ordine a mercato ed è eseguito al primo prezzo disponibile"],
   ['Gap', 'il prezzo salta da un livello all\'altro senza passare per quelli in mezzo']],
   ["Quattro cose cambiano.",
    "Lo spread: la differenza tra il prezzo di acquisto e quello di vendita si allarga, a volte di molte volte rispetto al normale.",
    "La liquidità: nei secondi prima del dato chi fornisce i prezzi si ritira, e ci sono pochi ordini disponibili.",
    "Lo slippage: quando il prezzo tocca il tuo stop, lo stop diventa un ordine a mercato ed è eseguito al primo prezzo disponibile, che può essere molto peggiore.",
    "E il gap: il prezzo può saltare da un livello all'altro senza passare per quelli in mezzo."]),
 EX('Esempio illustrativo: lo stop che salta', [
   ['Posizione', 'EURUSD, 0,50 lotti, stop a 20 pip'],
   ['Rischio previsto', '20 pip × 5 € (valore del pip arrotondato) = 100 €'],
   ['Al dato', 'il prezzo salta di 35 pip in un secondo'],
   ['Stop eseguito', 'a 35 pip invece di 20']],
   ["Un esempio con numeri illustrativi. Hai una posizione su euro dollaro, mezzo lotto, con lo stop a venti pip.",
    "Il rischio previsto è di cento euro: venti pip per cinque euro a pip.",
    "Esce il dato e il prezzo salta di trentacinque pip in un secondo.",
    "Lo stop viene eseguito a trentacinque pip invece di venti. La perdita è di centosettantacinque euro: quasi il doppio di quella prevista."],
   risultato='Perdita 175 € invece di 100 €', k=[1, 2, 3, 5]),
 P('Cosa fare', [
   ('Chiudere o ridurre prima', 'se non vuoi essere esposto al dato'),
   ('Niente ordini a ridosso', 'pendenti e stop vicini al prezzo sono i più esposti'),
   ('Lotto più piccolo', "se resti dentro, calcola il rischio con uno slippage possibile"),
   ('Aspettare', 'dopo qualche minuto spread e liquidità tornano normali')],
   ["Cosa fare, allora?",
    "Se non vuoi essere esposto al dato, chiudi o riduci la posizione prima.",
    "Evita ordini piazzati a ridosso dell'orario: pendenti e stop molto vicini al prezzo sono i più esposti.",
    "Se decidi di restare dentro, usa un lotto più piccolo e calcola il rischio considerando che lo stop possa essere eseguito più lontano.",
    "Oppure aspetta: dopo qualche minuto spread e liquidità tornano normali."]),
 P('Uno strumento che ti aiuta', [
   ('Riskly Pro', 'filtro notizie: non apre operazioni nei minuti vicini ai dati importanti (prodotto mio)')],
   ["Lo dichiaro, perché è un mio prodotto: Riskly Pro ha un filtro notizie, che impedisce di aprire operazioni nei minuti vicini ai dati importanti. Non è l'unico modo: lo stesso risultato lo ottieni con il calendario e un po' di disciplina."]),
])
