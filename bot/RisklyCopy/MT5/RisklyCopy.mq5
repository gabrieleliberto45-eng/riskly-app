//+------------------------------------------------------------------+
//| RisklyCopy (MT5) - copia le operazioni tra conti sullo stesso PC  |
//| Modalita' INVIA sul conto principale, RICEVI sugli altri.         |
//| I conti si parlano dalla cartella comune di MetaTrader            |
//| (...\MetaQuotes\Terminal\Common\Files), anche tra MT4 e MT5.     |
//| Il lotto del conto che riceve si ricalcola sul suo rischio.       |
//+------------------------------------------------------------------+
#property copyright "Riskly - riskly.trade"
#property link      "https://riskly.trade"
#property version   "1.00"
#property description "Copia le operazioni tra conti MT4/MT5 sullo stesso computer o VPS."
#property description "Il lotto si ricalcola sul conto che riceve: moltiplicatore, saldo, rischio % o lotto fisso."
#property strict

#include <Trade\Trade.mqh>

enum ENUM_RC_MODO  { RC_INVIA = 0,    // Invia (conto principale)
                     RC_RICEVI = 1 }; // Ricevi (conto che copia)
enum ENUM_RC_LOTTO { RC_MOLTIPLICATORE = 0, // Stesso lotto x moltiplicatore
                     RC_SALDO = 1,          // In proporzione al saldo
                     RC_RISCHIO = 2,        // Rischio % sullo stop loss
                     RC_FISSO = 3 };        // Lotto fisso

input group "Collegamento"
input ENUM_RC_MODO  InpModo        = RC_RICEVI; // Modalita'
input string        InpCanale      = "riskly";  // Nome del canale (uguale su tutti i conti collegati)

input group "Lotto (solo RICEVI)"
input ENUM_RC_LOTTO InpLotto       = RC_SALDO;  // Come calcolare il lotto
input double        InpMoltiplicatore = 1.0;    // Moltiplicatore
input double        InpRischio     = 1.0;       // Rischio per operazione (%) - modo Rischio
input double        InpLottoFisso  = 0.01;      // Lotto fisso - modo Lotto fisso
input double        InpLottoMax    = 5.0;       // Lotto massimo per operazione
input bool          InpRaggruppa   = true;      // Conto piccolo: copia al lotto minimo e raggruppa le operazioni (false = non copiare)
input double        InpRischioMin  = 0;         // Conto piccolo: rischio massimo con il lotto minimo (%) (0 = nessun limite)

input group "Filtri (solo RICEVI)"
input bool          InpCopiaSLTP   = true;      // Copia stop loss e take profit
input bool          InpCopiaAperte = false;     // All'avvio copia anche le posizioni gia' aperte
input int           InpEtaMax      = 60;        // Non copiare posizioni aperte da piu' di N secondi
input double        InpScostMax    = 30;        // Non copiare se il prezzo si e' spostato di piu' di N pip
input int           InpPosMax      = 20;        // Numero massimo di posizioni copiate aperte
input string        InpSimboli     = "";        // Copia solo questi simboli (vuoto = tutti, es. XAUUSD,EURUSD)
input string        InpMappa       = "";        // Nomi diversi tra broker (es. GOLD=XAUUSD,US30=DJ30)
input string        InpPrefisso    = "";        // Prefisso dei simboli su questo conto
input string        InpSuffisso    = "";        // Suffisso dei simboli su questo conto (es. .r)
input int           InpRitardoMax  = 15;        // Se il conto principale tace da N secondi, non fare nulla
input long          InpMagic       = 77001;     // Numero magico delle posizioni copiate

CTrade   trade;
datetime avvio;
string   stato = "";

// ----------------------------------------------------------------- utilita'
string FileCanale() { return "RisklyCopy\\" + InpCanale + ".csv"; }
string GV(string chiave) { return "RC_" + InpCanale + "_" + chiave; }

double NormLotto(string sym, double lotto)
{
   double passo = SymbolInfoDouble(sym, SYMBOL_VOLUME_STEP), mn = SymbolInfoDouble(sym, SYMBOL_VOLUME_MIN), mx = SymbolInfoDouble(sym, SYMBOL_VOLUME_MAX);
   if(passo <= 0) passo = 0.01;
   lotto = MathFloor(lotto / passo + 1e-9) * passo;
   lotto = MathMin(lotto, MathMin(mx, InpLottoMax));
   if(lotto < mn) return 0;               // troppo piccolo per questo conto: non si copia
   return NormalizeDouble(lotto, 8);
}

double Pip(string sym)
{
   int cifre = (int)SymbolInfoInteger(sym, SYMBOL_DIGITS);
   double punto = SymbolInfoDouble(sym, SYMBOL_POINT);
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
         string ab[]; StringTrimLeft(coppie[i]); StringTrimRight(coppie[i]);
         if(StringSplit(coppie[i], '=', ab) == 2) { StringTrimLeft(ab[0]); StringTrimRight(ab[0]); StringTrimLeft(ab[1]); StringTrimRight(ab[1]); if(ab[0] == sym) { base = ab[1]; break; } }
      }
   }
   return InpPrefisso + base + InpSuffisso;
}

bool SimboloAmmesso(string sym)
{
   if(InpSimboli == "") return true;
   string l[]; int n = StringSplit(InpSimboli, ',', l);
   for(int i = 0; i < n; i++) { StringTrimLeft(l[i]); StringTrimRight(l[i]); if(l[i] == sym) return true; }
   return false;
}

// ----------------------------------------------------------------- INVIA
void Invia()
{
   // appena avviato o senza collegamento la lista delle posizioni puo' essere vuota: non la si manda, altrimenti
   // i conti che ricevono chiuderebbero tutto
   if(!TerminalInfoInteger(TERMINAL_CONNECTED) || TimeGMT() - avvio < 5) { stato = "In attesa del collegamento al broker"; return; }
   string tmp = FileCanale() + ".tmp";
   int h = FileOpen(tmp, FILE_WRITE | FILE_TXT | FILE_COMMON | FILE_ANSI);
   if(h == INVALID_HANDLE) { stato = "Errore nella scrittura del file comune (" + (string)GetLastError() + ")"; return; }
   FileWriteString(h, StringFormat("H;%I64d;%.2f;%.2f;%s\n", (long)TimeGMT(), AccountInfoDouble(ACCOUNT_BALANCE),
                                   AccountInfoDouble(ACCOUNT_EQUITY), AccountInfoString(ACCOUNT_CURRENCY)));
   int n = 0;
   for(int i = 0; i < PositionsTotal(); i++)
   {
      ulong t = PositionGetTicket(i); if(t == 0) continue;
      long tipo = PositionGetInteger(POSITION_TYPE);
      FileWriteString(h, StringFormat("P;%I64u;%s;%d;%.8f;%.8f;%.8f;%.8f;%I64d\n", t, PositionGetString(POSITION_SYMBOL), (int)tipo,
                                      PositionGetDouble(POSITION_VOLUME), PositionGetDouble(POSITION_PRICE_OPEN),
                                      PositionGetDouble(POSITION_SL), PositionGetDouble(POSITION_TP),
                                      (long)PositionGetInteger(POSITION_TIME) - (long)(TimeTradeServer() - TimeGMT())));
      n++;
   }
   FileClose(h);
   if(!FileMove(tmp, FILE_COMMON, FileCanale(), FILE_COMMON | FILE_REWRITE))
      stato = "Errore nell'aggiornamento del file comune (" + (string)GetLastError() + ")";
   else stato = "INVIA · canale \"" + InpCanale + "\" · " + (string)n + " posizioni";
}

// ----------------------------------------------------------------- RICEVI
struct PosMaster { ulong ticket; string sym; int tipo; double vol, prezzo, sl, tp; long apertura; };
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
      if(c[0] == "H" && n >= 3) { masterOra = StringToInteger(c[1]); masterSaldo = StringToDouble(c[2]); header = true; }
      else if(c[0] == "P" && n >= 9)
      {
         int k = ArraySize(master); ArrayResize(master, k + 1);
         master[k].ticket = (ulong)StringToInteger(c[1]); master[k].sym = c[2]; master[k].tipo = (int)StringToInteger(c[3]);
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

int TrovaMaster(ulong t) { for(int i = 0; i < ArraySize(master); i++) if(master[i].ticket == t) return i; return -1; }

double CalcolaLotto(const PosMaster &m, string sym)
{
   double lotto = m.vol * InpMoltiplicatore;
   double saldo = AccountInfoDouble(ACCOUNT_BALANCE);
   if(InpLotto == RC_FISSO) lotto = InpLottoFisso;
   else if(InpLotto == RC_SALDO || (InpLotto == RC_RISCHIO && m.sl <= 0))
      lotto = (masterSaldo > 0) ? m.vol * saldo / masterSaldo * InpMoltiplicatore : 0;
   else if(InpLotto == RC_RISCHIO)
   {
      double tick = SymbolInfoDouble(sym, SYMBOL_TRADE_TICK_SIZE), valore = SymbolInfoDouble(sym, SYMBOL_TRADE_TICK_VALUE);
      double dist = MathAbs(m.prezzo - m.sl);
      if(tick > 0 && valore > 0 && dist > 0) lotto = (AccountInfoDouble(ACCOUNT_EQUITY) * InpRischio / 100.0) / (dist / tick * valore);
   }
   return MathMin(lotto, InpLottoMax);
}

int ContaCopiate()
{
   int n = 0;
   for(int i = 0; i < PositionsTotal(); i++) { ulong t = PositionGetTicket(i); if(t && PositionGetInteger(POSITION_MAGIC) == InpMagic) n++; }
   return n;
}


// Lotto da aprire per una nuova posizione del principale.
// Se il lotto giusto e' sotto il minimo del broker (es. conto da 100 che copia un conto da 10.000) e InpRaggruppa e' attivo:
// la prima operazione si copia al lotto minimo; le successive sullo stesso simbolo e direzione si aprono solo quando
// la somma dei lotti "giusti" delle posizioni aperte sul principale supera quello che e' gia' aperto qui.
// Esempio: 10 operazioni da 0,005 "giuste" -> sul secondario circa 5 posizioni da 0,01 (stessa esposizione totale).
double LottoDaAprire(const PosMaster &m, string sym, double giusto, string &nota)
{
   double norm = NormLotto(sym, giusto);
   if(norm > 0) return norm;
   if(!InpRaggruppa) { nota = "lotto sotto il minimo"; return 0; }
   double minimo = SymbolInfoDouble(sym, SYMBOL_VOLUME_MIN);
   int tipo = m.tipo;
   double obiettivo = 0, attuale = 0;
   for(int k = 0; k < ArraySize(master); k++)
      if(master[k].tipo == tipo && Mappa(master[k].sym) == sym && GlobalVariableCheck(GV("d" + (string)master[k].ticket)))
         obiettivo += GlobalVariableGet(GV("d" + (string)master[k].ticket));
   for(int i = 0; i < PositionsTotal(); i++)
   {
      ulong t = PositionGetTicket(i);
      if(t && PositionGetInteger(POSITION_MAGIC) == InpMagic && PositionGetString(POSITION_SYMBOL) == sym &&
         (int)PositionGetInteger(POSITION_TYPE) == tipo) attuale += PositionGetDouble(POSITION_VOLUME);
   }
   double lotto = 0;
   if(attuale <= 0) lotto = minimo;                                   // niente di aperto: si copia al minimo
   else if(obiettivo - attuale >= minimo - 1e-9) lotto = NormLotto(sym, obiettivo - attuale);
   if(lotto <= 0) { nota = "raggruppata con le posizioni gia' aperte (esposizione gia' coperta)"; return 0; }
   if(InpRischioMin > 0)
   {
      double t = SymbolInfoDouble(sym, SYMBOL_TRADE_TICK_SIZE), v = SymbolInfoDouble(sym, SYMBOL_TRADE_TICK_VALUE), d = MathAbs(m.prezzo - m.sl), e = AccountInfoDouble(ACCOUNT_EQUITY);
      if(m.sl > 0 && t > 0 && v > 0 && e > 0 && lotto * d / t * v / e * 100.0 > InpRischioMin)
      { nota = "col lotto minimo il rischio supera il " + DoubleToString(InpRischioMin, 1) + "%"; return 0; }
   }
   return lotto;
}
// una posizione nuova del conto principale: la copia o la scarta (una volta sola)
void CopiaNuova(const PosMaster &m, int &copiate)
{
   string chiave = GV("m" + (string)m.ticket);
   if(!InpCopiaAperte && m.apertura < (long)avvio) { GlobalVariableSet(chiave, 0); return; }
   if(!InpCopiaAperte && (long)TimeGMT() - m.apertura > InpEtaMax)
   { GlobalVariableSet(chiave, 0); Print("RisklyCopy: posizione ", m.ticket, " troppo vecchia, non copiata"); return; }
   if(!SimboloAmmesso(m.sym)) { GlobalVariableSet(chiave, 0); return; }
   if(copiate >= InpPosMax) { GlobalVariableSet(chiave, 0); Print("RisklyCopy: raggiunto il massimo di posizioni copiate"); return; }
   string sym = Mappa(m.sym);
   if(!SymbolSelect(sym, true)) { GlobalVariableSet(chiave, 0); Print("RisklyCopy: simbolo ", sym, " non trovato su questo conto"); return; }
   double prezzo = (m.tipo == POSITION_TYPE_BUY) ? SymbolInfoDouble(sym, SYMBOL_ASK) : SymbolInfoDouble(sym, SYMBOL_BID);
   if(InpScostMax > 0 && MathAbs(prezzo - m.prezzo) > InpScostMax * Pip(sym))
   { GlobalVariableSet(chiave, 0); Print("RisklyCopy: prezzo troppo lontano dall'entrata del conto principale, ", m.ticket, " non copiata"); return; }
   double giusto = CalcolaLotto(m, sym);
   if(giusto <= 0) { GlobalVariableSet(chiave, 0); Print("RisklyCopy: lotto non calcolabile per ", m.ticket); return; }
   GlobalVariableSet(GV("d" + (string)m.ticket), giusto);
   string nota = "";
   double lotto = LottoDaAprire(m, sym, giusto, nota);
   if(lotto <= 0) { GlobalVariableSet(chiave, 0); Print("RisklyCopy: ", m.ticket, " non copiata: ", nota); return; }
   int cifre = (int)SymbolInfoInteger(sym, SYMBOL_DIGITS);
   double sl = InpCopiaSLTP ? NormalizeDouble(m.sl, cifre) : 0, tp = InpCopiaSLTP ? NormalizeDouble(m.tp, cifre) : 0;
   trade.SetTypeFillingBySymbol(sym);
   bool ok = (m.tipo == POSITION_TYPE_BUY) ? trade.Buy(lotto, sym, 0, sl, tp, "RC#" + (string)m.ticket)
                                          : trade.Sell(lotto, sym, 0, sl, tp, "RC#" + (string)m.ticket);
   if(ok && trade.ResultRetcode() == TRADE_RETCODE_DONE)
   {
      ulong st = 0, deal = trade.ResultDeal();
      if(deal > 0 && HistoryDealSelect(deal)) st = (ulong)HistoryDealGetInteger(deal, DEAL_POSITION_ID);
      if(st == 0) st = trade.ResultOrder();
      GlobalVariableSet(GV("s" + (string)st), (double)m.ticket);
      GlobalVariableSet(GV("mi" + (string)m.ticket), m.vol);
      GlobalVariableSet(GV("si" + (string)m.ticket), lotto);
      GlobalVariableSet(chiave, 1);
      copiate++;
   }
   // se non riesce (mercato chiuso, prezzo cambiato...) riprova al giro dopo, finche' la posizione non e' troppo vecchia
   else
   {
      Print("RisklyCopy: copia di ", m.ticket, " non riuscita, codice ", trade.ResultRetcode(), " ", trade.ResultRetcodeDescription());
      string tent = GV("r" + (string)m.ticket);
      double n = GlobalVariableCheck(tent) ? GlobalVariableGet(tent) + 1 : 1;
      GlobalVariableSet(tent, n);
      if(n >= 5) { GlobalVariableSet(chiave, 0); GlobalVariableDel(tent); Print("RisklyCopy: ", m.ticket, " scartata dopo 5 tentativi"); }
   }
}

// toglie le variabili globali delle posizioni del principale ormai chiuse (una volta al minuto)
datetime ultimaPulizia = 0;
void Pulizia()
{
   if(TimeGMT() - ultimaPulizia < 60) return;
   ultimaPulizia = TimeGMT();
   string pref[] = {"m", "d", "r"};
   for(int i = GlobalVariablesTotal() - 1; i >= 0; i--)
   {
      string nome = GlobalVariableName(i);
      for(int j = 0; j < 3; j++)
      {
         string p = GV(pref[j]);
         if(StringFind(nome, p) != 0) continue;
         string resto = StringSubstr(nome, StringLen(p));
         ulong tk = (ulong)StringToInteger(resto);
         if(tk > 0 && (string)tk == resto && TrovaMaster(tk) < 0) GlobalVariableDel(nome);
      }
   }
}

void Ricevi()
{
   if(!LeggiMaster()) return;

   // 1) posizioni copiate: chiusura, chiusura parziale, stop e take profit
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong t = PositionGetTicket(i); if(t == 0 || PositionGetInteger(POSITION_MAGIC) != InpMagic) continue;
      ulong mt = 0;
      if(GlobalVariableCheck(GV("s" + (string)t))) mt = (ulong)GlobalVariableGet(GV("s" + (string)t));
      else { string cm = PositionGetString(POSITION_COMMENT); if(StringFind(cm, "RC#") == 0) mt = (ulong)StringToInteger(StringSubstr(cm, 3)); }
      if(mt == 0) continue;
      int k = TrovaMaster(mt);
      string assente = GV("x" + (string)t);
      if(k < 0)
      {
         double volte = GlobalVariableCheck(assente) ? GlobalVariableGet(assente) + 1 : 1;
         GlobalVariableSet(assente, volte);
         if(volte < 3) continue;                       // conferma: la posizione deve mancare per 3 letture di fila
         if(trade.PositionClose(t)) { GlobalVariableDel(GV("s" + (string)t)); GlobalVariableDel(GV("mi" + (string)mt)); GlobalVariableDel(GV("si" + (string)mt)); GlobalVariableDel(GV("m" + (string)mt)); GlobalVariableDel(GV("d" + (string)mt)); GlobalVariableDel(assente); }
         continue;
      }
      if(GlobalVariableCheck(assente)) GlobalVariableDel(assente);
      // chiusura parziale in proporzione
      double mIniz = GlobalVariableCheck(GV("mi" + (string)mt)) ? GlobalVariableGet(GV("mi" + (string)mt)) : master[k].vol;
      double sIniz = GlobalVariableCheck(GV("si" + (string)mt)) ? GlobalVariableGet(GV("si" + (string)mt)) : PositionGetDouble(POSITION_VOLUME);
      string sym = PositionGetString(POSITION_SYMBOL);
      if(mIniz > 0 && master[k].vol < mIniz - 1e-9)
      {
         double obiettivo = sIniz * master[k].vol / mIniz, attuale = PositionGetDouble(POSITION_VOLUME);
         double passo = SymbolInfoDouble(sym, SYMBOL_VOLUME_STEP);
         double togli = MathFloor((attuale - obiettivo) / passo + 1e-9) * passo;
         if(togli >= SymbolInfoDouble(sym, SYMBOL_VOLUME_MIN)) trade.PositionClosePartial(t, NormalizeDouble(togli, 8));
      }
      if(InpCopiaSLTP)
      {
         int cifre = (int)SymbolInfoInteger(sym, SYMBOL_DIGITS);
         double sl = NormalizeDouble(master[k].sl, cifre), tp = NormalizeDouble(master[k].tp, cifre);
         if(MathAbs(PositionGetDouble(POSITION_SL) - sl) > SymbolInfoDouble(sym, SYMBOL_POINT) / 2 ||
            MathAbs(PositionGetDouble(POSITION_TP) - tp) > SymbolInfoDouble(sym, SYMBOL_POINT) / 2)
         {
            string ultimo = GV("q" + (string)t), firma = DoubleToString(sl, cifre) + "/" + DoubleToString(tp, cifre);
            double hash = (double)StringLen(firma) * 1000003.0 + sl * 7919.0 + tp * 104729.0;
            if(!GlobalVariableCheck(ultimo) || GlobalVariableGet(ultimo) != hash)
            {
               GlobalVariableSet(ultimo, hash);
               if(!trade.PositionModify(t, sl, tp)) Print("RisklyCopy: modifica SL/TP non riuscita su ", t, ": ", trade.ResultRetcodeDescription());
            }
         }
      }
   }

   // 2) nuove posizioni del conto principale
   int copiate = ContaCopiate();
   for(int k = 0; k < ArraySize(master); k++)
      if(!GlobalVariableCheck(GV("m" + (string)master[k].ticket))) CopiaNuova(master[k], copiate);
   Pulizia();
   stato = "RICEVI · canale \"" + InpCanale + "\" · " + (string)copiate + " posizioni copiate aperte";
}

// ----------------------------------------------------------------- ciclo
int OnInit()
{
   avvio = TimeGMT();
   trade.SetExpertMagicNumber(InpMagic);
   trade.SetDeviationInPoints(30);
   if(InpModo == RC_RICEVI && AccountInfoInteger(ACCOUNT_MARGIN_MODE) != ACCOUNT_MARGIN_MODE_RETAIL_HEDGING)
      Alert("RisklyCopy: questo conto e' in modalita' netting. Per copiare le posizioni serve un conto hedging.");
   if(StringLen(InpCanale) == 0) { Alert("RisklyCopy: scrivi un nome per il canale"); return INIT_PARAMETERS_INCORRECT; }
   EventSetMillisecondTimer(300);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason) { EventKillTimer(); Comment(""); }

void OnTimer()
{
   if(InpModo == RC_INVIA) Invia();
   else if(TerminalInfoInteger(TERMINAL_TRADE_ALLOWED) && MQLInfoInteger(MQL_TRADE_ALLOWED)) Ricevi();
   else stato = "Trading algoritmico disattivato: attiva Algo Trading";
   Comment("RisklyCopy · ", stato);
}

void OnTick() {}
//+------------------------------------------------------------------+
