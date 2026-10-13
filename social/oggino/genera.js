/* Monta una puntata di "Oggi no." (1080×1920, 30 fps) da puntate.json + voce/<id>-NN.wav/.json
   uso: (python3 -m http.server 8792 in questa cartella) node genera.js p01-quarta */
const { chromium } = require('playwright');
const { execSync, spawnSync, spawn } = require('child_process');
const fs = require('fs'); const path = require('path');
const Q = __dirname, FPS = 30, CODA = 3.2;
const PAUSE = { trader: .55, robot: .45 };       // silenzio dopo ogni battuta
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const durata = f => { const o = spawnSync(FF, ['-i', f]).stderr.toString().match(/Duration: (\d+):(\d+):([\d.]+)/); return +o[1] * 3600 + +o[2] * 60 + +o[3]; };
const norm = w => w.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '');
// effetti sonori agganciati alle azioni: [file, ritardo dall'azione]
const SUONI = { cursore: [['click', 1.0]], entra: [['whoosh', 0], ['tonfo', .4]], timbro: [['timbro', 0]], rabbia: [['ronzio', 0]], fine: [['chiusura', .8]] };

(async () => {
  const tutte = JSON.parse(fs.readFileSync(path.join(Q, 'puntate.json'), 'utf8'));
  const scelte = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('errore pagina:', e.message));
  await p.goto('http://127.0.0.1:8792/modello.html'); await p.waitForFunction(() => window.visPronto, null, { timeout: 60000 });
  for(const ep of tutte){
    if(scelte.length && !scelte.includes(ep.id)) continue;
    const tmp = path.join(Q, 'tmp-' + ep.id); fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp);
    const segs = ep.segmenti.map((s, i) => { const base = path.join(Q, 'voce', `${ep.id}-${String(i + 1).padStart(2, '0')}`);
      const D = durata(base + '.wav') + PAUSE[s.chi] + (i === ep.segmenti.length - 1 ? CODA : 0);
      return { s, base, par: JSON.parse(fs.readFileSync(base + '.json', 'utf8')), D }; });
    const battute = []; let off = 0; const inizi = [];
    for(const g of segs){ let da = 0; inizi.push(off);
      for(const bt of (g.s.battute || [])){ const k = norm(bt.su); let j = g.par.findIndex((w, x) => x >= da && norm(w[2]).startsWith(k));
        if(j < 0){ console.error('parola non trovata:', ep.id, bt.su); j = da; } da = j + 1;
        battute.push({ ...bt, t: off + (g.par[j] ? g.par[j][0] : 0) }); }
      off += g.D; }
    await p.evaluate(bb => window.ep.imposta(bb), battute);
    const enc = spawn(FF, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '24', '-pix_fmt', 'yuv420p', path.join(tmp, 'muto.mp4')], { stdio: ['pipe', 'ignore', 'ignore'] });
    const scrivi = buf => new Promise(ok => enc.stdin.write(buf) ? ok() : enc.stdin.once('drain', ok));
    let tg = 0;
    for(let i = 0; i < segs.length; i++){
      await p.evaluate(([s, par]) => window.prepara(s, par), [segs[i].s, segs[i].par]);
      const N = Math.round(segs[i].D * FPS);
      for(let f = 0; f < N; f++){
        await p.evaluate(([t, tg]) => window.fotogramma(t, tg), [f / FPS, tg + f / FPS]);
        await scrivi(await (await p.$('#v')).screenshot({ type: 'jpeg', quality: 90 }));
      }
      tg += N / FPS; process.stdout.write(`${ep.id} ${i + 1}/${segs.length}\n`);
    }
    await new Promise(ok => { enc.on('close', ok); enc.stdin.end(); });
    // audio: voci al loro inizio + effetti alle azioni + base bassa
    const ingressi = [], filtri = []; let n = 0;
    segs.forEach((g, i) => { ingressi.push('-i', g.base + '.wav'); filtri.push(`[${n}:a]adelay=${Math.round(inizi[i] * 1000)}|${Math.round(inizi[i] * 1000)},aresample=48000,aformat=channel_layouts=stereo[a${n}]`); n++; });
    for(const bt of battute) for(const [f, d] of (SUONI[bt.azione] || [])){
      const ms = Math.max(0, Math.round((bt.t + d) * 1000));
      ingressi.push('-i', path.join(Q, 'sfx', f + '.wav')); filtri.push(`[${n}:a]volume=0.8,adelay=${ms}|${ms},aresample=48000,aformat=channel_layouts=stereo[a${n}]`); n++; }
    const musica = path.join(Q, '..', 'generatore', 'musica', 'c.m4a');
    if(fs.existsSync(musica)){ ingressi.push('-stream_loop', '-1', '-i', musica); filtri.push(`[${n}:a]volume=0.10,aresample=48000,aformat=channel_layouts=stereo[a${n}]`); n++; }
    const tot = (tg).toFixed(2);
    const fc = filtri.join(';') + ';' + [...Array(n).keys()].map(k => `[a${k}]`).join('') + `amix=inputs=${n}:duration=longest:normalize=0,atrim=0:${tot},loudnorm=I=-14:TP=-1.5[a]`;
    const r = spawnSync(FF, ['-y', '-i', path.join(tmp, 'muto.mp4'), ...ingressi, '-filter_complex', fc.replace(/\[(\d+):a\]/g, (m, k) => `[${+k + 1}:a]`),
      '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-ar', '48000', '-b:a', '192k', '-movflags', '+faststart', '-shortest', path.join(Q, ep.id + '.mp4')]);
    if(r.status) console.error(r.stderr.toString().slice(-1500));
    fs.rmSync(tmp, { recursive: true, force: true });
    console.log(ep.id + '.mp4', tot + ' s');
  }
  await b.close();
})();
