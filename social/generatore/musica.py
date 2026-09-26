"""Basi musicali lo-fi originali per i video Riskly (nessun diritto d'autore di terzi).

uso:  python3 social/generatore/musica.py      → crea social/generatore/musica/{a,b,c}.m4a
serve: numpy e ffmpeg (quello di `pip install imageio-ffmpeg` va bene)
"""
import os, subprocess, shutil, tempfile, wave
import numpy as np

SR = 44100
DURATA = 34.0          # più lunga di qualsiasi video: il generatore la taglia con una dissolvenza
CARTELLA = os.path.join(os.path.dirname(__file__), 'musica')

BASI = {
    # nome: (bpm, [(accordo in note MIDI, basso MIDI), ...] un accordo per battuta)
    'a': (84, [((57, 60, 64, 67), 45), ((53, 57, 60, 64), 41), ((48, 52, 55, 59), 36), ((55, 59, 62, 64), 43)]),  # Am7 Fmaj7 Cmaj7 G6
    'b': (90, [((50, 53, 57, 60, 64), 38), ((55, 59, 62, 65), 43), ((48, 52, 55, 59), 36), ((57, 60, 64, 67), 45)]),  # Dm9 G7 Cmaj7 Am7
    'c': (78, [((52, 55, 59, 62), 40), ((48, 52, 55, 59), 36), ((55, 59, 62, 67), 43), ((50, 54, 57, 62), 38)]),  # Em7 Cmaj7 G D
}

rng = np.random.default_rng(7)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
t_tot = np.arange(int(SR * DURATA)) / SR


def liscia(x, n):
    """filtro passa-basso semplice: media mobile di n campioni"""
    return np.convolve(x, np.ones(n) / n, mode='same')


def aggiungi(buf, suono, inizio, pan=0.0):
    i = int(inizio * SR)
    if i >= len(buf):
        return
    s = suono[:len(buf) - i]
    buf[i:i + len(s), 0] += s * (1 - pan) ** .5
    buf[i:i + len(s), 1] += s * (1 + pan) ** .5


def tono(f, dur, armoniche=(1, .35, .12), att=.01, dec=1.0, detune=0.0):
    t = np.arange(int(SR * dur)) / SR
    x = sum(a * np.sin(2 * np.pi * f * (k + 1) * (1 + detune) * t) for k, a in enumerate(armoniche))
    env = np.minimum(t / att, 1) * np.exp(-t / dec)
    return x * env


def cassa(dur=.45):
    t = np.arange(int(SR * dur)) / SR
    f = 45 + 75 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def rullante(dur=.25):
    n = rng.standard_normal(int(SR * dur))
    t = np.arange(len(n)) / SR
    return liscia(n, 6) * np.exp(-t * 22) * .5


def charleston(dur=.06):
    n = rng.standard_normal(int(SR * dur))
    return np.diff(n, prepend=0) * np.exp(-np.arange(len(n)) / SR * 70) * .12


def base(bpm, giro):
    buf = np.zeros((len(t_tot), 2))
    beat = 60 / bpm
    battuta = beat * 4
    n_batt = int(DURATA / battuta) + 1
    swing = beat * .06
    for b in range(n_batt):
        accordo, basso = giro[b % len(giro)]
        t0 = b * battuta
        # pad: accordo lungo, morbido, leggermente allargato in stereo
        for j, m in enumerate(accordo):
            p = tono(hz(m), battuta + .6, armoniche=(1, .18, .05), att=.35, dec=3.5, detune=.0015 * (j % 2 * 2 - 1))
            aggiungi(buf, p * .085, t0, pan=(-.35 if j % 2 else .35))
        # piano elettrico: accordo ribattuto sul 1 e sul "e" del 3
        for colpo in (0, 2.5):
            for m in accordo:
                aggiungi(buf, tono(hz(m + 12), 1.2, armoniche=(1, .25), att=.004, dec=.45) * .07, t0 + colpo * beat + swing)
        # basso sul 1 e sul 3
        for colpo in (0, 2):
            aggiungi(buf, tono(hz(basso), beat * 1.6, armoniche=(1, .2), att=.01, dec=.6) * .15, t0 + colpo * beat)
        # batteria: cassa 1 e 3, rullante 2 e 4, charleston in ottavi con swing
        for colpo in (0, 2):
            aggiungi(buf, cassa() * .32, t0 + colpo * beat)
        aggiungi(buf, cassa() * .18, t0 + 2.5 * beat)
        for colpo in (1, 3):
            aggiungi(buf, rullante(), t0 + colpo * beat, pan=.1)
        for k in range(8):
            aggiungi(buf, charleston() * (1 if k % 2 == 0 else .6), t0 + k * beat / 2 + (swing if k % 2 else 0), pan=-.25)
    # fruscio da vinile, molto basso
    buf += liscia(rng.standard_normal((len(t_tot), 1))[:, 0], 3)[:, None] * .006
    buf = np.tanh(buf * 1.4)                       # saturazione morbida
    return buf / np.max(np.abs(buf)) * .89


def ffmpeg():
    if shutil.which('ffmpeg'):
        return 'ffmpeg'
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


if __name__ == '__main__':
    os.makedirs(CARTELLA, exist_ok=True)
    for nome, (bpm, giro) in BASI.items():
        audio = (base(bpm, giro) * 32767).astype('<i2')
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            wav = f.name
        with wave.open(wav, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(audio.tobytes())
        out = os.path.join(CARTELLA, nome + '.m4a')
        subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'aac', '-b:a', '192k', out], check=True)
        os.remove(wav)
        print(nome, bpm, 'bpm →', out)
