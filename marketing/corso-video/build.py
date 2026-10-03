# Corso video Riskly: voce sintetica (edge-tts, it-IT-DiegoNeural) + slide (slide.html via Playwright) + ffmpeg.
# uso:  python3 build.py voce            → genera/riusa gli mp3 di ogni passaggio (cartella voce/)
#       python3 build.py png             → fotogrammi delle slide (out/png/)
#       python3 build.py video [id ...]  → video delle lezioni (out/) ; senza id = tutte + corso intero
#       python3 build.py tutto [id ...]
# Le lezioni stanno in lezioni/*.py (dizionario LEZIONE). Ogni slide ha una lista "voce": un passaggio per elemento mostrato.
import sys, os, json, hashlib, asyncio, subprocess, re, glob, importlib.util, certifi
if os.path.exists('/root/.ccr/ca-bundle.crt'): certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts
QUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, QUI + '/lezioni')
FF = os.environ.get('FFMPEG') or subprocess.check_output(['python3', '-c', 'import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())']).decode().strip()
VOCE, RATE, PAUSA, PAUSA_SLIDE = os.environ.get('CORSO_VOCE', 'it-IT-DiegoNeural'), os.environ.get('CORSO_RATE', '-2%'), 0.35, 0.55
def carica():
    L = []
    for f in sorted(glob.glob(f'{QUI}/lezioni/m*.py')):
        sp = importlib.util.spec_from_file_location('l', f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
        L.append(m.LEZIONE)
    import extra
    for l in L:
        for anc, sl in getattr(extra, 'INS', {}).get(l['id'], []):
            idx = next((i for i, x in enumerate(l['slide']) if x.get('titolo') == anc), None)
            assert idx is not None, ('ancora non trovata', l['id'], anc)
            l['slide'].insert(idx + 1, sl)
        l['slide'] = [x for x in l['slide'] if x.get('titolo') not in getattr(extra, 'DEL', {}).get(l['id'], [])]
        if l['id'] in extra.EXTRA: l['slide'] = l['slide'][:-1] + [x for e in extra.EXTRA[l['id']] for x in (e if isinstance(e, list) else [e])] + l['slide'][-1:]
    return L
def n_el(s):
    t = s['tipo']
    if t in ('titolo',): return 0
    if t == 'citazione': return 1
    if t == 'punti': return len(s['punti'])
    if t == 'formula': return 1 + len(s.get('legenda', []))
    if t == 'tabella': return len(s['righe']) + (1 if s.get('nota') else 0)
    if t == 'esempio': return len(s['righe']) + (1 if s.get('risultato') else 0)
    if t == 'confronto': return 2 + (1 if s.get('risultato') else 0)
    if t == 'grafico': return 1 + (1 if s.get('didascalia') else 0)
    if t == 'numero': return 1 + (1 if s.get('testo') else 0)
    if t == 'avviso': return 1
    if t == 'disegno': return len(s['passi'])
    if t == 'schermata': return len(s['punti'])
    raise Exception('tipo? ' + t)
def passi(s):
    n = n_el(s); v = s['voce']
    if s.get('k'):
        assert len(s['k']) == len(v), f"k/voce: {s.get('titolo')}"
        return list(zip(v, s['k']))
    off = 1 if (n and len(v) == n + 1) else 0
    if n and len(v) not in (n, n + 1) and len(v) > n + 1: raise Exception(f"troppi passaggi voce: {s.get('titolo')} ({len(v)} vs {n})")
    return [(t, n if j == len(v) - 1 else max(0, min(n, j + 1 - off))) for j, t in enumerate(v)]
ESPANDI = {'Riassumiamo.': 'Riassumiamo ora i punti principali di questa lezione.'}
def testo_tts(t):
    """Per la voce multilingue: evita frasi di 1-3 parole (la lingua viene riconosciuta male) unendole alla successiva."""
    t = t.strip()
    if t in ESPANDI: return ESPANDI[t]
    fr = re.split(r'(?<=[.!?])\s+', t); out = []
    i = 0
    while i < len(fr):
        f = fr[i]
        while len(f.split()) <= 3 and f.endswith('.') and i + 1 < len(fr):
            i += 1; nxt = fr[i]; f = f[:-1] + ', ' + nxt[0].lower() + nxt[1:] if not nxt.startswith(('L\'', 'E ')) else f[:-1] + ', ' + nxt
        out.append(f); i += 1
    if len(out) > 1 and len(out[-1].split()) <= 3 and out[-2].endswith('.'):
        u = out.pop(); out[-1] = out[-1][:-1] + ', ' + u[0].lower() + u[1:]
    return ' '.join(out)
def fname(t): return f"{QUI}/voce/{hashlib.md5((VOCE+RATE+testo_tts(t)).encode()).hexdigest()[:16]}.mp3"
def durata(f):
    r = subprocess.run([FF, '-i', f, '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = re.findall(r'time=(\d+):(\d+):([\d.]+)', r)[-1]; return int(m[0]) * 3600 + int(m[1]) * 60 + float(m[2])
def tutti_i_passi(L):
    out = []
    for li, l in enumerate(L):
        for si, s in enumerate(l['slide']):
            for pj, (t, k) in enumerate(passi(s)): out.append((li, si, pj, t, k))
    return out
async def voce(L):
    sem = asyncio.Semaphore(6); todo = [t for _, _, _, t, _ in tutti_i_passi(L) if not os.path.exists(fname(t))]
    todo = list(dict.fromkeys(todo)); print(len(todo), 'passaggi da sintetizzare')
    async def una(t):
        async with sem:
            for tent in range(4):
                try:
                    c = edge_tts.Communicate(testo_tts(t), VOCE, rate=RATE); tmp = fname(t) + '.tmp'
                    await c.save(tmp); os.replace(tmp, fname(t)); return
                except Exception as e:
                    print('retry', tent, str(e)[:80]); await asyncio.sleep(2 * (tent + 1))
            raise Exception('voce fallita: ' + t[:50])
    await asyncio.gather(*[una(t) for t in todo])
def manifest(L):
    tot = sum(len(l['slide']) for l in L); man = []; done = 0
    for li, l in enumerate(L):
        for si, s in enumerate(l['slide']):
            done += 1
            for pj, (t, k) in enumerate(passi(s)):
                info = dict(mod=l['modulo'], modTitolo=l['modTitolo'], lez=l['id'], titolo=l['titolo'], pct=done / tot)
                man.append(dict(png=f"{l['id']}_{si:02d}_{k}", slide=s, k=k, info=info))
    return man
def png(L):
    man = manifest(L); os.makedirs(f'{QUI}/out/png', exist_ok=True)
    json.dump(man, open(f'{QUI}/out/manifest.json', 'w'), ensure_ascii=False)
    subprocess.check_call(['node', f'{QUI}/rendi.js'])
def video(L, ids):
    os.makedirs(f'{QUI}/out/tmp', exist_ok=True); tot = 0; fatti = []
    for l in L:
        mp4 = f"{QUI}/out/{l['id']}.mp4"; fatti.append(mp4)
        if ids and l['id'] not in ids: continue
        lista = []; wavs = []; d_lez = 0
        for si, s in enumerate(l['slide']):
            ps = passi(s)
            for pj, (t, k) in enumerate(ps):
                f = fname(t); d = durata(f); extra = PAUSA_SLIDE if pj == len(ps) - 1 else PAUSA
                wav = f"{QUI}/out/tmp/{l['id']}_{si:02d}_{pj}.wav"
                subprocess.check_call([FF, '-y', '-v', 'error', '-i', f, '-ar', '44100', '-ac', '2', '-af', f'apad=pad_dur={extra}', wav])
                wavs.append(wav); lista.append((f"{QUI}/out/png/{l['id']}_{si:02d}_{k}.png", d + extra)); d_lez += d + extra
        with open(f"{QUI}/out/tmp/{l['id']}.txt", 'w') as f:
            for p, d in lista: f.write(f"file '{p}'\nduration {d:.3f}\n")
            f.write(f"file '{lista[-1][0]}'\n")
        with open(f"{QUI}/out/tmp/{l['id']}_a.txt", 'w') as f:
            for w in wavs: f.write(f"file '{w}'\n")
        subprocess.check_call([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f"{QUI}/out/tmp/{l['id']}.txt",
            '-f', 'concat', '-safe', '0', '-i', f"{QUI}/out/tmp/{l['id']}_a.txt",
            '-vf', 'fps=25,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '27', '-tune', 'stillimage',
            '-af', 'loudnorm=I=-16:TP=-1.5:LRA=9', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest', mp4])
        print(l['id'], f'{d_lez/60:.1f} min'); tot += d_lez
    if not ids:
        with open(f'{QUI}/out/tmp/tutto.txt', 'w') as f:
            for m in fatti: f.write(f"file '{m}'\n")
        subprocess.check_call([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{QUI}/out/tmp/tutto.txt', '-c', 'copy', f'{QUI}/out/corso-completo.mp4'])
        print('totale', f'{tot/60:.1f} min')
def stat(L):
    tutti_i_passi(L)
    parole = 0; dur = 0
    for l in L:
        p = sum(len(t.split()) for s in l['slide'] for t in s['voce']); parole += p
        print(f"{l['id']:5} {l['titolo'][:44]:44} {p:5} parole  ~{p/150:.1f} min  {len(l['slide'])} slide")
    print('TOTALE', parole, 'parole  ~', round(parole / 150), 'min')
if __name__ == '__main__':
    a = sys.argv[1:] or ['stat']; L = carica(); cmd = a[0]; ids = a[1:]
    if ids: L_sel = [l for l in L if l['id'] in ids]
    if cmd == 'stat': stat(L)
    if cmd in ('voce', 'tutto'): asyncio.run(voce([l for l in L if not ids or l['id'] in ids]))
    if cmd in ('png', 'tutto'): png(L)
    if cmd in ('video', 'tutto'): video(L, ids)
