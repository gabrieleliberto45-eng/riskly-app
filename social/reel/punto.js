/* Monta un reel "Il punto" (social/reel/punto.html, deciso con Gabriele il 1° novembre: il ritmo del riferimento, ma grafica nostra): pagina opaca, niente video sotto,
   voce frase per frase con le pause ("pause": true nel json) e clic delle palette/timbri sotto la voce.
   Prima: python3 social/youtube/voce.py rNN  e  python3 social/reel/parole.py rNN
   Uso: node social/reel/punto.js rNN  → social/reel/rNN.mp4 */
const { chromium } = require('playwright');
const { spawn, spawnSync, execSync } = require('child_process');
const fs = require('fs'), path = require('path');
const QUI = __dirname, YT = path.join(QUI, '..', 'youtube');
const ID = process.argv[2];
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const FPS = 25, CODA = 0.3, VEL = 1, SR = 44100;
const durata = f => { const o = spawnSync(FF, ['-i', f]).stderr.toString().match(/Duration: (\d+):(\d+):([\d.]+)/); return +o[1]*3600 + +o[2]*60 + +o[3]; };

// effetti sintetizzati: clic secco, colpo basso, notifica a due toni
function effetti(eventi, totale, out){
  const n = Math.ceil((totale + 1) * SR), a = new Float32Array(n);
  let seme = 7; const rnd = () => (seme = (seme * 16807) % 2147483647) / 2147483647 * 2 - 1;
  for(const [t, tipo] of eventi){
    const i0 = Math.floor(t * SR); if(i0 < 0 || i0 >= n) continue;
    if(tipo === 'clic') for(let i = 0; i < SR * 0.012 && i0 + i < n; i++) a[i0 + i] += rnd() * 0.35 * Math.exp(-i / (SR * 0.002));
    if(tipo === 'colpo') for(let i = 0; i < SR * 0.25 && i0 + i < n; i++){ const s = i / SR; a[i0 + i] += (Math.sin(2 * Math.PI * (70 - 30 * s) * s) * 0.9 + rnd() * 0.25 * Math.exp(-s / 0.01)) * Math.exp(-s / 0.07); }
    if(tipo === 'notifica') for(let i = 0; i < SR * 0.5 && i0 + i < n; i++){ const s = i / SR, f = s < 0.12 ? 988 : 1319; a[i0 + i] += Math.sin(2 * Math.PI * f * s) * 0.35 * Math.exp(-((s % 0.12) || s) / 0.15); }
  }
  const b = Buffer.alloc(44 + n * 2);
  b.write('RIFF', 0); b.writeUInt32LE(36 + n * 2, 4); b.write('WAVEfmt ', 8); b.writeUInt32LE(16, 16); b.writeUInt16LE(1, 20); b.writeUInt16LE(1, 22);
  b.writeUInt32LE(SR, 24); b.writeUInt32LE(SR * 2, 28); b.writeUInt16LE(2, 32); b.writeUInt16LE(16, 34); b.write('data', 36); b.writeUInt32LE(n * 2, 40);
  for(let i = 0; i < n; i++) b.writeInt16LE(Math.max(-32767, Math.min(32767, Math.round(a[i] * 32767))), 44 + i * 2);
  fs.writeFileSync(out, b);
}

(async () => {
  const spec = JSON.parse(fs.readFileSync(path.join(YT, ID + '.json')));
  const parole = JSON.parse(fs.readFileSync(path.join(QUI, ID + '-parole.json'))).map(s => s.map(([t, w]) => [t / VEL, w]));
  const voci = spec.scene.map((s, i) => path.join(YT, 'voce', `${ID}-${String(i + 1).padStart(2, '0')}.mp3`));
  const dur = voci.map(v => durata(v) / VEL + CODA);
  const inizio = dur.map((d, i) => dur.slice(0, i).reduce((a, b) => a + b, 0));
  const totale = dur.reduce((a, b) => a + b, 0);
  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'punto-'));

  // voce: ogni traccia accelerata e allungata alla durata della sua scena
  const wav = voci.map((v, i) => { const o = path.join(tmp, `v${i}.wav`); spawnSync(FF, ['-y', '-v', 'error', '-i', v, '-af', `apad=whole_dur=${dur[i].toFixed(3)}`, '-ar', String(SR), '-ac', '1', o]); return o; });
  fs.writeFileSync(path.join(tmp, 'v.txt'), wav.map(p => `file '${p}'`).join('\n'));
  spawnSync(FF, ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'v.txt'), path.join(tmp, 'voce.wav')]);

  // video: la pagina fotogramma per fotogramma, direttamente in H.264
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(QUI, 'punto.html')); await p.evaluate(() => document.fonts.ready);
  const video = path.join(tmp, 'video.mp4');
  const enc = spawn(FF, ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', video]);
  const n = Math.ceil(totale * FPS); let scena = -1; const eventi = [];
  for(let f = 0; f < n; f++){
    const t = f / FPS; let i = inizio.findIndex((a, k) => t >= a && t < a + dur[k]); if(i < 0) i = spec.scene.length - 1;
    if(i !== scena){
      scena = i; await p.evaluate(([s, w, h]) => window.mostra(s, w, h), [spec.scene[i], parole[i] || [], [spec.data, i, spec.scene.length, dur[i], inizio[i]]]);
      eventi.push([inizio[i], 'colpo'], ...(await p.evaluate(() => window.suoni())).map(([x, k]) => [inizio[i] + x, k]));
    }
    const tl = t - inizio[i];
    const pw = parole[i] || []; let k = -1; pw.forEach((w, j) => { if(w[0] <= tl) k = j; });
    let testo = '';
    if(k >= 0 && tl < dur[i] - CODA + 0.1){ const g = Math.floor(k / 4) * 4; testo = pw.slice(g, g + 4).map((w, j) => g + j === k ? `<mark>${w[1]}</mark>` : w[1]).join(' '); }
    await p.evaluate(([a, b]) => window.fotogramma(a, b), [tl, testo]);
    const img = await p.screenshot({ type: 'jpeg', quality: 92 });
    if(!enc.stdin.write(img)) await new Promise(r => enc.stdin.once('drain', r));
    if(f % 100 === 0) console.log(`${f}/${n}`);
  }
  enc.stdin.end(); await new Promise(r => enc.on('close', r)); await b.close();
  effetti(eventi, totale, path.join(tmp, 'sfx.wav'));

  // tutto insieme: video + voce + clic + base musicale bassa
  const basi = fs.readdirSync(path.join(QUI, '..', 'generatore', 'musica')).filter(f => f.endsWith('.m4a')).sort();
  const out = path.join(QUI, ID + '.mp4');
  const r = spawnSync(FF, ['-y', '-v', 'error', '-i', video, '-i', path.join(tmp, 'voce.wav'), '-i', path.join(tmp, 'sfx.wav'),
    '-stream_loop', '-1', '-i', path.join(QUI, '..', 'generatore', 'musica', basi[1] || basi[0]),
    '-filter_complex', `[3:a]volume=0.09,afade=t=out:st=${(totale - 2).toFixed(2)}:d=2[m];[2:a]volume=0.45[x];[1:a][x][m]amix=inputs=3:duration=first:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.5[a]`,
    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-ar', '48000', '-b:a', '192k', '-movflags', '+faststart', '-t', totale.toFixed(2), out]);
  if(r.status) { console.error(r.stderr.toString().slice(-2000)); process.exit(1); }
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(`${ID}.mp4 ${Math.floor(totale / 60)}:${String(Math.round(totale % 60)).padStart(2, '0')}`);
})();
