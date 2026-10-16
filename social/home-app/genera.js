/* fotogrammi di reel.html → reel.mp4 (1080×1920, 30 fps). uso: python3 -m http.server 8792 in social/ poi node genera.js [t1 t2 ...] (anteprime) */
const { chromium } = require('playwright'); const { execSync } = require('child_process'); const fs = require('fs');
(async () => {
  const ant = process.argv.slice(2).map(Number);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('http://127.0.0.1:8792/home-app/reel.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  if (ant.length) { for (const t of ant) { await p.evaluate(t => render(t), t); await p.screenshot({ path: `anteprima-${t}.jpg`, type: 'jpeg', quality: 80 }); } await b.close(); return; }
  fs.mkdirSync('fot', { recursive: true }); const D = await p.evaluate(() => DURATA), FPS = 30;
  for (let i = 0; i < D * FPS; i++) { await p.evaluate(t => render(t), i / FPS); await p.screenshot({ path: `fot/${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 88 }); }
  await b.close();
  const FF = process.env.FFMPEG || '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';
  execSync(`${FF} -v error -y -framerate ${FPS} -i fot/%04d.jpg -f lavfi -i anullsrc=r=44100:cl=stereo -shortest -c:v libx264 -crf 22 -pix_fmt yuv420p -c:a aac -movflags +faststart reel.mp4`);
  fs.rmSync('fot', { recursive: true }); console.log('reel.mp4', D, 's');
})();
