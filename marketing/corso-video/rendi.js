// Disegna le slide (slide.html) in PNG 1920x1080 secondo out/manifest.json
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const man = JSON.parse(fs.readFileSync(path.join(__dirname, 'out', 'manifest.json'), 'utf8'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.join(__dirname, 'slide.html')); await p.evaluate(() => document.fonts.ready);
  let n = 0, nuovi = 0;
  for (const m of man) {
    const f = path.join(__dirname, 'out', 'png', m.png + '.png'); n++;
    if (fs.existsSync(f) && !process.env.RIFAI) continue;
    await p.evaluate(([s, k, i]) => window.mostra(s, k, i), [m.slide, m.k, m.info]);
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(30);
    await p.screenshot({ path: f }); nuovi++;
  }
  console.log(n, 'passaggi,', nuovi, 'immagini nuove'); await b.close();
})();
