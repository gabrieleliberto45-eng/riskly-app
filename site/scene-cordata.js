/* Riskly · mondo "Cordata": curve di livello vive dietro tutto il sito.
   Ogni pagina è una montagna diversa; scorrendo la carta sale di quota.
   Con "riduci movimento" la carta resta ferma e si muove solo con lo scorrimento. */
(function(){
  const fermo = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const MONTI = { home:11, bot:23, calc:37, app:41, journal:53, corso:67, metodo:71, faq:83 };

  function picchi(seme){
    let x = seme * 9301 + 49297;
    const rnd = () => (x = (x * 9301 + 49297) % 233280) / 233280;
    const p = [];
    for(let i = 0; i < 7; i++) p.push({ x: rnd(), y: rnd() * 1.6 - .3, h: .55 + rnd() * .9, s: .12 + rnd() * .22 });
    return p;
  }

  // quota in un punto: somma di cime morbide + un po' di rugosità
  function quota(P, x, y, t){
    let z = 0;
    for(const p of P){
      const dx = x - p.x - Math.sin(t * .07 + p.h) * .02, dy = y - p.y;
      z += p.h * Math.exp(-(dx * dx + dy * dy) / (2 * p.s * p.s));
    }
    return z + .06 * Math.sin(x * 9 + t * .05) * Math.cos(y * 7 - t * .04);
  }

  // marching squares: traccia le isolinee del campo su una griglia
  function curve(cx, W, H, P, t, scroll, colore, passoQuota, maestra){
    const C = W > 900 ? 12 : 10, nx = Math.ceil(W / C) + 1, ny = Math.ceil(H / C) + 1;
    const g = new Float32Array(nx * ny), asp = H / W;
    for(let j = 0; j < ny; j++) for(let i = 0; i < nx; i++)
      g[j * nx + i] = quota(P, i / (nx - 1), (j / (ny - 1)) * asp + scroll, t);
    const livelli = [];
    for(let l = passoQuota; l < 1.8; l += passoQuota) livelli.push(l);
    livelli.forEach((L, k) => {
      const indice = (k + 1) % 5 === 0;
      cx.beginPath();
      for(let j = 0; j < ny - 1; j++) for(let i = 0; i < nx - 1; i++){
        const a = g[j*nx+i], b = g[j*nx+i+1], c = g[(j+1)*nx+i+1], d = g[(j+1)*nx+i];
        const m = (a > L) | (b > L) << 1 | (c > L) << 2 | (d > L) << 3;
        if(m === 0 || m === 15) continue;
        const x = i * C, y = j * C;
        const e = [
          [x + C * (L - a) / (b - a), y],
          [x + C, y + C * (L - b) / (c - b)],
          [x + C * (L - d) / (c - d), y + C],
          [x, y + C * (L - a) / (d - a)]
        ];
        const seg = (p, q) => { cx.moveTo(e[p][0], e[p][1]); cx.lineTo(e[q][0], e[q][1]); };
        switch(m){
          case 1: case 14: seg(3,0); break;  case 2: case 13: seg(0,1); break;
          case 3: case 12: seg(3,1); break;  case 4: case 11: seg(1,2); break;
          case 6: case 9:  seg(0,2); break;  case 7: case 8:  seg(3,2); break;
          case 5: seg(3,0); seg(1,2); break; case 10: seg(0,1); seg(3,2); break;
        }
      }
      cx.strokeStyle = indice ? maestra : colore;
      cx.lineWidth = indice ? 1.4 : .8;
      cx.stroke();
    });
  }

  function pittore(cv, opz){
    const cx = cv.getContext('2d');
    const s = { W: 0, H: 0, P: picchi(MONTI.home), Pa: null, mix: 1 };
    function misura(){
      const r = cv.getBoundingClientRect(), dpr = Math.min(devicePixelRatio || 1, 2);
      s.W = Math.max(1, r.width); s.H = Math.max(1, r.height);
      cv.width = s.W * dpr; cv.height = s.H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function picchiCorrenti(){
      if(!s.Pa || s.mix >= 1) return s.P;
      const k = 1 - Math.pow(1 - s.mix, 3);
      return s.P.map((p, i) => { const q = s.Pa[i]; return { x: q.x + (p.x - q.x) * k, y: q.y + (p.y - q.y) * k, h: q.h + (p.h - q.h) * k, s: q.s + (p.s - q.s) * k }; });
    }
    return {
      misura,
      cambia(seme){ s.Pa = picchiCorrenti(); s.P = picchi(seme); s.mix = 0; },
      disegna(t){
        if(s.mix < 1) s.mix = Math.min(1, s.mix + .04);
        cx.clearRect(0, 0, s.W, s.H);
        curve(cx, s.W, s.H, picchiCorrenti(), t, opz.scroll(), opz.colore, opz.passo, opz.maestra);
      }
    };
  }

  // sfondo di tutto il sito
  const cv = document.createElement('canvas');
  cv.id = 'sfondo'; cv.setAttribute('aria-hidden', 'true');
  document.body.prepend(cv);
  const fondo = pittore(cv, { colore: 'rgba(47,93,124,.16)', maestra: 'rgba(47,93,124,.30)', passo: .075,
    scroll: () => scrollY / Math.max(innerWidth, 1) * .35 });

  // carta sopra il campo arancio dell'apertura
  const hc = document.querySelector('.hero-topo');
  const apertura = hc ? pittore(hc, { colore: 'rgba(28,33,36,.16)', maestra: 'rgba(28,33,36,.32)', passo: .09, scroll: () => .15 }) : null;

  function misuraTutto(){ fondo.misura(); if(apertura) apertura.misura(); }
  misuraTutto();
  addEventListener('resize', misuraTutto);

  let pagina = 'home';
  new MutationObserver(() => {
    const on = document.querySelector('.page.on');
    if(on && on.id !== pagina){ pagina = on.id; fondo.cambia(MONTI[pagina] || 97); }
  }).observe(document.body, { subtree: true, attributes: true, attributeFilter: ['class'] });

  let t = 0, ultimo = 0, sporco = true;
  addEventListener('scroll', () => { sporco = true; }, { passive: true });
  function giro(ora){
    if(ora - ultimo > 66 && (!fermo || sporco)){   // ~15 fotogrammi al secondo bastano a una carta che respira
      ultimo = ora; if(!fermo) t += .066;
      fondo.disegna(t);
      if(apertura && scrollY < innerHeight * 1.2) apertura.disegna(t * 1.4);
      sporco = false;
    }
    requestAnimationFrame(giro);
  }
  requestAnimationFrame(giro);
})();
