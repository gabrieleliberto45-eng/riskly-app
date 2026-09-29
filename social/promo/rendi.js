/* Rende il video di presentazione: promo.html fotogramma per fotogramma + voce (voce/w1…w7.mp3) + base musicale.
   uso:  node social/promo/rendi.js                → social/promo/riskly-presentazione.mp4
         node social/promo/rendi.js prova 3 12 40  → solo i fotogrammi a 3 s, 12 s, 40 s (png, per controllo)
   serve: playwright (Chromium) e ffmpeg — va bene quello di `pip install imageio-ffmpeg`
   MUSICA=percorso.m4a per scegliere la base (serve lunga almeno quanto il video: musica.py con DURATA più alta) */
const { chromium } = require('playwright');
const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30, CART = __dirname;
const ffmpeg = process.env.FFMPEG || (() => { try{ execSync('ffmpeg -version', { stdio:'ignore' }); return 'ffmpeg'; }
  catch(e){ return execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim(); } })();

(async () => {
  const parole = JSON.parse(fs.readFileSync(path.join(CART, 'parole.json'), 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport:{ width:1080, height:1920 } });
  await page.goto('file://' + path.join(CART, 'promo.html'));
  await page.evaluate(() => document.fonts.ready);
  const durata = await page.evaluate(d => window.prepara(d), { parole });
  const inizi = await page.evaluate(() => S.map(s => s.ini));
  console.log('durata', durata.toFixed(2), 's · scene a', inizi.map(x => x.toFixed(2)).join(', '));

  if(process.argv[2] === 'prova'){
    for(const s of process.argv.slice(3)){
      await page.evaluate(t => window.disegna(t), +s);
      await page.screenshot({ path: path.join(CART, `prova-${s}.png`) });
    }
    return browser.close();
  }

  /* audio: voci alle loro posizioni + musica bassa sotto, uniformato a −14 LUFS */
  const musica = process.env.MUSICA || path.join(CART, '..', 'generatore', 'musica', 'h.m4a');
  const voci = inizi.map((_, i) => ['-i', path.join(CART, 'voce', `w${i + 1}.mp3`)]).flat();
  const ritardi = inizi.map((x, i) => `[${i + 1}:a]adelay=${Math.round(x * 1000)}|${Math.round(x * 1000)},aformat=channel_layouts=stereo[v${i}]`).join(';');
  const filtro = `${ritardi};${inizi.map((_, i) => `[v${i}]`).join('')}amix=inputs=${inizi.length}:normalize=0,volume=1.0[voce];`
    + `[${inizi.length + 1}:a]volume=0.16,afade=t=in:d=0.6,afade=t=out:st=${(durata - 2).toFixed(2)}:d=2[mus];`
    + `[voce][mus]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]`;
  const mp4 = path.join(CART, 'riskly-presentazione.mp4');
  const ff = spawn(ffmpeg, ['-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    ...voci, '-stream_loop', '-1', '-i', musica,
    '-filter_complex', filtro, '-map', '0:v', '-map', '[a]', '-t', durata.toFixed(3),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium',
    '-c:a', 'aac', '-ar', '44100', '-b:a', '192k', '-movflags', '+faststart', mp4], { stdio:['pipe', 'inherit', 'inherit'] });
  const fine = new Promise((ok, ko) => ff.on('close', c => c === 0 ? ok() : ko(new Error('ffmpeg ' + c))));
  const n = Math.round(durata * FPS);
  for(let f = 0; f < n; f++){
    await page.evaluate(t => window.disegna(t), f / FPS);
    const buf = await page.screenshot({ type:'jpeg', quality:92 });
    if(!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if(f % 300 === 0) console.log(`${f}/${n}`);
  }
  ff.stdin.end(); await fine; await browser.close();
  console.log('→', mp4);
})();
