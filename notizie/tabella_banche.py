# Tabella delle stime delle banche per UN dato (Gabriele, 25/11: "mettere in colonna le stime delle banche divise per PIL, PCE, eccetera, non tutto mischiato").
# Crea un'immagine 1600×(altezza dinamica) nella paletta del sito e la carica nell'archivio delle copertine; stampa la riga "GRAFICO|url|didascalia" per il corpo.
# Una tabella per ogni dato (PCE, PIL, CPI...). Solo cifre verificate; dove una banca non ha pubblicato quel numero: "—".
# uso: python3 notizie/tabella_banche.py ID NOME spec.json
#   spec.json: {"titolo": "...", "sotto": "...", "colonne": ["Banca","Core, mese","Core, anno"], "righe": [["Goldman Sachs","+0,30%","3,24%"], ...], "evidenzia": [0], "nota": "Fonti: ..."}
#   "evidenzia" = indici delle righe in neretto/fondo oro chiaro (es. il consenso)
import json, os, subprocess, sys, textwrap
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
CARTA, BLU, ORO, GRIGIO, LINEA, ORO_CHIARO = '#F6F6F3', '#12263F', '#D4AE5A', '#8A8F94', '#D9D9D3', '#F1E6C8'
QUI = os.path.dirname(os.path.abspath(__file__)); COP = os.path.join(QUI, '..', 'nuovo', 'news', 'copertine')
ID, NOME, SPEC = sys.argv[1:4]; S = json.load(open(SPEC))
col, rig = S['colonne'], S['righe']; ev = set(S.get('evidenzia', []))
NOTA = textwrap.fill(S.get('nota', ''), 150) if S.get('nota') else ''
H = 1.9 + 0.62 * (len(rig) + 1) + (0.3 + 0.3 * NOTA.count(chr(10)) + 0.3 if NOTA else 0)
f = plt.figure(figsize=(16, H), dpi=100); f.patch.set_facecolor(CARTA)
a = f.add_axes([0, 0, 1, 1]); a.set_xlim(0, 16); a.set_ylim(0, H); a.axis('off')
a.text(.55, H - .62, S['titolo'], fontsize=27, fontweight='bold', color=BLU, va='center')
a.text(.55, H - 1.18, S.get('sotto', ''), fontsize=15, color=GRIGIO, va='center')
w0 = 5.6; n = len(col) - 1; wc = (15.45 - .55 - w0) / n; y = H - 1.9
xs = [.55] + [.55 + w0 + wc * (i + .5) for i in range(n)]
a.plot([.55, 15.45], [y + .3, y + .3], color=BLU, lw=2.2)
a.text(xs[0], y, col[0], fontsize=15, fontweight='bold', color=BLU, va='center')
for i in range(n): a.text(xs[i + 1], y, col[i + 1], fontsize=15, fontweight='bold', color=BLU, va='center', ha='center')
y -= .62
for k, r in enumerate(rig):
    if k in ev: a.add_patch(plt.Rectangle((.45, y - .29), 15.1, .58, color=ORO_CHIARO, lw=0))
    a.text(xs[0], y, r[0], fontsize=16, fontweight='bold' if k in ev else 'normal', color=BLU, va='center')
    for i in range(n):
        v = r[i + 1]; a.text(xs[i + 1], y, v, fontsize=17, fontweight='bold' if k in ev else 'normal', color=GRIGIO if v.strip() in ('—', '-') else BLU, va='center', ha='center')
    a.plot([.55, 15.45], [y - .31, y - .31], color=LINEA, lw=1)
    y -= .62
if NOTA: a.text(.55, .25 + .3 * NOTA.count(chr(10)) / 2 + .05, NOTA, fontsize=12.5, color=GRIGIO, va='center', linespacing=1.5)
pass
out = os.path.join(COP, f'{ID}-{NOME}.jpg'); f.savefig(out, facecolor=CARTA, pil_kwargs={'quality': 90}); plt.close(f)
o = subprocess.run([sys.executable, os.path.join(QUI, 'carica_copertina.py'), f'{ID}-{NOME}'], capture_output=True, text=True)
url = [l for l in o.stdout.split() if l.startswith('https://')][-1]
print(f"GRAFICO|{url}|{S['titolo']}: {S.get('sotto', '')}")
