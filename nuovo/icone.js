/* icone Riskly (riquadro chiaro, linea oro, base grigia) in tutte le misure.
   uso: node nuovo/icone.js <cartella>   → apple-touch-icon.png, icon-192.png, icon-512.png, favicon-32.png, favicon-48.png */
const { chromium } = require('playwright'); const path = require('path');
const svg = (s, r) => `<html><body style="margin:0;background:transparent"><svg width="${s}" height="${s}" viewBox="0 0 44 44"><rect width="44" height="44" rx="${r}" fill="#FBFBF9"/><path d="M10 30 L17 20 L23 25 L34 12" stroke="#B97C00" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/><path d="M10 34.5 H34" stroke="#5E656D" stroke-width="3.6" stroke-linecap="round"/></svg></body></html>`;
(async () => {
  const dir = process.argv[2]; const b = await chromium.launch(); const p = await b.newPage();
  /* le icone delle app hanno angoli dritti (li arrotonda il telefono); le favicon e la foto profilo sono arrotondate */
  for (const [s, f, r] of [[180, 'apple-touch-icon.png', 0], [192, 'icon-192.png', 0], [512, 'icon-512.png', 0], [32, 'favicon-32.png', 9], [48, 'favicon-48.png', 9], [800, 'icona-800.png', 0]]) {
    await p.setViewportSize({ width: s, height: s }); await p.setContent(svg(s, r));
    await p.screenshot({ path: path.join(dir, f), omitBackground: true });
  }
  await b.close();
})();
