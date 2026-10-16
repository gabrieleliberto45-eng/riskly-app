from h import *
LEZIONE = L('11.2', 'Modulo 11', 'Extra: petrolio, posizionamento e stagionalità', 'Il COT: come sono posizionati i grandi', [
 T('MODULO 11 · LEZIONE 2', 'Il COT: **dove sono** i grandi', 'Il rapporto settimanale sulle posizioni nei future americani.',
   "In questa lezione vediamo il rapporto COT, Commitments of Traders, che ogni settimana mostra come sono posizionati i grandi operatori nei mercati future americani. Non è un segnale, ma racconta quanto è affollata una scommessa."),
 P('Cos\'è e quando esce', [
   ('Chi lo pubblica', 'la CFTC, l\'autorità americana dei future'),
   ('Quando', 'il venerdì alle 21:30 ora italiana, con le posizioni del martedì'),
   ('Cosa mostra', 'posizioni lunghe e corte per categoria di operatori')],
   ["Il rapporto lo pubblica la CFTC, l'autorità americana che vigila sui mercati dei future.",
    "Esce ogni venerdì alle ventuno e trenta ora italiana, ma fotografa le posizioni del martedì precedente: quando lo leggi, ha già tre giorni.",
    "Mostra quante posizioni lunghe e corte hanno le diverse categorie di operatori, su valute, oro, petrolio, indici e titoli di Stato."]),
 TB('Le categorie principali', ['Categoria', 'Chi sono', 'Come leggerli'], [
   ['Operatori commerciali', 'produttori e utilizzatori che si coprono', 'si coprono dal rischio, non scommettono'],
   ['Fondi speculativi', 'hedge fund e gestori', 'seguono le tendenze: la loro posizione netta è la più osservata'],
   ['Piccoli operatori', 'posizioni sotto le soglie di segnalazione', 'spesso arrivano tardi']],
  ["Le categorie principali sono tre.",
   "Gli operatori commerciali sono produttori e utilizzatori, per esempio una compagnia petrolifera o una compagnia aerea, che usano i future per coprirsi dal rischio. La loro posizione non è una scommessa.",
   "I fondi speculativi, come hedge fund e gestori, seguono le tendenze: la loro posizione netta, cioè lunghe meno corte, è il numero più osservato del rapporto.",
   "I piccoli operatori sono tutti quelli sotto le soglie di segnalazione. Spesso entrano tardi nelle tendenze."]),
 P('Come usarlo, con cautela', [
   ('Posizionamento estremo', 'quando i fondi sono tutti dalla stessa parte, la scommessa è affollata'),
   ('Non è un segnale di inversione', 'un estremo può durare mesi'),
   ('Per il rischio', 'su una scommessa affollata, una sorpresa fa più male: lotti più piccoli')],
   ["Come si usa il COT, con cautela.",
    "Il dato più utile sono gli estremi: quando i fondi speculativi hanno una posizione netta vicina ai massimi degli ultimi anni, tutti sono dalla stessa parte. È una scommessa affollata.",
    "Questo non significa che il prezzo stia per invertire: un posizionamento estremo può restare tale per mesi, mentre il prezzo continua nella stessa direzione.",
    "Il punto è il rischio: quando una scommessa è affollata e arriva una sorpresa, molti devono chiudere insieme, e il movimento contrario è più violento. In quelle fasi, lotti più piccoli."]),
 RIEP([('COT', 'posizioni nei future americani, ogni venerdì alle 21:30'), ('Ritardo', 'fotografa il martedì: è un dato di contesto'), ('Per il rischio', 'scommessa affollata = movimenti contrari più violenti')],
   ["Riassumiamo ora i punti principali di questa lezione.",
    "Il COT mostra le posizioni nei future americani ed esce ogni venerdì alle ventuno e trenta ora italiana.",
    "Fotografa il martedì precedente: è un dato di contesto, non un segnale per entrare.",
    "E sul rischio: quando una scommessa è affollata, i movimenti contrari sono più violenti, quindi riduci i lotti."]),
 Q('Quando tutti sono dalla stessa parte, **l\'uscita è stretta**.', "Quando tutti sono dalla stessa parte, l'uscita è stretta."),
])
