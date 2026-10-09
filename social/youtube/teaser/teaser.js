/* Clip verticali (1080×1920) che portano al video YouTube: cornice con gancio + spezzone del video 16:9 + invito
   uso: node teaser.js <video.mp4> <uscita.mp4> <inizio s> <durata s> '<json testi cornice>' */
const { chromium } = require('playwright'); const { execSync, spawnSync } = require('child_process'); const path = require('path');
const [src, out, ss, dur, testi] = process.argv.slice(2);
const FF = execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'cornice.html')); await p.evaluate(o => window.imposta(o), JSON.parse(testi));
  await p.evaluate(() => document.fonts.ready); const png = out.replace(/\.mp4$/, '-cornice.png');
  await p.screenshot({ path: png }); await b.close();
  const r = spawnSync(FF, ['-y', '-loop', '1', '-i', png, '-ss', ss, '-t', dur, '-i', src,
    '-filter_complex', `[1:v]scale=1080:608[v];[0:v][v]overlay=0:740:shortest=1,format=yuv420p[o];[1:a]afade=t=in:d=0.3,afade=t=out:st=${(+dur - 1).toFixed(2)}:d=1[a]`,
    '-map', '[o]', '-map', '[a]', '-r', '30', '-c:v', 'libx264', '-crf', '21', '-c:a', 'aac', '-ar', '48000', '-movflags', '+faststart', out]);
  if(r.status) console.error(r.stderr.toString().slice(-800)); else console.log(out);
})();
