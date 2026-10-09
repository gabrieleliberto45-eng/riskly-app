# Voce dei video lunghi YouTube (edge-tts, stessa voce dei reel)
# uso: python3 voce.py v01  → voce/v01-NN.mp3 (una traccia per scena)
import certifi, json, asyncio, sys, os
if os.path.exists('/root/.ccr/ca-bundle.crt'): certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts
QUI = os.path.dirname(os.path.abspath(__file__))
async def main(vid):
    spec = json.load(open(os.path.join(QUI, vid + '.json')))
    for i, s in enumerate(spec['scene']):
        out = os.path.join(QUI, 'voce', f'{vid}-{i+1:02d}.mp3')
        if os.path.exists(out): continue
        c = edge_tts.Communicate(s['voce'], 'it-IT-GiuseppeMultilingualNeural', rate='+0%')
        await c.save(out)
        print(out)
asyncio.run(main(sys.argv[1]))
