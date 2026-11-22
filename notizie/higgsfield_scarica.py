# Scarica un'immagine creata con Higgsfield e la segna nel registro dei crediti (budget 100/mese, Gabriele 22/11).
# uso: python3 notizie/higgsfield_scarica.py ID URL USCITA.jpg [crediti=0.75]  → stampa il percorso e i crediti usati nel mese
import datetime as dt, io, json, os, sys, urllib.request
from PIL import Image
ID, URL, OUT = sys.argv[1:4]; CR = float(sys.argv[4]) if len(sys.argv) > 4 else .75
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read())).convert('RGB').save(OUT, quality=88)
reg = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'higgsfield_registro.json'); R = json.load(open(reg)) if os.path.exists(reg) else []
if not any(x.get('src') == URL for x in R): R.append({'data': dt.date.today().isoformat(), 'id': ID, 'src': URL, 'crediti': CR})
json.dump(R, open(reg, 'w'), ensure_ascii=False, indent=0)
m = dt.date.today().strftime('%Y-%m'); print(OUT); print(f"crediti Higgsfield usati questo mese: {sum(x['crediti'] for x in R if x['data'].startswith(m)):.2f} / 100")
