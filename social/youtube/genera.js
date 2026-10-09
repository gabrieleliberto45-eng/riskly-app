/* Monta un video lungo YouTube (1920×1080) da social/youtube/<id>.json + voce/<id>-NN.mp3
   uso: node social/youtube/genera.js v01
   Ogni scena: gli elementi compaiono uno alla volta, distribuiti lungo la voce; tra una comparsa e l'altra
   l'immagine resta ferma (si rendono solo i fotogrammi delle animazioni). Esce <id>.mp4, <id>-miniatura.jpg, <id>-capitoli.txt */
const { chromium } = require('playwright');
const { execSync, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const QUI = __dirname, ID = process.argv[2] || 'v01';
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
const FPS = 30, ANIM = 0.7, PAUSA = 0.7;          // durata comparsa, silenzio tra le scene
const durata = f => { const o = spawnSync(FF, ['-i', f]).stderr.toString().match(/Duration: (\d+):(\d+):([\d.]+)/); return +o[1]*3600 + +o[2]*60 + +o[3]; };

(async () => {
  const spec = JSON.parse(fs.readFileSync(path.join(QUI, ID + '.json'), 'utf8'));
  const tmp = path.join(QUI, 'tmp-' + ID); fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.join(QUI, 'modello.html')); await p.evaluate(() => document.fonts.ready);

  const voci = spec.scene.map((s, i) => path.join(QUI, 'voce', `${ID}-${String(i + 1).padStart(2, '0')}.mp3`));
  const durate = voci.map(durata).map(d => d + PAUSA);
  const totale = durate.reduce((a, c) => a + c, 0);
  const lista = []; let fot = 0, inizio = 0; const capitoli = [];
  const scatto = async () => { const f = path.join(tmp, `f${String(fot++).padStart(5, '0')}.jpg`); await (await p.$('#v')).screenshot({ path: f, type: 'jpeg', quality: 90 }); return f; };

  for(let i = 0; i < spec.scene.length; i++){
    const s = spec.scene[i], D = durate[i];
    capitoli.push([inizio, s.capitolo]);
    const n = await p.evaluate(([s, i, N, a]) => window.scena(s, i, N, a), [s, i, spec.scene.length, (inizio + D / 2) / totale]);
    await p.evaluate(() => document.fonts.ready);
    // istanti di comparsa: titolo subito, il resto distribuito nel primo 75% della voce
    const tempi = [...Array(n)].map((_, k) => k === 0 ? 0 : Math.min(D - 1, 0.6 + (k / n) * D * 0.75));
    for(let k = 1; k <= n; k++){
      const fine = k < n ? tempi[k] : D;
      const passi = Math.round(ANIM * FPS);
      for(let f = 0; f < passi; f++){
        await p.evaluate(([k, t]) => window.mostra(k, t), [k, f / FPS]);
        lista.push([await scatto(), 1 / FPS]);
      }
      await p.evaluate(([k]) => window.mostra(k, 5), [k]);
      const resto = fine - tempi[k - 1] - ANIM;
      if(resto > 0.01) lista.push([await scatto(), resto]);
    }
    inizio += D;
    process.stdout.write(`scena ${i + 1}/${spec.scene.length}\r`);
  }
  // miniatura: scena 1 completa
  await p.evaluate(([s, N]) => { window.scena(s, 0, N, 0); window.mostra(99, 5); }, [spec.scene[0], spec.scene.length]);
  await (await p.$('#v')).screenshot({ path: path.join(QUI, ID + '-miniatura.jpg'), type: 'jpeg', quality: 92 });
  await b.close();

  // immagini → video
  const conc = lista.map(([f, d]) => `file '${f}'\nduration ${d.toFixed(4)}`).join('\n') + `\nfile '${lista[lista.length - 1][0]}'\n`;
  fs.writeFileSync(path.join(tmp, 'lista.txt'), conc);
  // voce: tracce in fila con la pausa tra le scene
  const ac = voci.map(v => `file '${v}'\nfile '${path.join(tmp, 'pausa.mp3')}'`).join('\n');
  spawnSync(FF, ['-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', String(PAUSA), '-c:a', 'libmp3lame', path.join(tmp, 'pausa.mp3')]);
  fs.writeFileSync(path.join(tmp, 'voce.txt'), ac);
  spawnSync(FF, ['-y', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'voce.txt'), '-ar', '44100', '-ac', '2', path.join(tmp, 'voce.wav')]);
  // base musicale molto bassa sotto la voce, in loop
  const basi = fs.readdirSync(path.join(QUI, '..', 'generatore', 'musica')).filter(f => f.endsWith('.m4a')).sort();
  const base = path.join(QUI, '..', 'generatore', 'musica', basi[0]);
  const r = spawnSync(FF, ['-y', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'lista.txt'), '-i', path.join(tmp, 'voce.wav'),
    '-stream_loop', '-1', '-i', base,
    '-filter_complex', `[2:a]volume=0.07,afade=t=out:st=${(totale - 3).toFixed(2)}:d=3[m];[1:a][m]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5[a]`,
    '-map', '0:v', '-map', '[a]', '-vf', `fps=${FPS},format=yuv420p`, '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
    '-c:a', 'aac', '-ar', '48000', '-b:a', '192k', '-movflags', '+faststart', '-shortest', path.join(QUI, ID + '.mp4')]);
  if(r.status) console.error(r.stderr.toString().slice(-1500));
  const mmss = t => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
  fs.writeFileSync(path.join(QUI, ID + '-capitoli.txt'), capitoli.map(([t, c]) => `${mmss(t)} ${c}`).join('\n') + '\n');
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('\n' + ID + '.mp4', mmss(totale), lista.length, 'immagini');
})();
