# Volume profile a intervallo fisso per il Setup XAU (Gabriele, 22/11: "volume a intervallo fisso, POC e gli altri due livelli").
# Dati: future sull'oro COMEX (GC=F, Yahoo) a 5 minuti. L'oro spot dei broker non ha volumi veri: si usa solo il future.
# Per ogni intervallo calcola POC (prezzo con più volume), VAH e VAL (bordi della value area, 70% del volume).
# Il volume di ogni candela è distribuito in modo uniforme tra minimo e massimo, a passi di 1 $.
# Intervalli: l'ultima seduta piena (giorno di calendario italiano precedente con scambi) e la settimana precedente (lun–ven).
# uso: python3 notizie/volume_profilo.py  → stampa JSON. Livelli osservati, non segnali.
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
ris['nota'] = ('Fine novembre: il contratto principale passa da dicembre a febbraio; nei giorni del passaggio il contratto continuo di Yahoo '
               'può mescolare i due e falsare un po\' i livelli.') if dt.date(oggi.year, 11, 20) <= oggi <= dt.date(oggi.year, 11, 30) else ''
print(json.dumps(ris, ensure_ascii=False, indent=1))
