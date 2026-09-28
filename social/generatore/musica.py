"""Basi musicali lo-fi originali per i video Riskly (nessun diritto d'autore di terzi).

uso:  python3 social/generatore/musica.py      → crea social/generatore/musica/*.m4a
Stili diversi (lo-fi, trap, deep house, cinematico, pluck) così i video non hanno sempre la stessa base:
il generatore le usa a rotazione, oppure quella indicata con "musica" nel json del video.
serve: numpy e ffmpeg (quello di `pip install imageio-ffmpeg` va bene)
"""
import os, subprocess, shutil, tempfile, wave
import numpy as np

SR = 44100
DURATA = 34.0          # più lunga di qualsiasi video: il generatore la taglia con una dissolvenza
CARTELLA = os.path.join(os.path.dirname(__file__), 'musica')

BASI = {
    # nome: (stile, bpm, [(accordo in note MIDI, basso MIDI), ...] un accordo per battuta)
    'a': ('lofi', 84, [((57, 60, 64, 67), 45), ((53, 57, 60, 64), 41), ((48, 52, 55, 59), 36), ((55, 59, 62, 64), 43)]),  # Am7 Fmaj7 Cmaj7 G6
    'b': ('lofi', 90, [((50, 53, 57, 60, 64), 38), ((55, 59, 62, 65), 43), ((48, 52, 55, 59), 36), ((57, 60, 64, 67), 45)]),  # Dm9 G7 Cmaj7 Am7
    'c': ('lofi', 78, [((52, 55, 59, 62), 40), ((48, 52, 55, 59), 36), ((55, 59, 62, 67), 43), ((50, 54, 57, 62), 38)]),  # Em7 Cmaj7 G D
    'd': ('trap', 140, [((57, 60, 64), 33), ((53, 57, 60), 29), ((55, 59, 62), 31), ((52, 55, 59), 28)]),  # Am F G Em, 808 basso
    'e': ('trap', 132, [((49, 52, 56), 37), ((45, 49, 52), 33), ((52, 56, 59), 40), ((47, 51, 54), 35)]),  # C#m A E B
    'f': ('house', 122, [((50, 53, 57, 60), 38), ((46, 50, 53, 57), 34), ((48, 52, 55, 58), 36), ((45, 48, 52, 55), 33)]),  # Dm7 Bbmaj7 C7 Am7
    'g': ('house', 118, [((55, 58, 62, 65), 43), ((51, 55, 58, 62), 39), ((53, 57, 60, 63), 41), ((50, 53, 57, 60), 38)]),  # Gm7 Ebmaj7 F7 Dm7
    'h': ('cinema', 96, [((45, 52, 57, 60), 33), ((41, 48, 53, 57), 29), ((48, 55, 60, 64), 36), ((43, 50, 55, 59), 31)]),  # Am F C G, pulsazione
    'i': ('cinema', 104, [((50, 57, 62, 65), 38), ((46, 53, 58, 62), 34), ((43, 50, 55, 58), 31), ((45, 52, 57, 61), 33)]),  # Dm Bb Gm A
    'j': ('pluck', 100, [((60, 64, 67, 71), 48), ((57, 60, 64, 67), 45), ((53, 57, 60, 64), 41), ((55, 59, 62, 65), 43)]),  # Cmaj7 Am7 Fmaj7 G7
    'k': ('pluck', 108, [((62, 65, 69, 72), 50), ((58, 62, 65, 69), 46), ((60, 64, 67, 70), 48), ((57, 60, 64, 67), 45)]),  # Dm7 Bbmaj7 C7 Am7
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


def ottotto(f, dur):
    """basso 808: sinusoide profonda con piccola discesa iniziale"""
    t = np.arange(int(SR * dur)) / SR
    ff = f * (1 + .6 * np.exp(-t * 40))
    return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(ff) / SR)) * np.exp(-t * 1.6) * np.minimum(t / .005, 1)


def pluck(f, dur=.5):
    """corda pizzicata (Karplus-Strong semplificato)"""
    n = int(SR * dur)
    periodo = max(int(SR / f), 2)
    buf = rng.uniform(-1, 1, periodo)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % periodo]
        buf[i % periodo] = .5 * (buf[i % periodo] + buf[(i + 1) % periodo]) * .996
    return out


def clap(dur=.2):
    n = rng.standard_normal(int(SR * dur))
    t = np.arange(len(n)) / SR
    inv = sum(np.exp(-np.maximum(t - d, 0) * 60) * (t >= d) for d in (0, .01, .022))
    return np.diff(n, prepend=0) * inv * .25


def base_stile(stile, bpm, giro):
    """arrangiamenti diversi dallo stile lo-fi"""
    buf = np.zeros((len(t_tot), 2))
    beat = 60 / bpm
    battuta = beat * 4
    n_batt = int(DURATA / battuta) + 1
    for b in range(n_batt):
        accordo, basso = giro[b % len(giro)]
        t0 = b * battuta
        if stile == 'trap':
            # half-time: cassa sull'1, clap sul 3, charleston a sedicesimi con rulli, 808 e campanelli
            for j, m in enumerate(accordo):
                aggiungi(buf, tono(hz(m + 12), battuta, armoniche=(1, .1), att=.02, dec=2.5) * .05, t0, pan=(-.4 if j % 2 else .4))
            aggiungi(buf, ottotto(hz(basso), battuta * .9) * .42, t0)
            aggiungi(buf, cassa() * .35, t0); aggiungi(buf, cassa() * .25, t0 + 2.75 * beat)
            aggiungi(buf, clap(), t0 + 2 * beat)
            for k in range(16):
                rullo = (b % 2 == 1 and k >= 12)
                passi = 3 if rullo else 1
                for r in range(passi):
                    aggiungi(buf, charleston() * .9, t0 + k * beat / 4 + r * beat / 12, pan=.2)
            for k, m in enumerate((accordo[-1] + 24, accordo[0] + 24, accordo[1] + 24)):
                aggiungi(buf, tono(hz(m), .5, armoniche=(1, .05), att=.003, dec=.2) * .05, t0 + (k * 1.5 + .5) * beat, pan=.3)
        elif stile == 'house':
            # cassa in quattro, charleston in levare, clap sul 2 e 4, accordi stab e basso in ottavi
            for k in range(4):
                aggiungi(buf, cassa(.35) * .36, t0 + k * beat)
                aggiungi(buf, charleston(.09) * 1.4, t0 + (k + .5) * beat, pan=.25)
            for k in (1, 3):
                aggiungi(buf, clap() * .9, t0 + k * beat)
            for colpo in (.5, 1.75, 2.5, 3.75):
                for m in accordo:
                    aggiungi(buf, tono(hz(m + 12), .3, armoniche=(1, .4, .2), att=.004, dec=.12) * .055, t0 + colpo * beat)
            for k in range(8):
                aggiungi(buf, tono(hz(basso + (12 if k % 2 else 0)), beat / 2, armoniche=(1, .3), att=.005, dec=.18) * .16, t0 + k * beat / 2)
        elif stile == 'cinema':
            # pad ampio, pulsazione in ottavi e timpano ogni due battute: tensione, adatto ai numeri
            for j, m in enumerate(accordo):
                aggiungi(buf, tono(hz(m), battuta + 1, armoniche=(1, .3, .1, .05), att=.8, dec=4) * .07, t0, pan=(-.5 if j % 2 else .5))
            for k in range(8):
                aggiungi(buf, tono(hz(basso + 12), beat / 2, armoniche=(1, .5, .25), att=.01, dec=.15) * (.14 if k % 2 == 0 else .09), t0 + k * beat / 2)
            if b % 2 == 0:
                aggiungi(buf, cassa(.9) * .45, t0)
            aggiungi(buf, cassa(.4) * .2, t0 + 2 * beat)
            for k in range(4):
                aggiungi(buf, charleston(.04) * .8, t0 + (k + .5) * beat, pan=-.3)
        elif stile == 'pluck':
            # arpeggio pizzicato a sedicesimi, cassa morbida e rullante leggero: positivo, adatto alla finanza
            note = list(accordo) + [accordo[1] + 12, accordo[2] + 12]
            for k in range(16):
                m = note[(k * 3) % len(note)] + (12 if k % 8 == 7 else 0)
                aggiungi(buf, pluck(hz(m), .45) * .09, t0 + k * beat / 4, pan=(-.3 if k % 2 else .3))
            for j, m in enumerate(accordo):
                aggiungi(buf, tono(hz(m - 12), battuta + .4, armoniche=(1, .15), att=.3, dec=3) * .05, t0, pan=(-.3 if j % 2 else .3))
            aggiungi(buf, tono(hz(basso), battuta * .95, armoniche=(1, .2), att=.01, dec=1.4) * .15, t0)
            for colpo in (0, 2, 2.5):
                aggiungi(buf, cassa() * .28, t0 + colpo * beat)
            for colpo in (1, 3):
                aggiungi(buf, rullante() * .8, t0 + colpo * beat, pan=.1)
    buf = np.tanh(buf * 1.3)
    return buf / np.max(np.abs(buf)) * .89


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
    import sys
    scelte = sys.argv[1:]
    for nome, (stile, bpm, giro) in BASI.items():
        if scelte and nome not in scelte:
            continue
        audio = ((base(bpm, giro) if stile == 'lofi' else base_stile(stile, bpm, giro)) * 32767).astype('<i2')
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            wav = f.name
        with wave.open(wav, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(audio.tobytes())
        out = os.path.join(CARTELLA, nome + '.m4a')
        subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'aac', '-b:a', '192k', out], check=True)
        os.remove(wav)
        print(nome, stile, bpm, 'bpm →', out)
