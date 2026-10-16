/* PDF delle dispense: node pdf.js rischio [modulo-02]  (con NODE_PATH=$(npm root -g) se playwright è globale) */
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const corso = process.argv[2], solo = process.argv[3], dir = path.join(__dirname, 'out', corso);
  const nomi = { rischio: 'Gestione del rischio', fondamentale: 'Analisi fondamentale' };
  const b = await chromium.launch(); const p = await b.newPage();
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html') && (!solo || f.startsWith(solo))).sort()) {
    await p.goto('file://' + path.join(dir, f)); await p.evaluate(() => document.fonts.ready);
    const piede = `<div style="width:100%;font-family:Arial;font-size:7.5px;color:#8a9097;padding:0 16mm;display:flex;justify-content:space-between">
      <span>Riskly · ${nomi[corso]} · ${f.replace('.html', '').replace('modulo-', 'Modulo ')}</span><span>riskly.trade · <span class="pageNumber"></span>/<span class="totalPages"></span></span></div>`;
    await p.pdf({ path: path.join(dir, f.replace('.html', '.pdf')), format: 'A4', printBackground: true, preferCSSPageSize: true,
      displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: piede });
    console.log(f);
  }
  await b.close();
})();
