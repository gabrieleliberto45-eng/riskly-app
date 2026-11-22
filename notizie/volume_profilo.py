# Volume profile a intervallo fisso per il Setup XAU (Gabriele, 22/11: "volume a intervallo fisso, POC e gli altri due livelli").
# Dati: future sull'oro COMEX (GC=F, Yahoo) a 5 minuti. L'oro spot dei broker non ha volumi veri: si usa solo il future.
# Per ogni intervallo calcola POC (prezzo con più volume), VAH e VAL (bordi della value area, 70% del volume).
# Il volume di ogni candela è distribuito in modo uniforme tra minimo e massimo, a passi di 1 $.
# Intervalli: l'ultima seduta piena (giorno di calendario italiano precedente con scambi) e la settimana precedente (lun–ven).
# uso: python3 notizie/volume_profilo.py [ID]  → stampa JSON. Con ID crea anche il grafico ID-vp.jpg (candele a 30 minuti + volume per prezzo,
#      POC in oro, VAH in rosso, VAL in verde: Gabriele 22/11), lo carica nell'archivio copertine e stampa la riga GRAFICO per il corpo.
# Livelli osservati, non segnali.
import datetime as dt, json, urllib.request
from collections import defaultdict
from zoneinfo import ZoneInfo
IT = ZoneInfo('Europe/Rome')

def candele(intervallo='5m', rng='1mo'):
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval={intervallo}&range={rng}'
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))['chart']['result'][0]
    q = r['indicators']['quote'][0]
    return [(dt.datetime.fromtimestamp(t, IT), h, l, v) for t, h, l, v in zip(r['timestamp'], q['high'], q['low'], q['volume']) if h and l and v]

def profilo(cc, passo=1.0):
    vol = defaultdict(float)
    for _, h, l, v in cc:
        a, b = int(l // passo), int(h // passo)
        n = b - a + 1
        for k in range(a, b + 1): vol[k] += v / n
    if not vol: return None
    livelli = sorted(vol); poc = max(livelli, key=lambda k: vol[k]); tot = sum(vol.values())
    lo = hi = livelli.index(poc); dentro = vol[poc]
    while dentro < .7 * tot and (lo > 0 or hi < len(livelli) - 1):
        su = vol[livelli[hi + 1]] if hi < len(livelli) - 1 else -1
        giu = vol[livelli[lo - 1]] if lo > 0 else -1
        if su >= giu: hi += 1; dentro += su
        else: lo -= 1; dentro += giu
    p = lambda k: round(k * passo + passo / 2, 1)
    return {'POC': p(poc), 'VAH': p(livelli[hi]), 'VAL': p(livelli[lo]), 'volume_totale': int(tot),
            'massimo': round(max(h for _, h, _, _ in cc), 1), 'minimo': round(min(l for _, _, l, _ in cc), 1), 'candele': len(cc)}

def vuoti(cc, soglia=.15, largh_min=8, bordo=6):
    """vuoti volumetrici (LVN): fasce di almeno largh_min $ dove il volume (media mobile su 5 $) è sotto soglia × picco.
    Esclusi i bordi del range (agli estremi il volume è sempre basso)."""
    vol = defaultdict(float)
    for _, h, l, v in cc:
        a, b = int(l // 1), int(h // 1)
        for k in range(a, b + 1): vol[k] += v / (b - a + 1)
    if not vol: return []
    ks = sorted(vol); lo, hi = ks[0], ks[-1]
    sm = {k: sum(vol.get(k + j, 0) for j in range(-2, 3)) / 5 for k in ks}
    lim = soglia * max(sm.values()); out = []; cur = None
    for k in ks + [hi + 1]:
        if k <= hi and sm[k] < lim: cur = [k, k] if cur is None else [cur[0], k]
        else:
            if cur and cur[1] - cur[0] >= largh_min and cur[0] > lo + bordo and cur[1] < hi - bordo: out.append([float(cur[0]), float(cur[1] + 1)])
            cur = None
    return out

cc = candele()
oggi = dt.datetime.now(IT).date()
giorni = sorted({t.date() for t, *_ in cc if t.date() < oggi and t.weekday() < 5})
ultimo = giorni[-1]
lun = oggi - dt.timedelta(days=oggi.weekday()); lun_prec = lun - dt.timedelta(days=7)
sett = [c for c in cc if lun_prec <= c[0].date() < lun]
ris = {'fonte': 'future oro COMEX (GC=F), candele a 5 minuti, ora italiana', 'calcolato': dt.datetime.now(IT).strftime('%d/%m %H:%M'),
       'ultima_seduta': dict(data=str(ultimo), **(profilo([c for c in cc if c[0].date() == ultimo]) or {})),
       'settimana_precedente': dict(dal=str(lun_prec), al=str(lun_prec + dt.timedelta(days=4)), **(profilo(sett) or {}))}
if oggi.weekday() >= 5 or oggi == lun:  # nel weekend e il lunedì la "settimana precedente" utile è quella appena chiusa
    lun2 = lun if oggi.weekday() >= 5 else lun_prec
    sett2 = [c for c in cc if lun2 <= c[0].date() < lun2 + dt.timedelta(days=5)]
    ris['settimana_precedente'] = dict(dal=str(lun2), al=str(lun2 + dt.timedelta(days=4)), **(profilo(sett2) or {}))
_w = ris['settimana_precedente']; _d0, _d1 = dt.date.fromisoformat(_w['dal']), dt.date.fromisoformat(_w['al'])
_w['vuoti'] = vuoti([c for c in cc if _d0 <= c[0].date() <= _d1])
ris['nota'] = ('Fine novembre: il contratto principale passa da dicembre a febbraio; nei giorni del passaggio il contratto continuo di Yahoo '
               'può mescolare i due e falsare un po\' i livelli.') if dt.date(oggi.year, 11, 20) <= oggi <= dt.date(oggi.year, 11, 30) else ''
if len(__import__('sys').argv) > 1:
    import os, subprocess, sys
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    ID = sys.argv[1]; QUI = os.path.dirname(os.path.abspath(__file__))
    CARTA, BLU, ORO, GRIGIO, ROSSO, VERDE = '#F6F6F3', '#12263F', '#D4AE5A', '#8A8F94', '#C8553D', '#2F7D62'
    it = lambda x: f'{x:,.1f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    W, S = ris['settimana_precedente'], ris['ultima_seduta']
    D0 = dt.date.fromisoformat(W['dal']); D1 = max(dt.date.fromisoformat(W['al']), dt.date.fromisoformat(S['data']))
    u = 'https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=30m&range=1mo'
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))['chart']['result'][0]; q = r['indicators']['quote'][0]
    bars = [(dt.datetime.fromtimestamp(t, IT), o, h, l, c) for t, o, h, l, c in zip(r['timestamp'], q['open'], q['high'], q['low'], q['close']) if None not in (o, h, l, c)]
    bars = [b for b in bars if D0 <= b[0].date() <= D1]
    f = plt.figure(figsize=(16, 9), dpi=100); f.patch.set_facecolor(CARTA)
    a = f.add_axes([.06, .1, .62, .72]); hx = f.add_axes([.82, .1, .15, .72], sharey=a)
    for ax in (a, hx):
        ax.set_facecolor(CARTA); [z.set_visible(False) for z in ax.spines.values()]; ax.tick_params(colors=BLU, labelsize=13, length=0)
    for i, (t, o, hi, lo, c) in enumerate(bars):
        col = VERDE if c >= o else ROSSO; a.plot([i, i], [lo, hi], color=col, lw=1, alpha=.8); a.add_patch(plt.Rectangle((i - .35, min(o, c)), .7, max(abs(c - o), .6), color=col, alpha=.8))
    ticks = [i for i, b in enumerate(bars) if i == 0 or b[0].date() != bars[i - 1][0].date()]
    G = ['lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom']
    a.set_xticks(ticks); a.set_xticklabels([f"{G[bars[i][0].weekday()]} {bars[i][0].day}" for i in ticks])
    a.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:,.0f}'.replace(',', '.')))
    vol = defaultdict(float)
    for _, hh, ll, v in [c for c in cc if dt.date.fromisoformat(W['dal']) <= c[0].date() <= dt.date.fromisoformat(W['al'])]:
        A, B = int(ll // 2), int(hh // 2)
        for k in range(A, B + 1): vol[k] += v / (B - A + 1)
    for k, v in vol.items():
        y = k * 2; dentro = W['VAL'] - 1 <= y <= W['VAH'] + 1
        hx.barh(y + 1, v, height=2, color=BLU if dentro else GRIGIO, alpha=.85 if dentro else .45)
    hx.set_xticks([]); hx.tick_params(labelleft=False)
    hx.text(0, 1.01, 'volume per prezzo\n(ultima settimana)', transform=hx.transAxes, fontsize=12, color=GRIGIO, va='bottom')
    MOSTRA_VUOTI = os.environ.get('VUOTI') != '0'  # accesi da Gabriele il 22/11
    if MOSTRA_VUOTI:
        for da, a_ in W.get('vuoti', []):
            a.axhspan(da, a_, color=GRIGIO, alpha=.16, lw=0, zorder=0); hx.axhspan(da, a_, color=GRIGIO, alpha=.16, lw=0, zorder=0)
            a.text(1, a_ - (a_ - da) * .08, f"vuoto volumetrico {da:,.0f}–{a_:,.0f} $".replace(',', '.'), va='top', fontsize=11, color='#6B7076', style='italic')
    n = len(bars); gs = [i for i in ticks if bars[i][0].date() == dt.date.fromisoformat(S['data'])]; x0g = gs[0] if gs else max(0, n - 46)
    gnome = G[dt.date.fromisoformat(S['data']).weekday()]
    for nome, val, col, ls, x0, lw in [('VAH settimana', W['VAH'], ROSSO, '--', 0, 2), ('POC settimana', W['POC'], ORO, '-', 0, 2.8), ('VAL settimana', W['VAL'], VERDE, '--', 0, 2),
                                      (f'VAH {gnome}', S['VAH'], ROSSO, ':', x0g, 2), (f'POC {gnome}', S['POC'], ORO, '-', x0g, 2.4), (f'VAL {gnome}', S['VAL'], VERDE, ':', x0g, 2)]:
        a.plot([x0, n], [val, val], color=col, ls=ls, lw=lw)
    # etichette a destra, distanziate se troppo vicine
    et = sorted([(W['VAH'], 'VAH settimana', ROSSO), (W['POC'], 'POC settimana', ORO), (W['VAL'], 'VAL settimana', VERDE),
                 (S['VAH'], f'VAH {gnome}', ROSSO), (S['POC'], f'POC {gnome}', ORO), (S['VAL'], f'VAL {gnome}', VERDE)], reverse=True)
    lo_, hi_ = a.get_ylim(); gap = (hi_ - lo_) * .035; ys = []
    for val, nome, col in et:
        y = val if not ys or ys[-1] - val >= gap else ys[-1] - gap; ys.append(y)
        a.text(n + 3, y, f'{nome}  {it(val)}', va='center', fontsize=13, color=col if col != ORO else '#9A7A2E', fontweight='bold', clip_on=False)
    a.set_xlim(-2, n + 2); a.grid(axis='y', color=BLU, alpha=.07)
    f.text(.06, .91, 'Oro (future COMEX) · volume profile a intervallo fisso', fontsize=26, fontweight='bold', color=BLU)
    f.text(.06, .865, f"ultima settimana ({dt.date.fromisoformat(W['dal']).strftime('%d/%m')}–{dt.date.fromisoformat(W['al']).strftime('%d/%m')}) e giorno precedente ({dt.date.fromisoformat(S['data']).strftime('%d/%m')}) · POC in oro, VAH in rosso, VAL in verde" + (' · in grigio i vuoti volumetrici' if MOSTRA_VUOTI else ''), fontsize=14, color=GRIGIO)
    f.text(.06, .035, 'Riskly News · dati Yahoo Finance (GC=F), candele a 30 minuti · value area = 70% del volume · livelli osservati, non segnali', fontsize=12, color=GRIGIO)
    f.savefig(os.path.join(QUI, '..', 'nuovo', 'news', 'copertine', f'{ID}-vp.jpg'), facecolor=CARTA, pil_kwargs={'quality': 88}); plt.close(f)
    out = subprocess.run([sys.executable, os.path.join(QUI, 'carica_copertina.py'), f'{ID}-vp'], capture_output=True, text=True)
    ris['grafico_url'] = [l for l in out.stdout.split() if l.startswith('https://')][-1]
    ris['riga_corpo'] = f"GRAFICO|{ris['grafico_url']}|Volume profile del future sull'oro: ultima settimana e giorno precedente (POC in oro, VAH in rosso, VAL in verde)"
print(json.dumps(ris, ensure_ascii=False, indent=1))
