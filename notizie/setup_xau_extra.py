# Scheda operativa dell'oro per il Setup XAU (11 novembre 2026, richiesta di Gabriele: cose concrete, niente tecnicismi inutili).
# Solo fatti calcolati dai prezzi: pivot, livelli e zone di confluenza (dove più livelli coincidono = zone di possibile inversione), ore più mosse, mappa delle sessioni,
# calendario dei dati USA di oggi e della settimana (ora italiana), tabella dei lotti. Niente Bollinger.
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
# --- zone di confluenza: livelli di fonti diverse che cadono entro ~0,15 ATR = zone dove il prezzo ha più motivi per reagire ---
liv = []
for k, v in piv.items(): liv.append((v, f'pivot giornaliero {k}'))
if pw:
    for k in ('P', 'R1', 'S1'): liv.append((pw[k], f'pivot settimanale {k}'))
    liv += [(pw['massimo'], 'massimo della settimana scorsa'), (pw['minimo'], 'minimo della settimana scorsa')]
liv += [(H, 'massimo dell\'ultima seduta'), (L, 'minimo dell\'ultima seduta'), (max(x[2] for x in corr_w), 'massimo della settimana'), (min(x[3] for x in corr_w), 'minimo della settimana')]
base = int(prezzo // 50) * 50
for k in range(-4, 6): liv.append((base + 50 * k, f'numero tondo {base + 50 * k}'))
ultimi = oro[-90:]
for i in range(3, len(ultimi) - 3):
    if ultimi[i][2] == max(x[2] for x in ultimi[i - 3:i + 4]): liv.append((ultimi[i][2], f'massimo del {ultimi[i][0].day}/{ultimi[i][0].month}'))
    if ultimi[i][3] == min(x[3] for x in ultimi[i - 3:i + 4]): liv.append((ultimi[i][3], f'minimo del {ultimi[i][0].day}/{ultimi[i][0].month}'))
liv = sorted([x for x in liv if abs(x[0] - prezzo) <= 3 * atr])
zone = []; cur = []
for x in liv:
    if cur and x[0] - cur[-1][0] > 0.15 * atr: zone.append(cur); cur = []
    cur.append(x)
if cur: zone.append(cur)
zone_conf = []
for z in zone:
    if len({n.split(' ')[0] + n.split(' ')[1] if n.startswith('pivot') else n for _, n in z}) >= 2:
        zone_conf.append(dict(da=r0(min(v for v, _ in z)), a=r0(max(v for v, _ in z)), livelli=sorted({n for _, n in z}), peso=len(z), distanza=r0(sum(v for v, _ in z) / len(z) - prezzo), posizione='sopra il prezzo' if sum(v for v, _ in z) / len(z) > prezzo else 'sotto il prezzo'))
zone_conf.sort(key=lambda z: abs(z['distanza']))
# --- calendario dei dati USA (ora italiana): oggi e resto della settimana ---
eventi = []
try:
    lun = lunedi(adesso.date()); da = dt.datetime.combine(adesso.date(), dt.time(0), tzinfo=dt.timezone.utc); a_ = dt.datetime.combine(lun + dt.timedelta(days=5), dt.time(0), tzinfo=dt.timezone.utc)
    u = f"https://economic-calendar.tradingview.com/events?from={da.strftime('%Y-%m-%dT%H:%M:%S.000Z')}&to={a_.strftime('%Y-%m-%dT%H:%M:%S.000Z')}&countries=US"
    for e in json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Origin': 'https://www.tradingview.com', 'User-Agent': 'Mozilla/5.0'}), timeout=30))['result']:
        if e.get('importance', 0) >= 1 or any(k in e['title'] for k in ('Fed ', 'FOMC', 'Powell', 'Warsh', 'Initial Jobless')):
            t = dt.datetime.fromisoformat(e['date'].replace('Z', '+00:00')).astimezone(ROMA)
            eventi.append(dict(quando=t.strftime('%a %d/%m %H:%M'), evento=e['title'], atteso=e.get('forecast'), precedente=e.get('previous')))
except Exception as ex:
    eventi = [dict(errore=str(ex)[:80])]
print(json.dumps(dict(
    data=str(oggi), ora_italia=adesso.astimezone(ROMA).strftime('%H:%M'), prezzo=r0(prezzo), ultima_seduta_piena=dict(data=str(piena[0].date()), massimo=r0(H), minimo=r0(L), chiusura=r0(C), ampiezza=r0(H - L)),
    pivot_giornalieri={k: r0(v) for k, v in piv.items()}, settimana_precedente={k: r0(v) for k, v in pw.items()} if pw else None,
    settimana_in_corso=dict(massimo=r0(max(x[2] for x in corr_w)), minimo=r0(min(x[3] for x in corr_w)), apertura=r0(corr_w[0][1])),
    zone_di_confluenza=zone_conf[:8], medie=dict(m20=r0(m20), m50=r0(m50), m200=r0(m200)), atr_14=r0(atr), distanza_52_settimane=dict(dal_massimo_pct=r0((prezzo / max52 - 1) * 100, 1), dal_minimo_pct=r0((prezzo / min52 - 1) * 100, 1)),
    correlazione_20_sedute=cor, ore_piu_mosse_italia=[dict(ora=f'{h}:00', ampiezza_media=r0(v)) for h, v in top], ore_piu_calme_italia=[dict(ora=f'{h}:00', ampiezza_media=r0(v)) for h, v in calme],
    mappa_sessioni=mappa, dati_usa_oggi_e_settimana=eventi, lotti_rischio_1pct=lotti), ensure_ascii=False, indent=1))
