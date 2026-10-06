/* Riskly · animazioni del sito.
   - Scene di sfondo a tutta larghezza in cima alle pagine (canvas), una per tema:
       terreno  (home)        mercato caotico sotto, linea verde della disciplina sopra
       candele  (bot)         grafico che scorre; le candele che toccano lo stop diventano rosse
       montecarlo (calcoli)   ventaglio di percorsi simulati, quello mediano in verde
       onde     (altre)       nastri di luce lenti
     Si muovono da sole, con lo scorrimento e con il mouse / l'inclinazione del telefono.
   - Riquadri che si inclinano e si illuminano sotto il mouse (solo con mouse).
   Con "riduci movimento" attivo le scene restano ferme e i riquadri non si inclinano. */
(function(){
  const fermo = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let mx = 0, my = 0, tx = 0, ty = 0;
  addEventListener('pointermove', e => { tx = e.clientX / innerWidth * 2 - 1; ty = e.clientY / innerHeight * 2 - 1; }, { passive: true });
  addEventListener('deviceorientation', e => {
    if(e.gamma == null) return;
    tx = Math.max(-1, Math.min(1, e.gamma / 30)); ty = Math.max(-1, Math.min(1, (e.beta - 45) / 40));
  });

  /* generatore pseudo-casuale ripetibile */
  const rng = s => () => (s = (s * 9301 + 49297) % 233280) / 233280;

  const TEMI = {
    terreno(cx, W, H, t, s){
      const piccolo = W < 700, righe = piccolo ? 26 : 38, punti = piccolo ? 64 : 110;
      const f = Math.min(W, 1400) * .9;
      const orizzonte = H * ((piccolo ? .66 : .50) + s.scroll * .25) + my * 18;
      const camH = 3.2 + s.scroll * 2.2, ruota = mx * .18, avanti = t * .9;
      const quota = (x, z) => Math.sin(x * .42 + z * .55 + t * .6) * .55 + Math.sin(x * .17 - z * .31 + t * .25) * .9
        + Math.sin(x * 1.1 + z * 1.3 - t * .9) * .18 + Math.pow(Math.abs(Math.sin(x * .23 + z * .19 + t * .35)), 6) * 2.2;
      for(let r = righe; r >= 1; r--){
        const z = r * .9 + 1.2 - (avanti % .9), prof = 1 - z / (righe * .9 + 1.2);
        cx.beginPath(); let rosso = 0;
        for(let i = 0; i <= punti; i++){
          const u = i / punti * 2 - 1, x = u * z * 1.25 + ruota * z, h = quota(x, z + avanti);
          if(h > 2.15) rosso++;
          const sx = W / 2 + (x - ruota * z) / z * f * .5 + u * 40 * prof, sy = orizzonte + (camH - h) / z * f * .16;
          i ? cx.lineTo(sx, sy) : cx.moveTo(sx, sy);
        }
        const al = .05 + prof * prof * .42;
        cx.strokeStyle = rosso > punti * .12 ? `rgba(239,90,80,${al * .9})` : `rgba(182,216,79,${al})`;
        cx.lineWidth = .6 + prof * 1.1; cx.stroke();
      }
      const y0 = orizzonte - H * (piccolo ? .1 : .06), pend = H * (piccolo ? .06 : .13), linea = [];
      for(let i = 0; i <= 120; i++){
        const u = i / 120;
        linea.push([u * W, y0 + pend * (.5 - u) + Math.sin(u * 9 + t * 1.3) * 5 + Math.sin(u * 23 - t * 2) * 2 + mx * 10 * (u - .5)]);
      }
      lineaLuce(cx, W, linea, t);
    },

    candele(cx, W, H, t, s){
      const passo = W < 700 ? 16 : 22, n = Math.ceil(W / passo) + 3;
      const base = H * (.55 + s.scroll * .2) + my * 14, amp = H * .2;
      const stop = base + amp * .62;
      const off = (t * 26) % passo, k0 = Math.floor(t * 26 / passo);
      const prezzo = k => Math.sin(k * .21) * .55 + Math.sin(k * .057 + 1) * .8 + Math.sin(k * .9) * .12;
      for(let i = 0; i < n; i++){
        const k = k0 + i, x = i * passo - off + mx * 12;
        const a = base - prezzo(k) * amp, b = base - prezzo(k + 1) * amp;
        const r = rng(k * 7 + 3);
        const hi = Math.min(a, b) - r() * 16, lo = Math.max(a, b) + r() * 16;
        const tocca = lo >= stop - 2, su = b < a;
        const col = tocca ? '239,90,80' : (su ? '74,222,128' : '182,216,79');
        const al = .16 + .22 * Math.sin(Math.PI * i / n);
        cx.strokeStyle = `rgba(${col},${al})`; cx.fillStyle = `rgba(${col},${al})`; cx.lineWidth = 1.2;
        cx.beginPath(); cx.moveTo(x, hi); cx.lineTo(x, Math.min(lo, stop)); cx.stroke();
        cx.fillRect(x - passo * .28, Math.min(a, b), passo * .56, Math.max(2, Math.abs(b - a)));
      }
      cx.save(); cx.setLineDash([10, 9]); cx.lineDashOffset = -t * 30;
      cx.strokeStyle = 'rgba(239,90,80,.55)'; cx.lineWidth = 2;
      cx.beginPath(); cx.moveTo(0, stop); cx.lineTo(W, stop); cx.stroke(); cx.restore();
    },

    montecarlo(cx, W, H, t, s){
      const N = W < 700 ? 40 : 70, passi = 60, x0 = W * .06, x1 = W * .98;
      const y0 = H * (.40 + s.scroll * .2) + my * 12, ciclo = 9, fase = (t % ciclo) / ciclo;
      const lotto = Math.floor(t / ciclo), mostra = Math.min(1, fase * 1.6);
      const finali = [];
      for(let p = 0; p < N; p++){
        const r = rng(lotto * 997 + p * 31 + 1);
        let y = y0; cx.beginPath(); cx.moveTo(x0, y);
        const lim = Math.floor(passi * mostra);
        for(let i = 1; i <= lim; i++){
          y += (r() - .47) * H * .045;
          cx.lineTo(x0 + (x1 - x0) * i / passi + mx * 6 * i / passi, y);
        }
        finali.push(y);
        const male = y > y0 + H * .2;
        cx.strokeStyle = male ? 'rgba(239,90,80,.3)' : 'rgba(182,216,79,.24)';
        cx.lineWidth = 1; cx.stroke();
      }
      /* percorso tipico, più luminoso */
      const r = rng(lotto * 13 + 5), linea = [[x0, y0]]; let y = y0;
      for(let i = 1; i <= Math.floor(passi * mostra); i++){ y += (r() - .62) * H * .02; linea.push([x0 + (x1 - x0) * i / passi + mx * 6 * i / passi, y]); }
      lineaLuce(cx, W, linea, t, true);
      if(fase > .85){ cx.fillStyle = `rgba(11,13,12,${(fase - .85) / .15 * .9})`; cx.fillRect(0, 0, W, H); }
    },

    /* prezzi: barre che respirano e disegnano una curva che sale */
    barre(cx, W, H, t, s){
      const n = W < 700 ? 26 : 48, gap = W / n, base = H * (.86 + s.scroll * .1) + my * 10;
      const punti = [];
      for(let i = 0; i < n; i++){
        const u = i / (n - 1);
        const h = H * (.10 + u * .34) + Math.sin(i * .7 + t * 1.4) * H * .035 + Math.sin(i * .23 - t * .6) * H * .05;
        const x = i * gap + gap * .2 + mx * 10 * (u - .5);
        const g = cx.createLinearGradient(0, base - h, 0, base);
        const a = .10 + u * .22;
        g.addColorStop(0, `rgba(200,227,106,${a + .1})`); g.addColorStop(1, 'rgba(182,216,79,0)');
        cx.fillStyle = g; cx.fillRect(x, base - h, gap * .6, h);
        punti.push([x + gap * .3, base - h - 10]);
      }
      lineaLuce(cx, W, punti, t, true);
    },

    /* corso: costellazione di punti che si collegano */
    costellazione(cx, W, H, t, s){
      const n = W < 700 ? 34 : 70, lim = W < 700 ? 110 : 150, pts = [];
      for(let i = 0; i < n; i++){
        const r = rng(i * 53 + 7);
        const x = (r() * W + Math.sin(t * (.1 + r() * .2) + i) * 40 + mx * 20 * (r() - .3)) % W;
        const y = r() * H * .85 + Math.cos(t * (.12 + r() * .2) + i * 2) * 30 + s.scroll * H * .2 + my * 12;
        pts.push([x, y, r()]);
      }
      for(let i = 0; i < n; i++) for(let j = i + 1; j < n; j++){
        const dx = pts[i][0] - pts[j][0], dy = pts[i][1] - pts[j][1], d = Math.hypot(dx, dy);
        if(d < lim){ cx.strokeStyle = `rgba(182,216,79,${(1 - d / lim) * .28})`; cx.lineWidth = 1;
          cx.beginPath(); cx.moveTo(pts[i][0], pts[i][1]); cx.lineTo(pts[j][0], pts[j][1]); cx.stroke(); }
      }
      for(const [x, y, k] of pts){
        const luce = k > .82;
        cx.save(); cx.fillStyle = luce ? '#E2F28F' : 'rgba(200,227,106,.55)';
        if(luce){ cx.shadowColor = '#C8E36A'; cx.shadowBlur = 14; }
        cx.beginPath(); cx.arc(x, y, luce ? 3 : 1.8, 0, Math.PI * 2); cx.fill(); cx.restore();
      }
    },

    /* metodo: griglia in prospettiva che scorre, con una strada dritta al centro */
    griglia(cx, W, H, t, s){
      const oriz = H * (.38 + s.scroll * .15) + my * 14, cxp = W / 2 + mx * 40, f = H * .9;
      const avanti = (t * .6) % 1;
      for(let k = 0; k < 22; k++){                         // linee trasversali
        const z = 1 + k - avanti, y = oriz + f / z * .55;
        if(y > H) continue;
        cx.strokeStyle = `rgba(182,216,79,${Math.min(.35, .5 / z)})`; cx.lineWidth = 1;
        cx.beginPath(); cx.moveTo(0, y); cx.lineTo(W, y); cx.stroke();
      }
      for(let k = -14; k <= 14; k++){                      // linee verso l'orizzonte
        const xb = cxp + k * W * .09;
        cx.strokeStyle = `rgba(182,216,79,${k === 0 ? 0 : .14})`; cx.lineWidth = 1;
        cx.beginPath(); cx.moveTo(cxp + (xb - cxp) * .04, oriz); cx.lineTo(xb + (xb - cxp) * 1.5, H * 1.3); cx.stroke();
      }
      /* la strada: due bordi luminosi */
      for(const lato of [-1, 1]){
        const g = cx.createLinearGradient(0, oriz, 0, H);
        g.addColorStop(0, 'rgba(226,242,143,0)'); g.addColorStop(1, 'rgba(226,242,143,.9)');
        cx.save(); cx.strokeStyle = g; cx.lineWidth = 2.5; cx.shadowColor = '#C8E36A'; cx.shadowBlur = 14;
        cx.beginPath(); cx.moveTo(cxp + lato * 3, oriz); cx.lineTo(cxp + lato * W * .16, H * 1.05); cx.stroke(); cx.restore();
      }
      const sole = cx.createRadialGradient(cxp, oriz, 0, cxp, oriz, W * .25);
      sole.addColorStop(0, 'rgba(226,242,143,.35)'); sole.addColorStop(1, 'rgba(226,242,143,0)');
      cx.fillStyle = sole; cx.fillRect(0, 0, W, H);
    },

    onde(cx, W, H, t, s){
      const nastri = 5, base = H * (.58 + s.scroll * .2) + my * 14;
      for(let n = 0; n < nastri; n++){
        const fase = n * 1.3, amp = H * (.06 + n * .018), ver = n === 2;
        cx.beginPath();
        for(let i = 0; i <= 140; i++){
          const u = i / 140, x = u * W;
          const y = base + (n - 2) * H * .05 + Math.sin(u * (3 + n * .6) + t * (.35 + n * .07) + fase) * amp
            + Math.sin(u * 11 - t * .8 + n) * amp * .15 + mx * 14 * (u - .5);
          i ? cx.lineTo(x, y) : cx.moveTo(x, y);
        }
        const g = cx.createLinearGradient(0, 0, W, 0);
        const c = ver ? '226,242,143' : '182,216,79', a = ver ? .75 : .18 + n * .03;
        g.addColorStop(0, `rgba(${c},0)`); g.addColorStop(.3, `rgba(${c},${a})`); g.addColorStop(.7, `rgba(${c},${a})`); g.addColorStop(1, `rgba(${c},0)`);
        cx.save(); cx.strokeStyle = g; cx.lineWidth = ver ? 2.5 : 1.2;
        if(ver){ cx.shadowColor = 'rgba(200,227,106,.9)'; cx.shadowBlur = 16; }
        cx.stroke(); cx.restore();
      }
    }
  };

  /* linea verde luminosa con punto che ci corre sopra */
  function lineaLuce(cx, W, linea, t, finoAllaFine){
    if(linea.length < 2) return;
    const g = cx.createLinearGradient(0, 0, W, 0);
    g.addColorStop(0, 'rgba(200,227,106,0)'); g.addColorStop(.25, 'rgba(200,227,106,.85)');
    g.addColorStop(.75, 'rgba(226,242,143,1)'); g.addColorStop(1, finoAllaFine ? 'rgba(226,242,143,1)' : 'rgba(226,242,143,0)');
    for(const [lw, a, bl] of [[10, .18, 24], [3, 1, 10]]){
      cx.save(); cx.shadowColor = 'rgba(200,227,106,.9)'; cx.shadowBlur = bl; cx.globalAlpha = a;
      cx.strokeStyle = g; cx.lineWidth = lw; cx.lineJoin = 'round'; cx.lineCap = 'round';
      cx.beginPath(); linea.forEach(([x, y], i) => i ? cx.lineTo(x, y) : cx.moveTo(x, y)); cx.stroke(); cx.restore();
    }
    const [px, py] = finoAllaFine ? linea[linea.length - 1] : linea[Math.floor(((t * .08) % 1) * (linea.length - 1))];
    cx.save(); cx.fillStyle = '#F1F8C8'; cx.shadowColor = '#C8E36A'; cx.shadowBlur = 22;
    cx.beginPath(); cx.arc(px, py, 4.5, 0, Math.PI * 2); cx.fill(); cx.restore();
  }

  /* una scena: si ridimensiona con la sezione, si ferma quando non si vede */
  const scene = [];
  function scena(cv, tema){
    const sez = cv.parentElement, cx = cv.getContext('2d');
    const s = { cv, cx, sez, tema, W: 0, H: 0, scroll: 0, vista: false, t: 3 + Math.random() * 4 };
    s.misura = () => {
      const dpr = Math.min(devicePixelRatio || 1, 2);
      s.W = cv.clientWidth; s.H = cv.clientHeight;
      if(!s.W || !s.H) return;
      cv.width = s.W * dpr; cv.height = s.H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    s.disegna = () => {
      if(!s.W) s.misura(); if(!s.W) return;
      const r = sez.getBoundingClientRect();
      s.scroll = Math.max(0, Math.min(1, -r.top / Math.max(1, s.H)));
      cx.clearRect(0, 0, s.W, s.H); TEMI[tema](cx, s.W, s.H, s.t, s);
    };
    new IntersectionObserver(v => { s.vista = v[0].isIntersecting; if(s.vista){ s.misura(); if(fermo) s.disegna(); } }).observe(sez);
    scene.push(s); s.misura(); if(fermo) s.disegna();
  }
  addEventListener('resize', () => scene.forEach(s => s.misura()));
  if(fermo) addEventListener('scroll', () => scene.forEach(s => s.vista && s.disegna()), { passive: true });

  let ultimo = 0;
  function ciclo(ora){
    const dt = Math.min(.05, (ora - (ultimo || ora)) / 1000); ultimo = ora;
    mx += (tx - mx) * .05; my += (ty - my) * .05;
    for(const s of scene) if(s.vista){ s.t += dt; s.disegna(); }
    requestAnimationFrame(ciclo);
  }

  /* home: canvas già nel markup; le altre pagine: aggiunto in cima alla prima sezione */
  const home = document.getElementById('h-scena');
  if(home) scena(home, 'terreno');
  const TEMA_PAGINA = { bot: 'candele', calc: 'montecarlo', journal: 'barre', corso: 'costellazione', metodo: 'griglia', faq: 'onde' };
  for(const [id, tema] of Object.entries(TEMA_PAGINA)){
    const sez = document.querySelector(`#${id} > section:first-child`);
    if(!sez) continue;
    sez.classList.add('con-scena');
    const cv = document.createElement('canvas'); cv.className = 'scena-pag'; cv.setAttribute('aria-hidden', 'true');
    sez.prepend(cv); scena(cv, tema);
  }
  if(!fermo) requestAnimationFrame(ciclo);

  /* riquadri che si inclinano sotto il mouse */
  if(!fermo && matchMedia('(hover: hover) and (pointer: fine)').matches){
    const SEL = '.bot, .plan, .pz, .lancio-box, .pz-corso, #calc .card, .tool, .jcard';
    document.addEventListener('pointermove', e => {
      const el = e.target.closest && e.target.closest(SEL); if(!el) return;
      const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      el.style.setProperty('--mx', (x * 100).toFixed(1) + '%'); el.style.setProperty('--my', (y * 100).toFixed(1) + '%');
      el.style.transform = `perspective(900px) rotateX(${((.5 - y) * 4).toFixed(2)}deg) rotateY(${((x - .5) * 5).toFixed(2)}deg) translateY(-3px)`;
      el.classList.add('inclina');
    }, { passive: true });
    document.addEventListener('pointerout', e => {
      const el = e.target.closest && e.target.closest(SEL); if(!el || el.contains(e.relatedTarget)) return;
      el.style.transform = ''; el.classList.remove('inclina');
    }, { passive: true });
  }
})();
