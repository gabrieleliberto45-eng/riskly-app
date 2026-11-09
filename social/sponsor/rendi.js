/* Rende il reel sponsor: sponsor.html fotogramma per fotogramma + voce (voce/s1…s6.mp3) + effetti sintetizzati + base musicale bassa.
   Prima: python3 social/sponsor/voce.py   Uso: node social/sponsor/rendi.js  → social/sponsor/sponsor.mp4
   Prova: node social/sponsor/rendi.js prova 1 5 12 → png dei secondi indicati */
const { chromium } = require('playwright');
const { spawn, spawnSync, execSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
const QUI = __dirname, FPS = 30, SR = 44100;
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const durata = f => { const o = spawnSync(FF, ['-i', f]).stderr.toString().match(/Duration: (\d+):(\d+):([\d.]+)/); return +o[1]*3600 + +o[2]*60 + +o[3]; };
function effetti(ev, tot, out){
  const n = Math.ceil((tot + 1) * SR), a = new Float32Array(n); let sm = 7; const rnd = () => (sm = (sm * 16807) % 2147483647) / 2147483647 * 2 - 1;
  for(const [t, k] of ev){ const i0 = Math.floor(t * SR);
    if(k === 'colpo') for(let i = 0; i < SR * .6 && i0 + i < n; i++){ const s = i / SR; a[i0 + i] += (Math.sin(2*Math.PI*(75 - 40*s)*s) * 1.0 + rnd() * .4 * Math.exp(-s/.02)) * Math.exp(-s/.14); }
    if(k === 'whoosh') for(let i = 0; i < SR * .7 && i0 + i < n; i++){ const s = i / SR, e = Math.sin(Math.PI * Math.min(1, s / .7)); a[i0 + i] += rnd() * .22 * e * e; }
    if(k === 'glitch') for(let i = 0; i < SR * .3 && i0 + i < n; i++){ const s = i / SR; a[i0 + i] += (Math.sign(Math.sin(2*Math.PI*(180 + 900*Math.floor(s*40)%7*60)*s)) * .25) * Math.exp(-s/.12); }
    if(k === 'tic') for(let i = 0; i < SR * .02 && i0 + i < n; i++) a[i0 + i] += rnd() * .3 * Math.exp(-i/(SR*.003)); }
  const b = Buffer.alloc(44 + n*2); b.write('RIFF',0); b.writeUInt32LE(36+n*2,4); b.write('WAVEfmt ',8); b.writeUInt32LE(16,16); b.writeUInt16LE(1,20); b.writeUInt16LE(1,22);
  b.writeUInt32LE(SR,24); b.writeUInt32LE(SR*2,28); b.writeUInt16LE(2,32); b.writeUInt16LE(16,34); b.write('data',36); b.writeUInt32LE(n*2,40);
  for(let i = 0; i < n; i++) b.writeInt16LE(Math.max(-32767, Math.min(32767, Math.round(a[i]*32767))), 44 + i*2); fs.writeFileSync(out, b);
}
(async () => {
  const parole = JSON.parse(fs.readFileSync(path.join(QUI, 'parole.json')));
  const voci = parole.map((_, i) => path.join(QUI, 'voce', `s${i + 1}.mp3`)), dur = voci.map(durata);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(QUI, 'sponsor.html'));
  await p.evaluate(async () => { await Promise.all(['400 100px ISerif', 'italic 400 100px ISerif', '600 40px ISans', '500 30px IMono'].map(f => document.fonts.load(f))); });
  const tot = await p.evaluate(([d, w]) => window.prepara(d, w), [dur, parole]); const ini = await p.evaluate(() => S.map(s => s.ini));
  console.log('durata', tot.toFixed(2), 'scene', ini.map(x => x.toFixed(2)).join(', '));
  if(process.argv[2] === 'prova'){ for(const s of process.argv.slice(3)){ await p.evaluate(t => window.disegna(t), +s); await p.screenshot({ path: path.join(os.tmpdir(), `sp-${s}.png`) }); console.log(`/tmp/sp-${s}.png`); } return b.close(); }
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'sp-')), fx = path.join(tmp, 'fx.wav');
  const ev = [[ini[2] + .02, 'colpo'], [ini[1] + 2.05, 'glitch'], [ini[1] + 2.05, 'colpo']]; ini.slice(1).forEach(x => ev.push([x - .05, 'whoosh']));
  [.2, 1.05, 1.9].forEach(x => ev.push([ini[1] + x, 'tic'])); parole[3].filter(w => /^(riskguard|trademanager|scalein)/i.test(w[1]) || /^riskly/i.test(w[1])).forEach(w => ev.push([ini[3] + w[0], 'tic']));
  effetti(ev, tot, fx);
  const musica = path.join(QUI, '..', 'generatore', 'musica', 'h.m4a');
  const vi = voci.map(v => ['-i', v]).flat();
  const rit = ini.map((x, i) => `[${i + 1}:a]adelay=${Math.round(x*1000)}|${Math.round(x*1000)},aformat=channel_layouts=stereo[v${i}]`).join(';');
  const n = ini.length, filtro = `${rit};${ini.map((_, i) => `[v${i}]`).join('')}amix=inputs=${n}:normalize=0[voce];[${n+1}:a]volume=0.9,aformat=channel_layouts=stereo[fx];`
    + `[${n+2}:a]volume=0.14,afade=t=in:d=0.5,afade=t=out:st=${(tot-1.8).toFixed(2)}:d=1.8,aformat=channel_layouts=stereo[mus];[voce][fx][mus]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]`;
  const mp4 = path.join(QUI, 'sponsor.mp4');
  const ff = spawn(FF, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', ...vi, '-i', fx, '-stream_loop', '-1', '-i', musica,
    '-filter_complex', filtro, '-map', '0:v', '-map', '[a]', '-t', tot.toFixed(3), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
  const fine = new Promise((ok, ko) => ff.on('close', c => c === 0 ? ok() : ko(new Error('ffmpeg ' + c))));
  const nf = Math.round(tot * FPS);
  for(let f = 0; f < nf; f++){ await p.evaluate(t => window.disegna(t), f / FPS); const buf = await p.screenshot({ type: 'jpeg', quality: 92 }); if(!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if(f % 300 === 0) console.log(f + '/' + nf); }
  ff.stdin.end(); await fine; await b.close(); console.log('→', mp4);
})();
