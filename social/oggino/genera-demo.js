/* Monta i video "come funziona" dei bot da demo-bot.json. uso: (server 8792 in questa cartella) node genera-demo.js b-trademanager ... */
const { chromium } = require('playwright');
const { execSync, spawnSync, spawn } = require('child_process');
const fs = require('fs'); const path = require('path');
const Q = __dirname, FPS = 30;
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
(async () => {
  const tutte = JSON.parse(fs.readFileSync(path.join(Q, 'demo-bot.json'), 'utf8')), scelte = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('errore pagina:', e.message));
  await p.goto('http://127.0.0.1:8792/demo.html'); await p.waitForFunction(() => window.visPronto); await p.evaluate(() => document.fonts.ready);
  for(const ep of tutte){
    if(scelte.length && !scelte.includes(ep.id)) continue;
    const tmp = path.join(Q, 'tmp-' + ep.id); fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp);
    await p.evaluate(e => window.imposta(e), ep);
    const enc = spawn(FF, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '23', '-pix_fmt', 'yuv420p', path.join(tmp, 'muto.mp4')], { stdio: ['pipe', 'ignore', 'ignore'] });
    const scrivi = buf => new Promise(ok => enc.stdin.write(buf) ? ok() : enc.stdin.once('drain', ok));
    const N = Math.round(ep.durata * FPS);
    for(let f = 0; f < N; f++){ await p.evaluate(([t, f]) => window.fotogramma(t, f), [f / FPS, f]); await scrivi(await (await p.$('#v')).screenshot({ type: 'jpeg', quality: 88 })); }
    await new Promise(ok => { enc.on('close', ok); enc.stdin.end(); });
    const ev = [];
    (ep.tocchi || []).forEach(([t]) => ev.push(['click', t, .9]));
    (ep.notifiche || []).forEach(([t]) => ev.push(['tick', t, .8]));
    (ep.linee || []).filter(l => l.colpo && l.a !== undefined).forEach(l => ev.push(['tasto', l.a - .6, 1]));
    if(ep.blocco) ev.push(['tonfo', ep.blocco[0], 1], ['timbro', ep.blocco[0], .6]);
    ev.push(['boom', ep.fine, .6], ['chiusura', ep.fine + .6, .8]);
    const ing = [], fil = []; let n = 0;
    for(const [f, t, vol] of ev){ const ms = Math.round(t * 1000); ing.push('-i', path.join(Q, 'sfx', f + '.wav'));
      fil.push(`[${n + 1}:a]volume=${vol},adelay=${ms}|${ms},aresample=48000,aformat=channel_layouts=stereo[s${n}]`); n++; }
    ing.push('-stream_loop', '-1', '-i', path.join(Q, '..', 'generatore', 'musica', 'c.m4a'));
    fil.push(`[${n + 1}:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.13[s${n}]`); n++;
    const fc = fil.join(';') + ';' + [...Array(n).keys()].map(k => `[s${k}]`).join('') + `amix=inputs=${n}:duration=longest:normalize=0,atrim=0:${ep.durata},afade=t=out:st=${(ep.durata - 1.2).toFixed(2)}:d=1.2,loudnorm=I=-14:TP=-1.5,aresample=48000[a]`;
    const r = spawnSync(FF, ['-y', '-i', path.join(tmp, 'muto.mp4'), ...ing, '-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy',
      '-c:a', 'aac', '-ar', '48000', '-b:a', '192k', '-movflags', '+faststart', '-shortest', path.join(Q, ep.id + '.mp4')]);
    if(r.status) console.error(r.stderr.toString().slice(-1500));
    fs.rmSync(tmp, { recursive: true, force: true }); console.log(ep.id + '.mp4', ep.durata + ' s');
  }
  await b.close();
})();
