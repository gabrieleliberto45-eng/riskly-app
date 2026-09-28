/* icone per la schermata Home del journal: logo centrato con margine (le icone Android vengono ritagliate a cerchio) */
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:800,height:800}});
await p.goto('file://'+__dirname+'/grafica.html'); await p.evaluate(()=>document.fonts.ready);
await p.addStyleTag({content:'.avatar svg{width:430px!important;height:430px!important}'});
await p.waitForTimeout(300);
await (await p.$('#avatar')).screenshot({path:__dirname+'/icona-800.png'});
await b.close();})();
