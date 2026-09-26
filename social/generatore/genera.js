/* Genera i video verticali (1080×1920, MP4) e le copertine dai file in social/video/*.json
   uso:  node social/generatore/genera.js [g01 g02 ...]   (senza argomenti li genera tutti)
   serve: playwright (Chromium) e ffmpeg — va bene quello di `pip install imageio-ffmpeg` */
const { chromium } = require('playwright');
const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30;
const CARTELLA = path.join(__dirname, '..', 'video');
const MODELLO = 'file://' + path.join(__dirname, 'modello.html');
const MUSICA = path.join(__dirname, 'musica');   // basi originali create da musica.py

/* base del video: "musica" nel json (a, b, c), altrimenti a rotazione sul numero del video */
function sceltaMusica(id, spec){
  const basi = fs.existsSync(MUSICA) ? fs.readdirSync(MUSICA).filter(f => f.endsWith('.m4a')).sort() : [];
  if(!basi.length) return null;
  if(spec.musica && basi.includes(spec.musica + '.m4a')) return path.join(MUSICA, spec.musica + '.m4a');
  const n = parseInt(id.replace(/\D/g, ''), 10) || 0;
  return path.join(MUSICA, basi[n % basi.length]);
}

function trovaFfmpeg(){
  if(process.env.FFMPEG) return process.env.FFMPEG;
  try{ execSync('ffmpeg -version', { stdio:'ignore' }); return 'ffmpeg'; }catch(e){}
  return execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
}

(async () => {
  const ffmpeg = trovaFfmpeg();
  const scelti = process.argv.slice(2);
  const specs = fs.readdirSync(CARTELLA).filter(f => f.endsWith('.json'))
    .map(f => f.replace('.json', ''))
    .filter(id => !scelti.length || scelti.includes(id)).sort();

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport:{ width:1080, height:1920 } });
  await page.goto(MODELLO);
  await page.evaluate(() => document.fonts.ready);

  for(const id of specs){
    const spec = JSON.parse(fs.readFileSync(path.join(CARTELLA, id + '.json'), 'utf8'));
    const durata = await page.evaluate(s => window.prepara(s), spec);
    await page.evaluate(() => document.fonts.ready);
    const frame = Math.round(durata * FPS);

    const mp4 = path.join(CARTELLA, id + '.mp4');
    const musica = sceltaMusica(id, spec);
    /* musica: entra morbida, esce con una dissolvenza di 1,5 s, volume uniformato per i social (−14 LUFS) */
    const ingressoAudio = musica ? ['-i', musica] : ['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo'];
    const filtroAudio = musica
      ? ['-af', `afade=t=in:d=0.4,afade=t=out:st=${(durata - 1.5).toFixed(2)}:d=1.5,loudnorm=I=-14:TP=-1.5:LRA=7`]
      : [];
    const ff = spawn(ffmpeg, ['-y', '-loglevel', 'error',
      '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      ...ingressoAudio,
      '-map', '0:v', '-map', '1:a', '-t', durata.toFixed(3), ...filtroAudio,
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium',
      '-c:a', 'aac', '-ar', '44100', '-b:a', musica ? '160k' : '64k', '-movflags', '+faststart', mp4], { stdio:['pipe', 'inherit', 'inherit'] });
    const fine = new Promise((ok, ko) => ff.on('close', c => c === 0 ? ok() : ko(new Error('ffmpeg ' + c))));

    for(let f = 0; f < frame; f++){
      await page.evaluate(t => window.disegna(t), f / FPS);
      const buf = await page.screenshot({ type:'jpeg', quality:92 });
      if(!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await fine;

    /* copertina: il gancio iniziale già tutto visibile */
    await page.evaluate(t => window.disegna(t), Math.min(spec.copertina ?? 2.6, durata - .1));
    await page.screenshot({ path: path.join(CARTELLA, id + '-copertina.jpg'), type:'jpeg', quality:90 });
    console.log(`${id}: ${durata.toFixed(1)}s, ${frame} frame, musica ${musica ? path.basename(musica) : 'nessuna'} → ${path.relative(process.cwd(), mp4)}`);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
