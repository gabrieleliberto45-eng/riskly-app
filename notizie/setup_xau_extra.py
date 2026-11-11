# Scheda tecnica e operativa dell'oro per il Setup XAU (10-11 novembre 2026, richiesta di Gabriele: "più valore tecnico e operativo").
# Solo fatti calcolati dai prezzi: pivot, struttura settimanale, Bollinger, distanza dalle medie, correlazioni, ore più mosse, mappa delle sessioni, tabella dei lotti.
# MAI segnali, ingressi o obiettivi: sono livelli e statistiche. Uso: python3 notizie/setup_xau_extra.py  → stampa un JSON.
import datetime as dt, json, math, urllib.request
from zoneinfo import ZoneInfo
ROMA = ZoneInfo('Europe/Rome')
def yahoo(simb, rng, interv):
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{simb}?range={rng}&interval={interv}'
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))['chart']['result'][0]
    q = r['indicators']['quote'][0]
    return [(dt.datetime.fromtimestamp(t, dt.timezone.utc), o, h, l, c) for t, o, h, l, c in zip(r['timestamp'], q['open'], q['high'], q['low'], q['close']) if None not in (o, h, l, c)]
def corr(a, b):
    n = min(len(a), len(b)); a, b = a[-n:], b[-n:]
    ma, mb = sum(a) / n, sum(b) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a)); sb = math.sqrt(sum((x - mb) ** 2 for x in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else None
def rend(c): return [c[i] / c[i - 1] - 1 for i in range(1, len(c))]
def r0(x, n=1): return None if x is None else round(x, n)

oro = yahoo('GC=F', '1y', '1d'); oggi = oro[-1][0].date()
# ultima seduta piena = l'ultima barra con data diversa da oggi (se la barra di oggi è in corso)
adesso = dt.datetime.now(dt.timezone.utc)
piena = oro[-2] if oro[-1][0].date() == adesso.date() else oro[-1]
corrente = oro[-1]; H, L, C = piena[2], piena[3], piena[4]
P = (H + L + C) / 3
piv = dict(P=P, R1=2 * P - L, R2=P + (H - L), S1=2 * P - H, S2=P - (H - L))
# settimana precedente e settimana in corso (lun–ven)
def lunedi(d): return d - dt.timedelta(days=d.weekday())
sett = {}
for b in oro: sett.setdefault(lunedi(b[0].date()), []).append(b)
chiavi = sorted(sett); corr_w = sett[chiavi[-1]]; prec_w = sett[chiavi[-2]] if len(chiavi) > 1 else None
pw = None
if prec_w:
    wH, wL, wC = max(x[2] for x in prec_w), min(x[3] for x in prec_w), prec_w[-1][4]; wP = (wH + wL + wC) / 3
    pw = dict(massimo=wH, minimo=wL, chiusura=wC, P=wP, R1=2 * wP - wL, S1=2 * wP - wH)
chiusure = [b[4] for b in oro]
def media(n): return sum(chiusure[-n:]) / n
m20, m50, m200 = media(20), media(50), media(200)
sd20 = math.sqrt(sum((x - m20) ** 2 for x in chiusure[-20:]) / 20)
bb_su, bb_giu = m20 + 2 * sd20, m20 - 2 * sd20
prezzo = corrente[4]
tr = [max(oro[i][2] - oro[i][3], abs(oro[i][2] - oro[i - 1][4]), abs(oro[i][3] - oro[i - 1][4])) for i in range(1, len(oro))]
atr = sum(tr[-14:]) / 14
# serie consecutive
serie = 0; verso = 0
for i in range(len(oro) - 1, 0, -1):
    d = 1 if oro[i][4] > oro[i - 1][4] else -1
    if verso == 0: verso = d
    if d == verso: serie += 1
    else: break
# correlazioni a 20 sedute
cor = {}
for nome, simb in [('dollaro (DXY)', 'DX-Y.NYB'), ('decennale USA', '^TNX')]:
    try:
        s = yahoo(simb, '3mo', '1d'); dd = {b[0].date(): b[4] for b in s}; oo = {b[0].date(): b[4] for b in oro}
        giorni = sorted(set(dd) & set(oo))[-21:]
        cor[nome] = r0(corr(rend([oo[g] for g in giorni]), rend([dd[g] for g in giorni])), 2)
    except Exception: cor[nome] = None
# ore più mosse (ora italiana) e mappa delle sessioni dell'ultima seduta piena, da barre orarie
orarie = yahoo('GC=F', '1mo', '1h')
per_ora = {}
for t, o, h, l, c in orarie:
    ora = t.astimezone(ROMA).hour; per_ora.setdefault(ora, []).append(h - l)
medie = {h: sum(v) / len(v) for h, v in per_ora.items() if len(v) >= 8}
top = sorted(medie.items(), key=lambda x: -x[1])[:4]; calme = sorted(medie.items(), key=lambda x: x[1])[:3]
def sessione(giorno, a, b):
    bs = [x for x in orarie if x[0].astimezone(ROMA).date() == giorno and a <= x[0].astimezone(ROMA).hour < b]
    return None if not bs else dict(massimo=r0(max(x[2] for x in bs)), minimo=r0(min(x[3] for x in bs)), ampiezza=r0(max(x[2] for x in bs) - min(x[3] for x in bs)))
g = piena[0].date()
mappa = {'Asia (1:00–9:00)': sessione(g, 1, 9), 'Londra (9:00–15:00)': sessione(g, 9, 15), 'New York (15:00–22:00)': sessione(g, 15, 22)}
# tabella dei lotti: rischio 1% con stop = 0,5 / 1 / 1,5 ATR (oro: 1 lotto = 100 once)
lotti = {}
for conto in (5000, 10000):
    lotti[str(conto)] = {f'{k} ATR': dict(stop_dollari=r0(atr * k), lotti=round((conto * 0.01) / (atr * k * 100), 3)) for k in (0.5, 1, 1.5)}
max52, min52 = max(b[2] for b in oro[-252:]), min(b[3] for b in oro[-252:])
print(json.dumps(dict(
    data=str(oggi), prezzo=r0(prezzo), ultima_seduta_piena=dict(data=str(piena[0].date()), massimo=r0(H), minimo=r0(L), chiusura=r0(C), ampiezza=r0(H - L)),
    pivot_giornalieri={k: r0(v) for k, v in piv.items()}, settimana_precedente={k: r0(v) for k, v in pw.items()} if pw else None,
    settimana_in_corso=dict(massimo=r0(max(x[2] for x in corr_w)), minimo=r0(min(x[3] for x in corr_w)), apertura=r0(corr_w[0][1])),
    bollinger_20_2=dict(superiore=r0(bb_su), inferiore=r0(bb_giu), larghezza_pct=r0((bb_su - bb_giu) / m20 * 100, 1), pos_pct=r0((prezzo - bb_giu) / (bb_su - bb_giu) * 100, 0)),
    distanza_medie=dict(m20=dict(valore=r0(m20), pct=r0((prezzo / m20 - 1) * 100, 2)), m50=dict(valore=r0(m50), pct=r0((prezzo / m50 - 1) * 100, 2)), m200=dict(valore=r0(m200), pct=r0((prezzo / m200 - 1) * 100, 2))),
    atr_14=r0(atr), atr_pct=r0(atr / prezzo * 100, 2), serie_chiusure=dict(numero=serie, verso='rialzo' if verso > 0 else 'ribasso'),
    distanza_52_settimane=dict(dal_massimo_pct=r0((prezzo / max52 - 1) * 100, 1), dal_minimo_pct=r0((prezzo / min52 - 1) * 100, 1)),
    correlazione_20_sedute=cor, ore_piu_mosse_italia=[dict(ora=f'{h}:00', ampiezza_media=r0(v)) for h, v in top], ore_piu_calme_italia=[dict(ora=f'{h}:00', ampiezza_media=r0(v)) for h, v in calme],
    mappa_sessioni=mappa, lotti_rischio_1pct=lotti), ensure_ascii=False, indent=1))
