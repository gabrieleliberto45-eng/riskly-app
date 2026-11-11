# Controllo orario "notizie straordinarie" (Riskly News) fatto da uno script, così l'assistente non deve leggere né calcolare niente.
# Stampa UNA riga:  STOP: <motivo>   oppure   SERVE: <movimenti sopra soglia> | articoli di oggi: <...>
# Regole di Gabriele (2 novembre): soglie sui movimenti, max 2 "straordinarie" al giorno, niente se il movimento è già spiegato da un dato analizzato.
# Serve SUPABASE_ACCESS_TOKEN nell'ambiente (con o senza spazi). uso: python3 notizie/controlla_movimenti.py
import datetime as dt, json, os, urllib.request
from zoneinfo import ZoneInfo
SOGLIE = {  # simbolo: (nome, soglia giorno %, soglia ora %)  — decennale in punti base sul giorno
    'CL=F': ('petrolio WTI', 4, 2.5), 'BZ=F': ('petrolio Brent', 4, 2.5), 'GC=F': ('oro', 1.5, 1), 'DX-Y.NYB': ('indice del dollaro', 0.6, None),
    '^TNX': ('decennale USA', 8, None), 'ES=F': ('future S&P 500', 1.5, 1), 'NQ=F': ('future Nasdaq', 1.5, 1)}
def serie(s):
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{s}?range=1d&interval=5m'
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=25))['chart']['result'][0]
    c = [x for x in r['indicators']['quote'][0]['close'] if x]
    return c, r['meta']['chartPreviousClose']
giorno, ora = [], []
for s, (nome, sg, so) in SOGLIE.items():
    try: c, p = serie(s)
    except Exception: continue
    if len(c) < 14: continue
    if s == '^TNX': vg = (c[-1] - p) * 100; um = ' pb'     # ^TNX è in % (4,86 = 4,86%): 0,01 = 1 punto base
    else: vg = (c[-1] / p - 1) * 100; um = '%'
    vo = (c[-1] / c[-13] - 1) * 100 if so else 0
    if abs(vg) >= sg: giorno.append(f'{nome} {vg:+.2f}{um} sul giorno')
    if so and abs(vo) >= so: ora.append(f'{nome} {vo:+.2f}% nell\'ultima ora')
tok = os.environ['SUPABASE_ACCESS_TOKEN'].replace(' ', '')
def sql(q):
    r = urllib.request.Request('https://api.supabase.com/v1/projects/swlztverwfgdgchgpudt/database/query', data=json.dumps({'query': q}).encode(), headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r, timeout=30))
oggi = dt.datetime.now(ZoneInfo('Europe/Rome')).date()
art = sql(f"select id,categoria,left(titolo,70) t from notizie where data>='{oggi - dt.timedelta(days=1)}' order by creato desc")
straord = [a for a in art if a['categoria'] == 'straordinarie' and a['id'].startswith(str(oggi))]
elenco = '; '.join(f"{a['id']} ({a['categoria']})" for a in art[:8])
if not giorno and not ora: print('STOP: nessuna soglia superata'); raise SystemExit
if len(straord) >= 2: print(f'STOP: oggi sono già uscite {len(straord)} notizie straordinarie'); raise SystemExit
dati = [a for a in art if a['categoria'] in ('dati', 'fed', 'tassi')]
if not ora and dati:   # solo soglie sul giorno e c'è già un dato/Fed/tassi analizzato ieri o oggi: il movimento è quasi certamente quello
    print(f"STOP: sopra soglia solo sul giorno ({'; '.join(giorno)}), già spiegato da un articolo recente ({dati[0]['id']}); nessun movimento rapido nell'ultima ora"); raise SystemExit
print('SERVE: ' + '; '.join(giorno + ora) + ' | articoli recenti: ' + elenco)
