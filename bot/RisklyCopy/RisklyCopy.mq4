//+------------------------------------------------------------------+
//| RisklyCopy (MT4) - copia le operazioni tra conti sullo stesso PC  |
//| Modalita' INVIA sul conto principale, RICEVI sugli altri.         |
//| I conti si parlano dalla cartella comune di MetaTrader            |
//| (...\MetaQuotes\Terminal\Common\Files), anche tra MT4 e MT5.     |
//| Il lotto del conto che riceve si ricalcola sul suo rischio.       |
//+------------------------------------------------------------------+
#property copyright "Riskly - riskly.trade"
#property link      "https://riskly.trade"
#property version   "1.00"
#property description "Copia le operazioni tra conti MT4/MT5 sullo stesso computer o VPS."
#property strict

enum ENUM_RC_MODO  { RC_INVIA = 0,    // Invia (conto principale)
                     RC_RICEVI = 1 }; // Ricevi (conto che copia)
enum ENUM_RC_LOTTO { RC_MOLTIPLICATORE = 0, // Stesso lotto x moltiplicatore
                     RC_SALDO = 1,          // In proporzione al saldo
                     RC_RISCHIO = 2,        // Rischio % sullo stop loss
                     RC_FISSO = 3 };        // Lotto fisso

input string        _c1            = "--- Collegamento ---";      // ·
input ENUM_RC_MODO  InpModo        = RC_RICEVI; // Modalita'
input string        InpCanale      = "riskly";  // Nome del canale (uguale su tutti i conti collegati)
input string        _c2            = "--- Lotto (solo RICEVI) ---"; // ·
input ENUM_RC_LOTTO InpLotto       = RC_SALDO;  // Come calcolare il lotto
input double        InpMoltiplicatore = 1.0;    // Moltiplicatore
input double        InpRischio     = 1.0;       // Rischio per operazione (%) - modo Rischio
input double        InpLottoFisso  = 0.01;      // Lotto fisso - modo Lotto fisso
input double        InpLottoMax    = 5.0;       // Lotto massimo per operazione
input double        InpRischioMin  = 2.0;       // Conto piccolo: usa il lotto minimo solo se rischia al massimo questa % (0 = mai)
input string        _c3            = "--- Filtri (solo RICEVI) ---"; // ·
input bool          InpCopiaSLTP   = true;      // Copia stop loss e take profit
input bool          InpCopiaAperte = false;     // All'avvio copia anche le posizioni gia' aperte
input int           InpEtaMax      = 60;        // Non copiare posizioni aperte da piu' di N secondi
input double        InpScostMax    = 30;        // Non copiare se il prezzo si e' spostato di piu' di N pip
input int           InpPosMax      = 20;        // Numero massimo di posizioni copiate aperte
input string        InpSimboli     = "";        // Copia solo questi simboli (vuoto = tutti)
input string        InpMappa       = "";        // Nomi diversi tra broker (es. GOLD=XAUUSD,US30=DJ30)
input string        InpPrefisso    = "";        // Prefisso dei simboli su questo conto
input string        InpSuffisso    = "";        // Suffisso dei simboli su questo conto (es. .r)
input int           InpRitardoMax  = 15;        // Se il conto principale tace da N secondi, non fare nulla
input int           InpMagic       = 77001;     // Numero magico delle posizioni copiate
input int           InpSlippage    = 30;        // Scostamento massimo in esecuzione (punti)

datetime avvio;
string   stato = "";

string FileCanale() { return "RisklyCopy\\" + InpCanale + ".csv"; }
string GV(string chiave) { return "RC_" + InpCanale + "_" + chiave; }
string Pulito(string s) { StringTrimLeft(s); StringTrimRight(s); return s; }

double NormLotto(string sym, double lotto)
{
   double passo = MarketInfo(sym, MODE_LOTSTEP), mn = MarketInfo(sym, MODE_MINLOT), mx = MarketInfo(sym, MODE_MAXLOT);
   if(passo <= 0) passo = 0.01;
   lotto = MathFloor(lotto / passo + 1e-9) * passo;
   lotto = MathMin(lotto, MathMin(mx, InpLottoMax));
   if(lotto < mn) return 0;
   return NormalizeDouble(lotto, 2);
}

double Pip(string sym)
{
   int cifre = (int)MarketInfo(sym, MODE_DIGITS);
   double punto = MarketInfo(sym, MODE_POINT);
   return (cifre == 3 || cifre == 5) ? punto * 10 : punto;
}

string Mappa(string sym)
{
   string base = sym;
   if(InpMappa != "")
   {
      string coppie[]; int n = StringSplit(InpMappa, ',', coppie);
      for(int i = 0; i < n; i++)
      {
         string ab[];
         if(StringSplit(Pulito(coppie[i]), '=', ab) == 2 && Pulito(ab[0]) == sym) { base = Pulito(ab[1]); break; }
      }
   }
   return InpPrefisso + base + InpSuffisso;
}

bool SimboloAmmesso(string sym)
{
   if(InpSimboli == "") return true;
   string l[]; int n = StringSplit(InpSimboli, ',', l);
   for(int i = 0; i < n; i++) if(Pulito(l[i]) == sym) return true;
   return false;
}

// ----------------------------------------------------------------- INVIA
void Invia()
{
   string tmp = FileCanale() + ".tmp";
   int h = FileOpen(tmp, FILE_WRITE | FILE_TXT | FILE_COMMON | FILE_ANSI);
   if(h == INVALID_HANDLE) { stato = "Errore nella scrittura del file comune (" + (string)GetLastError() + ")"; return; }
   FileWriteString(h, StringFormat("H;%d;%.2f;%.2f;%s\n", (int)TimeGMT(), AccountBalance(), AccountEquity(), AccountCurrency()));
   long diff = (long)(TimeCurrent() - TimeGMT());
   int n = 0;
   for(int i = 0; i < OrdersTotal(); i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      if(OrderType() != OP_BUY && OrderType() != OP_SELL) continue;      // solo posizioni a mercato
      FileWriteString(h, StringFormat("P;%d;%s;%d;%.8f;%.8f;%.8f;%.8f;%d\n", OrderTicket(), OrderSymbol(), OrderType(),
                                      OrderLots(), OrderOpenPrice(), OrderStopLoss(), OrderTakeProfit(), (int)((long)OrderOpenTime() - diff)));
      n++;
   }
   FileClose(h);
   if(!FileMove(tmp, FILE_COMMON, FileCanale(), FILE_COMMON | FILE_REWRITE))
      stato = "Errore nell'aggiornamento del file comune (" + (string)GetLastError() + ")";
   else stato = "INVIA · canale \"" + InpCanale + "\" · " + (string)n + " posizioni";
}

// ----------------------------------------------------------------- RICEVI
struct PosMaster { long ticket; string sym; int tipo; double vol, prezzo, sl, tp; long apertura; };
PosMaster master[];
double    masterSaldo = 0;
long      masterOra = 0;

bool LeggiMaster()
{
   ArrayResize(master, 0);
   int h = FileOpen(FileCanale(), FILE_READ | FILE_TXT | FILE_COMMON | FILE_ANSI | FILE_SHARE_READ | FILE_SHARE_WRITE);
   if(h == INVALID_HANDLE) { stato = "In attesa del conto principale (canale \"" + InpCanale + "\")"; return false; }
   bool header = false;
   while(!FileIsEnding(h))
   {
      string riga = FileReadString(h); if(riga == "") continue;
      string c[]; int n = StringSplit(riga, ';', c);
      if(n >= 3 && c[0] == "H") { masterOra = StringToInteger(c[1]); masterSaldo = StringToDouble(c[2]); header = true; }
      else if(n >= 9 && c[0] == "P")
      {
         int k = ArraySize(master); ArrayResize(master, k + 1);
         master[k].ticket = StringToInteger(c[1]); master[k].sym = c[2]; master[k].tipo = (int)StringToInteger(c[3]);
         master[k].vol = StringToDouble(c[4]); master[k].prezzo = StringToDouble(c[5]); master[k].sl = StringToDouble(c[6]);
         master[k].tp = StringToDouble(c[7]); master[k].apertura = StringToInteger(c[8]);
      }
   }
   FileClose(h);
   if(!header) { stato = "File del canale incompleto, riprovo"; return false; }
   if((long)TimeGMT() - masterOra > InpRitardoMax)
   { stato = "Il conto principale non risponde da " + (string)((long)TimeGMT() - masterOra) + " s: nessuna azione"; return false; }
   return true;
}

int TrovaMaster(long t) { for(int i = 0; i < ArraySize(master); i++) if(master[i].ticket == t) return i; return -1; }

double CalcolaLotto(const PosMaster &m, string sym)
{
   double lotto = m.vol * InpMoltiplicatore;
   if(InpLotto == RC_FISSO) lotto = InpLottoFisso;
   else if(InpLotto == RC_SALDO || (InpLotto == RC_RISCHIO && m.sl <= 0))
      lotto = (masterSaldo > 0) ? m.vol * AccountBalance() / masterSaldo * InpMoltiplicatore : 0;
   else if(InpLotto == RC_RISCHIO)
   {
      double tick = MarketInfo(sym, MODE_TICKSIZE), valore = MarketInfo(sym, MODE_TICKVALUE), dist = MathAbs(m.prezzo - m.sl);
      if(tick > 0 && valore > 0 && dist > 0) lotto = (AccountEquity() * InpRischio / 100.0) / (dist / tick * valore);
   }
   double norm = NormLotto(sym, lotto);
   if(norm > 0 || lotto <= 0) return norm;
   // il lotto giusto e' sotto il minimo del broker (es. conto da 100 che copia un conto da 10.000):
   // il lotto minimo farebbe rischiare di piu' del conto principale, quindi si usa solo se il rischio resta accettabile
   double minimo = MarketInfo(sym, MODE_MINLOT), t = MarketInfo(sym, MODE_TICKSIZE), v = MarketInfo(sym, MODE_TICKVALUE), d = MathAbs(m.prezzo - m.sl), eq = AccountEquity();
   if(InpRischioMin <= 0 || m.sl <= 0 || t <= 0 || v <= 0 || eq <= 0)
   { Print("RisklyCopy: lotto calcolato ", DoubleToString(lotto, 4), " sotto il minimo ", minimo, " e rischio non verificabile: non copiata"); return 0; }
   double rischio = minimo * d / t * v / eq * 100.0;
   if(rischio <= InpRischioMin) { Print("RisklyCopy: uso il lotto minimo ", minimo, " (rischio ", DoubleToString(rischio, 2), "%)"); return NormalizeDouble(minimo, 2); }
   Print("RisklyCopy: col lotto minimo ", minimo, " rischieresti il ", DoubleToString(rischio, 2), "% del conto (limite ", InpRischioMin, "%): non copiata");
   return 0;
}

int ContaCopiate()
{
   int n = 0;
   for(int i = 0; i < OrdersTotal(); i++) if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES) && OrderMagicNumber() == InpMagic) n++;
   return n;
}

long MasterDiOrdine(int t)
{
   if(GlobalVariableCheck(GV("s" + (string)t))) return (long)GlobalVariableGet(GV("s" + (string)t));
   string cm = OrderComment();
   if(StringFind(cm, "RC#") == 0) return StringToInteger(StringSubstr(cm, 3));
   // dopo una chiusura parziale MT4 crea un nuovo ordine con commento "from #vecchio"
   int p = StringFind(cm, "from #");
   if(p >= 0)
   {
      string vecchio = StringSubstr(cm, p + 6);
      if(GlobalVariableCheck(GV("s" + vecchio)))
      {
         double mt = GlobalVariableGet(GV("s" + vecchio));
         GlobalVariableSet(GV("s" + (string)t), mt); GlobalVariableDel(GV("s" + vecchio));
         return (long)mt;
      }
   }
   return 0;
}

void CopiaNuova(const PosMaster &m, int &copiate)
{
   string chiave = GV("m" + (string)m.ticket);
   if(!InpCopiaAperte && m.apertura < (long)avvio) { GlobalVariableSet(chiave, 0); return; }
   if(!InpCopiaAperte && (long)TimeGMT() - m.apertura > InpEtaMax)
   { GlobalVariableSet(chiave, 0); Print("RisklyCopy: posizione ", m.ticket, " troppo vecchia, non copiata"); return; }
   if(!SimboloAmmesso(m.sym)) { GlobalVariableSet(chiave, 0); return; }
   if(copiate >= InpPosMax) { GlobalVariableSet(chiave, 0); Print("RisklyCopy: raggiunto il massimo di posizioni copiate"); return; }
   string sym = Mappa(m.sym);
   if(!SymbolSelect(sym, true) || MarketInfo(sym, MODE_POINT) <= 0)
   { GlobalVariableSet(chiave, 0); Print("RisklyCopy: simbolo ", sym, " non trovato su questo conto"); return; }
   RefreshRates();
   double prezzo = (m.tipo == OP_BUY) ? MarketInfo(sym, MODE_ASK) : MarketInfo(sym, MODE_BID);
   if(InpScostMax > 0 && MathAbs(prezzo - m.prezzo) > InpScostMax * Pip(sym))
   { GlobalVariableSet(chiave, 0); Print("RisklyCopy: prezzo troppo lontano dall'entrata del conto principale, ", m.ticket, " non copiata"); return; }
   double lotto = CalcolaLotto(m, sym);
   if(lotto <= 0) { GlobalVariableSet(chiave, 0); Print("RisklyCopy: lotto troppo piccolo per ", m.ticket); return; }
   int cifre = (int)MarketInfo(sym, MODE_DIGITS);
   double sl = InpCopiaSLTP ? NormalizeDouble(m.sl, cifre) : 0, tp = InpCopiaSLTP ? NormalizeDouble(m.tp, cifre) : 0;
   int t = OrderSend(sym, m.tipo, lotto, prezzo, InpSlippage, sl, tp, "RC#" + (string)m.ticket, InpMagic, 0, m.tipo == OP_BUY ? clrLime : clrRed);
   if(t > 0)
   {
      GlobalVariableSet(GV("s" + (string)t), (double)m.ticket);
      GlobalVariableSet(GV("mi" + (string)m.ticket), m.vol);
      GlobalVariableSet(GV("si" + (string)m.ticket), lotto);
      GlobalVariableSet(chiave, 1);
      copiate++;
   }
   else
   {
      Print("RisklyCopy: copia di ", m.ticket, " non riuscita, errore ", GetLastError());
      string tent = GV("r" + (string)m.ticket);
      double n = GlobalVariableCheck(tent) ? GlobalVariableGet(tent) + 1 : 1;
      GlobalVariableSet(tent, n);
      if(n >= 5) { GlobalVariableSet(chiave, 0); GlobalVariableDel(tent); Print("RisklyCopy: ", m.ticket, " scartata dopo 5 tentativi"); }
   }
}

void Ricevi()
{
   if(!LeggiMaster()) return;
   RefreshRates();

   // 1) posizioni copiate: chiusura, chiusura parziale, stop e take profit
   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES) || OrderMagicNumber() != InpMagic) continue;
      if(OrderType() != OP_BUY && OrderType() != OP_SELL) continue;
      int t = OrderTicket(); string sym = OrderSymbol();
      long mt = MasterDiOrdine(t); if(mt == 0) continue;
      double chiudi = (OrderType() == OP_BUY) ? MarketInfo(sym, MODE_BID) : MarketInfo(sym, MODE_ASK);
      int k = TrovaMaster(mt);
      if(k < 0)
      {
         if(OrderClose(t, OrderLots(), chiudi, InpSlippage, clrGray))
         {
            GlobalVariableDel(GV("s" + (string)t)); GlobalVariableDel(GV("mi" + (string)mt));
            GlobalVariableDel(GV("si" + (string)mt)); GlobalVariableDel(GV("m" + (string)mt));
         }
         continue;
      }
      double mIniz = GlobalVariableCheck(GV("mi" + (string)mt)) ? GlobalVariableGet(GV("mi" + (string)mt)) : master[k].vol;
      double sIniz = GlobalVariableCheck(GV("si" + (string)mt)) ? GlobalVariableGet(GV("si" + (string)mt)) : OrderLots();
      if(mIniz > 0 && master[k].vol < mIniz - 1e-9)
      {
         double obiettivo = sIniz * master[k].vol / mIniz, passo = MarketInfo(sym, MODE_LOTSTEP);
         double togli = MathFloor((OrderLots() - obiettivo) / passo + 1e-9) * passo;
         if(togli >= MarketInfo(sym, MODE_MINLOT) && OrderClose(t, NormalizeDouble(togli, 2), chiudi, InpSlippage, clrGray)) continue;
      }
      if(InpCopiaSLTP)
      {
         int cifre = (int)MarketInfo(sym, MODE_DIGITS); double punto = MarketInfo(sym, MODE_POINT);
         double sl = NormalizeDouble(master[k].sl, cifre), tp = NormalizeDouble(master[k].tp, cifre);
         if(MathAbs(OrderStopLoss() - sl) > punto / 2 || MathAbs(OrderTakeProfit() - tp) > punto / 2)
            if(!OrderModify(t, OrderOpenPrice(), sl, tp, 0, clrNONE)) Print("RisklyCopy: modifica SL/TP non riuscita, errore ", GetLastError());
      }
   }

   // 2) nuove posizioni del conto principale
   int copiate = ContaCopiate();
   for(int k = 0; k < ArraySize(master); k++)
      if(!GlobalVariableCheck(GV("m" + (string)master[k].ticket))) CopiaNuova(master[k], copiate);
   stato = "RICEVI · canale \"" + InpCanale + "\" · " + (string)copiate + " posizioni copiate aperte";
}

// ----------------------------------------------------------------- ciclo
int OnInit()
{
   avvio = TimeGMT();
   if(StringLen(InpCanale) == 0) { Alert("RisklyCopy: scrivi un nome per il canale"); return INIT_PARAMETERS_INCORRECT; }
   EventSetMillisecondTimer(300);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason) { EventKillTimer(); Comment(""); }

void OnTimer()
{
   if(InpModo == RC_INVIA) Invia();
   else if(IsTradeAllowed()) Ricevi();
   else stato = "Trading automatico disattivato: attiva AutoTrading";
   Comment("RisklyCopy · ", stato);
}

void OnTick() {}
//+------------------------------------------------------------------+
