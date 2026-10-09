# voce + tempi delle parole per le "Storie di rischio": voce/<id>-NN.mp3 e .json
import certifi, json, asyncio, sys, os
if os.path.exists('/root/.ccr/ca-bundle.crt'): certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts
Q = os.path.dirname(os.path.abspath(__file__))
async def main():
    for st in json.load(open(os.path.join(Q, 'storie.json'))):
        if len(sys.argv) > 1 and st['id'] not in sys.argv[1:]: continue
        solo_ultimo = os.environ.get('SOLO_ULTIMO')
        for i, s in enumerate(st['segmenti']):
            if solo_ultimo and i != len(st['segmenti']) - 1: continue
            base = os.path.join(Q, 'voce', f"{st['id']}-{i+1:02d}")
            c = edge_tts.Communicate(s['voce'], 'it-IT-GiuseppeMultilingualNeural', rate='+6%', pitch='-4Hz', boundary='WordBoundary')
            parole = []
            with open(base + '.mp3', 'wb') as f:
                async for ch in c.stream():
                    if ch['type'] == 'audio': f.write(ch['data'])
                    elif ch['type'] == 'WordBoundary': parole.append([ch['offset'] / 1e7, (ch['offset'] + ch['duration']) / 1e7, ch['text']])
            json.dump(parole, open(base + '.json', 'w'), ensure_ascii=False)
        print(st['id'])
asyncio.run(main())
