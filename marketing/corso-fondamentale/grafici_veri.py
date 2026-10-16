# Grafici con dati veri (dati/*.csv, vedi dati/FONTI.md) → grafici/*.png, stile delle slide.
# Stampa anche i numeri chiave di ogni grafico (fatti.json): la voce delle lezioni cita solo questi.
# uso: python3 scarica_dati.py && python3 grafici_veri.py
import os, json, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt, matplotlib.dates as mdates, matplotlib.ticker
QUI = os.path.dirname(os.path.abspath(__file__)); os.makedirs(f'{QUI}/grafici', exist_ok=True)
PN, AC, RD, BL, TX, DM, LN, GI = '#151916', '#B6D84F', '#F0716B', '#6FB1E8', '#E6EDF3', '#8B98A9', '#2A312B', '#E9C46A'
plt.rcParams.update({'figure.facecolor': PN, 'axes.facecolor': PN, 'savefig.facecolor': PN, 'axes.edgecolor': LN, 'axes.labelcolor': DM,
                     'xtick.color': DM, 'ytick.color': DM, 'text.color': TX, 'font.size': 19, 'axes.grid': True, 'grid.color': LN,
                     'grid.linewidth': .8, 'axes.spines.top': False, 'axes.spines.right': False, 'legend.frameon': False})
FATTI = {}


def s(nome):
    d = pd.read_csv(f'{QUI}/dati/{nome}.csv', parse_dates=['data']).set_index('data')['valore'].astype(float)
    return d[~d.index.duplicated()]


def yoy(x, n=12): return (x / x.shift(n) - 1) * 100
def mese(x): return x.resample('MS').mean()
def it(v, d=1): return f'{v:.{d}f}'.replace('.', ',')
def mm(t): return ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'][t.month - 1] + f' {t.year}'


def recessioni(ax, da):
    r = s('USREC'); r = r[r.index >= da]; dentro = None
    for t, v in r.items():
        if v == 1 and dentro is None: dentro = t
        if v == 0 and dentro is not None: ax.axvspan(dentro, t, color=DM, alpha=.16, lw=0); dentro = None


def fonte(ax, t): ax.text(1, -0.13, 'Fonte: ' + t, transform=ax.transAxes, ha='right', va='top', fontsize=14, color=DM)


def salva(f, nome, fatti):
    for a in f.axes: a.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    f.savefig(f'{QUI}/grafici/{nome}.png', dpi=100, bbox_inches='tight', pad_inches=.35); plt.close(f)
    FATTI[nome] = fatti


def fig(): return plt.subplots(figsize=(16, 7))


def anni(ax, passo=4):
    ax.xaxis.set_major_locator(mdates.YearLocator(passo)); ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))


def punta(ax, t, v, testo, dx=30, dy=20, c=TX):
    ax.scatter([t], [v], color=c, s=90, zorder=6)
    ax.annotate(testo, (t, v), textcoords='offset points', xytext=(dx, dy), fontsize=17, color=c,
                arrowprops=dict(arrowstyle='-', color=c, lw=1.2))


# ---------- Modulo 3 · inflazione ----------
cpi, core = yoy(s('CPIAUCSL')), yoy(s('CPILFESL'))
a, b = cpi['2000':], core['2000':]
f, ax = fig(); ax.plot(a, color=RD, lw=3, label='CPI generale'); ax.plot(b, color=AC, lw=3, label='CPI core (senza cibo ed energia)')
ax.axhline(2, color=BL, lw=1.6, ls='--'); ax.text(a.index[2], 2.25, 'obiettivo 2%', color=BL, fontsize=16)
pk = a.idxmax(); punta(ax, pk, a[pk], f'picco {mm(pk)}: {it(a[pk])}%', -260, 0, RD)
mn = a['2008':'2010'].idxmin(); punta(ax, mn, a[mn], f'{mm(mn)}: {it(a[mn])}%', 30, -10, RD)
ax.set_ylabel('Variazione su un anno (%)'); ax.legend(loc='upper left'); anni(ax); fonte(ax, 'BLS via FRED, dati mensili fino a ' + mm(a.index[-1]))
salva(f, 'v_cpi', dict(picco=(mm(pk), round(a[pk], 1)), core_picco=(mm(b.idxmax()), round(b.max(), 1)), minimo_2009=(mm(mn), round(a[mn], 1)),
                       ultimo=(mm(a.index[-1]), round(a.iloc[-1], 1)), core_ultimo=round(b.iloc[-1], 1)))

pce = yoy(s('PCEPILFE')); a, b = core['2012':], pce['2012':]
f, ax = fig(); ax.plot(a, color=RD, lw=3, label='CPI core'); ax.plot(b, color=AC, lw=3, label='PCE core (quello che guarda la Fed)')
ax.axhline(2, color=BL, lw=1.6, ls='--'); ax.text(a.index[2], 2.2, 'obiettivo 2%', color=BL, fontsize=16)
dif = (a - b).dropna()
ax.set_ylabel('Variazione su un anno (%)'); ax.legend(loc='upper left'); anni(ax, 2); fonte(ax, 'BLS e BEA via FRED, fino a ' + mm(b.index[-1]))
salva(f, 'v_cpi_pce', dict(diff_media=round(dif.mean(), 2), pce_picco=(mm(b.idxmax()), round(b.max(), 1)), cpi_core_picco=(mm(a.idxmax()), round(a.max(), 1)),
                           pce_ultimo=(mm(b.index[-1]), round(b.iloc[-1], 1)), cpi_core_stesso_mese=round(a[b.index[-1]], 1)))

ppi = yoy(s('PPIFIS')); a, b = ppi['2011':], cpi['2011':]
f, ax = fig(); ax.plot(a, color=GI, lw=3, label='PPI (prezzi alla produzione)'); ax.plot(b, color=RD, lw=3, label='CPI (prezzi al consumo)')
pk = a.idxmax(); punta(ax, pk, a[pk], f'PPI {mm(pk)}: {it(a[pk])}%', 30, -5, GI)
ax.axhline(0, color=DM, lw=1); ax.set_ylabel('Variazione su un anno (%)'); ax.legend(loc='upper left'); anni(ax, 2); fonte(ax, 'BLS via FRED, fino a ' + mm(a.index[-1]))
salva(f, 'v_ppi', dict(ppi_picco=(mm(pk), round(a[pk], 1)), cpi_picco=(mm(b.idxmax()), round(b.max(), 1)), ppi_ultimo=(mm(a.index[-1]), round(a.iloc[-1], 1)),
                       ppi_min_2020=(mm(a['2020'].idxmin()), round(a['2020'].min(), 1))))

ez, itl = yoy(s('CP0000EZ19M086NEST'))['2000':], yoy(s('CP0000ITM086NEST'))['2000':]
f, ax = fig(); ax.plot(ez, color=BL, lw=3, label='Area euro'); ax.plot(itl, color=AC, lw=3, label='Italia')
ax.axhline(2, color=DM, lw=1.6, ls='--'); ax.text(ez.index[2], 2.25, 'obiettivo BCE 2%', color=DM, fontsize=16)
pi = itl.idxmax(); punta(ax, pi, itl[pi], f'Italia {mm(pi)}: {it(itl[pi])}%', -330, -10, AC)
pe = ez.idxmax(); ax.set_ylabel('Variazione su un anno (%)'); ax.legend(loc='upper left'); anni(ax); fonte(ax, 'Eurostat (HICP) via FRED, fino a ' + mm(ez.index[-1]))
salva(f, 'v_hicp', dict(ez_picco=(mm(pe), round(ez[pe], 1)), it_picco=(mm(pi), round(itl[pi], 1)), ez_ultimo=(mm(ez.index[-1]), round(ez.iloc[-1], 1)),
                        it_ultimo=round(itl.iloc[-1], 1), it_min=(mm(itl.idxmin()), round(itl.min(), 1))))

be, mi = mese(s('T5YIE'))['2005':], s('MICH')['2005':]
f, ax = fig(); ax.plot(be, color=AC, lw=3, label='Mercato: breakeven a 5 anni'); ax.plot(mi, color=GI, lw=3, label='Famiglie: inflazione attesa a 1 anno (Michigan)')
ax.axhline(2, color=BL, lw=1.4, ls='--'); ax.set_ylabel('Inflazione attesa (%)'); ax.legend(loc='upper left'); anni(ax); fonte(ax, 'Fed di St. Louis e Università del Michigan via FRED')
salva(f, 'v_aspettative', dict(be_max=(mm(be.idxmax()), round(be.max(), 2)), be_min=(mm(be.idxmin()), round(be.min(), 2)), be_ultimo=(mm(be.index[-1]), round(be.iloc[-1], 2)),
                               mich_max=(mm(mi.idxmax()), round(mi.max(), 1)), mich_ultimo=(mm(mi.index[-1]), round(mi.iloc[-1], 1))))

# ---------- Modulo 2 · banche centrali ----------
ff, ecb = s('FEDFUNDS')['2000':], mese(s('ECBDFR'))['2000':]
f, ax = fig(); ax.step(ff.index, ff, color=AC, lw=3, where='post', label='Fed (fed funds)'); ax.step(ecb.index, ecb, color=BL, lw=3, where='post', label='BCE (tasso sui depositi)')
ax.axhline(0, color=DM, lw=1); ax.set_ylabel('Tasso (%)'); ax.legend(loc='upper right'); anni(ax); fonte(ax, 'Fed e BCE via FRED, fino a ' + mm(ff.index[-1]))
ecb_neg = ecb[ecb < 0]
salva(f, 'v_tassi', dict(fed_ultimo=(mm(ff.index[-1]), round(ff.iloc[-1], 2)), bce_ultimo=round(ecb.iloc[-1], 2), bce_min=round(ecb.min(), 2),
                         bce_negativo=(mm(ecb_neg.index[0]), mm(ecb_neg.index[-1])), fed_2007=round(ff['2007'].max(), 2), fed_max_2023=round(ff['2022':'2024'].max(), 2)))

w = s('WALCL')['2003':] / 1e6
f, ax = fig(); ax.plot(w, color=AC, lw=3.5); ax.fill_between(w.index, 0, w, color=AC, alpha=.1)
for t, txt in (('2008-11-25', 'QE1'), ('2010-11-03', 'QE2'), ('2012-09-13', 'QE3'), ('2020-03-15', 'Covid'), ('2017-10-01', 'QT'), ('2022-06-01', 'QT')):
    t = pd.Timestamp(t); v = w[w.index >= t].iloc[0]; ax.annotate(txt, (t, v), textcoords='offset points', xytext=(-10, 26), fontsize=17, color=GI if txt == 'QT' else TX, ha='right')
pk = w.idxmax(); ax.set_ylabel('Attivi della Fed (migliaia di miliardi $)'); anni(ax); fonte(ax, 'Federal Reserve (H.4.1) via FRED, fino a ' + mm(w.index[-1]))
salva(f, 'v_bilancio_fed', dict(pre_2008=round(w[:'2008-08'].iloc[-1], 2), picco=(mm(pk), round(w[pk], 2)), ultimo=(mm(w.index[-1]), round(w.iloc[-1], 2)),
                                fine_2019=round(w[:'2019-12-31'].iloc[-1], 2)))

eu = s('EXUSEU')['2000':]; d = (ff - ecb).dropna()['2000':]
f, ax = fig(); ax.plot(d, color=AC, lw=3, label='Tasso Fed − tasso BCE (punti %, sinistra)'); ax.set_ylabel('Differenziale (punti %)')
ax2 = ax.twinx(); ax2.plot(eu, color=BL, lw=2.6, label='EUR/USD (destra)'); ax2.invert_yaxis(); ax2.set_ylabel('EUR/USD (scala rovesciata)', color=BL); ax2.tick_params(colors=BL); ax2.grid(False)
ax2.spines['right'].set_visible(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, loc='lower left', bbox_to_anchor=(0, 1.0), ncol=2); anni(ax)
fonte(ax, 'Fed, BCE e cambio ufficiale via FRED · dati mensili')
j = pd.concat([d, eu], axis=1).dropna(); c_tot = j.corr().iloc[0, 1]; c_22 = j['2021':'2023'].corr().iloc[0, 1]
salva(f, 'v_differenziale', dict(corr_2000=round(c_tot, 2), corr_2021_2023=round(c_22, 2), eurusd_min_2022=(mm(eu['2022'].idxmin()), round(eu['2022'].min(), 4)),
                                 diff_2022_fine=round(d['2022-12'].iloc[0], 2), eurusd_max=(mm(eu.idxmax()), round(eu.max(), 4))))

# ---------- Modulo 4 · lavoro ----------
nfp = s('PAYEMS').diff()['2023':]
f, ax = fig(); ax.bar(nfp.index, nfp, width=22, color=[AC if v >= 0 else RD for v in nfp])
ax.axhline(0, color=DM, lw=1); ax.set_ylabel('Nuovi posti di lavoro nel mese (migliaia)'); ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
fonte(ax, 'BLS (non farm payrolls, dati rivisti) via FRED, fino a ' + mm(nfp.index[-1]))
salva(f, 'v_nfp', dict(media_2023=round(nfp['2023'].mean()), media_ultimi_12=round(nfp.iloc[-12:].mean()), ultimo=(mm(nfp.index[-1]), round(nfp.iloc[-1])),
                       mesi_negativi=[mm(t) for t in nfp[nfp < 0].index], max=(mm(nfp.idxmax()), round(nfp.max()))))

u, p = s('UNRATE')['2000':], s('CIVPART')['2000':]
f, ax = fig(); recessioni(ax, '2000'); ax.plot(u, color=RD, lw=3, label='Disoccupazione (%, sinistra)'); ax.set_ylabel('Disoccupazione (%)')
ax2 = ax.twinx(); ax2.plot(p, color=BL, lw=2.6, label='Partecipazione (%, destra)'); ax2.set_ylabel('Partecipazione (%)', color=BL); ax2.tick_params(colors=BL); ax2.grid(False); ax2.spines['right'].set_visible(True)
pk = u.idxmax(); punta(ax, pk, u[pk], f'{mm(pk)}: {it(u[pk])}%', 30, -10, RD)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, loc='lower left', bbox_to_anchor=(0, 1.0), ncol=2); anni(ax)
fonte(ax, 'BLS via FRED · in grigio le recessioni (NBER)')
salva(f, 'v_disoccupazione', dict(picco=(mm(pk), round(u[pk], 1)), max_2009=(mm(u['2009':'2010'].idxmax()), round(u['2009':'2010'].max(), 1)), ultimo=(mm(u.index[-1]), round(u.iloc[-1], 1)),
                                  min_post_2019=(mm(u['2019':].idxmin()), round(u['2019':].min(), 1)), part_2000=round(p.iloc[0], 1), part_ultimo=round(p.iloc[-1], 1)))

sal = yoy(s('CES0500000003'))['2008':]; c2 = cpi['2008':]; reale = (sal - c2).dropna()
f, ax = fig(); ax.fill_between(reale.index, 0, reale, where=reale < 0, color=RD, alpha=.18, label='Salari sotto l\'inflazione')
ax.plot(sal, color=AC, lw=3, label='Salario orario medio'); ax.plot(c2, color=RD, lw=2.6, label='Inflazione (CPI)'); ax.axhline(0, color=DM, lw=1)
ax.set_ylabel('Variazione su un anno (%)'); ax.legend(loc='upper left'); anni(ax, 2); fonte(ax, 'BLS via FRED, fino a ' + mm(sal.index[-1]))
neg = reale['2021':][reale['2021':] < 0]
salva(f, 'v_salari', dict(sal_ultimo=(mm(sal.index[-1]), round(sal.iloc[-1], 1)), cpi_stesso=round(c2[sal.index[-1]], 1), sal_max_post2021=(mm(sal['2021-06':].idxmax()), round(sal['2021-06':].max(), 1)),
                          negativi_da=mm(neg.index[0]) if len(neg) else None, negativi_a=mm(neg.index[-1]) if len(neg) else None))

ic = s('ICSA')['2015':] / 1000
f, ax = fig(); ax.plot(ic, color=AC, lw=2); ax.set_yscale('log'); ax.set_yticks([150, 200, 300, 500, 1000, 2000, 5000]); ax.set_yticklabels(['150', '200', '300', '500', '1.000', '2.000', '5.000'])
pk = ic.idxmax(); punta(ax, pk, ic[pk], f'settimana del {pk.day} {mm(pk)}: {ic[pk]:,.0f}'.replace(',', '.') + ' mila', 30, -10, RD)
ax.set_ylabel('Richieste di sussidio a settimana (migliaia, scala log)'); anni(ax, 2); fonte(ax, 'Dipartimento del Lavoro USA via FRED')
salva(f, 'v_sussidi', dict(picco=(f'{pk.day} {mm(pk)}', round(ic[pk])), media_2019=round(ic['2019'].mean()), ultimo=(f'{ic.index[-1].day} {mm(ic.index[-1])}', round(ic.iloc[-1])),
                           media_ultimi_3m=round(ic.iloc[-13:].mean())))

# ---------- Modulo 5 · crescita ----------
pil = s('A191RL1Q225SBEA')['2000':]
f, ax = fig(); recessioni(ax, '2000'); ax.bar(pil.index, pil.clip(-12, 12), width=70, color=[AC if v >= 0 else RD for v in pil])
for t in (pil.idxmin(), pil.idxmax()): ax.text(t, max(min(pil[t], 11), -11) + (0.8 if pil[t] > 0 else -1.6), f'{it(pil[t])}%', ha='center', fontsize=16, color=TX)
ax.axhline(0, color=DM, lw=1); ax.set_ylim(-14, 14); ax.set_ylabel('PIL, trimestre su trimestre, annualizzato (%)'); anni(ax)
fonte(ax, 'BEA via FRED · in grigio le recessioni (NBER) · barre tagliate a ±12%')
neg = pil[pil < 0]
salva(f, 'v_pil', dict(min=(str(pil.idxmin().date()), round(pil.min(), 1)), max=(str(pil.idxmax().date()), round(pil.max(), 1)), ultimo=(str(pil.index[-1].date()), round(pil.iloc[-1], 1)),
                       neg_2022=[str(t.date()) for t in neg['2022'].index], neg_2025=[str(t.date()) for t in neg['2024':].index]))

rs = yoy(s('RSAFS'))['2010':]
f, ax = fig(); ax.plot(rs.clip(-25, 55), color=AC, lw=3); ax.axhline(0, color=DM, lw=1); ax.plot(cpi['2010':], color=RD, lw=2, ls='--', label='Inflazione (CPI)')
ax.set_ylabel('Vendite al dettaglio, su un anno (%)'); ax.legend(loc='upper left'); anni(ax, 2); fonte(ax, 'Census Bureau via FRED (valori nominali), fino a ' + mm(rs.index[-1]))
salva(f, 'v_vendite', dict(min_2020=(mm(rs['2020'].idxmin()), round(rs['2020'].min(), 1)), max_2021=(mm(rs['2021'].idxmax()), round(rs['2021'].max(), 1)), ultimo=(mm(rs.index[-1]), round(rs.iloc[-1], 1))))

um = s('UMCSENT')['2000':]
f, ax = fig(); recessioni(ax, '2000'); ax.plot(um, color=AC, lw=3); mn = um.idxmin(); punta(ax, mn, um[mn], f'minimo storico {mm(mn)}: {it(um[mn])}', 30, 10, RD)
ax.set_ylabel('Fiducia dei consumatori (Michigan)'); anni(ax); fonte(ax, 'Università del Michigan via FRED · in grigio le recessioni')
salva(f, 'v_fiducia', dict(min=(mm(mn), round(um[mn], 1)), max=(mm(um.idxmax()), round(um.max(), 1)), ultimo=(mm(um.index[-1]), round(um.iloc[-1], 1))))

ip = yoy(s('INDPRO'))['2000':]
f, ax = fig(); recessioni(ax, '2000'); ax.plot(ip, color=AC, lw=3); ax.axhline(0, color=DM, lw=1)
ax.set_ylabel('Produzione industriale, su un anno (%)'); anni(ax); fonte(ax, 'Federal Reserve via FRED · in grigio le recessioni')
salva(f, 'v_produzione', dict(min=(mm(ip.idxmin()), round(ip.min(), 1)), ultimo=(mm(ip.index[-1]), round(ip.iloc[-1], 1))))

# ---------- Modulo 6 · obbligazioni ----------
y10, y2 = mese(s('DGS10'))['2000':], mese(s('DGS2'))['2000':]
f, ax = fig(); ax.plot(y10, color=AC, lw=3, label='Treasury 10 anni'); ax.plot(y2, color=BL, lw=3, label='Treasury 2 anni')
mn = y10.idxmin(); punta(ax, mn, y10[mn], f'{mm(mn)}: {it(y10[mn], 2)}%', 30, 30, AC)
ax.set_ylabel('Rendimento (%)'); ax.legend(loc='upper right'); anni(ax); fonte(ax, 'Tesoro USA via FRED · medie mensili')
salva(f, 'v_rendimenti', dict(min10=(mm(mn), round(y10[mn], 2)), ultimo10=(mm(y10.index[-1]), round(y10.iloc[-1], 2)), ultimo2=round(y2.iloc[-1], 2), max10_post2020=(mm(y10['2021':].idxmax()), round(y10['2021':].max(), 2))))

cu = mese(s('T10Y2Y'))['1980':]
f, ax = fig(); recessioni(ax, '1980'); ax.fill_between(cu.index, 0, cu, where=cu < 0, color=RD, alpha=.5, label='Curva invertita'); ax.plot(cu, color=AC, lw=2.4)
ax.axhline(0, color=DM, lw=1); ax.set_ylabel('10 anni − 2 anni (punti %)'); ax.legend(loc='upper left'); anni(ax, 5); fonte(ax, 'Fed di St. Louis via FRED · in grigio le recessioni (NBER)')
inv = cu['2022':][cu['2022':] < 0]
salva(f, 'v_curva', dict(inv_2022_da=mm(inv.index[0]), inv_2022_a=mm(inv.index[-1]), min_2023=(mm(cu['2022':].idxmin()), round(cu['2022':].min(), 2)), ultimo=(mm(cu.index[-1]), round(cu.iloc[-1], 2))))

re_, oro = mese(s('DFII10'))['2006':], mese(s('GCF'))['2001':]
f, ax = fig(); ax.plot(re_, color=AC, lw=3, label='Rendimento reale 10 anni (%, sinistra, scala rovesciata)'); ax.invert_yaxis(); ax.set_ylabel('Rendimento reale (%)')
ax2 = ax.twinx(); ax2.plot(oro['2006':], color=GI, lw=2.6, label='Oro ($/oncia, destra)'); ax2.set_ylabel('Oro ($)', color=GI); ax2.tick_params(colors=GI); ax2.grid(False); ax2.spines['right'].set_visible(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, loc='upper left', fontsize=16); anni(ax)
fonte(ax, 'Fed di St. Louis (TIPS) via FRED · oro: future COMEX, Yahoo Finance')
j = pd.concat([re_, oro['2006':]], axis=1).dropna(); c1 = j[:'2021'].corr().iloc[0, 1]; c2_ = j['2022':].corr().iloc[0, 1]
salva(f, 'v_reali_oro', dict(corr_2006_2021=round(c1, 2), corr_2022_oggi=round(c2_, 2), reale_ultimo=(mm(re_.index[-1]), round(re_.iloc[-1], 2)),
                             reale_min=(mm(re_.idxmin()), round(re_.min(), 2)), oro_2022=round(oro['2022-10'].iloc[0]), oro_ultimo=round(oro.iloc[-1])))

sp = (s('IRLTLT01ITM156N') - s('IRLTLT01DEM156N')).dropna()['1995':] * 100
f, ax = fig(); ax.plot(sp, color=AC, lw=3); pk = sp['2010':].idxmax(); punta(ax, pk, sp[pk], f'{mm(pk)}: {sp[pk]:.0f} punti base', 30, -5, RD)
ax.set_ylabel('BTP − Bund a 10 anni (punti base)'); anni(ax); fonte(ax, 'OCSE via FRED · medie mensili')
salva(f, 'v_spread', dict(picco=(mm(pk), round(sp[pk])), max_2018=(mm(sp['2018'].idxmax()), round(sp['2018'].max())), max_2022=(mm(sp['2022'].idxmax()), round(sp['2022'].max())),
                          ultimo=(mm(sp.index[-1]), round(sp.iloc[-1])), min_2000s=round(sp['2003':'2007'].min())))

# ---------- Modulo 7 · correlazioni ----------
dol = s('DTWEXBGS').resample('W-FRI').last(); orod = s('GCF').resample('W-FRI').last()
r = pd.concat([dol.pct_change(), orod.pct_change()], axis=1).dropna()['2007':]; rc = r.iloc[:, 0].rolling(52).corr(r.iloc[:, 1]).dropna()
f, ax = fig(); ax.fill_between(rc.index, 0, rc, color=BL, alpha=.25); ax.plot(rc, color=BL, lw=2.6); ax.axhline(0, color=DM, lw=1)
ax.set_ylim(-1, 1); ax.set_ylabel('Correlazione su 52 settimane'); anni(ax, 2); fonte(ax, 'dollaro: Fed via FRED · oro: Yahoo Finance · variazioni settimanali')
ax.set_title('Dollaro e oro: la correlazione cambia nel tempo', color=TX, fontsize=21, loc='left')
salva(f, 'v_corr_mobile', dict(min=(mm(rc.idxmin()), round(rc.min(), 2)), max=(mm(rc.idxmax()), round(rc.max(), 2)), ultimo=(mm(rc.index[-1]), round(rc.iloc[-1], 2)), media=round(rc.mean(), 2)))

dm = mese(s('DTWEXBGS'))['2015':]; om = oro['2015':]
f, ax = fig(); ax.plot(dm, color=BL, lw=3, label='Dollaro (indice, sinistra)'); ax.set_ylabel('Indice del dollaro')
ax2 = ax.twinx(); ax2.plot(om, color=GI, lw=3, label='Oro ($, destra)'); ax2.set_ylabel('Oro ($)', color=GI); ax2.tick_params(colors=GI); ax2.grid(False); ax2.spines['right'].set_visible(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, loc='upper left'); anni(ax, 2)
fonte(ax, 'Fed via FRED · Yahoo Finance · medie mensili')
salva(f, 'v_dollaro_oro', dict(oro_2015=round(om.iloc[0]), oro_ultimo=round(om.iloc[-1]), dol_2022_max=(mm(dm['2022'].idxmax()), round(dm['2022'].max(), 1)), dol_ultimo=round(dm.iloc[-1], 1)))

jp = mese(s('DEXJPUS'))['2020':]; y10b = y10['2020':]
f, ax = fig(); ax.plot(y10b, color=AC, lw=3, label='Treasury 10 anni (%, sinistra)'); ax.set_ylabel('Rendimento (%)')
ax2 = ax.twinx(); ax2.plot(jp, color=RD, lw=3, label='USD/JPY (destra)'); ax2.set_ylabel('USD/JPY', color=RD); ax2.tick_params(colors=RD); ax2.grid(False); ax2.spines['right'].set_visible(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, loc='upper left'); ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
fonte(ax, 'Tesoro USA e Fed via FRED · medie mensili')
j = pd.concat([y10b, jp], axis=1).dropna()
salva(f, 'v_yen', dict(corr=round(j.corr().iloc[0, 1], 2), jp_2021=round(jp['2021-01'].iloc[0], 1), jp_max=(mm(jp.idxmax()), round(jp.max(), 1)), jp_ultimo=(mm(jp.index[-1]), round(jp.iloc[-1], 1)),
                       y_2021=round(y10b['2021-01'].iloc[0], 2)))

wti, cad = mese(s('DCOILWTICO'))['2010':], mese(s('DEXCAUS'))['2010':]
f, ax = fig(); ax.plot(wti, color=GI, lw=3, label='Petrolio WTI ($, sinistra)'); ax.set_ylabel('Petrolio ($ al barile)')
ax2 = ax.twinx(); ax2.plot(cad, color=BL, lw=3, label='USD/CAD (destra, scala rovesciata)'); ax2.invert_yaxis(); ax2.set_ylabel('USD/CAD', color=BL); ax2.tick_params(colors=BL); ax2.grid(False); ax2.spines['right'].set_visible(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, loc='lower left'); anni(ax, 2)
fonte(ax, 'EIA e Fed via FRED · medie mensili')
j = pd.concat([wti, cad], axis=1).dropna()
salva(f, 'v_petrolio_cad', dict(corr_2010_2016=round(j[:'2016'].corr().iloc[0, 1], 2), corr_2020_oggi=round(j['2020':].corr().iloc[0, 1], 2), wti_2014=round(wti['2014-06'].iloc[0]), wti_2016=(mm(wti['2015':'2016'].idxmin()), round(wti['2015':'2016'].min())),
                                cad_2014=round(cad['2014-06'].iloc[0], 2), cad_2016=round(cad['2016-01'].iloc[0], 2), wti_ultimo=(mm(wti.index[-1]), round(wti.iloc[-1]))))

vix, spx = s('VIXCLS')['2007':], s('GSPC')['2007':]
f, ax = plt.subplots(2, 1, figsize=(16, 8), sharex=True, gridspec_kw={'height_ratios': [1.4, 1]})
ax[0].plot(spx, color=AC, lw=2.2); ax[0].set_yscale('log'); ax[0].set_ylabel('S&P 500 (log)'); ax[1].plot(vix, color=RD, lw=1.8); ax[1].set_ylabel('VIX')
for t in (vix['2008':'2009'].idxmax(), vix['2020'].idxmax()): ax[1].annotate(f'{t.day} {mm(t)}: {it(vix[t])}', (t, vix[t]), textcoords='offset points', xytext=(12, -8), fontsize=16, color=RD)
anni(ax[1], 2); fonte(ax[1], 'Cboe via FRED · S&P 500: Yahoo Finance · dati giornalieri')
salva(f, 'v_vix', dict(vix_2008=(str(vix['2008':'2009'].idxmax().date()), round(vix['2008':'2009'].max(), 1)), vix_2020=(str(vix['2020'].idxmax().date()), round(vix['2020'].max(), 1)),
                       vix_media=round(vix.mean(), 1), vix_ultimo=(str(vix.index[-1].date()), round(vix.iloc[-1], 1)),
                       spx_2020_calo=round((spx['2020-02-01':'2020-04-30'].min() / spx['2020-02-01':'2020-02-29'].max() - 1) * 100, 1)))

ag = mese(s('SIF'))['2015':]; og = oro['2015':]
f, ax = fig(); ax.plot(og / og.iloc[0] * 100, color=GI, lw=3, label='Oro'); ax.plot(ag / ag.iloc[0] * 100, color=DM, lw=3, label='Argento')
ax.axhline(100, color=LN, lw=1.5); ax.set_ylabel('Gennaio 2015 = 100'); ax.legend(loc='upper left'); anni(ax, 2); fonte(ax, 'future COMEX, Yahoo Finance · dati mensili')
ra = (og / ag).dropna()
salva(f, 'v_oro_argento', dict(oro_x=round(og.iloc[-1] / og.iloc[0], 2), ag_x=round(ag.iloc[-1] / ag.iloc[0], 2), corr_rend=round(pd.concat([og.pct_change(), ag.pct_change()], axis=1).dropna().corr().iloc[0, 1], 2),
                               rapporto_ultimo=round(ra.iloc[-1]), rapporto_max=(mm(ra.idxmax()), round(ra.max()))))

# ---------- Modulo 8 · beni rifugio ----------
f, ax = fig(); ax.plot(oro, color=GI, lw=3); ax.set_yscale('log'); ax.set_yticks([250, 500, 1000, 2000, 4000]); ax.set_yticklabels(['250', '500', '1.000', '2.000', '4.000'])
for a_, b_ in (('2011-09', 'massimo 2011'), ('2015-12', 'minimo 2015')):
    t = pd.Timestamp(a_ + '-01'); punta(ax, t, oro[t], f'{b_}: {oro[t]:,.0f} $'.replace(',', '.'), 20, 25 if 'mass' in b_ else -40, GI)
ax.set_ylabel('Oro, $ per oncia (scala log)'); anni(ax); fonte(ax, 'future COMEX, Yahoo Finance · medie mensili')
o_ = oro['2011':'2015']
salva(f, 'v_oro', dict(o2000=round(oro.iloc[0]), max2011=(mm(o_['2011':'2012'].idxmax()), round(o_['2011':'2012'].max())), min2015=(mm(o_['2013':].idxmin()), round(o_['2013':].min())),
                       calo=round((o_['2013':].min() / o_['2011':'2012'].max() - 1) * 100), ultimo=(mm(oro.index[-1]), round(oro.iloc[-1]))))

g, e = s('GCF')['2020-02-14':'2020-04-15'], s('GSPC')['2020-02-14':'2020-04-15']
f, ax = fig(); ax.plot(g / g.iloc[0] * 100, color=GI, lw=3.5, label='Oro'); ax.plot(e / e.iloc[0] * 100, color=RD, lw=3.5, label='S&P 500')
ax.axhline(100, color=LN, lw=1.5); ax.set_ylabel('14 febbraio 2020 = 100'); ax.legend(loc='lower left'); ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
fonte(ax, 'Yahoo Finance · chiusure giornaliere'); ax.set_title('Marzo 2020: anche l\'oro scende quando serve liquidità', color=TX, fontsize=21, loc='left')
gm = g[:'2020-03-31']
salva(f, 'v_marzo2020', dict(oro_calo=round((gm.min() / gm[:'2020-03-09'].max() - 1) * 100, 1), oro_min=str(gm.idxmin().date()), oro_max=str(gm[:'2020-03-09'].idxmax().date()),
                             spx_calo=round((e.min() / e.iloc[0] - 1) * 100, 1), spx_min=str(e.idxmin().date())))

jy = mese(s('DEXJPUS'))['2000':]; chf = s('EURCHFX_mese')['2003':]
# ---------- Modulo 9 · eventi straordinari ----------
ec = s('EURCHFX')['2014-12-15':'2015-02-27']
f, ax = fig(); ax.plot(ec, color=RD, lw=3.5, marker='o', ms=5); ax.axhline(1.20, color=BL, lw=1.6, ls='--'); ax.text(ec.index[1], 1.205, 'soglia minima 1,20 difesa dalla BNS', color=BL, fontsize=16)
t = pd.Timestamp('2015-01-15'); ax.annotate('15 gennaio 2015, 10:30:\nla BNS abbandona la soglia', (t, ec[t] if t in ec.index else ec.iloc[20]), textcoords='offset points', xytext=(30, -40), fontsize=17, color=TX)
ax.set_ylabel('EUR/CHF'); ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m')); fonte(ax, 'Yahoo Finance · chiusure giornaliere (il minimo intraday è stato molto più basso)')
salva(f, 'v_franco2015', dict(prima=round(ec[:'2015-01-14'].iloc[-1], 4), chiusura_15=round(ec['2015-01-15'], 4) if pd.Timestamp('2015-01-15') in ec.index else None,
                              min_chiusura=(str(ec.idxmin().date()), round(ec.min(), 4)), fine_feb=round(ec.iloc[-1], 4)))

json.dump(FATTI, open(f'{QUI}/grafici/fatti.json', 'w'), indent=1, ensure_ascii=False, default=str)
print(json.dumps(FATTI, indent=1, ensure_ascii=False, default=str))
