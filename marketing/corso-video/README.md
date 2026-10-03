# Corso di gestione del rischio · video con voce sintetica

47 lezioni in 11 parti (introduzione + 10 moduli, compreso il modulo 9 «Tecniche avanzate»: compounding, trailing, ingressi e uscite a scaglioni, mitigazione, hedging), slide in stile Riskly (1920×1080) con voce `it-IT-DiegoNeural` (edge-tts).
Le lezioni sono file Python in `lezioni/` (testo parlato + contenuto di ogni slide, un passaggio di voce per ogni elemento che compare).

## Costruire i video
```bash
pip install edge-tts imageio-ffmpeg matplotlib numpy pillow   # + playwright (node) con Chromium
python3 grafici.py            # grafici in grafici/
python3 build.py stat         # parole e minuti per lezione
python3 check.py              # controlla che voce e slide siano allineate
python3 build.py voce         # sintetizza la voce (cache in voce/)
RIFAI=1 python3 build.py png  # fotogrammi delle slide (out/png/)
python3 build.py video        # video per lezione (out/*.mp4) + out/corso-completo.mp4
python3 build.py video 3.2    # una sola lezione
```
Per cambiare un testo: modifica il file in `lezioni/`, rilancia `voce`, `png` (con `RIFAI=1`) e `video <id>`.
Per ricontrollare i numeri citati: `python3 sim_numeri.py`.

## Regole del corso
- Ogni numero di simulazione viene da `sim_numeri.py` (sistema d'esempio: 45% di vincite, +1,8 R / −1 R, 200 trade, 40.000 percorsi).
- Avviso «educativo, non consulenza» in apertura, in chiusura e nel piè di pagina di ogni slide.
- I prodotti Riskly compaiono nelle lezioni 1.4, 2.5, 5.2, 8.4 e 9.4 e sono sempre dichiarati come «miei prodotti».
