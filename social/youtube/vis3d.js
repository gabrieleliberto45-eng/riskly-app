/* Scene 3D dei video lunghi: una per capitolo, animate nel tempo t (secondi dall'inizio della scena).
   window.vis.imposta(tipo) prepara la scena, window.vis.disegna(t) disegna il fotogramma. */
import * as THREE from './three/three.module.min.js';

const LIME = 0xB6D84F, SU = 0x22C55E, GIU = 0xEF4444, ORO = 0xE8B84A, GRIGIO = 0x3A423A, TESTO = 0xEEF2EA;
const cv = document.getElementById('gl');
const gl = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, preserveDrawingBuffer: true });
gl.setPixelRatio(1); gl.setSize(cv.width, cv.height, false); gl.setClearColor(0x000000, 0);
const cam = new THREE.PerspectiveCamera(36, cv.width / cv.height, .1, 200);
let scena = null, agg = () => {}, orbita = { r: 14, h: 5, guarda: new THREE.Vector3(0, 1.5, 0), giri: .06 };

const ease = x => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .45, metalness: .25, ...o });
const bordi = (geo, c = TESTO, op = .5) => new THREE.LineSegments(new THREE.EdgesGeometry(geo), new THREE.LineBasicMaterial({ color: c, transparent: true, opacity: op }));
function base(){
  const s = new THREE.Scene();
  s.add(new THREE.AmbientLight(0xffffff, .7));
  const l = new THREE.DirectionalLight(0xffffff, 1.6); l.position.set(5, 10, 7); s.add(l);
  const l2 = new THREE.DirectionalLight(LIME, .5); l2.position.set(-6, 3, -4); s.add(l2);
  const g = new THREE.GridHelper(40, 40, 0x2A3A1A, 0x1A201A); g.material.transparent = true; g.material.opacity = .6; s.add(g);
  return s;
}
let seme = 3; const rnd = () => (seme = (seme * 16807) % 2147483647) / 2147483647;

const V = {
  /* candele che scendono fino alla lastra rossa dello stop e si fermano */
  candele(){
    const s = base(), N = 26, c = []; let p = 3;
    for(let i = 0; i < N; i++){ const o = p; p += (i < 18 ? -.22 : .18) + (rnd() - .5) * .35; p = Math.max(p, .55); c.push([o, p]); }
    const corpi = c.map(([o, cl], i) => {
      const m = new THREE.Mesh(new THREE.BoxGeometry(.5, 1, .5), mat(cl >= o ? SU : GIU));
      m.position.set((i - N / 2) * .62, (o + cl), 0); m.userData.h = Math.max(Math.abs(cl - o) * 2, .1); s.add(m); return m;
    });
    const stop = new THREE.Mesh(new THREE.BoxGeometry(N * .62 + 1, .04, 3), new THREE.MeshBasicMaterial({ color: GIU, transparent: true, opacity: .35 }));
    stop.position.y = 1.0; s.add(stop); { const bb = bordi(new THREE.BoxGeometry(N * .62 + 1, .04, 3), GIU, .9); bb.position.copy(stop.position); s.add(bb); }
    agg = t => corpi.forEach((m, i) => { const e = ease(t * 1.4 - i * .12); m.scale.y = Math.max(e * m.userData.h, .001); m.visible = e > 0; });
    orbita = { r: 12, h: 3.5, guarda: new THREE.Vector3(0, 2.6, 0), giri: .05 };
    return s;
  },
  /* due pile di monete: stesso trade, 100 $ contro 1.000 $ */
  pile(){
    const s = base(), geo = new THREE.CylinderGeometry(.9, .9, .18, 40), pile = [[], []];
    [[-2.2, 4], [2.2, 30]].forEach(([x, n], k) => { for(let i = 0; i < n; i++){ const m = new THREE.Mesh(geo, mat(ORO, { metalness: .7, roughness: .3 })); m.position.set(x, .09 + i * .2, 0); s.add(m); pile[k].push(m); } });
    agg = t => pile.forEach(p => p.forEach((m, i) => { m.visible = t > .3 + i * .08; m.rotation.y = t * .6 + i * .3; }));
    orbita = { r: 13, h: 5, guarda: new THREE.Vector3(0, 2.4, 0), giri: .08 };
    return s;
  },
  /* tre file di 10 barre che scendono: 1%, 2%, 5% a operazione */
  drawdown(){
    const s = base(), file = [.01, .02, .05].map((r, k) => {
      const b = []; for(let i = 0; i <= 10; i++){ const v = Math.pow(1 - r, i); const m = new THREE.Mesh(new THREE.BoxGeometry(.5, 1, .5), mat(k === 2 ? GIU : k === 1 ? 0xD9A13A : SU));
        m.position.set((i - 5) * .7, 0, (k - 1) * 1.6); m.userData.v = v * 4; s.add(m); b.push(m); } return b; });
    agg = t => file.forEach((b, k) => b.forEach((m, i) => { const e = ease(t * 1.2 - i * .18 - k * .2); const h = Math.max(.001, m.userData.v * e); m.scale.y = h; m.position.y = h / 2; }));
    orbita = { r: 13, h: 6, guarda: new THREE.Vector3(0, 1.5, 0), giri: .05 };
    return s;
  },
  /* lotto standard, mini, micro: tre blocchi in scala 100 : 10 : 1 */
  lotti(){
    const s = base(), lati = [Math.cbrt(100), Math.cbrt(10), 1].map(x => x * .75), xs = [-2.6, 1.2, 3.3];
    const b = lati.map((l, i) => { const g = new THREE.BoxGeometry(l, l, l); const m = new THREE.Mesh(g, mat(i === 0 ? LIME : GRIGIO)); m.add(bordi(g, TESTO, .6)); m.position.set(xs[i], l / 2, 0); s.add(m); return m; });
    agg = t => b.forEach((m, i) => { const e = ease(t * 1.3 - i * .5); m.scale.setScalar(Math.max(e, .001)); m.rotation.y = .4 + Math.sin(t * .5 + i) * .15; });
    orbita = { r: 11, h: 4, guarda: new THREE.Vector3(0, 1.2, 0), giri: .05 };
    return s;
  },
  /* bilancia: stop lungo con lotto piccolo, stop corto con lotto grande, sempre in equilibrio */
  bilancia(){
    const s = base(), asse = new THREE.Group(); s.add(asse); asse.position.y = 2.2;
    const perno = new THREE.Mesh(new THREE.ConeGeometry(.5, 2.2, 4), mat(GRIGIO)); perno.position.y = 1.1; s.add(perno);
    const barra = new THREE.Mesh(new THREE.BoxGeometry(9, .12, .3), mat(TESTO)); asse.add(barra);
    const peso = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), mat(LIME)); asse.add(peso);
    const rischio = new THREE.Mesh(new THREE.BoxGeometry(.9, .9, .9), mat(GIU)); rischio.position.set(-2.2, .52, 0); asse.add(rischio);
    agg = t => { const f = (Math.sin(t * .7) + 1) / 2; const x = 1 + f * 3.4; const sc = 2.2 / x * 1.1;
      peso.position.set(x, .06 + sc / 2, 0); peso.scale.setScalar(sc); asse.rotation.z = Math.sin(t * 2.2) * .02; };
    orbita = { r: 12, h: 3.5, guarda: new THREE.Vector3(0, 2, 0), giri: .03 };
    return s;
  },
  /* lingotto d'oro che ruota, tirato da due forze */
  oro(){
    const s = base(), g = new THREE.Group(); s.add(g); g.position.y = 2;
    const forma = new THREE.Shape(); forma.moveTo(-1.6, -.6); forma.lineTo(1.6, -.6); forma.lineTo(1.25, .6); forma.lineTo(-1.25, .6); forma.lineTo(-1.6, -.6);
    const geo = new THREE.ExtrudeGeometry(forma, { depth: 1.4, bevelEnabled: true, bevelSize: .05, bevelThickness: .05 }); geo.center();
    g.add(new THREE.Mesh(geo, mat(ORO, { metalness: .95, roughness: .22 })));
    const freccia = (c, dir) => { const a = new THREE.ArrowHelper(new THREE.Vector3(0, dir, 0), new THREE.Vector3(dir * 2.6, -dir * .6, 0), 1.8, c, .5, .4); s.add(a); a.position.y += 2; return a; };
    const su = freccia(SU, 1), giu = freccia(GIU, -1);
    agg = t => { g.rotation.y = t * .5; g.rotation.x = .25; g.position.y = 2 + Math.sin(t * 1.3) * .2; su.position.y = 2.6 + Math.sin(t * 2) * .15; giu.position.y = 1.4 - Math.sin(t * 2) * .15; };
    orbita = { r: 7, h: 2.6, guarda: new THREE.Vector3(0, 2, 0), giri: .03 };
    return s;
  },
  /* palazzi che crescono: indici di borsa */
  indici(){
    const s = base(), b = [];
    for(let i = 0; i < 7; i++) for(let j = 0; j < 4; j++){ const h = .6 + rnd() * 3.6; const m = new THREE.Mesh(new THREE.BoxGeometry(.8, 1, .8), mat(rnd() < .3 ? LIME : GRIGIO)); m.position.set((i - 3) * 1.1, 0, (j - 1.5) * 1.1); m.userData.h = h; s.add(m); b.push(m); }
    agg = t => b.forEach((m, k) => { const h = Math.max(.001, m.userData.h * ease(t * .9 - k * .03)); m.scale.y = h; m.position.y = h / 2; });
    orbita = { r: 13, h: 7, guarda: new THREE.Vector3(0, 1.4, 0), giri: .06 };
    return s;
  },
  /* globo con rotte: Hormuz, Europa–USA */
  globo(){
    const s = base(); s.children.filter(c => c.type === 'GridHelper').forEach(c => s.remove(c));
    const g = new THREE.Group(); g.position.y = 2.4; s.add(g);
    g.add(new THREE.Mesh(new THREE.SphereGeometry(2.4, 48, 32), mat(0x101810, { roughness: .9 })));
    g.add(new THREE.LineSegments(new THREE.WireframeGeometry(new THREE.SphereGeometry(2.42, 24, 16)), new THREE.LineBasicMaterial({ color: 0x3E5A20, transparent: true, opacity: .5 })));
    const punto = (lat, lon) => { const f = (90 - lat) * Math.PI / 180, l = (lon + 180) * Math.PI / 180; return new THREE.Vector3(-2.45 * Math.sin(f) * Math.cos(l), 2.45 * Math.cos(f), 2.45 * Math.sin(f) * Math.sin(l)); };
    const luoghi = [[26.5, 56.3, GIU], [41.9, 12.5, LIME], [40.7, -74, LIME], [35.7, 139.7, TESTO]];
    const sfere = luoghi.map(([a, b, c]) => { const m = new THREE.Mesh(new THREE.SphereGeometry(.12, 16, 12), new THREE.MeshBasicMaterial({ color: c })); m.position.copy(punto(a, b)); g.add(m); return m; });
    const arco = (a, b) => { const A = punto(...a), B = punto(...b), M = A.clone().add(B).multiplyScalar(.5).normalize().multiplyScalar(3.4);
      const c = new THREE.QuadraticBezierCurve3(A, M, B); const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(c.getPoints(60)), new THREE.LineBasicMaterial({ color: LIME })); g.add(l); return l; };
    const archi = [arco([26.5, 56.3], [41.9, 12.5]), arco([41.9, 12.5], [40.7, -74])];
    agg = t => { g.rotation.y = -1.3 + t * .12; sfere[0].scale.setScalar(1 + Math.sin(t * 4) * .4); archi.forEach((a, i) => a.geometry.setDrawRange(0, Math.floor(61 * ease(t * .5 - i * .8)))); };
    orbita = { r: 9, h: 3, guarda: new THREE.Vector3(0, 2.4, 0), giri: 0 };
    return s;
  },
  /* domino: petrolio → inflazione → Fed → dollaro → oro e azioni */
  domino(){
    const s = base(), colori = [ORO, GIU, LIME, TESTO, ORO], d = [];
    for(let i = 0; i < 5; i++){ const p = new THREE.Group(); const g = new THREE.BoxGeometry(.5, 2.6, 1.4); const m = new THREE.Mesh(g, mat(colori[i])); m.position.y = 1.3; const bb = bordi(g, 0x000000, .4); bb.position.copy(m.position); p.add(m, bb); p.position.x = (i - 2) * 1.7; s.add(p); d.push(p); }
    agg = t => d.forEach((p, i) => { const e = ease((t % 9) * .9 - 1 - i * .55); p.rotation.z = -e * 1.05; });
    orbita = { r: 12, h: 4, guarda: new THREE.Vector3(0, 1.3, 0), giri: .04 };
    return s;
  },
  /* scalini che salgono: tassi e rendimenti */
  scale(){
    const s = base(), st = [];
    for(let i = 0; i < 7; i++){ const h = .4 + i * .45; const m = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1, 2), mat(i === 6 ? LIME : GRIGIO)); m.position.set((i - 3) * 1.25, 0, 0); m.userData.h = h; s.add(m); st.push(m); }
    const palla = new THREE.Mesh(new THREE.SphereGeometry(.32, 24, 16), mat(TESTO)); s.add(palla);
    agg = t => { st.forEach((m, i) => { const h = Math.max(.001, m.userData.h * ease(t * 1.2 - i * .15)); m.scale.y = h; m.position.y = h / 2; });
      const k = Math.min(6, (t * .9) % 8), i = Math.floor(k), f = k - i; const a = st[i], b = st[Math.min(6, i + 1)];
      palla.position.set(a.position.x + (b.position.x - a.position.x) * f, a.userData.h + .32 + (b.userData.h - a.userData.h) * f + Math.sin(f * Math.PI) * .5, 0); };
    orbita = { r: 12, h: 4, guarda: new THREE.Vector3(0, 1.6, 0), giri: .05 };
    return s;
  },
  /* calendario: tessere dei giorni che si girano, le date chiave si accendono */
  calendario(){
    const s = base(), t2 = [], chiave = [9, 10, 23, 24];
    for(let k = 0; k < 28; k++){ const g = new THREE.BoxGeometry(.9, .9, .12); const m = new THREE.Mesh(g, mat(chiave.includes(k) ? LIME : GRIGIO)); m.position.set((k % 7 - 3) * 1.05, 3.6 - Math.floor(k / 7) * 1.05, 0); s.add(m); t2.push(m); }
    agg = t => t2.forEach((m, k) => { const e = ease(t * 1.5 - k * .06); m.rotation.y = (1 - e) * Math.PI; m.position.z = chiave.includes(k) ? .3 + Math.sin(t * 2 + k) * .15 : 0; });
    orbita = { r: 10, h: 2.5, guarda: new THREE.Vector3(0, 2, 0), giri: .02 };
    return s;
  },
  /* scudo esagonale: le particelle rosse rimbalzano */
  scudo(){
    const s = base(), g = new THREE.CylinderGeometry(2.2, 2.2, .25, 6), sc = new THREE.Mesh(g, mat(LIME, { transparent: true, opacity: .35 }));
    sc.rotation.x = Math.PI / 2; sc.position.y = 2.4; s.add(sc); const b = bordi(g, LIME, 1); b.rotation.x = Math.PI / 2; b.position.y = 2.4; s.add(b);
    const N = 30, p = []; for(let i = 0; i < N; i++){ const m = new THREE.Mesh(new THREE.SphereGeometry(.1, 10, 8), new THREE.MeshBasicMaterial({ color: GIU })); m.userData = { a: rnd() * 6.28, r: rnd() * 1.6, o: rnd() * 3 }; s.add(m); p.push(m); }
    agg = t => { sc.rotation.z = t * .2; b.rotation.z = t * .2;
      p.forEach(m => { const u = m.userData, k = ((t + u.o) % 3) / 3; const z = k < .5 ? 6 - k * 2 * 5.8 : .2 + (k - .5) * 2 * 6;
        m.position.set(Math.cos(u.a) * u.r * (k < .5 ? 1 : 1 + (k - .5) * 4), 2.4 + Math.sin(u.a) * u.r * (k < .5 ? 1 : 1 + (k - .5) * 4), z); }); };
    orbita = { r: 11, h: 3.5, guarda: new THREE.Vector3(0, 2.4, 0), giri: .05 };
    return s;
  },
  /* moneta minuscola contro il blocco del lotto minimo */
  minimo(){
    const s = base(), mon = new THREE.Mesh(new THREE.CylinderGeometry(.35, .35, .08, 32), mat(ORO, { metalness: .8, roughness: .3 })); mon.position.set(-1.8, .04, 0); s.add(mon);
    const g = new THREE.BoxGeometry(1.6, 1.6, 1.6), blk = new THREE.Mesh(g, mat(GIU)); blk.add(bordi(g, TESTO, .6)); blk.position.set(1.6, .8, 0); s.add(blk);
    agg = t => { mon.rotation.y = t; blk.scale.setScalar(Math.max(.001, ease(t * .8 - .6))); blk.position.y = .8 * blk.scale.y; };
    orbita = { r: 8, h: 3, guarda: new THREE.Vector3(0, .8, 0), giri: .05 };
    return s;
  }
};

window.vis = {
  imposta(tipo){ seme = 3; scena = tipo && V[tipo] ? V[tipo]() : null; cv.style.display = scena ? 'block' : 'none'; },
  disegna(t){
    if(!scena) return;
    agg(t);
    const a = .6 + t * orbita.giri;
    cam.position.set(Math.sin(a) * orbita.r, orbita.h + Math.sin(t * .3) * .3, Math.cos(a) * orbita.r);
    cam.lookAt(orbita.guarda);
    gl.render(scena, cam);
  }
};
window.visPronto = true;
