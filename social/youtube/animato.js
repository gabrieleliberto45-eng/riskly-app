/* Video lungo YouTube ANIMATO (1920×1080), come i reel (Gabriele, 18/11/2026).
   Prima: voce (python3 social/youtube/voce.py vNN) e tempi delle parole (python3 social/youtube/parole.py vNN).
   Uso: node social/youtube/animato.js vNN [--fumetto]        → social/youtube/vNN-animato.mp4 + vNN-capitoli.txt
   Prova: node social/youtube/animato.js vNN prova 3 40 90   → png dei secondi indicati nella scratchpad di sistema */
const { chromium } = require('playwright');
const { spawn, spawnSync, execSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
const QUI = __dirname, ID = process.argv[2], ARG = process.argv.slice(3).filter(a => !a.startsWith('--'));
const FUMETTO = process.argv.includes('--fumetto'), FPS = 25, SR = 44100;
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const durata = f => { const o = spawnSync(FF, ['-i', f]).stderr.toString().match(/Duration: (\d+):(\d+):([\d.]+)/); return +o[1]*3600 + +o[2]*60 + +o[3]; };
function effetti(ev, tot, out){
  const n = Math.ceil((tot + 1) * SR), a = new Float32Array(n); let sm = 7; const rnd = () => (sm = (sm * 16807) % 2147483647) / 2147483647 * 2 - 1;
  for(const [t, k] of ev){ const i0 = Math.floor(t * SR); if(i0 < 0) continue;
    if(k === 'colpo') for(let i = 0; i < SR * .6 && i0 + i < n; i++){ const s = i / SR; a[i0 + i] += (Math.sin(2*Math.PI*(75 - 40*s)*s) + rnd() * .4 * Math.exp(-s/.02)) * Math.exp(-s/.14) * .8; }
    if(k === 'whoosh') for(let i = 0; i < SR * .7 && i0 + i < n; i++){ const s = i / SR, e = Math.sin(Math.PI * Math.min(1, s / .7)); a[i0 + i] += rnd() * .16 * e * e; }
    if(k === 'riser') for(let i = 0; i < SR && i0 + i < n; i++){ const s = i / SR; a[i0 + i] += (rnd() * .2 + Math.sin(2*Math.PI*(200 + 1400*s*s)*s) * .1) * s * s; }
    if(k === 'notifica') for(let i = 0; i < SR * .5 && i0 + i < n; i++){ const s = i / SR, f = s < .12 ? 988 : 1319; a[i0 + i] += Math.sin(2*Math.PI*f*s) * .3 * Math.exp(-(s < .12 ? s : s - .12) / .15); }
    if(k === 'tic') for(let i = 0; i < SR * .02 && i0 + i < n; i++) a[i0 + i] += rnd() * .25 * Math.exp(-i/(SR*.003)); }
  const b = Buffer.alloc(44 + n*2); b.write('RIFF',0); b.writeUInt32LE(36+n*2,4); b.write('WAVEfmt ',8); b.writeUInt32LE(16,16); b.writeUInt16LE(1,20); b.writeUInt16LE(1,22);
  b.writeUInt32LE(SR,24); b.writeUInt32LE(SR*2,28); b.writeUInt16LE(2,32); b.writeUInt16LE(16,34); b.write('data',36); b.writeUInt32LE(n*2,40);
  for(let i = 0; i < n; i++) b.writeInt16LE(Math.max(-32767, Math.min(32767, Math.round(a[i]*32767))), 44 + i*2); fs.writeFileSync(out, b);
}
(async () => {
  const spec = JSON.parse(fs.readFileSync(path.join(QUI, ID + '.json'), 'utf8'));
  const parole = JSON.parse(fs.readFileSync(path.join(QUI, `parole-${ID}.json`), 'utf8'));
  const voci = spec.scene.map((s, i) => path.join(QUI, 'voce', `${ID}-${String(i + 1).padStart(2, '0')}.mp3`)), dur = voci.map(durata);
  /* serie orarie dei grafici: oro/<lunedì>.json accanto al png */
  const serie = {}; spec.scene.filter(s => s.tipo === 'grafico' && s.img).forEach(s => { const j = path.join(QUI, s.img.replace(/\.png$/, '.json')); if(fs.existsSync(j)){ const d = JSON.parse(fs.readFileSync(j, 'utf8')); serie[s.img] = { serie: d.serie_oro || [], massimo: d.oro?.massimo, minimo: d.oro?.minimo, quando_max: d.oro?.quando_max, quando_min: d.oro?.quando_min, var_pct: d.oro?.var_pct }; } });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.join(QUI, 'animato.html') + (FUMETTO ? '?tema=fumetto' : ''));
  await p.evaluate(async () => { await Promise.all(['400 100px ISerif', 'italic 400 100px ISerif', '600 40px ISans', '500 30px IMono', '400 100px Bangers', '700 40px Comic'].map(f => document.fonts.load(f))); });
  const { tot, ini } = await p.evaluate(([s, d, w, z]) => window.prepara(s, d, w, z), [spec, dur, parole, serie]);
  console.log('durata', tot.toFixed(1), 's · scene', ini.map(x => x.toFixed(1)).join(', '));
  const cap = ini.map((x, i) => `${Math.floor(x / 60)}:${String(Math.floor(x % 60)).padStart(2, '0')} ${spec.scene[i].capitolo}`); cap[0] = '0:00 ' + spec.scene[0].capitolo;
  if(ARG[0] !== 'prova') fs.writeFileSync(path.join(QUI, `${ID}-capitoli.txt`), cap.join('\n') + '\n');
  if(ARG[0] === 'prova'){ for(const s of ARG.slice(1)){ await p.evaluate(t => window.disegna(t), +s); const f = path.join(os.tmpdir(), `yt-${ID}-${s}.png`); await p.screenshot({ path: f }); console.log(f); } return b.close(); }
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'yt-')), fx = path.join(tmp, 'fx.wav'); effetti(await p.evaluate(() => window.eventi()), tot, fx);
  const musica = path.join(QUI, '..', 'generatore', 'musica', 'h.m4a'), n = ini.length;
  const filtro = ini.map((x, i) => `[${i + 1}:a]adelay=${Math.round(x*1000)}|${Math.round(x*1000)},aformat=channel_layouts=stereo[v${i}]`).join(';') + ';' + ini.map((_, i) => `[v${i}]`).join('') + `amix=inputs=${n}:normalize=0[voce];`
    + `[${n+1}:a]volume=0.8,aformat=channel_layouts=stereo[fx];[${n+2}:a]volume=0.11,afade=t=in:d=1,afade=t=out:st=${(tot-3).toFixed(2)}:d=3,aformat=channel_layouts=stereo[mus];[voce][fx][mus]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]`;
  const mp4 = path.join(QUI, `${ID}-animato${FUMETTO ? '-fumetto' : ''}.mp4`);
  const ff = spawn(FF, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', ...voci.flatMap(v => ['-i', v]), '-i', fx, '-stream_loop', '-1', '-i', musica,
    '-filter_complex', filtro, '-map', '0:v', '-map', '[a]', '-t', tot.toFixed(3), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
  const fine = new Promise((ok, ko) => ff.on('close', c => c === 0 ? ok() : ko(new Error('ffmpeg ' + c))));
  const nf = Math.round(tot * FPS);
  for(let f = 0; f < nf; f++){ await p.evaluate(t => window.disegna(t), f / FPS); const buf = await p.screenshot({ type: 'jpeg', quality: 88 }); if(!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if(f % 500 === 0) console.log(f + '/' + nf); }
  ff.stdin.end(); await fine; await b.close(); console.log('→', mp4);
})();
