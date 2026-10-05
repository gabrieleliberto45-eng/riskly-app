/* Compone il reel: modello.html + fotogrammi dello schermo + voce + base musicale bassa
   uso: node componi.js p02 → ../video/p02.mp4 */
const { chromium } = require('playwright');
const { spawn, execSync } = require('child_process');
const fs = require('fs'), path = require('path');
const ID = process.argv[2], FPS = 30, D = __dirname;
const cfg = JSON.parse(fs.readFileSync(path.join(D, 'testi-video.json')))[ID];
const parole = JSON.parse(fs.readFileSync(path.join(D, 'voce', ID + '.json')));
const FR = path.join(D, 'fotogrammi', ID), frames = fs.readdirSync(FR).filter(f => f.endsWith('.jpg')).sort();
const fine = parole[parole.length - 1][1] + .3, DUR = fine + 2.2;
const ffmpeg = process.env.FFMPEG || execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const musica = path.join(D, '..', 'generatore', 'musica', (cfg.musica || 'e') + '.m4a');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(D, 'modello.html')); await p.evaluate(() => document.fonts.ready);
  const tw = w => w === '' ? 0 : ((parole.find(x => x[2].toLowerCase().startsWith(w)) || [0])[0]);
  cfg.titoli = cfg.titoli.map(([k, h]) => [typeof k === 'string' ? tw(k) : k, h]);
  await p.evaluate(s => window.prepara(s), Object.assign({}, cfg, { parole, fine }));
  const out = path.join(D, '..', 'video', ID + '.mp4');
  const ff = spawn(ffmpeg, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', path.join(D, 'voce', ID + '.mp3'), '-i', musica,
    '-filter_complex', `[1:a]adelay=0|0,volume=1.0[v];[2:a]volume=0.14,afade=t=out:st=${(DUR - 1.2).toFixed(2)}:d=1.2[m];[v][m]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]`,
    '-map', '0:v', '-map', '[a]', '-t', DUR.toFixed(2), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-ar', '44100', '-ac', '2', '-b:a', '160k', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const chiuso = new Promise(r => ff.on('close', r));
  const N = Math.round(DUR * FPS);
  for(let f = 0; f < N; f++){
    const src = 'file://' + path.join(FR, frames[Math.min(f, frames.length - 1)]);
    await p.evaluate(([t, s]) => window.disegna(t, s), [f / FPS, src]);
    const buf = await p.screenshot({ type: 'jpeg', quality: 90 });
    if(!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if(f === Math.round(2 * FPS)) await p.screenshot({ path: path.join(D, ID + '-copertina.jpg'), type: 'jpeg', quality: 88 });
  }
  ff.stdin.end(); await chiuso; await b.close(); console.log(out, DUR.toFixed(1) + ' s');
})();
