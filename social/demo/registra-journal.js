/* Registra lo schermo del journal (fotogramma per fotogramma, nitido) seguendo i tempi della voce.
   uso: node registra-journal.js p02 → fotogrammi/p02/0000.jpg … */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ID = process.argv[2] || 'p02', FPS = 30;
const parole = JSON.parse(fs.readFileSync(path.join(__dirname, 'voce', ID + '.json')));
const DUR = parole[parole.length - 1][1] + 1.2;
const OUT = path.join(__dirname, 'fotogrammi', ID); fs.mkdirSync(OUT, { recursive: true });
const JR = 'file:///home/user/jr/index.html';
const quando = w => (parole.find(p => p[2].toLowerCase().startsWith(w)) || [0])[0];

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 360, height: 780 }, deviceScaleFactor: 3 });
  await ctx.route(/supabase\.co|cloudflareinsights/, r => r.abort());
  const p = await ctx.newPage();
  await p.addInitScript(() => { try{ localStorage.setItem('riskly-metodo','generale'); localStorage.setItem('riskly-metodo-chiesto','1'); localStorage.setItem('riskly-saldo-iniziale','10000'); localStorage.removeItem('riskly-scag-rapido'); localStorage.removeItem('riskly-vpip'); }catch(e){} });
  await p.goto(JR); await p.waitForTimeout(1200);
  await p.evaluate(() => { utente = { id:'u1', email:'demo@riskly.trade', user_metadata:{ metodo:'generale', saldo_iniziale:10000, nome:'Trader' } }; profilo = { piano:'pro' };
    j_trades = j_generaDemo(); aggiornaVista(); jVista('nuova'); document.querySelectorAll('.jchat,[class*=chat-btn]').forEach(e => e.remove()); [...document.querySelectorAll('header a, header button, nav a, nav button, .btn')].filter(e => /registrati|accedi/i.test(e.textContent)).forEach(e => e.style.visibility = 'hidden'); });
  await p.waitForTimeout(600);
  await p.addStyleTag({ content: '*{transition:none!important;animation:none!important;scroll-behavior:auto!important}' });

  /* azioni: [tempo, funzione] */
  const t = { scrivo: quando('scrivo'), lotti: quando('lotti'), stop: quando('stop'), tocco: quando('tocco'), quaranta: quando('quaranta'), rischio: quando('rischio'), dopo: quando('mese') - .4, sette: quando('sette') };
  const scriviA = async (sel, testo, t0, t1, tt) => {   /* digitazione progressiva */
    const n = Math.max(0, Math.min(testo.length, Math.floor((tt - t0) / Math.max(.05, (t1 - t0)) * testo.length + 1)));
    if(tt < t0) return;
    await p.evaluate(([s, v]) => { const el = document.querySelector(s); if(el.value === v) return; el.value = v; el.dispatchEvent(new Event('input', { bubbles:true })); }, [sel, testo.slice(0, n)]);
  };
  const scrollA = async (y) => p.evaluate(y => window.scrollTo(0, y), y);
  const yDi = async sel => p.evaluate(s => document.querySelector(s).getBoundingClientRect().top + scrollY, sel);
  const yForm = await yDi('#add') - 70, yScag = await yDi('#fScag') - 90;
  let fatto = {};
  const una = async (k, fn) => { if(!fatto[k]){ fatto[k] = 1; await fn(); } };
  const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);

  const N = Math.round(DUR * FPS);
  for(let f = 0; f < N; f++){
    const s = f / FPS;
    if(s < t.sette){
      if(s < t.dopo){
        /* modulo: scorre dal titolo alla sezione di calcolo, poi al riepilogo */
        let y = yForm;
        if(s > t.scrivo - .6) y = yForm + (yScag - yForm) * ease((s - (t.scrivo - .6)) / .6) * 0;
        await scriviA('#f-symbol', 'XAUUSD', t.scrivo, t.scrivo + .9, s);
        if(s >= t.scrivo) await una('scroll1', async () => {});
        const yS = await yDi('#fScag') - 90;
        const yR = await yDi('#scagStima') - 300;
        let target = yForm;
        if(s >= t.lotti - .5) target = yForm + (yS - yForm) * ease((s - (t.lotti - .5)) / .45);
        if(s >= t.rischio - .3) target = yS + (yR - yS) * ease((s - (t.rischio - .3)) / .5);
        await scrollA(target);
        await scriviA('#rp-tot', '0.50', t.lotti, t.lotti + .35, s);
        await scriviA('#rp-stop', '30', t.stop, t.stop + .25, s);
        if(s >= t.tocco + .55) await una('tp', () => p.click('[data-fine="tp"]'));
        if(s >= t.tocco + .55) await scriviA('#rp-fine', '40', t.quaranta, t.quaranta + .3, s);
      } else {
        await una('stat', async () => { await p.evaluate(() => { jVista('statistiche'); }); await p.waitForTimeout(300); });
        const yO = await p.evaluate(() => { const h = [...document.querySelectorAll('h3')].find(x => /fascia oraria/i.test(x.textContent)); return h ? h.closest('.jcard').getBoundingClientRect().top + scrollY - 120 : 0; });
        await scrollA(yO * ease((s - t.dopo) / .6));
      }
    }
    await p.screenshot({ path: path.join(OUT, String(f).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 88 });
  }
  console.log('fotogrammi', N, 'durata', DUR.toFixed(1));
  await b.close();
})();
