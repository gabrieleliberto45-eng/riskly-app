# Riepilogo settimanale dell'oro: scarica i prezzi orari della settimana (oro COMEX, indice del dollaro, rendimento del decennale USA)
# e prepara numeri + grafico per il video del weekend.
# uso: python3 settimana.py [AAAA-MM-GG del lunedì]   (default: il lunedì di questa settimana)
# esce: oro/<lunedì>.json (numeri) e oro/<lunedì>.png (grafico 1500×760, stile Riskly)
import datetime as dt, json, os, sys, urllib.request
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

QUI = os.path.dirname(os.path.abspath(__file__))
ROMA = dt.timezone(dt.timedelta(hours=2))   # solo per le etichette dei giorni; i dati restano in UTC

def serie(simbolo, da, a):
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{simbolo}?period1={int(da.timestamp())}&period2={int(a.timestamp())}&interval=1h'
    r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))['chart']['result'][0]
    q = r['indicators']['quote'][0]
    righe = [(dt.datetime.fromtimestamp(t, dt.timezone.utc), o, h, l, c) for t, o, h, l, c in zip(r['timestamp'], q['open'], q['high'], q['low'], q['close']) if c is not None]
    return [x for x in righe if da <= x[0] <= a]          # Yahoo a volte restituisce più giorni del richiesto

def riassunto(s):
    o, c = s[0][1], s[-1][4]
    hi = max(s, key=lambda x: x[2]); lo = min(s, key=lambda x: x[3])
    return dict(apertura=round(o, 2), chiusura=round(c, 2), var=round(c - o, 2), var_pct=round((c / o - 1) * 100, 2),
                massimo=round(hi[2], 2), quando_max=hi[0].isoformat(), minimo=round(lo[3], 2), quando_min=lo[0].isoformat())

lun = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today() - dt.timedelta(days=dt.date.today().weekday())
da = dt.datetime.combine(lun, dt.time(0), dt.timezone.utc) - dt.timedelta(hours=2)          # apertura di domenica sera
a = dt.datetime.combine(lun + dt.timedelta(days=4), dt.time(21, 30), dt.timezone.utc)         # chiusura di venerdì
oro, usd, tnx = serie('GC=F', da, a), serie('DX-Y.NYB', da, a), serie('%5ETNX', da, a)
dati = dict(settimana=lun.isoformat(), oro=riassunto(oro), dollaro=riassunto(usd), decennale=riassunto(tnx),
            giorni=[dict(giorno=(lun + dt.timedelta(days=i)).isoformat(),
                         chiusura=round([x for x in oro if x[0].date() <= lun + dt.timedelta(days=i)][-1][4], 2)) for i in range(5)
                    if any(x[0].date() <= lun + dt.timedelta(days=i) for x in oro)],
            fonte='Yahoo Finance: oro future COMEX (GC=F), indice del dollaro (DX-Y.NYB), rendimento Treasury 10 anni (^TNX); dati orari')
dati['decennale']['var_pb'] = round(dati['decennale']['var'] * 100)      # punti base
json.dump(dati, open(f'{QUI}/{lun}.json', 'w'), indent=1, ensure_ascii=False)

# grafico: oro orario, giorni separati, massimo e minimo evidenziati
fp = font_manager.FontProperties(family='DejaVu Sans')
fig, ax = plt.subplots(figsize=(15, 7.6), dpi=100); fig.patch.set_facecolor('#0B0D0C'); ax.set_facecolor('#0B0D0C')
x = list(range(len(oro))); y = [v[4] for v in oro]
ax.plot(x, y, color='#E8C15A', lw=3)
ax.fill_between(x, y, min(y) - (max(y) - min(y)) * .08, color='#E8C15A', alpha=.08)
NOMI = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven']
for i in range(5):
    g = lun + dt.timedelta(days=i); idx = [j for j, v in enumerate(oro) if v[0].astimezone(ROMA).date() == g]
    if not idx: continue
    ax.axvline(idx[0], color='#232823', lw=1.5); ax.text(idx[0] + 2, 1.0, NOMI[i], transform=ax.get_xaxis_transform(), color='#9AA39A', fontsize=18, va='bottom')
for v, col, k in [(max(oro, key=lambda z: z[2]), '#00C853', 2), (min(oro, key=lambda z: z[3]), '#FF5A4E', 3)]:
    j = oro.index(v); ax.scatter([j], [v[k]], color=col, s=90, zorder=5)
    ax.annotate(f'{v[k]:,.0f}'.replace(',', '.'), (j, v[k]), textcoords='offset points', xytext=(10, 10 if k == 2 else -28), color=col, fontsize=20, weight='bold')
ax.tick_params(colors='#9AA39A', labelsize=16); ax.set_xticks([])
for s_ in ax.spines.values(): s_.set_visible(False)
ax.yaxis.grid(color='#232823', lw=1); ax.yaxis.tick_right()
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:,.0f}'.replace(',', '.')))
plt.tight_layout(); plt.savefig(f'{QUI}/{lun}.png', facecolor=fig.get_facecolor()); print(json.dumps(dati, indent=1, ensure_ascii=False))
