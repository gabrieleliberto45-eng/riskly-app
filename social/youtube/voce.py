# Voce dei video YouTube (lunghi e Shorts)
# Dal 24 ottobre 2026: George di ElevenLabs con l'effetto stanza, come i corsi (scelta di Gabriele, "bellissima").
# Serve la chiave in ELEVEN_API_KEY (mai nel repository); senza chiave, o se ElevenLabs rifiuta (crediti finiti),
# usa la voce di prima (edge-tts, Giuseppe) e lo scrive.
# uso: ELEVEN_API_KEY=... python3 voce.py v01  → voce/v01-NN.mp3 (una traccia per scena)
import certifi, json, asyncio, sys, os, subprocess
if os.path.exists('/root/.ccr/ca-bundle.crt'): certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts, re
# pronuncia delle sigle (verificata trascrivendo l'audio); vale solo per la voce
PRONUNCIA = {'CPI': 'ci-pi-ài', 'PPI': 'P P I', 'PCE': 'P C E', 'CME': 'C M E', 'NFP': 'N F P', 'PMI': 'P M I', 'BoJ': 'Banca del Giappone', 'BoE': "Banca d'Inghilterra", 'CFTC': 'C F T C', 'WTI': 'W T I', 'NYMEX': 'Naimex', 'Hormuz': 'Ormùz'}
def pronuncia(t):
    for k, v in PRONUNCIA.items(): t = re.sub(r'\b' + re.escape(k) + r'\b', v, t)
    return t
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', '..', 'marketing'))
import voce_eleven
FF = subprocess.check_output([sys.executable, '-c', 'import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())']).decode().strip()
async def main(vid):
    spec = json.load(open(os.path.join(QUI, vid + '.json')))
    george = bool(os.environ.get('ELEVEN_API_KEY'))
    if not george: print('ATTENZIONE: manca ELEVEN_API_KEY, uso la voce di riserva (Giuseppe)')
    else:
        # niente video con due voci: se i crediti non bastano per tutto, tutto con la voce di riserva
        servono = sum(len(pronuncia(s['voce'])) for i, s in enumerate(spec['scene']) if not os.path.exists(os.path.join(QUI, 'voce', f'{vid}-{i+1:02d}.mp3')))
        try:
            import urllib.request
            r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.elevenlabs.io/v1/user/subscription', headers={'xi-api-key': os.environ['ELEVEN_API_KEY']}), timeout=30))
            restano = r['character_limit'] - r['character_count']
            print(f'ElevenLabs: servono {servono} crediti, ne restano {restano}')
            if restano < servono:
                george = False; print('ATTENZIONE: crediti ElevenLabs insufficienti, uso la voce di riserva (Giuseppe)')
        except Exception as e:
            print('crediti non verificati:', str(e)[:80])
    for i, s in enumerate(spec['scene']):
        out = os.path.join(QUI, 'voce', f'{vid}-{i+1:02d}.mp3')
        if os.path.exists(out): continue
        if george:
            try:
                voce_eleven.sintetizza(pronuncia(s['voce']), out, FF); print(out, 'George'); continue
            except Exception as e:
                george = False; print('ATTENZIONE: ElevenLabs non risponde (' + str(e)[:120] + '), uso la voce di riserva (Giuseppe)')
        if spec.get('pause'):
            await frasi(pronuncia(s['voce']), out)
        else:
            # voce e velocità si possono scegliere nel json ("voce_edge", "velocita"); di base Giuseppe
            c = edge_tts.Communicate(pronuncia(s['voce']), spec.get('voce_edge', 'it-IT-GiuseppeMultilingualNeural'), rate=spec.get('velocita', '+0%'))
            await c.save(out)
        print(out, spec.get('voce_edge', 'Giuseppe'))

# Giuseppe tende a legare le frasi (1° novembre: "Niente previsioni: segna le date" diventava un'altra cosa):
# con "pause": true nel json ogni frase è sintetizzata da sola e unita con un silenzio vero (punto 0,35 s, domanda 0,5 s, due punti 0,3 s)
async def frasi(testo, out):
    pezzi = [p.strip() for p in re.findall(r'[^.?!:]+[.?!:]?', testo) if p.strip()]
    tmp = out + '.parti'; os.makedirs(tmp, exist_ok=True); lista = []
    for i, p in enumerate(pezzi):
        mp3 = os.path.join(tmp, f'{i}.mp3'); wav = os.path.join(tmp, f'{i}.wav')
        await edge_tts.Communicate(p if p[-1] in '.?!' else p.rstrip(':') + '.', 'it-IT-GiuseppeMultilingualNeural', rate='+0%').save(mp3)
        pausa = {'?': 0.5, ':': 0.3}.get(p[-1], 0.35) if i < len(pezzi) - 1 else 0
        subprocess.run([FF, '-y', '-v', 'error', '-i', mp3, '-af', f'silenceremove=start_periods=1:start_threshold=-55dB,areverse,silenceremove=start_periods=1:start_threshold=-65dB,areverse,apad=pad_dur={pausa + 0.08}', '-ar', '24000', '-ac', '1', wav], check=True)
        lista.append(wav)
    open(os.path.join(tmp, 'l.txt'), 'w').write('\n'.join(f"file '{w}'" for w in lista))
    subprocess.run([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(tmp, 'l.txt'), '-b:a', '128k', out], check=True)
    subprocess.run(['rm', '-rf', tmp])
asyncio.run(main(sys.argv[1]))
