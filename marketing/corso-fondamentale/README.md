# Corso «Riskly · Analisi fondamentale» · video

Stessa struttura del corso di gestione del rischio (`../corso-video`): lezioni in `lezioni/*.py`, slide 1920×1080 da `slide.html`,
voce `it-IT-GiuseppeMultilingualNeural` a velocità normale (+0%), la stessa del corso di rischio (verificato sulle sue tracce audio) (edge-tts ≥ 7.3: le versioni vecchie vengono rifiutate con errore 403).

```bash
python3 check.py            # voce e slide allineate
python3 build.py stat       # parole e minuti per lezione
python3 build.py voce       # sintetizza (cache in voce/)
python3 verifica_voce.py    # trascrive ogni traccia e la confronta con il testo (somiglianza media e passaggi peggiori)
RIFAI=1 python3 build.py png
python3 build.py video      # out/<id>.mp4 + out/corso-completo.mp4
```
Pronuncia delle sigle: dizionario PRONUNCIA in build.py (vale solo per la voce, le slide restano uguali).
Grafici con dati veri (29, nei moduli 2–9): `python3 scarica_dati.py` scarica le serie (FRED e Yahoo Finance, fonti in `dati/FONTI.md`),
`python3 grafici_veri.py` disegna `grafici/v_*.png` e scrive `grafici/fatti.json` con i numeri citati dalla voce.
Le slide stanno in `lezioni/dati_veri.py` (inserite da `extra.py`). Quando i dati si aggiornano: rifare i due script, ricontrollare i numeri nella voce con `fatti.json`, poi voce, png e video.

Regole: esempi dichiarati illustrativi, dati storici con fonte e data, niente previsioni né segnali, ogni lezione chiude sul rischio.

## Testi "a tu per tu" e voce ElevenLabs
- `lezioni/umano/m*.py`: i testi parlati riscritti come una spiegazione a tu per tu (UMANO[id] = una lista di passaggi per ogni slide, stesso numero di passaggi). Hanno la precedenza su `parlato_*.py`; `check.py` e `build.py` controllano che i passaggi tornino.
- Voce scelta: ElevenLabs "George" con leggero effetto stanza (`../voce_eleven.py`). Si attiva con `CORSO_TTS=eleven ELEVEN_API_KEY=... python3 build.py voce`; la chiave non va mai nel repository. Gli mp3 hanno un nome diverso da quelli edge-tts, quindi le due voci convivono nella cartella `voce/`.
