/* Monta un video lungo YouTube (1920×1080) da social/youtube/<id>.json + voce/<id>-NN.mp3
   uso: node social/youtube/genera.js v01
   Ogni scena: gli elementi compaiono uno alla volta, distribuiti lungo la voce; tra una comparsa e l'altra
   l'immagine resta ferma (si rendono solo i fotogrammi delle animazioni). Esce <id>.mp4, <id>-miniatura.jpg, <id>-capitoli.txt */
const { chromium } = require('playwright');
const { execSync, spawnSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const QUI = __dirname, ID = process.argv[2] || 'v01';
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const FPS = 24, ANIM = 0.7, PAUSA = 0.7;          // durata comparsa, silenzio tra le scene
const durata = f => { const o = spawnSync(FF, ['-i', f]).stderr.toString().match(/Duration: (\d+):(\d+):([\d.]+)/); return +o[1]*3600 + +o[2]*60 + +o[3]; };

(async () => {
  const spec = JSON.parse(fs.readFileSync(path.join(QUI, ID + '.json'), 'utf8'));
  const tmp = path.join(QUI, 'tmp-' + ID); fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  // i moduli 3D non si caricano da file://: serve un server locale (python3 -m http.server 8790 nella cartella)
  await p.goto(process.env.URL || 'http://127.0.0.1:8790/modello.html');
  await p.waitForFunction(() => window.visPronto); await p.evaluate(() => document.fonts.ready);

  const voci = spec.scene.map((s, i) => path.join(QUI, 'voce', `${ID}-${String(i + 1).padStart(2, '0')}.mp3`));
  const durate = voci.map(durata).map(d => d + PAUSA);
  const totale = durate.reduce((a, c) => a + c, 0);
  let inizio = 0, scritti = 0, dovuti = 0; const capitoli = [];
  // i fotogrammi vanno direttamente a ffmpeg (niente migliaia di file su disco), a fotogrammi costanti
  const enc = spawn(FF, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', path.join(tmp, 'muto.mp4')], { stdio: ['pipe', 'ignore', 'ignore'] });
  const scrivi = buf => new Promise(ok => enc.stdin.write(buf) ? ok() : enc.stdin.once('drain', ok));
  const scatto = async () => (await p.$('#v')).screenshot({ type: 'jpeg', quality: 92 });
  const lista = { push: async ([buf, d]) => { dovuti += d; const n = Math.max(1, Math.round(dovuti * FPS) - scritti); for(let k = 0; k < n; k++) await scrivi(buf); scritti += n; } };

  for(let i = 0; i < spec.scene.length; i++){
    const s = spec.scene[i], D = durate[i];
    capitoli.push([inizio, s.capitolo]);
    const n = await p.evaluate(([s, i, N, a]) => window.scena(s, i, N, a), [s, i, spec.scene.length, (inizio + D / 2) / totale]);
    await p.evaluate(() => document.fonts.ready);
    // titolo subito, il resto distribuito nel primo 75% della voce
    const tempi = [...Array(n)].map((_, k) => k === 0 ? 0 : Math.min(D - 1, 0.6 + (k / n) * D * 0.75));
    if(s.visual){                       // scena 3D: ogni fotogramma è diverso
      const tot = Math.round(D * FPS);
      for(let f = 0; f < tot; f++){
        await p.evaluate(([t, tempi]) => window.fotogramma(t, tempi), [f / FPS, tempi]);
        await lista.push([await scatto(), 1 / FPS]);
      }
    } else {                            // senza 3D: solo le comparse, poi immagine ferma
      let t = 0;
      while(t < D){
        await p.evaluate(([t, tempi]) => window.fotogramma(t, tempi), [t, tempi]);
        const f = await scatto();
        const inAnim = tempi.some(x => t >= x && t < x + ANIM);
        const prossimo = inAnim ? t + 1 / FPS : Math.min(D, ...tempi.filter(x => x > t), D);
        await lista.push([f, Math.max(1 / FPS, prossimo - t)]); t = Math.max(prossimo, t + 1 / FPS);
      }
    }
    inizio += D;
    process.stdout.write(`scena ${i + 1}/${spec.scene.length}\n`);
  }
  // miniatura: scena 1 completa
  await p.evaluate(([s, N]) => { window.scena(s, 0, N, 0); window.fotogramma(8, Array(30).fill(0)); }, [spec.scene[0], spec.scene.length]);
  await (await p.$('#v')).screenshot({ path: path.join(QUI, ID + '-miniatura.jpg'), type: 'jpeg', quality: 92 });
  await b.close();

  await new Promise(ok => { enc.on('close', ok); enc.stdin.end(); });
  // voce: tracce in fila con la pausa tra le scene
  const ac = voci.map(v => `file '${v}'\nfile '${path.join(tmp, 'pausa.mp3')}'`).join('\n');
  spawnSync(FF, ['-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', String(PAUSA), '-c:a', 'libmp3lame', path.join(tmp, 'pausa.mp3')]);
  fs.writeFileSync(path.join(tmp, 'voce.txt'), ac);
  spawnSync(FF, ['-y', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'voce.txt'), '-ar', '44100', '-ac', '2', path.join(tmp, 'voce.wav')]);
  // base musicale molto bassa sotto la voce, in loop
  const basi = fs.readdirSync(path.join(QUI, '..', 'generatore', 'musica')).filter(f => f.endsWith('.m4a')).sort();
  const base = path.join(QUI, '..', 'generatore', 'musica', basi[0]);
  const r = spawnSync(FF, ['-y', '-i', path.join(tmp, 'muto.mp4'), '-i', path.join(tmp, 'voce.wav'),
    '-stream_loop', '-1', '-i', base,
    '-filter_complex', `[2:a]volume=0.07,afade=t=out:st=${(totale - 3).toFixed(2)}:d=3[m];[1:a][m]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5[a]`,
    '-map', '0:v', '-map', '[a]', '-c:v', 'copy',
    '-c:a', 'aac', '-ar', '48000', '-b:a', '192k', '-movflags', '+faststart', '-shortest', path.join(QUI, ID + '.mp4')]);
  if(r.status) console.error(r.stderr.toString().slice(-1500));
  const mmss = t => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
  fs.writeFileSync(path.join(QUI, ID + '-capitoli.txt'), capitoli.map(([t, c]) => `${mmss(t)} ${c}`).join('\n') + '\n');
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(ID + '.mp4', mmss(totale), scritti, 'fotogrammi');
})();
