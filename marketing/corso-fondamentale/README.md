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
Regole: esempi dichiarati illustrativi, dati storici con fonte e data, niente previsioni né segnali, ogni lezione chiude sul rischio.
