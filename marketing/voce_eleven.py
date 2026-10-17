# Voce dei corsi con ElevenLabs (voce "George" + leggero effetto stanza, scelta di Gabriele: prova 1c).
# Usata da corso-video/build.py e corso-fondamentale/build.py quando CORSO_TTS=eleven.
# La chiave sta nella variabile ELEVEN_API_KEY (mai nel repository).
import os, json, subprocess, time, urllib.request, urllib.error

VOCE_ID = os.environ.get('ELEVEN_VOCE', 'JBFqnCBsd6RMkjVDRZzb')   # George
MODELLO = os.environ.get('ELEVEN_MODELLO', 'eleven_v4')   # scelto da Gabriele (prova 4)
IMPOSTAZIONI = dict(stability=0.4, similarity_boost=0.8, style=0.3, use_speaker_boost=True)
# il filtro della prova 1c, senza loudnorm (la normalizzazione la fa già il montaggio del video)
STANZA = 'equalizer=f=180:t=q:w=1:g=2,equalizer=f=6500:t=q:w=1.5:g=-2,aecho=0.8:0.85:28|47:0.10|0.06'

def firma():
    return f'eleven-{VOCE_ID}-{MODELLO}-' + json.dumps(IMPOSTAZIONI, sort_keys=True) + STANZA

def sintetizza(testo, out, ff):
    chiave = os.environ['ELEVEN_API_KEY']
    corpo = json.dumps(dict(text=testo, model_id=MODELLO, voice_settings=IMPOSTAZIONI)).encode()
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{VOCE_ID}?output_format=mp3_44100_128'
    for tent in range(5):
        try:
            req = urllib.request.Request(url, data=corpo, headers={'xi-api-key': chiave, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
            grezzo = out + '.raw.mp3'
            with urllib.request.urlopen(req, timeout=120) as r, open(grezzo, 'wb') as f: f.write(r.read())
            tmp = out + '.tmp.mp3'
            subprocess.check_call([ff, '-y', '-v', 'error', '-i', grezzo, '-af', STANZA, '-b:a', '128k', tmp])
            os.replace(tmp, out); os.remove(grezzo); return
        except urllib.error.HTTPError as e:
            msg = e.read()[:200]
            if e.code in (401, 402, 403): raise Exception(f'ElevenLabs {e.code}: {msg}')
            print('retry', tent, e.code, msg); time.sleep(3 * (tent + 1))
        except Exception as e:
            print('retry', tent, str(e)[:80]); time.sleep(3 * (tent + 1))
    raise Exception('voce fallita: ' + testo[:50])
