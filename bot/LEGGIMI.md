# Bot Riskly

Ogni bot ha la sua cartella, con le versioni per MT4 e MT5. Nessun bot apre operazioni da solo: lavorano sulle operazioni del trader.

| Bot | Cosa fa | Prezzo di lancio → dopo | Sorgenti qui |
|---|---|---|---|
| [RiskGuard](RiskGuard/) | Ti ferma dopo N perdite di fila, blocca la perdita giornaliera con un margine di sicurezza, stop loss obbligatorio, massimo di operazioni al giorno, chiusura al target | 99 € → 149 € | da caricare |
| [TradeManager](TradeManager/) | Stop loss e take profit automatici in pip se mancano, break-even dopo N pip, trailing stop con avvio, distanza e passo | 49 € → 79 € | da caricare |
| [ScaleIn](ScaleIn/) | Apri una posizione a mano e apre le altre con take profit scaglionati in pip, a mercato o con pendenti; stop automatico e blocco se il rischio totale è eccessivo | 79 € → 129 € | da caricare |
| [Riskly Pro](RisklyPro/) | Tutto insieme: pulsanti BUY/SELL con il lotto calcolato sul rischio, RiskGuard + TradeManager + ScaleIn, rischio su tutte le posizioni, filtro spread e notizie, stato e operazioni nel journal. Licenza per 3 conti, videocorso al 50% | 199 € → 299 € | da caricare |
| [RisklyCopy](RisklyCopy/) | Copia le operazioni tra conti MT4/MT5 sullo stesso PC o VPS, con il lotto ricalcolato sul conto che riceve (saldo, rischio %, lotto minimo con raggruppamento per i conti piccoli) | da decidere | sì, prima versione da compilare e provare |

Lancio dei bot: 23 ottobre 2026.

## Collegamento al journal (RiskGuard e Riskly Pro)
In **ogni** terminale (MT4 e MT5 hanno impostazioni separate):
1. Strumenti → Opzioni (Ctrl+O) → Consulenti Esperti → "Consenti WebRequest per gli URL elencati" → `https://swlztverwfgdgchgpudt.supabase.co`
2. Nei parametri del bot: la chiave del journal (journal → Bot → collegamento).
3. Algo Trading / AutoTrading attivo.
4. Errori: scheda "Esperti" in basso.

MT5 accetta un bot per grafico, non uno per terminale: bot diversi vanno su grafici diversi.
