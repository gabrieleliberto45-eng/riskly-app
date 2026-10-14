# Trova i pezzi in cui la voce multilingue "cambia lingua": per ogni frase pronunciata (segmenti di faster-whisper)
# rileva la lingua sull'audio di quel pezzo, senza forzare l'italiano. uso: python3 verifica_lingua.py [soglia]
import build, sys, json
from faster_whisper import WhisperModel, decode_audio
SOGLIA = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6
L = build.carica(); w = WhisperModel('small', device='cpu', compute_type='int8'); sosp = []
for li, si, pj, t, k in build.tutti_i_passi(L):
    f = build.fname(t); audio = decode_audio(f, sampling_rate=16000)
    segs, _ = w.transcribe(audio, language='it', beam_size=1)
    for s in segs:
        pezzo = audio[int(s.start * 16000):int(s.end * 16000)]
        if len(pezzo) < 16000 * 0.8: continue
        lingua, prob, tutte = w.detect_language(pezzo)
        p_it = dict(tutte).get('it', 0)
        if lingua != 'it' or p_it < SOGLIA:
            sosp.append(dict(lez=L[li]['id'], slide=si, passo=pj, lingua=lingua, p_it=round(p_it, 2), testo=s.text.strip()))
            print(L[li]['id'], si, pj, lingua, round(p_it, 2), '|', s.text.strip()[:120])
json.dump(sosp, open('out/verifica_lingua.json', 'w'), ensure_ascii=False, indent=1)
print('pezzi sospetti:', len(sosp))
