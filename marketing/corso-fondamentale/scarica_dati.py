# Scarica le serie storiche vere usate nei grafici del corso → dati/*.csv (data,valore)
# Fonti: FRED (Federal Reserve Bank of St. Louis) e Yahoo Finance (oro, cambi, indici). uso: python3 scarica_dati.py
import os, csv, io, json, time, subprocess, urllib.parse
QUI = os.path.dirname(os.path.abspath(__file__)); D = f'{QUI}/dati'; os.makedirs(D, exist_ok=True)
FRED = {
 'CPIAUCSL': 'CPI USA, indice', 'CPILFESL': 'CPI core USA, indice', 'PCEPILFE': 'PCE core USA, indice', 'PCEPI': 'PCE USA, indice',
 'PPIFIS': 'PPI domanda finale USA, indice', 'CP0000EZ19M086NEST': 'HICP area euro, indice', 'CP0000ITM086NEST': 'HICP Italia, indice',
 'T5YIE': 'Breakeven 5 anni USA, %', 'MICH': 'Aspettative inflazione 1 anno Michigan, %',
 'FEDFUNDS': 'Fed funds effettivo, %', 'ECBDFR': 'Tasso BCE sui depositi, %', 'WALCL': 'Bilancio Fed, milioni $',
 'PAYEMS': 'Occupati non agricoli USA, migliaia', 'UNRATE': 'Disoccupazione USA, %', 'CIVPART': 'Partecipazione USA, %',
 'CES0500000003': 'Salario orario medio USA, $', 'ICSA': 'Richieste sussidi settimanali USA',
 'A191RL1Q225SBEA': 'PIL USA trimestrale annualizzato, %', 'USREC': 'Recessioni USA (NBER)', 'RSAFS': 'Vendite al dettaglio USA, milioni $',
 'UMCSENT': 'Fiducia consumatori Michigan', 'INDPRO': 'Produzione industriale USA, indice',
 'DGS10': 'Rendimento Treasury 10 anni, %', 'DGS2': 'Rendimento Treasury 2 anni, %', 'T10Y2Y': 'Differenza 10 anni − 2 anni, punti %',
 'DFII10': 'Rendimento reale 10 anni (TIPS), %', 'IRLTLT01ITM156N': 'Rendimento 10 anni Italia, %', 'IRLTLT01DEM156N': 'Rendimento 10 anni Germania, %',
 'EXUSEU': 'EUR/USD mensile', 'DEXJPUS': 'USD/JPY giornaliero', 'DEXCAUS': 'USD/CAD giornaliero', 'DCOILWTICO': 'Petrolio WTI, $',
 'VIXCLS': 'VIX', 'SP500': 'S&P 500', 'DTWEXBGS': 'Dollaro ponderato (broad)',
}
YAHOO = {'GC=F': 'Oro (future COMEX), $', 'EURCHF=X': 'EUR/CHF', 'USDJPY=X': 'USD/JPY', '^GSPC': 'S&P 500', 'GBPUSD=X': 'GBP/USD', 'AUDUSD=X': 'AUD/USD', 'SI=F': 'Argento (future), $'}
def get(url):
    for t in range(4):
        try: return subprocess.run(['curl', '-sfL', '--http1.1', '-m', '90'] + (['-A', 'Mozilla/5.0'] if 'yahoo' in url else []) + [url], check=True, capture_output=True).stdout.decode()
        except Exception as e: err = e; time.sleep(2 ** t)
    raise err
def scrivi(nome, righe):
    with open(f'{D}/{nome}.csv', 'w', newline='') as f: w = csv.writer(f); w.writerow(['data', 'valore']); w.writerows(righe)
for s in FRED:
    r = list(csv.reader(io.StringIO(get(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}'))))[1:]
    scrivi(s, [(a, b) for a, b in r if b not in ('.', '')]); print(s, len(r), r[-1])
for s in YAHOO:
    for iv, nome in (('1d', s), ('1mo', s + '_mese')):
        j = json.loads(get(f'https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(s)}?period1=946684800&period2={int(time.time())}&interval={iv}'))['chart']['result'][0]
        ts, cl = j['timestamp'], j['indicators']['quote'][0]['close']
        righe = [(time.strftime('%Y-%m-%d', time.gmtime(t)), round(c, 5)) for t, c in zip(ts, cl) if c is not None]
        scrivi(nome.replace('=', '').replace('^', ''), righe); print(nome, len(righe), righe[0], righe[-1])
open(f'{D}/FONTI.md', 'w').write('# Fonti dei dati\n\nScaricati con `scarica_dati.py` il ' + time.strftime('%d/%m/%Y') + '.\n\n'
    + ''.join(f'- `{k}.csv`: {v} · FRED, Federal Reserve Bank of St. Louis (fonte originale: BLS, BEA, Fed, BCE, Eurostat, OCSE, Università del Michigan, Cboe, S&P)\n' for k, v in FRED.items())
    + ''.join(f'- `{k.replace("=", "").replace("^", "")}.csv`: {v} · Yahoo Finance\n' for k, v in YAHOO.items()))
