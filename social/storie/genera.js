/* Monta le "Storie di rischio" (1080×1920, 30 fps) da storie.json + voce/<id>-NN.mp3/.json
   uso: (python3 -m http.server 8791 in questa cartella) node genera.js s01-franco */
const { chromium } = require('playwright');
const { execSync, spawnSync, spawn } = require('child_process');
const fs = require('fs'); const path = require('path');
const Q = __dirname, FPS = 30, PAUSA = .35;
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const durata = f => { const o = spawnSync(FF, ['-i', f]).stderr.toString().match(/Duration: (\d+):(\d+):([\d.]+)/); return +o[1] * 3600 + +o[2] * 60 + +o[3]; };

(async () => {
  const tutte = JSON.parse(fs.readFileSync(path.join(Q, 'storie.json'), 'utf8'));
  const scelte = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('http://127.0.0.1:8791/modello.html'); await p.waitForFunction(() => window.visPronto); await p.evaluate(() => document.fonts.ready);
  for(const st of tutte){
    if(scelte.length && !scelte.includes(st.id)) continue;
    const tmp = path.join(Q, 'tmp-' + st.id); fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp);
    const enc = spawn(FF, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '27', '-pix_fmt', 'yuv420p', path.join(tmp, 'muto.mp4')], { stdio: ['pipe', 'ignore', 'ignore'] });
    const scrivi = buf => new Promise(ok => enc.stdin.write(buf) ? ok() : enc.stdin.once('drain', ok));
    let fr = 0; const voci = [];
    // battute: ogni azione 3D parte quando la voce dice la sua parola chiave
    const norm = w => w.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]/g, '');
    const segs = st.segmenti.map((s, i) => { const base = path.join(Q, 'voce', `${st.id}-${String(i + 1).padStart(2, '0')}`);
      return { s, base, par: JSON.parse(fs.readFileSync(base + '.json', 'utf8')), D: durata(base + '.mp3') + PAUSA }; });
    const battute = []; let off = 0;
    for(const g of segs){ let da = 0;
      for(const b of (g.s.battute || [])){ const k = norm(b.su); let j = g.par.findIndex((w, x) => x >= da && norm(w[2]).startsWith(k));
        if(j < 0){ console.error('parola non trovata:', st.id, b.su); j = da; } da = j + 1;
        battute.push({ ...b, t: off + Math.max(0, g.par[j] ? g.par[j][0] : 0) }); }
      off += g.D; }
    battute.sort((a, b) => a.t - b.t);
    await p.evaluate(b => window.storia.imposta(b), battute);
    let tg = 0;
    for(let i = 0; i < segs.length; i++){
      const { base, par, D } = segs[i]; voci.push(base + '.mp3');
      await p.evaluate(([s, u, par]) => window.prepara(s, u, par), [st.segmenti[i], i === st.segmenti.length - 1, par]);
      for(let f = 0; f < Math.round(D * FPS); f++){
        await p.evaluate(([t, f, tg]) => window.fotogramma(t, f, tg), [f / FPS, fr++, tg + f / FPS]);
        await scrivi(await (await p.$('#v')).screenshot({ type: 'jpeg', quality: 90 }));
      }
      tg += Math.round(D * FPS) / FPS;
      process.stdout.write(`${st.id} ${i + 1}/${st.segmenti.length}\n`);
    }
    await new Promise(ok => { enc.on('close', ok); enc.stdin.end(); });
    spawnSync(FF, ['-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', String(PAUSA), '-c:a', 'libmp3lame', path.join(tmp, 'pausa.mp3')]);
    fs.writeFileSync(path.join(tmp, 'voce.txt'), voci.map(v => `file '${v}'\nfile '${path.join(tmp, 'pausa.mp3')}'`).join('\n'));
    spawnSync(FF, ['-y', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'voce.txt'), '-ar', '48000', '-ac', '2', path.join(tmp, 'voce.wav')]);
    const musica = path.join(Q, '..', 'generatore', 'musica', 'c.m4a');   // base cinematica
    const r = spawnSync(FF, ['-y', '-i', path.join(tmp, 'muto.mp4'), '-i', path.join(tmp, 'voce.wav'), '-stream_loop', '-1', '-i', musica,
      '-filter_complex', '[2:a]volume=0.16[m];[1:a][m]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5[a]',
      '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-ar', '48000', '-b:a', '192k', '-movflags', '+faststart', '-shortest', path.join(Q, st.id + '.mp4')]);
    if(r.status) console.error(r.stderr.toString().slice(-800));
    fs.rmSync(tmp, { recursive: true, force: true });
    console.log(st.id + '.mp4', (fr / FPS).toFixed(1) + ' s');
  }
  await b.close();
})();
