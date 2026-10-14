from h import *
LEZIONE = L('1.3', 'Modulo 1', 'Come il mercato reagisce alle notizie', 'Il prezzo anticipa le notizie', [
 T('MODULO 1 · LEZIONE 3', 'Quando la notizia arriva, è **già nel prezzo**', "Il mercato si muove sulle aspettative, prima che i fatti accadano.",
   "C'è un vecchio detto dei mercati: compra sulla voce, vendi sulla notizia. In inglese, buy the rumor, sell the news. Significa che il prezzo si muove sulle aspettative, prima che i fatti accadano."),
 P('Come funziona', [
   ('Prima', 'il mercato si aspetta un evento e compra in anticipo'),
   ('Durante', "l'evento arriva come previsto: niente sorpresa"),
   ('Dopo', 'chi aveva comprato incassa, e il prezzo può scendere')],
   ["Funziona così.",
    "Prima: il mercato si aspetta un evento, per esempio un taglio dei tassi, e compra in anticipo.",
    "Durante: l'evento arriva esattamente come previsto. Nessuna sorpresa.",
    "Dopo: chi aveva comprato in anticipo incassa il guadagno. E il prezzo, invece di salire, può scendere."]),
 EX('Esempio illustrativo', [
   ['Due settimane prima', 'il mercato prezza un taglio dei tassi quasi certo'],
   ['Nel frattempo', 'la valuta si indebolisce in anticipo'],
   ['Il giorno della decisione', 'taglio confermato, come previsto'],
   ['Reazione', 'la valuta si rafforza: era già tutto nel prezzo']],
   ["Un esempio illustrativo. Due settimane prima della riunione, il mercato considera quasi certo un taglio dei tassi.",
    "Nel frattempo la valuta si indebolisce: il taglio viene anticipato nei prezzi.",
    "Il giorno della decisione, il taglio arriva come previsto.",
    "E la valuta, invece di scendere ancora, si rafforza. Era già tutto nel prezzo, e chi aveva venduto in anticipo chiude le posizioni."],
   k=[1, 2, 3, 4]),
 P('Come capire cosa è già nel prezzo', [
   ('Probabilità implicite', 'per i tassi: strumenti come il FedWatch del CME'),
   ('Movimento delle settimane prima', 'se il prezzo ha già corso molto, la notizia pesa meno'),
   ('Le parole della banca centrale', 'guidano le attese prima della decisione')],
   ["Come si capisce cosa è già nel prezzo?",
    "Per i tassi esistono le probabilità implicite: per la Fed, per esempio, lo strumento FedWatch del CME mostra quanto il mercato considera probabile un taglio o un rialzo.",
    "Guarda il movimento delle settimane precedenti: se il prezzo ha già corso molto in una direzione, la notizia attesa pesa meno.",
    "E ascolta la banca centrale: con i suoi discorsi guida le attese molto prima della decisione."]),
 Q("Quello che **tutti** si aspettano, di solito, **non muove** il prezzo.",
   "Ricorda: quello che tutti si aspettano, di solito, non muove il prezzo. Lo muove la sorpresa."),
])
