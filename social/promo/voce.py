# Voce del video di presentazione (edge-tts, it-IT-DiegoNeural) + tempi di ogni parola in parole.json
# uso (dalla cartella social/promo): pip install edge-tts && python3 voce.py
# Voce del video di presentazione (edge-tts, voce it-IT-DiegoNeural) + tempi di ogni parola in parole.json
# uso: pip install edge-tts ; python3 social/promo/voce.py  (dalla cartella social/promo)
import certifi, json, asyncio, subprocess
import os
if os.path.exists('/root/.ccr/ca-bundle.crt'): certifi.where = lambda: '/root/.ccr/ca-bundle.crt'   # proxy dell'ambiente cloud
import edge_tts
righe = [
 "Il mercato non lo controlli. Tutto il resto sì.",
 "La maggior parte dei conti non salta per una strategia sbagliata. Salta per una giornata storta, quando smetti di rispettare le tue regole.",
 "Riskly è il software che le fa rispettare al posto tuo. Quattro bot per MetaTrader 4 e 5, che non aprono operazioni e non danno segnali: gestiscono il rischio di quelle che apri tu.",
 "RiskGuard ti ferma dopo le perdite di fila, e blocca la giornata prima del limite della tua prop firm. TradeManager sposta lo stop a pareggio e segue il prezzo. ScaleIn divide la posizione in più take profit. E Riskly Pro li mette insieme.",
 "Ogni operazione chiusa arriva da sola nel journal. Vedi winrate, drawdown, gli orari in cui perdi di più, e quali parti del tuo metodo funzionano davvero. Anche dal telefono.",
 "E intanto hai cinque calcolatori gratuiti, senza registrazione.",
 "Lancio il 23 ottobre. I primi dieci bloccano il prezzo per sempre. Vai su riskly punto trade.",
]
async def una(i, testo):
    c = edge_tts.Communicate(testo, 'it-IT-DiegoNeural', rate='+7%', boundary='WordBoundary')
    parole = []
    with open(f'voce/w{i}.mp3', 'wb') as f:
        async for ch in c.stream():
            if ch['type'] == 'audio': f.write(ch['data'])
            elif ch['type'] == 'WordBoundary':
                parole.append([round(ch['offset']/1e7, 3), round((ch['offset']+ch['duration'])/1e7, 3), ch['text']])
    return parole
async def main():
    out = []
    for i, r in enumerate(righe, 1):
        out.append(await una(i, r))
    json.dump(out, open('parole.json', 'w'), ensure_ascii=False)
asyncio.run(main())
