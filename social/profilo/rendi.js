const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2560,height:2400}});
await p.goto('file://'+__dirname+'/grafica.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await (await p.$('#avatar')).screenshot({path:__dirname+'/youtube-profilo.png'});
await (await p.$('#banner')).screenshot({path:__dirname+'/youtube-banner.png'});
await (await p.$('#og')).screenshot({path:__dirname+'/../../site/anteprima.png'});
await b.close();})();
