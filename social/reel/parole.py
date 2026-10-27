# Tempi delle parole per i sottotitoli dei reel: trascrivo ogni traccia con faster-whisper (tempi per parola)
# e li riporto sulle parole del testo originale (così numeri e accenti restano quelli scritti).
# uso: python3 social/reel/parole.py r01  → social/reel/r01-parole.json
import json, os, sys
from faster_whisper import WhisperModel
QUI = os.path.dirname(os.path.abspath(__file__))
YT = os.path.join(QUI, '..', 'youtube')
vid = sys.argv[1]
spec = json.load(open(os.path.join(YT, vid + '.json')))
m = WhisperModel('small', compute_type='int8')
out = []
for i, s in enumerate(spec['scene']):
    seg, _ = m.transcribe(os.path.join(YT, 'voce', f'{vid}-{i+1:02d}.mp3'), language='it', word_timestamps=True)
    tempi = [(w.start, w.end) for x in seg for w in x.words]
    parole = s['voce'].split()
    if not tempi:
        out.append([]); continue
    # la parola k del testo prende il tempo della parola proporzionale nella trascrizione
    righe = []
    for k, p in enumerate(parole):
        a = tempi[min(len(tempi) - 1, round(k * len(tempi) / len(parole)))][0]
        righe.append([round(a, 2), p])
    out.append(righe)
json.dump(out, open(os.path.join(QUI, vid + '-parole.json'), 'w'), ensure_ascii=False)
print('ok', [len(x) for x in out])
