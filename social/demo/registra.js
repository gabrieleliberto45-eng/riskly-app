/* Registra lo schermo per i reel demo, fotogramma per fotogramma, seguendo i tempi della voce.
   uso: node registra.js p01 [p04 ...]   → fotogrammi/pNN/0000.jpg …
   Le scene sono in scenari.js: pagina di partenza, preparazione e azioni agganciate alle parole. */
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs'), path = require('path');
const SCENARI = require('./scenari.js');
const FPS = 30, D = __dirname;
const FF = process.env.FFMPEG || execSync(`python3 -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())"`).toString().trim();

async function registra(b, ID){
  const sc = SCENARI[ID]; if(!sc) throw new Error('scena mancante ' + ID);
  const parole = JSON.parse(fs.readFileSync(path.join(D, 'voce', ID + '.json')));
  const DUR = parole[parole.length - 1][1] + 1.2, N = Math.round(DUR * FPS);
  const OUT = path.join(D, 'fotogrammi', ID); fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(OUT, { recursive: true });
  const W = w => { if(typeof w === 'number') return w; const [parola, n] = String(w).split('#');
    const lista = parole.filter(p => p[2].toLowerCase().replace(/[^a-zà-ù0-9']/g, '').startsWith(parola));
    const x = lista[(+n || 1) - 1]; if(!x) throw new Error(ID + ': parola non trovata ' + w); return x[0]; };

  /* corso: i fotogrammi arrivano dai video delle lezioni */
  if(sc.corso){
    let f = 0;
    for(const [file, da, w0] of sc.corso){
      const fine = sc.corso[sc.corso.indexOf(sc.corso.find(x => x[2] === w0)) + 1];
      const t1 = fine ? W(fine[2]) : DUR, t0 = W(w0);
      const n = Math.round((t1 - t0) * FPS);
      const tmp = path.join(OUT, 'seg'); fs.mkdirSync(tmp, { recursive: true });
      execSync(`"${FF}" -loglevel error -y -ss ${da} -i "${file}" -frames:v ${n} -vf fps=${FPS},scale=1440:-2 -q:v 3 "${tmp}/%05d.jpg"`);
      fs.readdirSync(tmp).sort().forEach(x => { fs.renameSync(path.join(tmp, x), path.join(OUT, String(f++).padStart(4, '0') + '.jpg')); });
      fs.rmSync(tmp, { recursive: true });
    }
    console.log(ID, 'fotogrammi', f, 'durata', DUR.toFixed(1)); return;
  }

  const ctx = await b.newContext({ viewport: { width: 360, height: 780 }, deviceScaleFactor: 3 });
  await ctx.route(/supabase\.co|cloudflareinsights|googletagmanager/, r => r.abort());
  const p = await ctx.newPage();
  await p.clock.install();
  if(sc.storage) await p.addInitScript(s => { try{ Object.entries(s).forEach(([k, v]) => v === null ? localStorage.removeItem(k) : localStorage.setItem(k, v)); }catch(e){} }, sc.storage);
  await p.goto(sc.app === 'jr' ? 'file:///home/user/jr/index.html' : 'file:///home/user/riskly-app/site/index.html');
  await p.clock.runFor(1200);
  await p.addStyleTag({ content: '#chatBtn,#chatBox,.jchat{display:none!important} *{scroll-behavior:auto!important}' });

  /* animazioni attive: [inizio, durata, funzione(progresso)] */
  let anim = [], vel = 1, t = 0;
  const ease = x => x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x);
  const H = {
    p, W, get t(){ return t; },
    velocita: v => { vel = v; },
    y: sel => p.evaluate(s => { const [q, n] = String(s).split('@'); const e = document.querySelectorAll(q)[+n || 0]; return e ? e.getBoundingClientRect().top + scrollY : 0; }, sel),
    scorri: async (dove, dur = .6, off = 80) => {
      const y1 = typeof dove === 'number' ? dove : Math.max(0, await H.y(dove) - off);
      const y0 = await p.evaluate(() => scrollY);
      anim.push([t, dur, k => p.evaluate(y => scrollTo(0, y), y0 + (y1 - y0) * ease(k))]);
    },
    scrivi: (sel, val, dur = .5) => anim.push([t, dur, k => p.evaluate(([s, v]) => { const e = document.querySelector(s); if(!e || e.value === v) return;
      e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }, [sel, val.slice(0, Math.max(1, Math.ceil(val.length * k)))])]),
    clic: sel => p.click(sel),
    js: (fn, arg) => p.evaluate(fn, arg),
    /* avvia una simulazione del sito e regola la velocità perché l'evento cada sulla parola */
    sim: async (k, msEvento, parolaEvento) => { const dt = W(parolaEvento) - t; vel = Math.max(.25, Math.min(2, msEvento / 1000 / dt)); await p.evaluate(k => window['play' + k](), k); },
  };
  if(sc.init) await sc.init(H);
  await p.clock.runFor(300);
  const passi = sc.passi.map(([w, fn]) => [W(w), fn]).sort((a, b) => a[0] - b[0]);
  let i = 0;
  for(let f = 0; f < N; f++){
    t = f / FPS;
    while(i < passi.length && passi[i][0] <= t){ await passi[i][1](H); i++; }
    for(const a of anim){ const k = (t - a[0]) / a[1]; if(k >= 0 && k <= 1.05) await a[2](Math.min(1, k)); }
    anim = anim.filter(a => (t - a[0]) / a[1] <= 1.05);
    await p.clock.runFor(1000 / FPS * vel);
    await p.screenshot({ path: path.join(OUT, String(f).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 88 });
  }
  console.log(ID, 'fotogrammi', N, 'durata', DUR.toFixed(1));
  await ctx.close();
}
(async () => { const b = await chromium.launch(); for(const id of process.argv.slice(2)) await registra(b, id); await b.close(); })();
