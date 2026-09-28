/* crea i PDF da HTML: node marketing/pdf/crea-pdf.js guida-journal-home */
const { chromium } = require('playwright');
(async()=>{const nome=process.argv[2]||'guida-journal-home';
const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+__dirname+'/'+nome+'.html'); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
await p.pdf({path:__dirname+'/'+nome+'.pdf',format:'A4',printBackground:true,margin:{top:0,right:0,bottom:0,left:0}});
await b.close();})();
