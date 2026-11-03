# Copertina illustrata di Riskly News (Gabriele, 3 novembre 2026): una scena disegnata per argomento, titolo e numero chiave.
# Niente persone reali e niente foto inventate.
# uso: python3 notizie/illustra.py ID SCENA CATEGORIA "TITOLO" ["NUMERO"] [uscita.jpg]
# SCENE: fed, bce, lingotti, setup (candele), petroliera, fabbrica, calendario, capitol, dollaro, lavoro, inflazione, borsa
#   oro → lingotti · Setup XAU → setup · Fed e tassi USA → fed · BCE → bce · petrolio, Iran, Hormuz → petroliera
#   ISM, industria → fabbrica · payrolls, JOLTS, sussidi → lavoro · CPI, PCE, PPI → inflazione
#   elezioni, Congresso, Casa Bianca → capitol · dollaro → dollaro · Borsa, indici → borsa · la settimana → calendario
import json, os, subprocess, sys
QUI = os.path.dirname(os.path.abspath(__file__))
ID, SCENA, CAT, TIT = sys.argv[1:5]
NUM = sys.argv[5] if len(sys.argv) > 5 else ''
OUT = sys.argv[6] if len(sys.argv) > 6 else os.path.join(QUI, '..', 'nuovo', 'news', 'copertine', ID + '.jpg')
COLORE = {'Straordinarie': '#C62F3B', 'Dato appena uscito': '#C62F3B', 'Fed': '#1D4FC4', 'Tassi e banche centrali': '#1D4FC4', 'Dollaro': '#0F8A4F'}.get(CAT, '')
dati = dict(scena=SCENA, categoria=CAT, titolo=TIT, numero=NUM, colore=COLORE)
js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 1600, height: 900 }} }});
  await p.goto('file://{QUI}/illustrazione.html'); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(d => window.disegna(d), {json.dumps(dati)}); await p.waitForTimeout(150);
  await p.screenshot({{ path: {json.dumps(OUT)}, type: 'jpeg', quality: 86 }}); await b.close(); }})();"""
os.makedirs(os.path.dirname(OUT), exist_ok=True)
subprocess.run(['node', '-e', js], check=True, env=dict(os.environ, NODE_PATH='/opt/node22/lib/node_modules'))
print(OUT)
