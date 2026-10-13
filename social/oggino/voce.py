# Voci di "Oggi no." con Piper (gira in locale, niente servizi esterni):
#   robot  = it_IT-riccardo (con effetto metallico)   trader = it_IT-paola
# uso: python3 voce.py [p01-quarta ...]   (modelli in $PIPER_DIR, default ./piper)
# Esce voce/<id>-NN.wav e voce/<id>-NN.json con i tempi stimati di ogni parola [inizio, fine, parola].
import json, os, re, subprocess, sys, wave
Q = os.path.dirname(os.path.abspath(__file__))
M = os.environ.get('PIPER_DIR', os.path.join(Q, 'piper'))
FF = subprocess.run(['python3', '-c', 'import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())'], capture_output=True, text=True).stdout.strip()
VOCI = {
    'robot':  ('it_IT-riccardo-x_low.onnx', '1.08',
               'highpass=f=140,lowpass=f=7200,flanger=delay=1.5:depth=1.2:regen=-30:width=60:speed=0.3,aecho=0.8:0.5:9:0.25,volume=1.6'),
    'trader': ('it_IT-paola-medium.onnx', '0.92', 'highpass=f=90,volume=1.2'),
}

def durata(f):
    with wave.open(f) as w: return w.getnframes() / w.getframerate()

def tempi(testo, tot):
    """tempi stimati: ogni parola pesa quanto le sue lettere, la punteggiatura aggiunge una pausa"""
    parole = testo.split()
    pesi = []
    for p in parole:
        w = len(re.sub(r'[^\wàèéìòù]', '', p)) + 1.5
        pausa = 6 if re.search(r'[.!?]$', p) else (3 if re.search(r'[,:;]$', p) else 0)
        pesi.append((w, pausa))
    totale = sum(w + z for w, z in pesi); t = 0.12; scala = (tot - 0.2) / totale
    out = []
    for p, (w, z) in zip(parole, pesi):
        out.append([round(t, 3), round(t + w * scala, 3), re.sub(r'[^\wàèéìòù%−-]', '', p)]); t += (w + z) * scala
    return out

for ep in json.load(open(os.path.join(Q, 'puntate.json'))):
    if len(sys.argv) > 1 and ep['id'] not in sys.argv[1:]: continue
    for i, s in enumerate(ep['segmenti']):
        base = os.path.join(Q, 'voce', f"{ep['id']}-{i+1:02d}")
        modello, lunghezza, filtro = VOCI[s['chi']]
        grezzo = base + '.grezzo.wav'
        subprocess.run([sys.executable, '-m', 'piper', '-m', os.path.join(M, modello), '--length-scale', lunghezza, '-f', grezzo],
                       input=s['voce'], text=True, check=True, capture_output=True)
        subprocess.run([FF, '-y', '-v', 'error', '-i', grezzo, '-af', filtro, '-ar', '24000', '-ac', '1', base + '.wav'], check=True)
        os.remove(grezzo)
        json.dump(tempi(s['voce'], durata(base + '.wav')), open(base + '.json', 'w'), ensure_ascii=False)
    print(ep['id'])
