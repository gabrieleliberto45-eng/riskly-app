# Carica una copertina nell'archivio pubblico "copertine" di Supabase e stampa l'indirizzo da mettere nel campo copertina dell'articolo.
# Dal 10 novembre 2026: niente più deploy Netlify per ogni copertina (i deploy consumavano i crediti Netlify).
# uso: python3 notizie/carica_copertina.py ID [file.jpg]   (file predefinito: nuovo/news/copertine/ID.jpg)
# Serve SUPABASE_ACCESS_TOKEN nell'ambiente. Il codice di caricamento sta nella tabella privata config_interna e si legge al volo (mai stampato).
import base64, json, os, sys, urllib.request
REF = 'swlztverwfgdgchgpudt'
ID = sys.argv[1]
QUI = os.path.dirname(os.path.abspath(__file__))
FILE = sys.argv[2] if len(sys.argv) > 2 else os.path.join(QUI, '..', 'nuovo', 'news', 'copertine', ID + '.jpg')
tok = os.environ['SUPABASE_ACCESS_TOKEN'].replace(' ', '')
def post(url, corpo, h):
    r = urllib.request.Request(url, data=json.dumps(corpo).encode(), headers=dict({'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}, **h))
    return json.load(urllib.request.urlopen(r, timeout=90))
t = post(f'https://api.supabase.com/v1/projects/{REF}/database/query', {'query': "select valore from public.config_interna where chiave='token_copertine'"}, {'Authorization': 'Bearer ' + tok})[0]['valore']
r = post(f'https://{REF}.supabase.co/functions/v1/copertina-carica', {'id': ID, 'jpg': base64.b64encode(open(FILE, 'rb').read()).decode()}, {'x-token': t})
print(r['url'])
