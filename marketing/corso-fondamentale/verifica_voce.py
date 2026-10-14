# Verifica della voce: trascrive ogni traccia (faster-whisper, modello small) e la confronta con il testo.
# uso: python3 verifica_voce.py  → stampa i passaggi con somiglianza più bassa e scrive out/verifica_voce.json
import build, difflib, json, re, os
from faster_whisper import WhisperModel
L = build.carica(); w = WhisperModel('small', device='cpu', compute_type='int8')
norm = lambda s: re.sub(r'[^a-zàèéìòù0-9 ]', ' ', s.lower()).split()
ris = []
for li, si, pj, t, k in build.tutti_i_passi(L):
    f = build.fname(t); segs, _ = w.transcribe(f, language='it', beam_size=1)
    tr = ' '.join(s.text.strip() for s in segs)
    a, b = norm(build.testo_tts(t)), norm(tr)
    ris.append(dict(lez=L[li]['id'], slide=si, passo=pj, sim=round(difflib.SequenceMatcher(None, a, b).ratio(), 3), testo=build.testo_tts(t), sentito=tr))
os.makedirs('out', exist_ok=True); json.dump(ris, open('out/verifica_voce.json', 'w'), ensure_ascii=False, indent=1)
ris.sort(key=lambda r: r['sim'])
print('media', round(sum(r['sim'] for r in ris) / len(ris), 3))
for r in ris[:12]: print(r['lez'], r['slide'], r['passo'], r['sim'], '\n  T:', r['testo'][:300], '\n  S:', r['sentito'][:300])
