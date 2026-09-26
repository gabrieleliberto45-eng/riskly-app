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
    const ff = spawn(ffmpeg, ['-y', '-loglevel', 'error',
      '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
      '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium',
      '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', mp4], { stdio:['pipe', 'inherit', 'inherit'] });
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
    console.log(`${id}: ${durata.toFixed(1)}s, ${frame} frame → ${path.relative(process.cwd(), mp4)}`);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
