/* Monta "Oggi no." v2 (senza voce) da sistema-puntate.json. uso: (server 8792 in questa cartella) node genera-sistema.js p01v2-quarta */
const { chromium } = require('playwright');
const { execSync, spawnSync, spawn } = require('child_process');
const fs = require('fs'); const path = require('path');
const Q = __dirname, FPS = 30;
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
(async () => {
  const tutte = JSON.parse(fs.readFileSync(path.join(Q, 'sistema-puntate.json'), 'utf8')), scelte = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('errore pagina:', e.message));
  await p.goto('http://127.0.0.1:8792/sistema.html'); await p.waitForFunction(() => window.visPronto); await p.evaluate(() => document.fonts.ready);
  for(const ep of tutte){
    if(scelte.length && !scelte.includes(ep.id)) continue;
    const T = ep.tempi, tmp = path.join(Q, 'tmp-' + ep.id); fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp);
    await p.evaluate(e => window.imposta(e), ep);
    const enc = spawn(FF, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '22', '-pix_fmt', 'yuv420p', path.join(tmp, 'muto.mp4')], { stdio: ['pipe', 'ignore', 'ignore'] });
    const scrivi = buf => new Promise(ok => enc.stdin.write(buf) ? ok() : enc.stdin.once('drain', ok));
    const N = Math.round(T.durata * FPS);
    for(let f = 0; f < N; f++){ await p.evaluate(([t, f]) => window.fotogramma(t, f), [f / FPS, f]); await scrivi(await (await p.$('#v')).screenshot({ type: 'jpeg', quality: 90 })); }
    await new Promise(ok => { enc.on('close', ok); enc.stdin.end(); });
    // suoni: tasti mentre si scrivono i pensieri, tocchi, il blocco, il titolo, le righe, la chiusura
    const ev = [];
    ep.pensieri.forEach(([a, testo]) => { for(let i = 0; i < testo.length; i++) if(testo[i] !== ' ' && a + i / 17 < T.blocco) ev.push(['tasto', a + i / 17, .5 + (i % 3) * .1]); });
    if(ep.lotto[0] !== ep.lotto[1]) ev.push(['click', T.lotto, .9]);
    if(T.dialogo) ev.push(['tick', T.dialogo, .8]);
    ev.push(['click', T.tocco, .9], ['tonfo', T.blocco, 1], ['timbro', T.blocco, .7], ['boom', T.titolo, .9]);
    ep.righe.forEach((r, i) => ev.push(['tick', T.righe + i * T.passo, .7]));
    if(ep.offerta){ ep.offerta.righe.forEach((r, i) => ev.push(['tick', T.offerta + .3 + i * T.passo, .8])); ev.push(['click', T.cta, .9]); }
    ev.push(['chiusura', T.fine + .2, .8]);
    const ing = [], fil = []; let n = 0;
    for(const [f, t, vol] of ev){ const ms = Math.round(t * 1000); ing.push('-i', path.join(Q, 'sfx', f + '.wav'));
      fil.push(`[${n + 1}:a]volume=${vol},adelay=${ms}|${ms},aresample=48000,aformat=channel_layouts=stereo[s${n}]`); n++; }
    // musica: tensione bassa, si spegne di colpo sul blocco e riparte piano dopo il titolo
    ing.push('-stream_loop', '-1', '-i', path.join(Q, '..', 'generatore', 'musica', 'c.m4a'));
    fil.push(`[${n + 1}:a]aresample=48000,aformat=channel_layouts=stereo,volume='if(lt(t,${T.blocco}),0.16,if(lt(t,${T.titolo + .6}),0,0.07))':eval=frame[s${n}]`); n++;
    const fc = fil.join(';') + ';' + [...Array(n).keys()].map(k => `[s${k}]`).join('') + `amix=inputs=${n}:duration=longest:normalize=0,atrim=0:${T.durata},loudnorm=I=-14:TP=-1.5,aresample=48000[a]`;
    const r = spawnSync(FF, ['-y', '-i', path.join(tmp, 'muto.mp4'), ...ing, '-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy',
      '-c:a', 'aac', '-ar', '48000', '-b:a', '192k', '-movflags', '+faststart', '-shortest', path.join(Q, ep.id + '.mp4')]);
    if(r.status) console.error(r.stderr.toString().slice(-1500));
    fs.rmSync(tmp, { recursive: true, force: true }); console.log(ep.id + '.mp4', T.durata + ' s');
  }
  await b.close();
})();
