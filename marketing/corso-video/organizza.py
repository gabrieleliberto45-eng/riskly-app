# Organizza i video per argomento: out/corso/<modulo>/<lezione>.mp4, un video per modulo, corso completo con capitoli, INDICE.md
import os, re, shutil, subprocess, build
L = build.carica(); FF = build.FF; O = build.QUI + '/out'; D = O + '/corso'
shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
def slug(t): return re.sub(r'[^A-Za-z0-9À-ÿ]+', '_', t).strip('_')
mod = {}
for l in L: mod.setdefault((l['modulo'], l['modTitolo']), []).append(l)
dur = {l['id']: build.durata(f"{O}/{l['id']}.mp4") for l in L}
def mmss(s): s = int(round(s)); return f"{s//3600}:{s%3600//60:02d}:{s%60:02d}" if s >= 3600 else f"{s//60}:{s%60:02d}"
righe = ['# Corso di gestione del rischio · indice', '', f"Durata totale: **{mmss(sum(dur.values()))}** · {len(L)} lezioni · {len(mod)} moduli", '']
chap = [';FFMETADATA1', 'title=Corso di gestione del rischio · Riskly']; t0 = 0; lista = []
for n, ((m, mt), ls) in enumerate(mod.items()):
    cart = f"{D}/{n:02d}_{slug(m + ' ' + mt)}"; os.makedirs(cart)
    righe += [f"## {m} · {mt} ({mmss(sum(dur[l['id']] for l in ls))})", '', '| Lezione | Titolo | Durata | Inizio nel corso completo |', '|---|---|---|---|']
    lm = []
    for l in ls:
        f = f"{cart}/{l['id']}_{slug(l['titolo'])}.mp4"; shutil.copy(f"{O}/{l['id']}.mp4", f); lm.append(f)
        righe.append(f"| {l['id']} | {l['titolo']} | {mmss(dur[l['id']])} | {mmss(t0)} |")
        chap += ['[CHAPTER]', 'TIMEBASE=1/1000', f"START={int(t0*1000)}", f"END={int((t0+dur[l['id']])*1000)}", f"title={l['id']} · {l['titolo']}"]
        t0 += dur[l['id']]; lista.append(f"{O}/{l['id']}.mp4")
    righe.append('')
    with open(f"{O}/tmp/mod{n}.txt", 'w') as fh: fh.write(''.join(f"file '{x}'\n" for x in lm))
    subprocess.check_call([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f"{O}/tmp/mod{n}.txt", '-c', 'copy', f"{D}/{n:02d}_{slug(m + ' ' + mt)}.mp4"])
open(f"{O}/tmp/chap.txt", 'w').write('\n'.join(chap) + '\n')
with open(f"{O}/tmp/tutto2.txt", 'w') as fh: fh.write(''.join(f"file '{x}'\n" for x in lista))
subprocess.check_call([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f"{O}/tmp/tutto2.txt", '-i', f"{O}/tmp/chap.txt", '-map_metadata', '1', '-map_chapters', '1', '-c', 'copy', f"{D}/00_CORSO_COMPLETO.mp4"])
open(f"{D}/INDICE.md", 'w').write('\n'.join(righe) + '\n')
print('ok', mmss(t0))
