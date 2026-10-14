from h import *
LEZIONE = L('1.3', 'Modulo 1', 'Come il mercato reagisce alle notizie', 'Il prezzo anticipa le notizie', [
 T('MODULO 1 · LEZIONE 3', 'Quando la notizia arriva, è **già nel prezzo**', "\"Buy the rumor, sell the news\": il mercato si muove sulle aspettative, prima che i fatti accadano.",
   "C'è un vecchio detto dei mercati, che in italiano suona così: compra sulla voce, vendi sulla notizia. Sulla slide lo trovi nella sua forma inglese, molto usata. Significa che il prezzo si muove sulle aspettative, prima che i fatti accadano, e che quando il fatto accade davvero il movimento spesso è già finito."),
 P('Come funziona', [
   ('Prima', 'il mercato si aspetta un evento e compra in anticipo'),
   ('Durante', "l'evento arriva come previsto: niente sorpresa"),
   ('Dopo', 'chi aveva comprato incassa, e il prezzo può scendere')],
   ["Vediamo il meccanismo passo per passo.",
    "Prima: il mercato si convince che succederà qualcosa, per esempio che la banca centrale taglierà i tassi. Chi pensa di guadagnarci prende posizione in anticipo, giorni o settimane prima. Il prezzo si muove già in quella direzione.",
    "Durante: l'evento arriva, esattamente come previsto. Per il mercato non c'è nessuna informazione nuova, perché era tutto già scontato nei prezzi.",
    "Dopo: chi aveva preso posizione in anticipo ha raggiunto il suo obiettivo e chiude, cioè incassa il guadagno. Ma chiudere una posizione significa fare l'operazione opposta. Se in tanti chiudono insieme, il prezzo si muove al contrario rispetto a quello che ti aspetteresti leggendo la notizia."]),
 EX('Esempio illustrativo', [
   ['Due settimane prima', 'il mercato prezza un taglio dei tassi quasi certo'],
   ['Nel frattempo', 'la valuta si indebolisce in anticipo'],
   ['Il giorno della decisione', 'taglio confermato, come previsto'],
   ['Reazione', 'la valuta si rafforza: era già tutto nel prezzo']],
   ["Un esempio illustrativo. Due settimane prima della riunione, il mercato considera quasi certo che la banca centrale taglierà i tassi.",
    "Un taglio dei tassi rende una valuta meno attraente, perché chi la tiene guadagna meno interessi. Quindi, nelle due settimane prima, la valuta si indebolisce: il taglio viene anticipato nei prezzi.",
    "Il giorno della decisione, il taglio arriva, esattamente come previsto.",
    "E la valuta, invece di scendere ancora, si rafforza. Chi l'aveva venduta in anticipo per guadagnare dal taglio ora la ricompra per chiudere la posizione. Chi legge solo la notizia, taglio dei tassi uguale valuta più debole, e vende in quel momento, si trova dalla parte sbagliata."],
   k=[1, 2, 3, 4]),
 P('Come capire cosa è già nel prezzo', [
   ('Probabilità implicite', 'per i tassi: strumenti come il FedWatch del CME'),
   ('Movimento delle settimane prima', 'se il prezzo ha già corso molto, la notizia pesa meno'),
   ('Le parole della banca centrale', 'guidano le attese prima della decisione')],
   ["Come si fa a capire quanto di una notizia è già nel prezzo? Ci sono tre indizi.",
    "Per i tassi esistono le probabilità implicite, calcolate dai prezzi dei contratti sui tassi. Per la banca centrale americana, lo strumento più usato è il FedWatch del CME, la borsa di Chicago: ti dice, per esempio, che il mercato dà al novanta per cento la probabilità di un taglio. Se la probabilità è così alta, il taglio è già quasi tutto nei prezzi.",
    "Il secondo indizio è il movimento delle settimane precedenti. Se il prezzo ha già fatto un lungo movimento nella direzione della notizia attesa, resta poco spazio per un movimento ulteriore, e aumenta il rischio di chiusure dopo l'annuncio.",
    "Il terzo sono le parole della banca centrale. Le banche centrali non amano sorprendere i mercati, quindi preparano il terreno con discorsi e interviste nelle settimane prima. Quando una decisione è stata annunciata a parole, il giorno della decisione conta soprattutto cosa diranno per il futuro."]),
 Q("Quello che **tutti** si aspettano, di solito, **non muove** il prezzo.",
   "Ricorda: quello che tutti si aspettano, di solito, non muove il prezzo. Lo muove la sorpresa. E quando una notizia attesa arriva, preparati anche alla reazione opposta."),
])
