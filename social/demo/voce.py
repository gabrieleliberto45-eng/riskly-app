# Voce dei reel prodotto in formato demo (edge-tts, it-IT-GiuseppeMultilingualNeural) + tempi delle parole
# uso: python3 voce.py p02 [p05 ...]  → voce/pNN.mp3 e voce/pNN.json
import certifi, json, asyncio, sys, os
if os.path.exists('/root/.ccr/ca-bundle.crt'): certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts
TESTI = json.load(open('testi.json'))
async def una(id_):
    c = edge_tts.Communicate(TESTI[id_], 'it-IT-GiuseppeMultilingualNeural', rate='-2%', boundary='WordBoundary')
    parole = []
    with open(f'voce/{id_}.mp3', 'wb') as f:
        async for ch in c.stream():
            if ch['type'] == 'audio': f.write(ch['data'])
            elif ch['type'] == 'WordBoundary':
                parole.append([round(ch['offset']/1e7, 3), round((ch['offset']+ch['duration'])/1e7, 3), ch['text']])
    json.dump(parole, open(f'voce/{id_}.json', 'w'), ensure_ascii=False)
    print(id_, round(parole[-1][1], 1), 's')
async def main():
    for i in (sys.argv[1:] or TESTI.keys()): await una(i)
asyncio.run(main())
