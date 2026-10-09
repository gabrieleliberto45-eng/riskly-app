/* miniatura YouTube 1280×720 dal modello: testo enorme, un numero evidenziato */
const { chromium } = require('playwright'); const path = require('path');
const [id, grande, piccolo] = process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.join(__dirname,'modello.html'));await p.evaluate(()=>document.fonts.ready);
await p.evaluate(([g,s])=>{window.scena({tipo:'titolo',capitolo:'Guida completa',grande:g,piccolo:s},0,1,1);window.mostra(9,5);
  const G=document.querySelector('.grande');G.style.fontSize='230px';G.style.lineHeight='.92';
  document.querySelector('.piccolo').style.cssText+='font-size:64px;color:#EEF2EA;font-weight:700;margin-top:50px';
  document.querySelector('.testa span:last-child').textContent='';document.querySelector('.barra').remove();},[grande,piccolo]);
await p.evaluate(()=>document.fonts.ready);
await (await p.$('#v')).screenshot({path:path.join(__dirname,id+'-miniatura.jpg'),type:'jpeg',quality:92});await b.close();})();
