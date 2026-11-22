# Grafici del giorno per l'articolo di Riskly News (Gabriele, 22/11: "giornalmente metti in un articolo il grafico del DXY, dei rendimenti USA").
# Crea due immagini 1600×900 nella paletta del sito e le carica nell'archivio pubblico delle copertine:
#   ID-dxy.jpg    indice del dollaro, 6 mesi, chiusure giornaliere + media a 50 giorni
#   ID-tassi.jpg  rendimenti USA a 5 anni e a 10 anni, 6 mesi
# Stampa un JSON con indirizzi, numeri (ultimo valore, variazione a 1 settimana e 1 mese) e le righe "GRAFICO|url|didascalia"
# da inserire nel corpo dell'articolo (il sito le mostra come immagini). Solo fatti, niente previsioni.
# uso: python3 notizie/grafici_macro.py ID
import datetime as dt, json, os, subprocess, sys, urllib.request
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

CARTA, BLU, ORO, GRIGIO, ROSSO = '#F6F6F3', '#12263F', '#D4AE5A', '#8A8F94', '#C8553D'
QUI = os.path.dirname(os.path.abspath(__file__))
COP = os.path.join(QUI, '..', 'nuovo', 'news', 'copertine')

def serie(s, rng='6mo'):
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{s}?range={rng}&interval=1d'
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))['chart']['result'][0]
    return [(dt.datetime.fromtimestamp(t, dt.timezone.utc).date(), c) for t, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']) if c]

from zoneinfo import ZoneInfo
ADESSO = dt.datetime.now(ZoneInfo('Europe/Rome'))
def quando(g): return f"oggi alle {ADESSO.strftime('%H:%M')}" if g == ADESSO.date() else f"chiusura del {g.strftime('%d/%m')}"
def it(x, d=2): return f'{x:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def var(v, n): return v[-1] - v[-1 - n] if len(v) > n else None

def base(titolo, sotto):
    f, a = plt.subplots(figsize=(16, 9), dpi=100); f.patch.set_facecolor(CARTA); a.set_facecolor(CARTA)
    for s in a.spines.values(): s.set_visible(False)
    a.grid(axis='y', color=BLU, alpha=.08); a.tick_params(colors=BLU, labelsize=15, length=0)
    a.yaxis.tick_right(); a.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    f.text(.045, .91, titolo, fontsize=30, fontweight='bold', color=BLU); f.text(.045, .86, sotto, fontsize=17, color=GRIGIO)
    f.text(.045, .035, 'Riskly News · dati Yahoo Finance, chiusure giornaliere · fatti, non previsioni', fontsize=13, color=GRIGIO)
    plt.subplots_adjust(left=.045, right=.93, top=.82, bottom=.1); return f, a

def carica(nome):
    out = subprocess.run([sys.executable, os.path.join(QUI, 'carica_copertina.py'), nome], capture_output=True, text=True)
    return [l for l in out.stdout.split() if l.startswith('https://')][-1]

ID = sys.argv[1]; ris = {}
# 1) dollaro
d = serie('DX-Y.NYB'); x = [a for a, _ in d]; v = [b for _, b in d]
m50 = [sum(v[i - 49:i + 1]) / 50 if i >= 49 else None for i in range(len(v))]
f, a = base('Indice del dollaro (DXY)', f'ultimi 6 mesi · {it(v[-1])} ({quando(x[-1])})')
a.plot(x, v, color=BLU, lw=3); a.plot([p for p, q in zip(x, m50) if q], [q for q in m50 if q], color=ORO, lw=2.2, label='media 50 giorni')
a.scatter([x[-1]], [v[-1]], color=ORO, s=110, zorder=5, edgecolor=BLU, linewidth=2)
a.annotate(it(v[-1]), (x[-1], v[-1]), xytext=(-14, 16), textcoords='offset points', ha='right', fontsize=20, fontweight='bold', color=BLU)
a.legend(frameon=False, fontsize=15, labelcolor=BLU, loc='upper left')
f.savefig(os.path.join(COP, f'{ID}-dxy.jpg'), facecolor=CARTA, pil_kwargs={'quality': 88}); plt.close(f)
ris['dxy'] = {'ultimo': round(v[-1], 2), 'data': str(x[-1]), 'var_1s': round(var(v, 5), 2), 'var_1m': round(var(v, 21), 2), 'max_6m': round(max(v), 2), 'min_6m': round(min(v), 2)}
# 2) rendimenti
y10 = dict(serie('^TNX')); y2 = dict(serie('^FVX')); gg = sorted(set(y10) & set(y2))
f, a = base('Rendimenti dei titoli di Stato USA', f'ultimi 6 mesi · 10 anni {it(y10[gg[-1]])}% · 5 anni {it(y2[gg[-1]])}% ({quando(gg[-1])})')
a.plot(gg, [y10[g] for g in gg], color=BLU, lw=3, label='10 anni'); a.plot(gg, [y2[g] for g in gg], color=ORO, lw=3, label='5 anni')
for s, c in ((y10, BLU), (y2, ORO)):
    a.scatter([gg[-1]], [s[gg[-1]]], color=c, s=100, zorder=5, edgecolor=BLU, linewidth=1.5)
a.yaxis.set_major_formatter(plt.FuncFormatter(lambda t, _: it(t) + '%')); a.legend(frameon=False, fontsize=15, labelcolor=BLU, loc='upper left')
f.savefig(os.path.join(COP, f'{ID}-tassi.jpg'), facecolor=CARTA, pil_kwargs={'quality': 88}); plt.close(f)
v10 = [y10[g] for g in gg]; v2 = [y2[g] for g in gg]
ris['tassi'] = {'data': str(gg[-1]), '10a': round(v10[-1], 3), '5a': round(v2[-1], 3), '10a_var_1s_pb': round(var(v10, 5) * 100), '10a_var_1m_pb': round(var(v10, 21) * 100),
                '5a_var_1s_pb': round(var(v2, 5) * 100), 'differenza_10a_5a_pb': round((v10[-1] - v2[-1]) * 100)}
# 3) caricamento e righe per il corpo
for k in ('dxy', 'tassi'): ris[k]['url'] = carica(f'{ID}-{k}')
ris['righe_corpo'] = [f"GRAFICO|{ris['dxy']['url']}|Indice del dollaro, ultimi 6 mesi, con la media a 50 giorni",
                      f"GRAFICO|{ris['tassi']['url']}|Rendimenti USA a 5 e a 10 anni, ultimi 6 mesi"]
print(json.dumps(ris, ensure_ascii=False, indent=1))
