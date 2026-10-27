/* Monta un reel verticale 1080×1920 nello stile "schede su video vero" con i colori del sito (richiesta di Gabriele, 27 ottobre).
   Prima: python3 social/youtube/voce.py rNN  e  python3 social/reel/parole.py rNN
   Uso: node social/reel/rendi.js rNN  → social/reel/rNN.mp4
   Sfondo: clip di social/reel/broll/<nome>.mp4 (Pexels, crediti nella didascalia), scurite e appena calde.
   Sopra: social/reel/modello.html renderizzata trasparente fotogramma per fotogramma. */
const { chromium } = require('playwright');
const { spawn, spawnSync, execSync } = require('child_process');
const fs = require('fs'), path = require('path');
const QUI = __dirname, YT = path.join(QUI, '..', 'youtube');
const ID = process.argv[2];
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const FPS = 25, CODA = 0.35;
const durata = f => { const o = spawnSync(FF, ['-i', f]).stderr.toString().match(/Duration: (\d+):(\d+):([\d.]+)/); return +o[1]*3600 + +o[2]*60 + +o[3]; };

(async () => {
  const spec = JSON.parse(fs.readFileSync(path.join(YT, ID + '.json')));
  const parole = JSON.parse(fs.readFileSync(path.join(QUI, ID + '-parole.json')));
  const voci = spec.scene.map((s, i) => path.join(YT, 'voce', `${ID}-${String(i + 1).padStart(2, '0')}.mp3`));
  const dur = voci.map(v => durata(v) + CODA);
  const inizio = dur.map((d, i) => dur.slice(0, i).reduce((a, b) => a + b, 0));
  const totale = dur.reduce((a, b) => a + b, 0);
  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'reel-'));

  // 1. sfondo: una clip per scena, riempie 1080×1920, scurita e tinta (rossa nel gancio se "tinta": "rosso")
  const pezzi = spec.scene.map((s, i) => {
    const o = path.join(tmp, `b${i}.mp4`);
    const tinta = s.tinta === 'rosso' ? 'colorbalance=rs=.25:gs=-.1:bs=-.1:rm=.2' : 'colorbalance=rs=.06:gs=.02:bs=-.08:rm=.05:bm=-.05';
    const vf = `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=${FPS},${tinta},eq=brightness=-0.18:saturation=0.75:contrast=1.05,gblur=sigma=1.2,` +
      `drawbox=c=black@0.38:t=fill,fade=t=in:st=0:d=0.25`;
    const r = spawnSync(FF, ['-y', '-v', 'error', '-stream_loop', '-1', '-i', path.join(QUI, 'broll', s.broll + '.mp4'), '-t', dur[i].toFixed(3), '-vf', vf, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', o]);
    if(r.status) throw new Error(r.stderr.toString());
    return o;
  });
  fs.writeFileSync(path.join(tmp, 'b.txt'), pezzi.map(p => `file '${p}'`).join('\n'));
  spawnSync(FF, ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'b.txt'), '-c', 'copy', path.join(tmp, 'sfondo.mp4')]);

  // 2. voce: tracce in fila, ognuna allungata alla durata della sua scena
  const wav = voci.map((v, i) => { const o = path.join(tmp, `v${i}.wav`); spawnSync(FF, ['-y', '-v', 'error', '-i', v, '-af', `apad=whole_dur=${dur[i].toFixed(3)}`, '-ar', '44100', '-ac', '1', o]); return o; });
  fs.writeFileSync(path.join(tmp, 'v.txt'), wav.map(p => `file '${p}'`).join('\n'));
  spawnSync(FF, ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'v.txt'), path.join(tmp, 'voce.wav')]);

  // 3. grafica trasparente, fotogramma per fotogramma, in un video con canale alfa
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(QUI, 'modello.html')); await p.evaluate(() => document.fonts.ready);
  const enc = spawn(FF, ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-', '-c:v', 'png', path.join(tmp, 'grafica.mov')]);
  const n = Math.ceil(totale * FPS); let scena = -1;
  for(let f = 0; f < n; f++){
    const t = f / FPS; let i = inizio.findIndex((a, k) => t >= a && t < a + dur[k]); if(i < 0) i = spec.scene.length - 1;
    if(i !== scena){ scena = i; await p.evaluate(s => window.mostra(s), spec.scene[i]); }
    const tl = t - inizio[i];
    // sottotitolo: gruppi di 4 parole, l'ultima detta evidenziata
    const pw = parole[i] || []; let k = -1; pw.forEach((w, j) => { if(w[0] <= tl) k = j; });
    let testo = '';
    if(k >= 0 && tl < dur[i] - CODA + 0.15){ const g = Math.floor(k / 4) * 4; testo = pw.slice(g, g + 4).map((w, j) => g + j === k ? `<mark>${w[1]}</mark>` : w[1]).join(' '); }
    await p.evaluate(([a, b]) => window.fotogramma(a, b), [tl, testo]);
    const img = await p.screenshot({ omitBackground: true, type: 'png' });
    if(!enc.stdin.write(img)) await new Promise(r => enc.stdin.once('drain', r));
    if(f % 100 === 0) console.log(`${f}/${n}`);
  }
  enc.stdin.end(); await new Promise(r => enc.on('close', r)); await b.close();

  // 4. tutto insieme: sfondo + grafica + voce + base musicale bassa
  const basi = fs.readdirSync(path.join(QUI, '..', 'generatore', 'musica')).filter(f => f.endsWith('.m4a')).sort();
  const out = path.join(QUI, ID + '.mp4');
  const r = spawnSync(FF, ['-y', '-v', 'error', '-i', path.join(tmp, 'sfondo.mp4'), '-i', path.join(tmp, 'grafica.mov'), '-i', path.join(tmp, 'voce.wav'),
    '-stream_loop', '-1', '-i', path.join(QUI, '..', 'generatore', 'musica', basi[0]),
    '-filter_complex', `[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v];[3:a]volume=0.08,afade=t=out:st=${(totale - 2).toFixed(2)}:d=2[m];[2:a][m]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5[a]`,
    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-c:a', 'aac', '-ar', '48000', '-b:a', '192k', '-movflags', '+faststart', '-t', totale.toFixed(2), out]);
  if(r.status) { console.error(r.stderr.toString().slice(-2000)); process.exit(1); }
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(`${ID}.mp4 ${Math.floor(totale / 60)}:${String(Math.round(totale % 60)).padStart(2, '0')}`);
})();
