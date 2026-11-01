/* Monta il reel "Terminale Riskly" (social/reel/terminale.html): niente voce, musica + effetti, 1080×1920 a 25 fps.
   Uso: node social/reel/terminale.js [uscita.mp4]   (predefinito: social/reel/terminale.mp4) */
const { chromium } = require('playwright');
const { spawn, spawnSync, execSync } = require('child_process');
const fs = require('fs'), path = require('path');
const QUI = __dirname, OUT = process.argv[2] || path.join(QUI, 'terminale.mp4');
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const FPS = 25, SR = 44100;

function effetti(eventi, totale, out){   // stessi suoni sintetizzati di punto.js
  const n = Math.ceil((totale + 1) * SR), a = new Float32Array(n);
  let seme = 7; const rnd = () => (seme = (seme * 16807) % 2147483647) / 2147483647 * 2 - 1;
  for(const [t, tipo] of eventi){
    const i0 = Math.floor(t * SR); if(i0 < 0 || i0 >= n) continue;
    if(tipo === 'clic') for(let i = 0; i < SR * 0.012 && i0 + i < n; i++) a[i0 + i] += rnd() * 0.35 * Math.exp(-i / (SR * 0.002));
    if(tipo === 'colpo') for(let i = 0; i < SR * 0.25 && i0 + i < n; i++){ const s = i / SR; a[i0 + i] += (Math.sin(2 * Math.PI * (70 - 30 * s) * s) * 0.9 + rnd() * 0.25 * Math.exp(-s / 0.01)) * Math.exp(-s / 0.07); }
    if(tipo === 'botto') for(let i = 0; i < SR * 0.7 && i0 + i < n; i++){ const s = i / SR; a[i0 + i] += (Math.sin(2 * Math.PI * (55 - 25 * s) * s) * 1.1 + rnd() * 0.5 * Math.exp(-s / 0.03) + rnd() * 0.15 * Math.exp(-s / 0.25)) * Math.exp(-s / 0.18); }
    if(tipo === 'notifica') for(let i = 0; i < SR * 0.5 && i0 + i < n; i++){ const s = i / SR, f = s < 0.12 ? 988 : 1319; a[i0 + i] += Math.sin(2 * Math.PI * f * s) * 0.35 * Math.exp(-((s % 0.12) || s) / 0.15); }
  }
  const b = Buffer.alloc(44 + n * 2);
  b.write('RIFF', 0); b.writeUInt32LE(36 + n * 2, 4); b.write('WAVEfmt ', 8); b.writeUInt32LE(16, 16); b.writeUInt16LE(1, 20); b.writeUInt16LE(1, 22);
  b.writeUInt32LE(SR, 24); b.writeUInt32LE(SR * 2, 28); b.writeUInt16LE(2, 32); b.writeUInt16LE(16, 34); b.write('data', 36); b.writeUInt32LE(n * 2, 40);
  for(let i = 0; i < n; i++) b.writeInt16LE(Math.max(-32767, Math.min(32767, Math.round(a[i] * 32767))), 44 + i * 2);
  fs.writeFileSync(out, b);
}

(async () => {
  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'term-'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(QUI, 'terminale.html')); await p.evaluate(() => document.fonts.ready);
  const totale = await p.evaluate(() => window.DURATA), eventi = await p.evaluate(() => window.suoni());
  const video = path.join(tmp, 'video.mp4');
  const enc = spawn(FF, ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', video]);
  const n = Math.ceil(totale * FPS);
  for(let f = 0; f < n; f++){
    await p.evaluate(t => window.fotogramma(t), f / FPS);
    const img = await p.screenshot({ type: 'jpeg', quality: 92 });
    if(!enc.stdin.write(img)) await new Promise(r => enc.stdin.once('drain', r));
    if(f % 100 === 0) console.log(`${f}/${n}`);
  }
  enc.stdin.end(); await new Promise(r => enc.on('close', r)); await b.close();
  effetti(eventi, totale, path.join(tmp, 'sfx.wav'));
  const basi = fs.readdirSync(path.join(QUI, '..', 'generatore', 'musica')).filter(f => f.endsWith('.m4a')).sort();
  const r = spawnSync(FF, ['-y', '-v', 'error', '-i', video, '-i', path.join(tmp, 'sfx.wav'),
    '-stream_loop', '-1', '-i', path.join(QUI, '..', 'generatore', 'musica', basi[2] || basi[0]),
    '-filter_complex', `[2:a]volume=0.32,afade=t=in:d=0.4,afade=t=out:st=${(totale - 1.5).toFixed(2)}:d=1.5[m];[1:a]volume=0.6[x];[x][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.5[a]`,
    '-map', '0:v', '-map', '[a]', '-t', totale.toFixed(2), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', OUT]);
  if(r.status) { console.error(r.stderr.toString()); process.exit(1); }
  console.log('fatto', OUT);
})();
