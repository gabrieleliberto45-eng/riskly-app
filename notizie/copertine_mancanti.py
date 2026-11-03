# Prima di ogni deploy del sito news: le copertine usate dagli articoli (public.notizie) devono essere nella cartella,
# altrimenti il deploy le cancella dal sito (3 novembre 2026: è successo con la copertina del JOLTS).
# Scarica da news.riskly.trade quelle che mancano e stampa quelle che non trova da nessuna parte.
# uso: python3 notizie/copertine_mancanti.py   (chiave Supabase: file scratchpad/supabase_key o SUPABASE_ACCESS_TOKEN)
import json, os, urllib.request
QUI = os.path.dirname(os.path.abspath(__file__)); DIR = os.path.join(QUI, '..', 'nuovo', 'news')
k = ''
for f in ['/tmp/claude-0/-home-user-riskly-app/828ac661-4dae-5bef-b009-53b6d39ce38e/scratchpad/supabase_key']:
    if os.path.exists(f): k = open(f).read().strip()
k = k or os.environ.get('SUPABASE_ACCESS_TOKEN', '').replace(' ', '')
req = urllib.request.Request('https://api.supabase.com/v1/projects/swlztverwfgdgchgpudt/database/query',
    data=json.dumps({'query': "select copertina from public.notizie where copertina like '/copertine/%'"}).encode(),
    headers={'Authorization': 'Bearer ' + k, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
mancano = 0
for r in json.load(urllib.request.urlopen(req)):
    p = os.path.join(DIR, r['copertina'].lstrip('/'))
    if os.path.exists(p): continue
    try:
        dati = urllib.request.urlopen(urllib.request.Request('https://news.riskly.trade' + r['copertina'], headers={'User-Agent': 'Mozilla/5.0'})).read()
        open(p, 'wb').write(dati); print('scaricata', r['copertina'])
    except Exception as e:
        mancano += 1; print('MANCA', r['copertina'], e)
print('copertine mancanti:', mancano)
