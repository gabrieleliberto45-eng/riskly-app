# Esempi di trade su prezzi VERI (EURUSD 1 ora, Yahoo Finance) per le lezioni del corso di rischio.
# Per ogni trade due immagini: "prima" (fino all'ingresso, con stop e target) e "dopo" (com'è finita). → ../grafici/e_*.png + esempi.json
# uso: python3 esempi_veri.py   (scarica eurusd_1h.json se manca)
import json, os, datetime as dt, subprocess
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.patches import Rectangle
QUI = os.path.dirname(os.path.abspath(__file__)); G = os.path.join(QUI, '..', 'grafici')
BG, PN, AC, RD, BL, TX, DM, LN = '#0B0D0C', '#151916', '#B6D84F', '#F0716B', '#6FB1E8', '#E6EDF3', '#8B98A9', '#2A312B'
plt.rcParams.update({'figure.facecolor': PN, 'axes.facecolor': PN, 'savefig.facecolor': PN, 'axes.edgecolor': LN, 'axes.labelcolor': DM,
                     'xtick.color': DM, 'ytick.color': DM, 'text.color': TX, 'font.size': 18, 'axes.grid': True, 'grid.color': LN, 'grid.linewidth': .7,
                     'axes.spines.top': False, 'axes.spines.right': False})
f = os.path.join(QUI, 'eurusd_1h.json')
if not os.path.exists(f):
    subprocess.run(['curl', '-sfL', '-A', 'Mozilla/5.0', '-o', f, 'https://query1.finance.yahoo.com/v8/finance/chart/EURUSD=X?range=60d&interval=1h'], check=True)
j = json.load(open(f))['chart']['result'][0]; q = j['indicators']['quote'][0]
B = [(dt.datetime.utcfromtimestamp(t) + dt.timedelta(hours=2), o, h, l, c) for t, o, h, l, c in zip(j['timestamp'], q['open'], q['high'], q['low'], q['close']) if None not in (o, h, l, c)]  # ora italiana (estate)
idx = {b[0]: i for i, b in enumerate(B)}
POS = {b[0]: i for i, b in enumerate(B)}   # asse x per numero di candela: niente buchi nel fine settimana
PIP = 0.0001; CAP, RISK = 10000, 0.01

def trova(t): return idx[t + dt.timedelta(hours=2)]
def candele(ax, a, z):
    for b in B[a:z]:
        x = B.index(b) if False else POS[b[0]]; su = b[4] >= b[1]; col = AC if su else RD
        ax.plot([x, x], [b[3], b[2]], color=col, lw=1.2, zorder=2)
        ax.add_patch(Rectangle((x - 0.32, min(b[1], b[4])), 0.64, max(abs(b[4] - b[1]), 0.00002), color=col, zorder=3))
def trade(nome, t_min, t_ing, fine_extra=8):
    i_min, i_e = trova(t_min), trova(t_ing)
    lo = B[i_min][3]; entry = B[i_e][4]; stop = round(lo - 5 * PIP, 5); dist = (entry - stop) / PIP; tgt = entry + 1.8 * (entry - stop)
    esito = None
    for k in range(i_e + 1, len(B)):
        if B[k][3] <= stop: esito = ('stop', k); break
        if B[k][2] >= tgt: esito = ('target', k); break
    pv_eur = 10 / entry                                   # valore del pip per 1 lotto in euro (conto in euro)
    lotti = int(CAP * RISK / (dist * pv_eur) * 100) / 100  # per difetto
    risultato = (1.8 * dist if esito[0] == 'target' else -dist) * lotti * pv_eur
    a = max(0, i_min - 30)
    for fase in ('prima', 'dopo'):
        z = (i_e + 1) if fase == 'prima' else min(len(B), esito[1] + fine_extra)
        fig, ax = plt.subplots(figsize=(16, 7.4)); candele(ax, a, z)
        x0, x1 = i_e, min(len(B) - 1, esito[1] + fine_extra)
        ax.axhline(stop, color=RD, lw=2, ls='--'); ax.axhline(tgt, color=AC, lw=2, ls='--'); ax.axhline(entry, color=TX, lw=1.2, ls=':')
        ax.fill_between([x0, x1], stop, entry, color=RD, alpha=.10); ax.fill_between([x0, x1], entry, tgt, color=AC, alpha=.08)
        ax.scatter([i_min], [lo], color=BL, s=90, zorder=5)
        ax.annotate(f'minimo {lo:.5f}'.replace('.', ','), (i_min, lo), textcoords='offset points', xytext=(14, -6), color=BL, fontsize=17, ha='left', va='top')
        ax.scatter([x0], [entry], color=TX, s=90, zorder=5)
        dx = a + 0.5
        ax.text(dx, stop, f' stop {stop:.5f} · −{dist:.1f} pip'.replace('.', ','), color=RD, fontsize=17, va='bottom')
        ax.text(dx, tgt, f' target {tgt:.5f} · +{1.8*dist:.1f} pip'.replace('.', ','), color=AC, fontsize=17, va='bottom')
        ax.annotate(f'ingresso {entry:.5f}'.replace('.', ','), (x0, entry), textcoords='offset points', xytext=(14, 10), color=TX, fontsize=17, ha='left', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.25', fc=PN, ec='none', alpha=.85))
        if fase == 'dopo':
            k = esito[1]; y = stop if esito[0] == 'stop' else tgt
            ax.scatter([k], [y], color=AC if esito[0] == 'target' else RD, s=160, zorder=6, marker='X')
            ax.annotate(('TARGET  ' if esito[0] == 'target' else 'STOP  ') + B[k][0].strftime('%d/%m %H:%M'), (k, y),
                        textcoords='offset points', xytext=(-20, 18 if esito[0] == 'target' else -36), color=AC if esito[0] == 'target' else RD, fontsize=18, ha='right', fontweight='bold')
        ax.set_xlim(a - 1, x1 + 1)
        tk = [i for i in range(a, x1 + 1) if B[i][0].hour == 0 or i == a]; ax.set_xticks(tk); ax.set_xticklabels([B[i][0].strftime('%d/%m') for i in tk])
        lo_y = min(b[3] for b in B[a:z] + [B[a]]) ; hi_y = max(max(b[2] for b in B[a:z]), tgt)
        ax.set_ylim(min(lo_y, stop) - 10 * PIP, hi_y + 8 * PIP)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f'{v:.4f}'.replace('.', ',')))
        ax.text(1, -0.16, 'EURUSD, candele da 1 ora, ora italiana · Fonte: Yahoo Finance · esempio didattico, non un segnale', transform=ax.transAxes, ha='right', fontsize=13, color=DM)
        fig.savefig(os.path.join(G, f'e_{nome}_{fase}.png'), dpi=100, bbox_inches='tight', pad_inches=.3); plt.close(fig)
    return dict(minimo=(B[i_min][0].strftime('%d/%m/%Y %H:%M'), round(lo, 5)), ingresso=(B[i_e][0].strftime('%d/%m/%Y %H:%M'), round(entry, 5)),
                stop=stop, pip_stop=round(dist, 1), target=round(tgt, 5), pip_target=round(1.8 * dist, 1), valore_pip_eur=round(pv_eur, 2), lotti=lotti,
                esito=esito[0], quando=B[esito[1]][0].strftime('%d/%m/%Y %H:%M'), ore=esito[1] - i_e, euro=round(risultato, 2))

R = {'vinto': trade('vinto', dt.datetime(2026, 8, 13, 6), dt.datetime(2026, 8, 13, 10)),
     'perso': trade('perso', dt.datetime(2026, 9, 14, 13), dt.datetime(2026, 9, 14, 17))}
json.dump(R, open(os.path.join(QUI, 'esempi.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps(R, indent=1, ensure_ascii=False))
