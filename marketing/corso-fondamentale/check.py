# Controlla ogni slide: numero di passaggi voce vs elementi (k espliciti o automatici). uso: python3 check.py
import build
L = build.carica(); bad = 0
for l in L:
    for si, s in enumerate(l['slide']):
        n = build.n_el(s); v = s['voce']; k = s.get('k')
        if k:
            ok = len(k) == len(v) and k[-1] == n and all(k[i] <= k[i+1] for i in range(len(k)-1))
            if not ok: print(l['id'], si, s.get('titolo') or s['tipo'], 'k/voce', len(k), len(v), 'n', n, k); bad += 1
        elif n and len(v) not in (n, n + 1):
            print(l['id'], si, s.get('titolo') or s['tipo'], 'voce', len(v), 'n', n); bad += 1
print('problemi:', bad)
