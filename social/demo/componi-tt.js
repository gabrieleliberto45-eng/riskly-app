/* Versione corta per TikTok: tiene solo alcune frasi della voce (vedi tagli-tt.json)
   e ricompone il reel con gli stessi fotogrammi, titoli e sottotitoli rimappati.
   uso: node componi-tt.js p02 → ../video/tt/p02.mp4 */
const { chromium } = require('playwright');
const { spawn, execSync } = require('child_process');
const fs = require('fs'), path = require('path');
const ID = process.argv[2], FPS = 30, D = __dirname;
const cfg = JSON.parse(fs.readFileSync(path.join(D, 'testi-video.json')))[ID];
const testo = JSON.parse(fs.readFileSync(path.join(D, 'testi.json')))[ID];
const tieni = JSON.parse(fs.readFileSync(path.join(D, 'tagli-tt.json')))[ID];
const tutte = JSON.parse(fs.readFileSync(path.join(D, 'voce', ID + '.json')));
const FR = path.join(D, 'fotogrammi', ID), frames = fs.readdirSync(FR).filter(f => f.endsWith('.jpg')).sort();
const ffmpeg = process.env.FFMPEG || execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const musica = path.join(D, '..', 'generatore', 'musica', (cfg.musica || 'e') + '.m4a');

// frasi → intervalli di parole (le parole della voce sono allineate 1:1 con il testo)
const frasi = testo.split(/(?<=[.?!])\s+/);
let k = 0; const fr = frasi.map(s => { const n = s.split(/\s+/).length; const r = tutte.slice(k, k + n); k += n; return r; });
if(k !== tutte.length) throw new Error(ID + ': testo e voce non allineati');
// segmenti nel tempo originale, con un po' di respiro prima e dopo
const seg = tieni.map(i => {
  const w = fr[i], prima = i > 0 ? fr[i - 1][fr[i - 1].length - 1][1] : 0, dopo = i < fr.length - 1 ? fr[i + 1][0][0] : w[w.length - 1][1] + 1;
  return [Math.max(prima, w[0][0] - .12), Math.min(dopo, w[w.length - 1][1] + .28), w];
});
let off = 0; const mappa = seg.map(([a, b]) => { const m = [a, b, off]; off += b - a; return m; });
const VOCE = off, fine = VOCE + .15, DUR = fine + 2.2;
const fuori = t => { for(const [a, b, o] of mappa){ if(t < a) return o; if(t <= b) return o + t - a; } return VOCE; };
const sorgente = t => { for(const [a, b, o] of mappa) if(t <= o + (b - a)) return a + Math.max(0, t - o); const u = mappa[mappa.length - 1]; return u[1]; };
const parole = seg.flatMap(([, , w]) => w.map(x => [fuori(x[0]), fuori(x[1]), x[2]]));

(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(D, 'modello.html')); await p.evaluate(() => document.fonts.ready);
  const tw = w => { if(w === '') return 0; const [q, n] = w.split('#'); const l = tutte.filter(x => x[2].toLowerCase().replace(/[^a-zà-ù0-9']/g, '').startsWith(q)); const x = l[(+n || 1) - 1]; if(!x) throw new Error(ID + ': titolo, parola non trovata ' + w); return x[0]; };
  const titoli = cfg.titoli.map(([k, h]) => [fuori(typeof k === 'string' ? tw(k) : k), h]).filter(x => x[0] < VOCE);
  await p.evaluate(s => window.prepara(s), Object.assign({}, cfg, { titoli, parole, fine }));
  fs.mkdirSync(path.join(D, '..', 'video', 'tt'), { recursive: true });
  const out = path.join(D, '..', 'video', 'tt', ID + '.mp4');
  const trim = mappa.map(([a, b], i) => `[1:a]atrim=${a.toFixed(3)}:${b.toFixed(3)},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st=${(b - a - .03).toFixed(3)}:d=0.03[s${i}]`).join(';');
  const ff = spawn(ffmpeg, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', path.join(D, 'voce', ID + '.mp3'), '-i', musica,
    '-filter_complex', `${trim};${mappa.map((_, i) => `[s${i}]`).join('')}concat=n=${mappa.length}:v=0:a=1[v];[2:a]volume=0.14,afade=t=out:st=${(DUR - 1.2).toFixed(2)}:d=1.2[m];[v][m]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]`,
    '-map', '0:v', '-map', '[a]', '-t', DUR.toFixed(2), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-ar', '44100', '-ac', '2', '-b:a', '160k', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const chiuso = new Promise(r => ff.on('close', r));
  const N = Math.round(DUR * FPS);
  for(let f = 0; f < N; f++){
    const t = f / FPS, i = Math.round(sorgente(Math.min(t, VOCE)) * FPS);
    const src = 'file://' + path.join(FR, frames[Math.min(i, frames.length - 1)]);
    await p.evaluate(([t, s]) => window.disegna(t, s), [t, src]);
    const buf = await p.screenshot({ type: 'jpeg', quality: 90 });
    if(!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await chiuso; await b.close(); console.log(out, DUR.toFixed(1) + ' s');
})();
