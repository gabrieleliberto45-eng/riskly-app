# Tempi delle parole del video lungo (per animato.html): python3 social/youtube/parole.py vNN → social/youtube/parole-vNN.json
# Usa le voci già fatte (voce/vNN-01.mp3 …) e il testo "voce" di ogni scena; i tempi vengono da faster-whisper.
import os, sys, json
QUI = os.path.dirname(os.path.abspath(__file__)); ID = sys.argv[1]
os.environ.setdefault('SSL_CERT_FILE', '/root/.ccr/ca-bundle.crt')
spec = json.load(open(os.path.join(QUI, ID + '.json')))
from faster_whisper import WhisperModel
m = WhisperModel('small', compute_type='int8'); res = []
for i, s in enumerate(spec['scene']):
    seg, _ = m.transcribe(os.path.join(QUI, 'voce', f'{ID}-{i+1:02d}.mp3'), language='it', word_timestamps=True)
    tempi = [w.start for x in seg for w in x.words]; par = s['voce'].split()
    res.append([[round(tempi[min(len(tempi) - 1, round(k * len(tempi) / len(par)))], 2), p] for k, p in enumerate(par)] if tempi else [])
json.dump(res, open(os.path.join(QUI, f'parole-{ID}.json'), 'w'), ensure_ascii=False)
print('ok', [len(x) for x in res])
