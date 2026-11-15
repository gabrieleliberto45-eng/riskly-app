/* Riskly News · nomi italiani dei dati del calendario (copia da strumenti/index.html, 15 novembre 2026). Se cambi lì, copia anche qui. */
const CAL_NOMI = [
  ['Non Farm Payrolls','Buste paga non agricole (NFP)'],['Initial Jobless Claims','Richieste di sussidi di disoccupazione'],['Unemployment Rate','Tasso di disoccupazione'],
  ['Unemployment Change','Variazione dei disoccupati'],['Employment Change','Variazione degli occupati'],['ADP Employment Change','Occupati ADP'],['JOLTs Job Openings','Posti di lavoro vacanti (JOLTS)'],
  ['Average Hourly Earnings','Salari orari medi'],['Participation Rate','Tasso di partecipazione'],
  ['Core Inflation Rate','Inflazione core'],['Inflation Rate','Inflazione'],['Core PCE Price Index','Indice PCE core'],['PCE Price Index','Indice PCE'],
  ['Core PPI','Prezzi alla produzione core'],['PPI','Prezzi alla produzione'],['Import Prices','Prezzi all\'importazione'],['Export Prices','Prezzi all\'esportazione'],
  ['Retail Sales Control Group','Vendite al dettaglio, gruppo di controllo'],['Retail Sales Ex Autos','Vendite al dettaglio senza auto'],['Retail Sales','Vendite al dettaglio'],
  ['Atlanta Fed GDPNow','Stima del PIL in tempo reale, Fed di Atlanta'],['GDP 3-Month Avg','PIL media 3 mesi'],['GDP Growth Rate','PIL'],['GDP Growth Annualized','PIL annualizzato'],['GDP Price Index','Deflatore del PIL'],['GDP','PIL'],
  ['Interest Rate Decision','decisione sui tassi'],['Deposit Facility Rate','Tasso sui depositi BCE'],['Press Conference','conferenza stampa'],['Monetary Policy Meeting Accounts','verbali della riunione'],
  ['Meeting Minutes','verbali della riunione'],['FOMC Minutes','Verbali FOMC'],['FOMC Economic Projections','Proiezioni economiche FOMC'],['Speech','discorso'],
  ['ISM Manufacturing PMI','PMI manifatturiero ISM'],['ISM Services PMI','PMI servizi ISM'],['Manufacturing PMI','PMI manifatturiero'],['Services PMI','PMI servizi'],['Composite PMI','PMI composito'],
  ['Industrial Production','Produzione industriale'],['Manufacturing Production','Produzione manifatturiera'],['Capacity Utilization','Utilizzo della capacità produttiva'],
  ['Durable Goods Orders','Ordini di beni durevoli'],['Factory Orders','Ordini all\'industria'],['Balance of Trade','Bilancia commerciale'],['Current Account','Partite correnti'],
  ['Michigan Consumer Sentiment','Fiducia consumatori Michigan'],['CB Consumer Confidence','Fiducia consumatori Conference Board'],['Consumer Confidence','Fiducia dei consumatori'],
  ['Business Confidence','Fiducia delle imprese'],['Ifo Business Climate','Clima d\'affari Ifo'],['ZEW Economic Sentiment Index','Sentiment economico ZEW'],['Economic Sentiment','Sentiment economico'],
  ['Housing Starts','Nuovi cantieri'],['Building Permits','Permessi di costruzione'],['Existing Home Sales','Vendite di case esistenti'],['New Home Sales','Vendite di case nuove'],['Pending Home Sales','Compromessi di vendita case'],
  ['Crude Oil Stocks Change','Scorte di petrolio'],['Crude Oil Stock Change','Scorte di petrolio'],['Gasoline Stocks Change','Scorte di benzina'],
  ['Personal Income','Redditi personali'],['Personal Spending','Spesa personale'],['Monthly Budget Statement','Bilancio federale mensile'],
  ['Philadelphia Fed Manufacturing Index','Indice manifatturiero Fed di Filadelfia'],['NY Empire State Manufacturing Index','Indice manifatturiero Empire State'],
  ['Business Inventories','Scorte delle imprese'],['Retail Inventories','Scorte al dettaglio'],['Wholesale Inventories','Scorte all\'ingrosso'],['Goods Trade Balance','Bilancia commerciale dei beni'],
  ['Full Time Employment Chg','Occupati a tempo pieno'],['Part Time Employment Chg','Occupati a tempo parziale'],['Employment Cost Index','Indice del costo del lavoro'],['Unemployed Persons','Disoccupati'],
  ['Wholesale Prices','Prezzi all\'ingrosso'],['Machinery Orders','Ordini di macchinari'],['New Yuan Loans','Nuovi prestiti in yuan'],['Loan Prime Rate','Tasso primario sui prestiti'],
  ['House Price Index','Indice dei prezzi delle case'],['Mortgage Approvals','Mutui approvati'],['Household Spending','Spesa delle famiglie'],['Net Long-term TIC Flows','Flussi di capitale TIC'],
  ['Imports','Importazioni'],['Exports','Esportazioni'],['Chicago PMI','PMI di Chicago'],['Gov ','governatore '],
  [' MoM',' m/m'],[' YoY',' a/a'],[' QoQ',' t/t'],[' Flash',' (stima flash)'],[' Prel',' (preliminare)'],[' Final',' (definitivo)'],[' Adv',' (anticipato)'],
  ['Fed Chair','Presidente Fed'],['ECB President','Presidente BCE']
];
function calNome(t){ let x = ' ' + t; for(const [a, b] of CAL_NOMI) x = x.split(a).join(b); x = x.trim(); return x.charAt(0).toUpperCase() + x.slice(1); }
/* titoli tradotti per intero (hanno la precedenza) */
const CAL_ESATTI = {
  'Foreign Bond Investment':'Investimenti esteri in obbligazioni','Stock Investment by Foreigners':'Investimenti esteri in azioni',
  'Jobless Claims 4-week Average':'Richieste di sussidio, media 4 settimane','Continuing Jobless Claims':'Richieste di sussidio continuative',
  'Fed Balance Sheet':'Bilancio della Fed','Baker Hughes Oil Rig Count':'Trivelle petrolifere attive (Baker Hughes)','Baker Hughes Total Rigs Count':'Trivelle attive totali (Baker Hughes)',
  'Foreign Exchange Reserves':'Riserve valutarie','ADP Employment Change Weekly':'Occupazione ADP settimanale','BoJ JGB Purchase':'Acquisti di titoli di Stato BoJ',
  'Consumer Inflation Expectations':'Attese di inflazione dei consumatori','Global Dairy Trade Price Index':'Prezzi asta latticini (GDT)',
  'NY Fed Bill Purchases 1 to 4 months':'Acquisti di T-bill Fed NY (1-4 mesi)','NY Fed Bill Purchases 4 to 12 months':'Acquisti di T-bill Fed NY (4-12 mesi)',
  'National Day Golden Week':'Festa nazionale (Golden Week)','TD-MI Inflation Gauge MoM':'Indicatore di inflazione TD-MI m/m','LMI Logistics Managers Index':'Indice dei responsabili logistica (LMI)',
  'RCM/TIPP Economic Optimism Index':'Ottimismo economico RCM/TIPP','Total Vehicle Sales':'Vendite di veicoli totali','Ai Group Industry Index':'Indice industria Ai Group',
  'Ai Group Construction Index':'Indice costruzioni Ai Group','Ai Group Manufacturing Index':'Indice manifatturiero Ai Group',
  'Nonfarm Payrolls Private':'Buste paga del settore privato','Government Payrolls':'Buste paga pubbliche','Average Weekly Hours':'Ore settimanali medie',
  'Manufacturing Payrolls':'Buste paga manifatturiere','Consumer Credit Change':'Variazione del credito al consumo','ECOFIN Meeting':'Riunione ECOFIN','Eurogroup Meeting':'Riunione dell\'Eurogruppo',
  'Eco Watchers Survey Current':'Indagine Eco Watchers: situazione attuale','Eco Watchers Survey Outlook':'Indagine Eco Watchers: prospettive',
  'NFIB Business Optimism Index':'Ottimismo delle piccole imprese (NFIB)','WASDE Report':'Rapporto WASDE (agricoltura USA)',
  'RICS House Price Balance':'Saldo prezzi delle case RICS','Goods Trade Balance Non-EU':'Bilancia commerciale beni extra UE','NIESR Monthly GDP Tracker':'Stima mensile del PIL NIESR',
  'Business NZ PMI':'PMI manifatturiero Business NZ','Reuters Tankan Index':'Indice Tankan Reuters','Total Social Financing':'Finanziamento sociale totale','Outstanding Loan Growth YoY':'Crescita dei prestiti in essere a/a',
  'Composite NZ PCI':'PMI composito NZ (PCI)','Services NZ PSI':'PMI servizi NZ (PSI)','NOPA Crush Report':'Rapporto NOPA sulla soia lavorata',
  'Claimant Count Change':'Variazione richiedenti sussidio','HMRC Payrolls Change':'Variazione buste paga HMRC','Average Earnings incl. Bonus (3Mo/Yr)':'Retribuzioni medie con bonus (3 mesi a/a)',
  'Average Earnings excl. Bonus (3Mo/Yr)':'Retribuzioni medie senza bonus (3 mesi a/a)','Foreign Securities Purchases':'Acquisti di titoli esteri','Foreign Securities Purchases by Canadians':'Acquisti di titoli esteri da parte di canadesi',
  'New Motor Vehicle Sales':'Vendite di veicoli nuovi','NAHB Housing Market Index':'Indice del mercato immobiliare NAHB','National People\'s Congress':'Congresso nazionale del popolo',
  'BoJ Summary of Opinions':'BoJ, sintesi delle opinioni','Early Close Bond Market':'Chiusura anticipata del mercato obbligazionario','Jobs/applications ratio':'Rapporto offerte/domande di lavoro',
  'Overall Net Capital Flows':'Flussi netti di capitale complessivi','Public Sector Net Borrowing Ex Banks':'Fabbisogno netto del settore pubblico (escl. banche)',
  'CBI Industrial Trends Orders':'Ordini industriali CBI','CFIB Business Barometer':'Barometro delle imprese CFIB','Chicago Fed National Activity Index':'Indice di attività nazionale Fed Chicago',
  'BRC Shop Price Inflation':'Inflazione dei prezzi nei negozi BRC','Non Defense Goods Orders Ex Air':'Ordini di beni capitali (escl. difesa e aerei)',
  'CB Consumer Confidence':'Fiducia dei consumatori (Conference Board)','CB Leading Index MoM':'Indice anticipatore Conference Board m/m','Money Supply':'Massa monetaria',
  'Net Lending to Individuals MoM':'Prestiti netti alle famiglie m/m','BoE Consumer Credit':'Credito al consumo BoE','Mortgage Lending':'Mutui erogati',
  'KOF Leading Indicators':'Indicatori anticipatori KOF','Budget Balance':'Saldo di bilancio','Treasury Refunding Financing Estimates':'Tesoro USA: stime di finanziamento',
  'Total Household Debt':'Debito totale delle famiglie','Treasury Refunding Announcement':'Tesoro USA: annuncio emissioni trimestrali',
  'BoE MPC Vote Unchanged':'BoE, voti per tassi invariati','BoE MPC Vote Hike':'BoE, voti per un rialzo','BoE MPC Vote Cut':'BoE, voti per un taglio',
  'EIA Short-Term Energy Outlook':'EIA, prospettive energetiche a breve termine','Investment Lending for Homes':'Prestiti per case da investimento','BTP Auction':'Asta BTP',
  'ECB Non-Monetary Policy Meeting':'BCE, riunione non di politica monetaria','ECB General Council Meeting':'BCE, riunione del Consiglio generale','Marginal Lending Rate':'Tasso sulle operazioni di rifinanziamento marginale',
  'Syndication Index-linked Gilt':'Gilt indicizzato (sindacato)','Midterm Elections':'Elezioni di metà mandato','General Election':'Elezioni politiche','Bond Auction':'Asta di titoli di Stato',
  'BoE Monetary Policy Report':'BoE, rapporto di politica monetaria','RBNZ Financial Stability Report':'RBNZ, rapporto sulla stabilità finanziaria',
  'BoE Financial Policy Committee Record':'BoE, verbale del Comitato di politica finanziaria','SNB Quarterly Bulletin':'BNS, bollettino trimestrale',
  'Quarterly Grain Stocks - Corn':'Scorte trimestrali di mais','Quarterly Grain Stocks - Wheat':'Scorte trimestrali di grano','Quarterly Grain Stocks - Soy':'Scorte trimestrali di soia',
  'Tankan Large All Industry Capex':'Tankan: investimenti grandi imprese','Tankan Non-Manufacturing Outlook':'Tankan: prospettive non manifatturiere','Tankan Small Manufacturers Index':'Tankan: piccole imprese manifatturiere',
  'Tankan Large Non-Manufacturing Index':'Tankan: grandi imprese non manifatturiere','Tankan Large Manufacturers Index':'Tankan: grandi imprese manifatturiere','Tankan Large Manufacturing Outlook':'Tankan: prospettive grandi imprese manifatturiere',
  'BoE Credit Conditions Survey':'BoE, indagine sulle condizioni del credito','Industrial Capacity Utilization':'Utilizzo della capacità industriale',
  'BoC Survey of Consumer Expectations':'BoC, indagine sulle attese dei consumatori','BoC Business Outlook Survey':'BoC, indagine sulle prospettive delle imprese',
  'SNB Monetary Policy Meeting Minutes':'BNS, verbali della riunione','CBI Business Optimism Index':'Ottimismo delle imprese CBI','EU-Bonds Auction':'Asta di EU-Bond','BTP€i Auction':'Asta BTP€i',
  'Autumn Budget 2026':'Legge di bilancio d\'autunno 2026','BoC Monetary Policy Report':'BoC, rapporto di politica monetaria','Conventional/Index-linked Gilt Tender':'Collocamento di Gilt',
  'BoJ Quarterly Outlook Report':'BoJ, rapporto trimestrale sulle prospettive','Employment Cost - Wages QoQ':'Costo del lavoro: salari t/t','Employment Cost - Benefits QoQ':'Costo del lavoro: benefit t/t',
  'Loan Officer Survey':'Indagine sui responsabili del credito','Senior Loan Officer Survey':'Indagine sui responsabili del credito (Fed)','Bundesbank Monthly Report':'Bundesbank, rapporto mensile',
  'Negotiated Wage Growth':'Crescita dei salari negoziati','Treasury Secretary Bessent Speech':'Discorso del Segretario al Tesoro Bessent','RBA Payments System Board Meeting':'RBA, riunione sui sistemi di pagamento',
  'RBA Bulletin':'RBA, bollettino','GDP Implicit Price QoQ':'Deflatore del PIL t/t','Non Farm Payrolls Annual Revision Prel':'Revisione annuale delle buste paga (preliminare)',
  'Company Gross Profits QoQ':'Profitti lordi delle imprese t/t','Net Exports Contribution to GDP':'Contributo delle esportazioni nette al PIL','GDP Chain Price Index QoQ':'Deflatore del PIL t/t',
  'Terms of Trade QoQ':'Ragioni di scambio t/t','BSI Large Manufacturing QoQ':'BSI grandi imprese manifatturiere t/t','BoC Summary of Deliberations':'BoC, sintesi delle deliberazioni',
  'Interest Rate Projection - 1st Yr':'Proiezione dei tassi: 1° anno','Interest Rate Projection - Current':'Proiezione dei tassi: anno in corso','Interest Rate Projection - Longer':'Proiezione dei tassi: lungo periodo',
  'Interest Rate Projection - 3rd Yr':'Proiezione dei tassi: 3° anno','Interest Rate Projection - 2nd Yr':'Proiezione dei tassi: 2° anno','SECO Economic Forecasts':'SECO, previsioni economiche',
  'President Trump and President Xi Summit':'Vertice tra il presidente Trump e il presidente Xi','Labor Day':'Festa del lavoro','Labour Day':'Festa del lavoro','Communist Party Fifth Plenum':'Quinto plenum del Partito comunista','Communist Party Fourth Plenum':'Quarto plenum del Partito comunista','Swiss National Day':'Festa nazionale svizzera','Civic Holiday':'Festività civica',
  'Late Summer Bank Holiday':'Festività di fine estate','Mountain Day':'Giornata della montagna','Respect for the Aged Day':'Giornata del rispetto per gli anziani','All Saints’ Day':'Ognissanti',
  'Culture Day':'Giornata della cultura','Remembrance Day':'Giorno della memoria','Veterans Day':'Giornata dei veterani','German Unity Day':'Giornata dell\'unità tedesca',
  'Thanksgiving Day':'Festa del Ringraziamento','Columbus Day':'Columbus Day','Health and Sports Day':'Giornata della salute e dello sport','Autumnal Equinox Day':'Equinozio d\'autunno',
  'National Day for Truth and Reconciliation':'Giornata per la verità e la riconciliazione','Christmas Day':'Natale','Boxing Day':'Santo Stefano','New Year\'s Day':'Capodanno','New Year\'s Eve':'Vigilia di Capodanno','Christmas Eve':'Vigilia di Natale','Good Friday':'Venerdì Santo','Easter Monday':'Lunedì dell\'Angelo',
  'Philly Fed CAPEX Index':'Fed Philadelphia: investimenti','Philly Fed Business Conditions':'Fed Philadelphia: condizioni delle imprese','Philly Fed Employment':'Fed Philadelphia: occupazione',
  'Philly Fed New Orders':'Fed Philadelphia: nuovi ordini','Philly Fed Prices Paid':'Fed Philadelphia: prezzi pagati','Cotality Dwelling Prices MoM':'Prezzi delle abitazioni Cotality m/m',
};
/* aste di titoli di Stato: "10-Year Note Auction" → "Asta Note a 10 anni" */
const CAL_UNITA = { Year:['anno','anni'], Month:['mese','mesi'], Week:['settimana','settimane'] };
function calAsta(t){
  let m = /^([\d/]+)-(Year|Month|Week) (.+?) (Auction|Auctions|Tender)$/.exec(t);
  if(m){ const n = m[1], u = CAL_UNITA[m[2]][n === '1' ? 0 : 1];
    const tipo = m[3].replace(/^Bill$/, 'T-bill').replace(/^Bond$/, 'titoli').replace(/^Note$/, 'T-note').replace(/^JGB$/, 'JGB').replace(/Index-Linked JGB/, 'JGB indicizzati').replace(/Climate Transition JGB/, 'JGB per la transizione climatica').replace(/^BOT$/, 'BOT');
    return 'Asta ' + tipo + ' a ' + n + ' ' + u; }
  m = /^(?:(\d{4}) )?(Index-linked Treasury Gilt|Treasury Gilt|Green Gilt|EU-Bonds|Bond) (\d{4})? ?(Auction|Auctions|Tender)$/.exec(t);
  if(m){ const anno = m[1] || m[3] || ''; const tipo = { 'Index-linked Treasury Gilt':'Gilt indicizzato', 'Treasury Gilt':'Gilt', 'Green Gilt':'Gilt verde', 'EU-Bonds':'EU-Bond', 'Bond':'titoli' }[m[2]];
    return 'Asta ' + tipo + (anno ? ' scadenza ' + anno : ''); }
  m = /^(\d+)-Year (BTP€i|BTP|BTP Short Term|TIPS|FRN|Schatz|Bobl|Bund|Bund\/g|Bobl\/g) Auction$/.exec(t);
  return m ? 'Asta ' + m[2] + ' a ' + m[1] + ' anni' : '';
}
/* parole e pezzi che restano in inglese, dopo le traduzioni principali */
const CAL_PEZZI = [
  ['MBA 30-Year Mortgage Rate','MBA tasso sui mutui a 30 anni'],['30-Year Mortgage Rate','Tasso sui mutui a 30 anni'],['15-Year Mortgage Rate','Tasso sui mutui a 15 anni'],['BBA Mortgage Rate','Tasso sui mutui BBA'],
  ['Mortgage Applications','richieste di mutuo'],['Mortgage Market Index','indice del mercato dei mutui'],['Mortgage Refinance Index','indice dei rifinanziamenti'],['Purchase Index','indice degli acquisti di case'],
  ['Distillate Fuel Production Change','produzione di distillati'],['Distillate Stocks Change','scorte di distillati'],['Gasoline Production Change','produzione di benzina'],['Refinery Crude Runs Change','petrolio lavorato nelle raffinerie'],
  ['Crude Oil Imports Change','importazioni di petrolio'],['Heating Oil Stocks Change','scorte di gasolio da riscaldamento'],['Natural Gas Stocks Change','scorte di gas naturale'],
  ['New Car Registrations','Immatricolazioni di auto nuove'],['New Car Sales','Vendite di auto nuove'],['Used Car Prices','Prezzi delle auto usate'],['Vehicle Sales','Vendite di veicoli'],['Car Production','Produzione di auto'],
  ['Construction Output','Produzione nelle costruzioni'],['Construction Orders','Ordini nelle costruzioni'],['Construction Spending','Spesa per costruzioni'],['Construction Work Done','Lavori di costruzione completati'],
  ['Construction PMI','PMI costruzioni'],['Commodity Prices','Prezzi delle materie prime'],['Raw Materials Prices','Prezzi delle materie prime'],
  ['ZEW Current Conditions','ZEW situazione attuale'],['Ifo Expectations','Ifo aspettative'],['Ifo Current Conditions','Ifo situazione attuale'],
  ['ISM Manufacturing Employment','ISM manifatturiero: occupazione'],['ISM Manufacturing Prices','ISM manifatturiero: prezzi'],['ISM Manufacturing New Orders','ISM manifatturiero: nuovi ordini'],
  ['ISM Services New Orders','ISM servizi: nuovi ordini'],['ISM Services Business Activity','ISM servizi: attività'],['ISM Services Employment','ISM servizi: occupazione'],['ISM Services Prices','ISM servizi: prezzi'],
  ['Average Cash Earnings','Retribuzioni medie'],['Average Hourly Wages','Salari orari medi'],['Average Weekly Earnings','Retribuzioni settimanali medie'],
  ['Michigan Consumer Expectations','Michigan attese dei consumatori'],['Michigan 5 Year Inflation Expectations','Michigan attese di inflazione a 5 anni'],['Michigan Inflation Expectations','Michigan attese di inflazione'],['Michigan Current Conditions','Michigan situazione attuale'],
  ['Private House Approvals','Permessi per case private'],['Leading Economic Index','Indice economico anticipatore'],['Coincident Index','Indice coincidente'],['Bank Lending','Prestiti bancari'],
  ['Westpac Consumer Confidence Index','Fiducia dei consumatori Westpac'],['Westpac Consumer Confidence Change','Fiducia dei consumatori Westpac, variazione'],['Westpac Leading Index','Indice anticipatore Westpac'],
  ['Electronic Retail Card Spending','Spesa con carte elettroniche'],['Credit Card Spending','Spesa con carte di credito'],['Machine Tool Orders','Ordini di macchine utensili'],
  ['Producer & Import Prices','Prezzi alla produzione e all\'importazione'],['M2 Money Supply','Massa monetaria M2'],['M3 Money Supply','Massa monetaria M3'],['M4 Money Supply','Massa monetaria M4'],
  ['PPI Ex Food, Energy and Trade','PPI escl. alimentari, energia e commercio'],['Manufacturing Sales','Vendite manifatturiere'],['Wholesale Sales','Vendite all\'ingrosso'],['Industrial Sales','Vendite industriali'],
  ['Fixed Asset Investment (YTD)','Investimenti fissi (da inizio anno)'],['Fixed Asset Investment','Investimenti fissi'],['Food Inflation','Inflazione alimentare'],['Tertiary Industry Index','Indice del terziario'],
  ['NY Fed Services Activity Index','Fed NY: attività nei servizi'],['Retail Sales Ex Gas/Autos','Vendite al dettaglio escl. benzina e auto'],['Retail Inventories Ex Autos','Scorte al dettaglio escl. auto'],
  ['Retail Sales ex Fuel','Vendite al dettaglio escl. carburanti'],['PPI Core Output','PPI core in uscita'],['PPI Output','PPI in uscita'],['Retail Price Index','Indice dei prezzi al dettaglio (RPI)'],
  ['NBS Non Manufacturing PMI','PMI non manifatturiero NBS'],['BoJ Monetary Policy Meeting Minutes','BoJ, verbali della riunione'],['Private Sector Credit','Credito al settore privato'],['Housing Credit','Credito per la casa'],
  ['Economic Sentiment Index','Indice del sentiment economico'],['Nationwide Housing Prices','Prezzi delle case Nationwide'],['Tokyo CPI Ex Food and Energy','Inflazione Tokyo escl. alimentari ed energia'],['Tokyo Core CPI','Inflazione core Tokyo'],
  ['DMP 1Y CPI Expectations','DMP attese di inflazione a 1 anno'],['DMP 3M Output Price Expectations','DMP attese sui prezzi a 3 mesi'],
  ['New Housing Price Index','Prezzi delle case nuove'],['Kansas Fed Manufacturing Index','Fed Kansas City: manifattura'],['Kansas Fed Composite Index','Fed Kansas City: indice composito'],
  ['Inflation Rate Ex-Food and Energy','Inflazione escl. alimentari ed energia'],['ECB Consumer Inflation Expectations','BCE, attese di inflazione dei consumatori'],
  ['Dallas Fed Manufacturing Index','Fed Dallas: manifattura'],['Dallas Fed Services Revenues Index','Fed Dallas: ricavi nei servizi'],['Dallas Fed Services Index','Fed Dallas: servizi'],
  ['Richmond Fed Services Revenues Index','Fed Richmond: ricavi nei servizi'],['Richmond Fed Manufacturing Shipments Index','Fed Richmond: spedizioni manifatturiere'],['Richmond Fed Manufacturing Index','Fed Richmond: manifattura'],
  ['Industrial Profits (YTD)','Profitti industriali (da inizio anno)'],['Loans to Households','Prestiti alle famiglie'],['Loans to Companies','Prestiti alle imprese'],
  ['Durable Goods Orders Ex Transp','Ordini di beni durevoli escl. trasporti'],['S&P/Case-Shiller Home Price','Prezzi delle case S&P/Case-Shiller'],
  ['Services Sentiment','Fiducia nei servizi'],['Selling Price Expectations','Attese sui prezzi di vendita'],['Industrial Sentiment','Fiducia nell\'industria'],['Economic Sentiment','Sentiment economico'],
  ['Labour Costs Index','Indice del costo del lavoro'],['Labour Cost Index','Indice del costo del lavoro'],['Nonfarm Productivity','Produttività non agricola'],['Unit Labour Costs','Costo del lavoro per unità di prodotto'],
  ['Home Loans','Mutui per la casa'],['Business Investment','Investimenti delle imprese'],['GDP Private Consumption','PIL: consumi privati'],['GDP Capital Expenditure','PIL: investimenti'],
  ['Business Inflation Expectations','Attese di inflazione delle imprese'],['Labour Productivity','Produttività del lavoro'],['Labor Productivity','Produttività del lavoro'],['Wage Price Index','Indice dei salari'],
  ['Real Consumer Spending','Spesa reale dei consumatori'],['Core PCE Prices','Prezzi PCE core'],['PCE Prices','Prezzi PCE'],['GDP Sales','PIL: vendite finali'],['Wage Growth','Crescita dei salari'],
  ['Plant Machinery Capital Expenditure','Investimenti in impianti e macchinari'],['Private Capital Expenditure','Investimenti privati'],['Building Capital Expenditure','Investimenti in edifici'],['Capital Spending','Spesa per investimenti'],
  ['Harmonised Inflation Rate','Inflazione armonizzata'],['RBA Weighted Median CPI','Inflazione RBA, mediana ponderata'],['Quarterly RBA Trimmed Mean CPI','Inflazione RBA trimestrale, media troncata'],['RBA Trimmed Mean CPI','Inflazione RBA, media troncata'],
  ['CPI Trimmed-Mean','Inflazione, media troncata'],['CPI Median','Inflazione, mediana'],['PPI Input','Prezzi alla produzione degli input'],['GDP External Demand','PIL: domanda estera'],
  ['Corporate Profits','Profitti delle imprese'],['ECB Monetary Policy Meeting Accounts','BCE, resoconto della riunione'],['ANZ-Indeed Job Ads','Annunci di lavoro ANZ-Indeed'],
  ['Factory Orders ex Transportation','Ordini all\'industria escl. trasporti'],['JOLTs Job Quits','Dimissioni volontarie (JOLTS)'],['Monetary Base','Base monetaria'],['Challenger Job Cuts','Licenziamenti annunciati (Challenger)'],
  ['Reserve Balances with Fed Banks','Riserve delle banche presso la Fed'],['Overtime Pay','Straordinari pagati'],['BRC Retail Sales Monitor','Vendite al dettaglio BRC'],['Balance of Trade Yuan','Bilancia commerciale in yuan'],
  ['NBS General PMI','PMI generale NBS'],['UN General Assembly','Assemblea generale ONU'],['Assumption of Mary','Ferragosto'],[' 3rd Est',' (terza stima)'],
  ['Baden Wuerttemberg CPI','Inflazione Baden-Württemberg'],['North Rhine Westphalia CPI','Inflazione Renania Settentrionale-Vestfalia'],['Bavaria CPI','Inflazione Baviera'],['Saxony CPI','Inflazione Sassonia'],
  ['Brandenburg CPI','Inflazione Brandeburgo'],['Hesse CPI','Inflazione Assia'],['S&P Global ','S&P Global '],
  ['Nonfarm Payrolls Private','Buste paga del settore privato'],['Nonfarm Payrolls','Buste paga non agricole (NFP)'],['FDI (YTD)','Investimenti diretti esteri (da inizio anno)'],['CPI Common','Inflazione, componente comune'],['Loan Prime Rate 1Y','Tasso primario sui prestiti a 1 anno'],['Loan Prime Rate 5Y','Tasso primario sui prestiti a 5 anni'],[' s.a',' (destagionalizzato)'],
  ['Redbook','Redbook (vendite al dettaglio)'],
  [' 2nd Est',' (seconda stima)'],[' Adv',' (anticipato)'],
];
function calNomeNuovo(t){
  if(CAL_ESATTI[t]) return CAL_ESATTI[t];
  const a = calAsta(t); if(a) return a;
  let x = ' ' + t + ' ';
  for(const [en, it] of CAL_PEZZI) x = x.split(en).join(it);
  return calRifinisci(calNome(x.trim()));
}
/* ultimi ritocchi: sigle italiane e ordine delle parole */
const CAL_BANCHE = { ECB:'BCE', SNB:'BNS', BOJ:'BoJ', Fed:'Fed', BoE:'BoE', BoJ:'BoJ', RBA:'RBA', RBNZ:'RBNZ', BoC:'BoC', PBoC:'PBoC', Bundesbank:'Bundesbank' };
function calRifinisci(x){
  let m = /^(ECB|SNB|BOJ|BoJ|Fed|BoE|RBA|RBNZ|BoC|PBoC|Bundesbank) (.+?) discorso$/.exec(x);
  m = m || /^(ECB|Fed|BoE|BoJ) (?:President|Presidente) (.+?) discorso$/.exec(x.replace(/^Presidente (BCE|Fed) /, (z, b) => (b === 'BCE' ? 'ECB' : b) + ' Presidente '));
  if(m && /^President /.test(m[2])) m[2] = 'presidente ' + m[2].slice(10);
  if(m) return (/^(governatore|presidente|Presidente) /.test(m[2]) ? 'Discorso del ' + m[2].charAt(0).toLowerCase() + m[2].slice(1) : 'Discorso di ' + m[2]) + ' (' + CAL_BANCHE[m[1]] + ')';
  m = /^(ECB|SNB|BOJ) (.+)$/.exec(x); if(m) x = CAL_BANCHE[m[1]] + ', ' + m[2];
  m = /^(Fed|BoE|BoJ|RBA|RBNZ|BoC|PBoC) (decisione|verbali|proiezioni|rapporto|conferenza|dichiarazione)(.*)$/.exec(x); if(m) x = m[1] + ', ' + m[2] + m[3];
  m = /^Quarterly (.+)$/.exec(x); if(m) x = m[1] + ' trimestrale';
  m = /^(ANZ Roy Morgan|Westpac|ZEW|Ifo|GfK|Sentix|NZIER|Lloyds|BRC) (Fiducia dei consumatori|Indice del sentiment economico|Fiducia delle imprese)(.*)$/.exec(x);
  if(m) x = m[2] + ' ' + m[1] + m[3];
  return x;
}
/* spiegazioni in italiano dei dati principali: [riconosce il titolo inglese, cosa misura, perché conta] */
