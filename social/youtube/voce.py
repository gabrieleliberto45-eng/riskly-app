# Voce dei video lunghi YouTube (edge-tts, stessa voce dei reel)
# uso: python3 voce.py v01  → voce/v01-NN.mp3 (una traccia per scena)
import certifi, json, asyncio, sys, os
if os.path.exists('/root/.ccr/ca-bundle.crt'): certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts, re
# pronuncia delle sigle (verificata trascrivendo l'audio); vale solo per la voce
PRONUNCIA = {'CPI': 'ci-pi-ài', 'PPI': 'P P I', 'PCE': 'P C E', 'CME': 'C M E', 'NFP': 'N F P', 'PMI': 'P M I', 'BoJ': 'Banca del Giappone', 'BoE': "Banca d'Inghilterra", 'CFTC': 'C F T C', 'WTI': 'W T I', 'NYMEX': 'Naimex'}
def pronuncia(t):
    for k, v in PRONUNCIA.items(): t = re.sub(r'\b' + re.escape(k) + r'\b', v, t)
    return t
QUI = os.path.dirname(os.path.abspath(__file__))
async def main(vid):
    spec = json.load(open(os.path.join(QUI, vid + '.json')))
    for i, s in enumerate(spec['scene']):
        out = os.path.join(QUI, 'voce', f'{vid}-{i+1:02d}.mp3')
        if os.path.exists(out): continue
        c = edge_tts.Communicate(pronuncia(s['voce']), 'it-IT-GiuseppeMultilingualNeural', rate='+0%')
        await c.save(out)
        print(out)
asyncio.run(main(sys.argv[1]))
