# Trova i pezzi in cui la voce multilingue "cambia lingua": per ogni frase pronunciata (segmenti di faster-whisper)
# rileva la lingua sull'audio di quel pezzo, senza forzare l'italiano. uso: python3 verifica_lingua.py [soglia]
import build, sys, json
from faster_whisper import WhisperModel, decode_audio
SOGLIA = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6
L = build.carica(); w = WhisperModel('small', device='cpu', compute_type='int8'); sosp = []
for li, si, pj, t, k in build.tutti_i_passi(L):
    f = build.fname(t); audio = decode_audio(f, sampling_rate=16000)
    # finestre di 2,5 s ogni 1,25 s: un cambio di lingua di poche parole non si perde dentro una frase lunga
    W, P = int(2.5 * 16000), int(1.25 * 16000)
    for a in range(0, max(1, len(audio) - W + 1), P):
        pezzo = audio[a:a + W]
        lingua, prob, tutte = w.detect_language(pezzo)
        p_it = dict(tutte).get('it', 0)
        if lingua != 'it' or p_it < SOGLIA:
            segs, _ = w.transcribe(pezzo, language='it', beam_size=1); tx = ' '.join(x.text.strip() for x in segs)
            sosp.append(dict(lez=L[li]['id'], slide=si, passo=pj, sec=round(a / 16000, 1), lingua=lingua, p_it=round(p_it, 2), testo=tx))
            print(L[li]['id'], si, pj, f'{a/16000:.1f}s', lingua, round(p_it, 2), '|', tx[:100])
json.dump(sosp, open('out/verifica_lingua.json', 'w'), ensure_ascii=False, indent=1)
print('pezzi sospetti:', len(sosp))
