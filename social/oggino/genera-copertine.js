/* Copertine dei video "come funziona" (server 8792 in questa cartella): node genera-copertine.js → copertine/<id>.jpg */
const { chromium } = require('playwright'); const path = require('path');
const C = [
  ['b-risklypro', 'Riskly Pro', 'Lotto, notizie, scaglioni e trailing. Tutto in uno.', 11],
  ['b-riskguard', 'RiskGuard', 'Ti ferma dopo 3 perdite di fila.', 23],
  ['b-trademanager', 'TradeManager', 'Pareggio e trailing stop in automatico.', 37],
  ['b-scalein', 'ScaleIn', 'Una entrata, tre uscite.', 41],
  ['b-risklycopy', 'RisklyCopy', 'Copia le operazioni su tutti i tuoi conti.', 53],
];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('http://127.0.0.1:8792/copertina.html'); await p.waitForFunction(() => window.pronto); await p.evaluate(() => document.fonts.ready);
  for(const [id, nome, frase, seme] of C){
    await p.evaluate(c => window.copertina(c), { nome, frase, seme });
    await (await p.$('#c')).screenshot({ path: path.join(__dirname, 'copertine', id + '.jpg'), type: 'jpeg', quality: 90 }); console.log(id);
  }
  await b.close();
})();
