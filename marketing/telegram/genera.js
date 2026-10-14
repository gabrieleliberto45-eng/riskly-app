const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1024, height: 1024 } });
  for (const [f, t] of [['profilo-gestione.jpg', 'Gestione<br>del rischio'], ['profilo-analisi.jpg', 'Analisi<br>fondamentale']]) {
    await p.goto('file://' + __dirname + '/profilo.html?t=' + encodeURIComponent(t)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: __dirname + '/' + f, type: 'jpeg', quality: 92, clip: { x: 0, y: 0, width: 1024, height: 1024 } });
  }
  await b.close();
})();
