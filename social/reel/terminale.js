/* Monta il reel "Terminale Riskly" (social/reel/terminale.html): voce + musica + effetti, 1080×1920 a 25 fps.
   Voce (Gabriele, 1° novembre: "con la voce"): social/youtube/term.json → python3 social/youtube/voce.py term.
   Il video si adatta alla voce: ogni pezzo della pagina (da 'inizio' a quello dopo) dura quanto la sua frase.
   Senza le tracce della voce resta la versione muta di 23,5 s.
   Uso: node social/reel/terminale.js [uscita.mp4]   (predefinito: social/reel/terminale.mp4) */
const { chromium } = require('playwright');
const { spawn, spawnSync, execSync } = require('child_process');
const fs = require('fs'), path = require('path');
const QUI = __dirname, OUT = process.argv[2] || path.join(QUI, 'terminale.mp4');
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const FPS = 25, SR = 44100, PAUSA = 0.3;
const durata = f => { const o = spawnSync(FF, ['-i', f]).stderr.toString().match(/Duration: (\d+):(\d+):([\d.]+)/); return +o[1]*3600 + +o[2]*60 + +o[3]; };

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
  const durStoria = await p.evaluate(() => window.DURATA), suoniStoria = await p.evaluate(() => window.suoni());
  // tempo del video (reale) → tempo della pagina (storia), a tratti: ogni pezzo dura quanto la sua frase
  const spec = JSON.parse(fs.readFileSync(path.join(QUI, '..', 'youtube', 'term.json')));
  const voci = spec.scene.map((x, i) => path.join(QUI, '..', 'youtube', 'voce', `term-${String(i + 1).padStart(2, '0')}.mp3`));
  const conVoce = voci.every(f => fs.existsSync(f));
  const S = [0, ...spec.scene.slice(1).map(x => x.inizio), durStoria];        // confini nella pagina
  let R = [0];                                                                  // confini nel video
  spec.scene.forEach((x, i) => {
    const pezzo = S[i + 1] - S[i];
    const parla = conVoce ? (i === 0 ? x.inizio : 0.12) + durata(voci[i]) + (i === spec.scene.length - 1 ? 1.0 : PAUSA) : pezzo;
    R.push(R[i] + Math.max(pezzo * 0.85, parla));
  });
  if(!conVoce) R = S.slice();
  const totale = R[R.length - 1];
  const storia = t => { for(let i = 1; i < R.length; i++) if(t <= R[i]) return S[i-1] + (t - R[i-1]) / (R[i] - R[i-1]) * (S[i] - S[i-1]); return durStoria; };
  const reale = x => { for(let i = 1; i < S.length; i++) if(x <= S[i]) return R[i-1] + (x - S[i-1]) / (S[i] - S[i-1]) * (R[i] - R[i-1]); return totale; };
  const eventi = suoniStoria.map(([x, k]) => [reale(x), k]);
  const partenze = spec.scene.map((x, i) => R[i] + (i === 0 ? x.inizio : 0.12));
  console.log(conVoce ? `con voce: ${totale.toFixed(1)} s` : 'senza voce');
  const video = path.join(tmp, 'video.mp4');
  const enc = spawn(FF, ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', video]);
  const n = Math.ceil(totale * FPS);
  for(let f = 0; f < n; f++){
    await p.evaluate(t => window.fotogramma(t), storia(f / FPS));
    const img = await p.screenshot({ type: 'jpeg', quality: 92 });
    if(!enc.stdin.write(img)) await new Promise(r => enc.stdin.once('drain', r));
    if(f % 100 === 0) console.log(`${f}/${n}`);
  }
  enc.stdin.end(); await new Promise(r => enc.on('close', r)); await b.close();
  effetti(eventi, totale, path.join(tmp, 'sfx.wav'));
  const basi = fs.readdirSync(path.join(QUI, '..', 'generatore', 'musica')).filter(f => f.endsWith('.m4a')).sort();
  // voce: le frasi una dopo l'altra, ognuna alla partenza del suo pezzo
  const ingressi = ['-i', video, '-i', path.join(tmp, 'sfx.wav'), '-stream_loop', '-1', '-i', path.join(QUI, '..', 'generatore', 'musica', basi[2] || basi[0])];
  let filtro = `[2:a]volume=${conVoce ? 0.14 : 0.32},afade=t=in:d=0.4,afade=t=out:st=${(totale - 1.5).toFixed(2)}:d=1.5[m];[1:a]volume=${conVoce ? 0.45 : 0.6}[x]`, mix = '[x][m]';
  if(conVoce){
    voci.forEach((f, i) => { ingressi.push('-i', f); const ms = Math.round(partenze[i] * 1000); filtro += `;[${3 + i}:a]aresample=${SR},adelay=${ms}|${ms},volume=1.6[v${i}]`; mix += `[v${i}]`; });
  }
  filtro += `;${mix}amix=inputs=${2 + (conVoce ? voci.length : 0)}:duration=longest:dropout_transition=0:normalize=0,loudnorm=I=-14:TP=-1.5[a]`;
  const r = spawnSync(FF, ['-y', '-v', 'error', ...ingressi, '-filter_complex', filtro,
    '-map', '0:v', '-map', '[a]', '-t', totale.toFixed(2), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', OUT]);
  if(r.status) { console.error(r.stderr.toString()); process.exit(1); }
  console.log('fatto', OUT);
})();
