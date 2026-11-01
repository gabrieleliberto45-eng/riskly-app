# Setup XAU (Riskly News, richiesto da Gabriele il 1° novembre 2026): numeri e grafico dell'oro per l'articolo del giorno.
# Solo fatti calcolati dai prezzi (livelli toccati, medie, volatilità): niente segnali, niente obiettivi di prezzo.
# uso: python3 notizie/setup_xau.py [uscita.png]   → stampa il JSON dei numeri e salva il grafico (copertina 1600×900)
import datetime as dt, json, sys, urllib.request
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def giornaliero(simbolo='GC=F', rng='1y'):
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{simbolo}?range={rng}&interval=1d'
    r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))['chart']['result'][0]
    q = r['indicators']['quote'][0]
    return [(dt.datetime.fromtimestamp(t, dt.timezone.utc).date(), o, h, l, c) for t, o, h, l, c
            in zip(r['timestamp'], q['open'], q['high'], q['low'], q['close']) if None not in (o, h, l, c)]

def media(v, n): return sum(v[-n:]) / n if len(v) >= n else None
def atr(d, n=14):
    tr = [max(d[i][2] - d[i][3], abs(d[i][2] - d[i - 1][4]), abs(d[i][3] - d[i - 1][4])) for i in range(1, len(d))]
    return sum(tr[-n:]) / n
def rsi(c, n=14):
    g = [max(c[i] - c[i - 1], 0) for i in range(1, len(c))]; p = [max(c[i - 1] - c[i], 0) for i in range(1, len(c))]
    ag, ap = sum(g[:n]) / n, sum(p[:n]) / n
    for i in range(n, len(g)): ag = (ag * (n - 1) + g[i]) / n; ap = (ap * (n - 1) + p[i]) / n
    return 100 - 100 / (1 + ag / ap) if ap else 100
def perni(d, k=3):
    """massimi e minimi locali (k giorni per lato): i livelli dove il prezzo ha girato"""
    alti = [(d[i][0], d[i][2]) for i in range(k, len(d) - k) if d[i][2] == max(x[2] for x in d[i - k:i + k + 1])]
    bassi = [(d[i][0], d[i][3]) for i in range(k, len(d) - k) if d[i][3] == min(x[3] for x in d[i - k:i + k + 1])]
    return alti, bassi

d = giornaliero()
c = [x[4] for x in d]
ult, prec = d[-1], d[-2]
a = atr(d)
alti, bassi = perni(d[-90:])
sopra = sorted({round(v) for _, v in alti if v > ult[4]})[:2]          # i più vicini sopra il prezzo
sotto = sorted({round(v) for _, v in bassi if v < ult[4]}, reverse=True)[:2]
m20, m50, m200 = media(c, 20), media(c, 50), media(c, 200)
# numeri tondi da 50 $ più vicini: livelli che molti guardano (utili soprattutto quando sotto non ci sono minimi recenti)
tondi_sotto = [int(ult[4] // 50 * 50 - 50 * i) for i in range(2)]
tondi_sopra = [int(ult[4] // 50 * 50 + 50 * (i + 1)) for i in range(2)]
sett = [x for x in d if x[0] > ult[0] - dt.timedelta(days=ult[0].weekday() + 1)] or d[-5:]
trend = ('sopra' if ult[4] > m200 else 'sotto') + ' la media a 200 giorni, ' + ('sopra' if ult[4] > m50 else 'sotto') + ' quella a 50'
num = dict(
    data=ult[0].isoformat(), chiusura=round(ult[4], 1), var=round(ult[4] - prec[4], 1), var_pct=round((ult[4] / prec[4] - 1) * 100, 2),
    massimo=round(ult[2], 1), minimo=round(ult[3], 1), escursione=round(ult[2] - ult[3], 1),
    settimana_max=round(max(x[2] for x in sett), 1), settimana_min=round(min(x[3] for x in sett), 1),
    max_20g=round(max(x[2] for x in d[-20:]), 1), min_20g=round(min(x[3] for x in d[-20:]), 1),
    max_52s=round(max(x[2] for x in d), 1), min_52s=round(min(x[3] for x in d), 1),
    media_20=round(m20, 1), media_50=round(m50, 1), media_200=round(m200, 1) if m200 else None,
    atr_14=round(a, 1), rsi_14=round(rsi(c), 1), posizione=trend,
    resistenze_osservate=sopra, supporti_osservati=sotto, tondi_sotto=tondi_sotto, tondi_sopra=tondi_sopra,
    fonte='Yahoo Finance, oro future COMEX (GC=F), dati giornalieri')
print(json.dumps(num, indent=1, ensure_ascii=False))

# grafico: candele degli ultimi 3 mesi, medie a 20/50/200, zone osservate (larghe mezzo ATR)
if len(sys.argv) > 1:
    v = d[-66:]
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100); fig.patch.set_facecolor('#0B0D0C'); ax.set_facecolor('#0B0D0C')
    for i, (_, o, h, l, cl) in enumerate(v):
        col = '#2BD98B' if cl >= o else '#FF4D5E'
        ax.plot([i, i], [l, h], color=col, lw=1.4)
        ax.add_patch(Rectangle((i - .32, min(o, cl)), .64, max(abs(cl - o), .3), color=col))
    for n, col in [(20, '#F9D27A'), (50, '#F2B83A'), (200, '#7FA5FF')]:
        mm = [media(c[:len(c) - 66 + i + 1], n) for i in range(len(v))]
        ax.plot(range(len(v)), mm, color=col, lw=2.2, label=f'media {n} giorni')
    for z in (tondi_sotto if not sotto else []):
        ax.axhline(z, color='#9AA39A', lw=1, ls=':'); ax.text(len(v) - 9, z + a / 8, f'{z:,.0f}'.replace(',', '.'), color='#9AA39A', fontsize=15, va='center')
    for z, col in [(x, '#FF4D5E') for x in sopra] + [(x, '#2BD98B') for x in sotto]:
        ax.axhspan(z - a / 4, z + a / 4, color=col, alpha=.12)
        ax.text(len(v) + .5, z, f'{z:,.0f}'.replace(',', '.'), color=col, fontsize=17, va='center', weight='bold')
    ax.axhline(ult[4], color='#ECEEEA', lw=1, ls='--')
    ax.text(.97, .97, 'XAU · ORO (future COMEX) · giornaliero', transform=ax.transAxes, color='#F2B83A', fontsize=20, weight='bold', va='top', ha='right')
    ax.text(.97, .91, f'Chiusura {ult[0].strftime("%d/%m")}: {ult[4]:,.1f} $'.replace(',', 'X').replace('.', ',').replace('X', '.'), transform=ax.transAxes, color='#ECEEEA', fontsize=17, va='top', ha='right')
    ax.legend(loc='upper right', bbox_to_anchor=(.97, .86), facecolor='#0B0D0C', edgecolor='#232823', labelcolor='#C3CAC5', fontsize=13)
    ax.tick_params(colors='#9AA39A', labelsize=14); ax.set_xticks([]); ax.yaxis.tick_right()
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f'{y:,.0f}'.replace(',', '.')))
    for s in ax.spines.values(): s.set_visible(False)
    ax.yaxis.grid(color='#1C211E', lw=1); ax.set_xlim(-1, len(v) + 4)
    fig.text(.012, .02, 'Riskly News · Setup XAU · livelli osservati, non segnali', color='#6E746F', fontsize=13)
    plt.tight_layout(); plt.savefig(sys.argv[1], facecolor=fig.get_facecolor())
