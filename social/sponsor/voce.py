# Voce del reel sponsor (Marco di ElevenLabs): una traccia per scena + tempi delle parole in parole.json
import certifi; certifi.where = lambda: "/root/.ccr/ca-bundle.crt"
# uso: ELEVEN_API_KEY e ELEVEN_VOCE nell'ambiente (chiave senza spazi); python3 social/sponsor/voce.py [prodotti|news|calc|journal]
import os, sys, json, subprocess
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', '..', 'marketing'))
os.environ.setdefault('SSL_CERT_FILE', '/root/.ccr/ca-bundle.crt')
import voce_eleven
FF = subprocess.check_output([sys.executable, '-c', 'import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())']).decode().strip()
VAR = sys.argv[1] if len(sys.argv) > 1 else 'prodotti'
SCENE = json.load(open(os.path.join(QUI, 'varianti.json')))[VAR]
os.makedirs(os.path.join(QUI, 'voce'), exist_ok=True)
for i, t in enumerate(SCENE):
    out = os.path.join(QUI, 'voce', f'{VAR}-s{i+1}.mp3')
    if os.path.exists(out): continue
    try: voce_eleven.sintetizza(t, out, FF)
    except Exception as e:
        print('ElevenLabs non disponibile, voce di riserva:', str(e)[:60])
        import certifi, asyncio, edge_tts
        certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
        asyncio.run(edge_tts.Communicate(t, 'it-IT-GiuseppeMultilingualNeural', rate='+4%').save(out))
from faster_whisper import WhisperModel
m = WhisperModel('small', compute_type='int8'); res = []
for i, t in enumerate(SCENE):
    seg, _ = m.transcribe(os.path.join(QUI, 'voce', f'{VAR}-s{i+1}.mp3'), language='it', word_timestamps=True)
    tempi = [w.start for x in seg for w in x.words]; par = t.split()
    res.append([[round(tempi[min(len(tempi)-1, round(k*len(tempi)/len(par)))], 2), p] for k, p in enumerate(par)])
json.dump(res, open(os.path.join(QUI, f'parole-{VAR}.json'), 'w'), ensure_ascii=False)
print('ok', [len(x) for x in res])
