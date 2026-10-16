const { chromium } = require('playwright'); const path = require('path');
const A = [
  ['../riskly/anteprima.png', { nome: 'Riskly', titolo: 'Il mercato non<br>lo controlli.<br><mark>Tutto il resto sì.</mark>', sotto: 'BOT MT4/MT5 · CORSI · JOURNAL · CALCOLATORI · <b>RISKLY.TRADE</b>' }],
  ['../strumenti/anteprima.png', { nome: 'Riskly · Strumenti', titolo: 'Calendario economico<br>e calcolatori.<br><mark>Gratis, prima del trade.</mark>', sotto: 'LOTTO · RISCHIO DI ROVINA · PROP FIRM · <b>STRUMENTI.RISKLY.TRADE</b>' }],
];
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + path.join(__dirname, 'anteprima.html'));
  for (const [f, d] of A) { await p.evaluate(d => mostra(d), d); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
    await (await p.$('#c')).screenshot({ path: path.join(__dirname, f) }); console.log(f); }
  await b.close(); })();
