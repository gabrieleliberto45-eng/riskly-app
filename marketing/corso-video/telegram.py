# Testi per il canale Telegram: indice, apertura dei moduli, didascalie delle lezioni → telegram-testi.md
import build, re
L = build.carica(); O = build.QUI + '/out'
import subprocess
def dur_rapida(f):
    h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', subprocess.run([build.FF, '-i', f], capture_output=True, text=True).stderr).groups(); return int(h)*3600 + int(m)*60 + float(s)
dur = {l['id']: dur_rapida(f"{O}/{l['id']}.mp4") for l in L}
mm = lambda s: f"{int(s//60)}:{int(round(s%60)):02d}"
pulisci = lambda t: re.sub(r'\*\*(.+?)\*\*', r'\1', t)
mod = {}
for l in L: mod.setdefault((l['modulo'], l['modTitolo']), []).append(l)
tot = sum(dur.values())
out = ['# Testi per il canale Telegram del corso', '', 'Ordine di pubblicazione: per ogni modulo prima il messaggio di apertura, poi i video delle lezioni (cartella `out/corso/`), ciascuno con la sua didascalia. Alla fine fissa in alto il messaggio indice.', '', '---', '', '## 1. Messaggio indice (da fissare in alto)', '', '```']
out += ['📚 CORSO DI GESTIONE DEL RISCHIO · RISKLY', f"{len(L)} lezioni · {len(mod)} parti · circa {int(tot//3600)} ore e {int(tot%3600//60)} minuti", '']
for (m, mt), ls in mod.items(): out.append(f"▸ {m} · {mt} ({mm(sum(dur[l['id']] for l in ls))})")
out += ['', 'Come usarlo: guarda una lezione alla volta, fai l\'esercizio a metà (metti in pausa) e alla fine dell\'ultimo modulo scrivi il tuo piano su una pagina.', '', '⚠️ Contenuto educativo, non consulenza finanziaria. Il trading con leva comporta un rischio elevato: puoi perdere tutto il capitale. Gli strumenti Riskly citati sono prodotti miei.', '```', '', '---', '']
for (m, mt), ls in mod.items():
    n = len(ls)
    out += [f"## {m} · {mt}", '', 'Messaggio di apertura del modulo:', '', '```', '━━━━━━━━━━━━━━', f"📂 {m.upper()} · {mt.upper()}", f"{n} {'lezione' if n == 1 else 'lezioni'} · {mm(sum(dur[l['id']] for l in ls))}", '━━━━━━━━━━━━━━', '```', '']
    for l in ls:
        riep = next((s for s in l['slide'] if s.get('titolo') == 'In breve'), None)
        punti = [pulisci(p if isinstance(p, str) else p[0]) for p in (riep['punti'] if riep else [])]
        out += [f"**{l['id']}** — didascalia del video `{l['id']}`:", '', '```', f"🎬 Lezione {l['id']} · {pulisci(l['titolo'])}  ({mm(dur[l['id']])})"]
        if punti: out += ['', 'In breve:'] + [f"• {p}" for p in punti]
        out += ['```', '']
open(build.QUI + '/telegram-testi.md', 'w').write('\n'.join(out))
print('ok')
