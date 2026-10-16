from h import *
LEZIONE = L('11.3', 'Modulo 11', 'Extra: mente, margine e costi', 'Swap e costi di tenere aperto', [
 T('LEZIONE 11.3', 'Swap: il costo **della notte**', 'Quanto costa tenere una posizione aperta per giorni.', "Lezione undici punto tre. Lo swap, il costo di tenere aperta una posizione durante la notte. Nel modulo due abbiamo visto spread, commissioni e slippage. Manca un costo che si paga piano piano, e per questo si dimentica."),
 P('Cos\'è lo swap', [('Un interesse giornaliero', 'pagato o incassato per ogni notte in cui la posizione resta aperta'), ('Dipende dai tassi', 'dal differenziale tra le due valute, più il ricarico del broker'), ('Spesso triplo', 'di solito il mercoledì notte sulle valute, per coprire il weekend')],
  ["Che cos'è lo swap.",
   "È un interesse giornaliero: lo paghi, o a volte lo incassi, per ogni notte in cui la posizione resta aperta oltre la chiusura della giornata di trading.",
   "Dipende dal differenziale dei tassi tra le due valute della coppia, più il ricarico del broker. Per questo spesso è negativo in entrambe le direzioni.",
   "E di solito, sulle valute, il mercoledì notte lo swap è triplo, per coprire il fine settimana. Il giorno esatto lo trovi nelle specifiche del simbolo."]),
 EX('Quanto costa davvero', [['Swap', '−7 € per lotto a notte'], ['Posizione', '0,40 lotti'], ['Tenuta', '10 notti, con 2 mercoledì'], ['Notti pagate', '10 + 2 × 2 = 14'], ['Costo', '0,40 × 7 × 14 = 39,20 €'], ['Rischio del trade', '100 € = 1 R']], risultato='Costo dello swap: circa 0,4 R', k=[1,2,3,4,5,6,7],
  voce=["Facciamo i conti con numeri illustrativi.", "Swap di meno sette euro per lotto a notte.", "Posizione da zero virgola quaranta lotti.", "La tieni dieci notti, e in mezzo ci sono due mercoledì.", "Ogni mercoledì conta tre volte, quindi le notti pagate sono quattordici.", "Zero virgola quaranta per sette per quattordici: trentanove euro e venti.", "Se il trade rischiava cento euro, cioè un R, lo swap ti è costato circa zero virgola quattro R. Su un sistema da più zero virgola ventisei R a trade, è più di tutto il vantaggio."]),
 P('Cosa fare', [('Leggi le specifiche', 'tasto destro sul simbolo → Specifiche: swap long, swap short, giorno triplo'), ('Mettilo nel calcolo', 'nei trade lunghi lo swap si somma ai costi, in R'), ('Prop firm e conti islamici', 'regole diverse: alcune prop vietano di tenere nel weekend')],
  ["Cosa fare in pratica.",
   "Leggi le specifiche del simbolo sulla piattaforma: trovi lo swap per le posizioni long, per quelle short e il giorno in cui è triplo.",
   "Se fai trade che durano giorni, metti lo swap nel calcolo dei costi, convertito in R come abbiamo fatto per spread e commissioni.",
   "E controlla le regole del tuo conto: alcuni conti non applicano lo swap, ma hanno altre commissioni, e alcune prop firm vietano di tenere posizioni nel fine settimana."]),
 RIEP(['Lo swap è un interesse per ogni notte di posizione aperta, spesso negativo in entrambe le direzioni', 'Di solito triplo il mercoledì sulle valute: controlla le specifiche', 'Nei trade lunghi va nel calcolo dei costi, in R'],
  ["Riassumiamo.", "Lo swap è un interesse per ogni notte di posizione aperta, e spesso è negativo in entrambe le direzioni.", "Di solito è triplo il mercoledì sulle valute: il giorno esatto è nelle specifiche.", "E nei trade che durano giorni va messo nel calcolo dei costi, in R."]),
 Q('Il costo che non vedi **lo paghi lo stesso**.', "Il costo che non vedi lo paghi lo stesso."),
])
