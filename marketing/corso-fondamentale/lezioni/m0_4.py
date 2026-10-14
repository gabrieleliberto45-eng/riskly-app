from h import *
LEZIONE = L('0.4', 'Introduzione', 'Prima di cominciare', 'Il metodo del corso: dato, aspettativa, reazione, rischio', [
 T('MODULO 0 · LEZIONE 4', 'Quattro domande per **ogni** notizia', 'Lo schema che useremo in tutto il corso.',
   "In tutto il corso useremo lo stesso schema. Quattro domande, da farsi davanti a qualsiasi notizia: un dato sull'inflazione, una decisione della banca centrale, una guerra."),
 P('Lo schema', [
   ('1 · Il dato', 'cosa misura e quando esce'),
   ("2 · L'aspettativa", 'cosa si aspetta il mercato (consenso)'),
   ('3 · La reazione', 'come si muovono valute, oro, indici, rendimenti'),
   ('4 · Il rischio', 'cosa cambia per lotto, stop e orari')],
   ["Prima domanda: il dato. Cosa misura, chi lo pubblica e quando esce.",
    "Seconda: l'aspettativa. Cosa si aspetta il mercato, cioè il consenso, e cosa è già nei prezzi.",
    "Terza: la reazione. Se il dato è diverso dalle attese, come tendono a muoversi valute, oro, indici e rendimenti.",
    "Quarta, la più importante per noi: il rischio. Cosa cambia per il lotto, per lo stop e per gli orari in cui operi."]),
 EX('Lo schema applicato (esempio illustrativo)', [
   ['Il dato', "inflazione USA (CPI), alle 14:30"],
   ["L'aspettativa", 'consenso 3,0% su base annua'],
   ['La reazione possibile', 'sopra le attese: dollaro più forte, oro e indici più deboli (di solito, non sempre)'],
   ['Il rischio', 'lotto ridotto, niente ordini a ridosso, stop che tiene conto dello slippage']],
   ["Applichiamolo a un esempio. I numeri sono illustrativi. Il dato: l'inflazione americana, alle quattordici e trenta.",
    "L'aspettativa: il consenso è al tre per cento su base annua.",
    "La reazione possibile: se esce sopra le attese, di solito il dollaro si rafforza e oro e indici scendono. Di solito, non sempre: lo vedremo.",
    "Il rischio: lotto ridotto, niente ordini piazzati a ridosso del dato, e uno stop che tiene conto dello slippage."], k=[1, 2, 3, 4]),
 Q("Non chiederti **dove andrà** il prezzo. Chiediti **quanto può costarti** se va dall'altra parte.",
   "Ricorda: non chiederti dove andrà il prezzo. Chiediti quanto può costarti se va dall'altra parte. Nel prossimo modulo vediamo come il mercato reagisce alle notizie."),
])
