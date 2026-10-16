/* schermate reali di strumenti.riskly.trade per il reel (server locale su nuovo/strumenti, porta 8811) */
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
await p.route(/supabase|googleapis/, r=>r.abort());
await p.goto('http://127.0.0.1:8811/?da=reel#posizione');await p.waitForTimeout(1200);
await p.evaluate(()=>{ if(window.strTab) strTab('posizione'); });
await p.selectOption('#c-sym','XAUUSD');await p.fill('#c-bal','10000');await p.fill('#c-risk','1');await p.fill('#c-pips','30');
await p.evaluate(()=>window.scrollTo(0,0));await p.waitForTimeout(300);
await p.screenshot({path:'sito-alto.png'});
await (await p.$('#c-pips')).scrollIntoViewIfNeeded(); await p.evaluate(()=>window.scrollBy(0,120)); await p.waitForTimeout(300);
await p.screenshot({path:'sito-calc.png'});
await b.close()})();
