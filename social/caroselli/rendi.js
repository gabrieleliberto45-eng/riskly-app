/* Rende i caroselli (1080×1350, JPG) da social/caroselli/caroselli.json
   uso: node social/caroselli/rendi.js [c01-lotto ...] */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dati = JSON.parse(fs.readFileSync(path.join(__dirname, 'caroselli.json'), 'utf8'));
  const scelti = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(__dirname, 'modello.html'));
  await p.evaluate(() => document.fonts.ready);
  for(const c of dati){
    if(scelti.length && !scelti.includes(c.id)) continue;
    const dir = path.join(__dirname, c.id); fs.mkdirSync(dir, { recursive: true });
    for(let i = 0; i < c.slide.length; i++){
      await p.evaluate(([d, i, n]) => window.mostra(d, i, n), [c.slide[i], i, c.slide.length]);
      await p.evaluate(() => document.fonts.ready);
      await (await p.$('#s')).screenshot({ path: path.join(dir, String(i + 1).padStart(2, '0') + '.jpg'), type: 'jpeg', quality: 92 });
    }
    console.log(c.id, c.slide.length, 'slide');
  }
  await b.close();
})();
