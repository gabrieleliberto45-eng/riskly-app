# Copertina di un articolo di Riskly News: python3 notizie/copertina.py ID CATEGORIA "TITOLO" [uscita.jpg]
# Disegna categoria, titolo e il grafico degli ultimi 3 mesi dell'attivo legato al tema (oro, dollaro o rendimento del decennale USA).
# La copertina del Setup XAU invece è il grafico di notizie/setup_xau.py.
import json, os, subprocess, sys, urllib.request
QUI = os.path.dirname(os.path.abspath(__file__))
ID, CAT, TIT = sys.argv[1:4]
OUT = sys.argv[4] if len(sys.argv) > 4 else os.path.join(QUI, '..', 'nuovo', 'news', 'copertine', ID + '.jpg')
TEMA = {  # categoria: (etichetta, colore, simbolo Yahoo, nome dell'ultimo valore, formato)
  'oro': ('Oro', '#F2B83A', 'GC=F', 'ORO', '{:,.0f} $'),
  'dollaro': ('Dollaro', '#2BD98B', 'DX-Y.NYB', 'INDICE DEL DOLLARO', '{:,.2f}'),
  'fed': ('Fed', '#7FA5FF', '%5ETNX', 'TREASURY 10 ANNI', '{:,.2f}%'),
  'tassi': ('Tassi e banche centrali', '#7FA5FF', '%5ETNX', 'TREASURY 10 ANNI', '{:,.2f}%'),
  'straordinarie': ('Straordinarie', '#FF4D5E', 'GC=F', 'ORO', '{:,.0f} $'),
  'settimana': ('La settimana', '#F2B83A', 'GC=F', 'ORO', '{:,.0f} $'),
}
et, col, sim, nome, fmt = TEMA.get(CAT, TEMA['oro'])
url = f'https://query1.finance.yahoo.com/v8/finance/chart/{sim}?range=3mo&interval=1d'
r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))['chart']['result'][0]
serie = [c for c in r['indicators']['quote'][0]['close'] if c is not None]
ultimo = fmt.format(serie[-1]).replace(',', 'X').replace('.', ',').replace('X', '.')
dati = dict(etichetta=et, colore=col, titolo=TIT, serie=serie, nome=nome, ultimo=ultimo)
js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 1600, height: 900 }} }});
  await p.goto('file://{QUI}/copertina.html'); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(d => window.disegna(d), {json.dumps(dati)}); await p.waitForTimeout(200);
  await p.screenshot({{ path: {json.dumps(OUT)}, type: 'jpeg', quality: 86 }}); await b.close(); }})();"""
os.makedirs(os.path.dirname(OUT), exist_ok=True)
subprocess.run(['node', '-e', js], check=True, env=dict(os.environ, NODE_PATH='/opt/node22/lib/node_modules'))
print(OUT)
