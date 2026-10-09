/* Motore 3D delle "Storie di rischio": la scena segue la voce.
   Ogni battuta ha un istante (la parola chiave detta in quel momento) e un'azione:
   grafico, linea, stop eseguito più in basso, etichette, contatori, palazzi che crollano, torre della leva, scudo.
   window.storia.imposta(battute) · window.storia.disegna(t)  (t = secondi dall'inizio della storia) */
import * as THREE from './three/three.module.min.js';

const C = { lime: 0xB6D84F, verde: 0x22C55E, rosso: 0xEF4444, oro: 0xE8B84A, grigio: 0x2E352E, bianco: 0xF3F1EA };
const hex = c => '#' + new THREE.Color(c).getHexString();
const cv = document.getElementById('gl');
const gl = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, preserveDrawingBuffer: true });
gl.setPixelRatio(1); gl.setSize(cv.width, cv.height, false); gl.setClearColor(0, 0);
const cam = new THREE.PerspectiveCamera(50, cv.width / cv.height, .1, 300);
const ease = x => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .45, metalness: .2, ...o });

let scena, oggetti, battute, inquadrature;

/* etichetta 3D: testo su sprite, sempre rivolto alla camera */
function etichetta(testo, colore = C.bianco, alto = 1, sfondo = 'rgba(0,0,0,.65)'){
  const c = document.createElement('canvas'), x = c.getContext('2d'), f = 120;
  x.font = `900 ${f}px Archivo`; const w = Math.ceil(x.measureText(testo).width) + 80;
  c.width = w; c.height = f + 60; x.font = `900 ${f}px Archivo`;
  if(sfondo){ x.fillStyle = sfondo; x.fillRect(0, 0, w, c.height); }
  x.fillStyle = hex(colore); x.textBaseline = 'middle'; x.fillText(testo, 40, c.height / 2 + 6);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthTest: false }));
  let sx = alto * w / c.height, sy = alto; if(sx > 8.4){ sy *= 8.4 / sx; sx = 8.4; }
  s.scale.set(sx, sy, 1); s.renderOrder = 10; s.userData.canvas = c; s.userData.ctx = x; s.userData.tex = t; s.userData.alto = alto;
  return s;
}
function riscrivi(s, testo, colore){
  const c = s.userData.canvas, x = s.userData.ctx;
  x.clearRect(0, 0, c.width, c.height); x.fillStyle = 'rgba(0,0,0,.65)'; x.fillRect(0, 0, c.width, c.height);
  x.font = `900 120px Archivo`; x.fillStyle = hex(colore); x.textBaseline = 'middle'; x.fillText(testo, 40, c.height / 2 + 6); s.userData.tex.needsUpdate = true;
}

/* grafico a candele: piatto, sale, scende, crollo (piatto poi una candela enorme rossa) */
function grafico(tipo, livello = 6){
  const g = new THREE.Group(), N = 30, cand = [], PASSO = .3;
  let p = livello;
  for(let i = 0; i < N; i++){
    let o = p, c;
    if(tipo === 'piatto') c = livello + Math.sin(i * 1.9) * .22;
    else if(tipo === 'sale') c = o + .18 + (Math.sin(i * 2.3) * .2);
    else if(tipo === 'scende') c = o - .2 + (Math.sin(i * 2.1) * .2);
    else if(tipo === 'crollo') c = i < 24 ? livello + Math.sin(i * 1.9) * .22 : i === 24 ? livello - 3.2 : o + (Math.sin(i * 3) * .25);
    const m = new THREE.Mesh(new THREE.BoxGeometry(.22, 1, .22), mat(c >= o ? C.verde : C.rosso, i === 24 && tipo === 'crollo' ? { emissive: C.rosso, emissiveIntensity: .5 } : {}));
    m.position.set((i - N / 2) * PASSO, (o + c) / 2, 0); m.userData = { h: Math.max(Math.abs(c - o), .14), ritardo: i * .05, dopo: tipo === 'crollo' && i >= 24 ? i - 24 : -1 };
    g.add(m); cand.push(m); p = c;
  }
  g.userData = { cand, crash: null, aggiorna(d, t){ cand.forEach(m => { let e = ease((d - m.userData.ritardo) * 2.5);
      if(m.userData.dopo >= 0) e = g.userData.crash === null ? 0 : ease((t - g.userData.crash - m.userData.dopo * .12) * 3);
      m.scale.y = Math.max(.001, m.userData.h * e); m.visible = e > 0; }); } };
  return g;
}

/* palazzi con il nome sopra: banche, broker */
function palazzi(nomi){
  const g = new THREE.Group(), lista = {};
  nomi.forEach((n, i) => {
    const h = 4 + (i % 3) * 1.2, p = new THREE.Group();
    const m = new THREE.Mesh(new THREE.BoxGeometry(1.5, h, 1.5), mat(C.grigio)); m.position.y = h / 2; p.add(m);
    for(let f = 0; f < Math.floor(h / .7); f++){ const fin = new THREE.Mesh(new THREE.BoxGeometry(1.54, .08, 1.54), new THREE.MeshBasicMaterial({ color: 0xE8E2C8, transparent: true, opacity: .25 })); fin.position.y = .5 + f * .7; p.add(fin); }
    const e = etichetta(n, C.bianco, .42); if(e.scale.x > 2.7){ e.scale.multiplyScalar(2.7 / e.scale.x); } e.position.y = h + .6; p.add(e);
    p.position.x = (i - (nomi.length - 1) / 2) * 2.9; p.userData = { h, crollo: null }; g.add(p); lista[n] = p;
  });
  g.userData = { lista, aggiorna(d, t){ Object.values(lista).forEach(p => { const c = p.userData.crollo; if(c === null) return; const k = Math.max(0, t - c);
    p.children[0].material.color.set(C.rosso); p.rotation.z = -Math.min(1.4, k * k * 1.2); p.position.y = -Math.min(p.userData.h * .6, k * k * 2); }); } };
  return g;
}

/* torre della leva: cresce, poi crolla */
function torre(){
  const g = new THREE.Group(), b = [];
  for(let i = 0; i < 20; i++){ const geo = new THREE.BoxGeometry(i % 2 ? 2.6 : .8, .45, i % 2 ? .8 : 2.6); const m = new THREE.Mesh(geo, mat(i > 15 ? C.rosso : i % 3 ? C.grigio : C.lime));
    m.userData = { y: .23 + i * .46, vx: Math.sin(i * 7.1) * 3, vz: Math.cos(i * 5.3) * 3, vr: Math.sin(i * 3.7) * 4 }; g.add(m); b.push(m); }
  g.userData = { crollo: null, aggiorna(d, t){ const cr = g.userData.crollo; b.forEach((m, i) => { const u = m.userData, n = ease(d * 2.5 - i * .12); m.visible = n > 0;
    if(cr === null || t < cr){ m.position.set(0, u.y * n, 0); m.rotation.set(0, 0, 0); }
    else { const k = t - cr, f = i / 20; m.position.set(u.vx * k * f, Math.max(.23, u.y - 4.9 * k * k * (.4 + f)), u.vz * k * f); m.rotation.set(u.vr * k * f, 0, u.vr * k * f * .7); } }); } };
  return g;
}

/* scudo con il nome di uno strumento Riskly */
function scudo(nome){
  const g = new THREE.Group(), geo = new THREE.CylinderGeometry(2.6, 2.6, .3, 6);
  const m = new THREE.Mesh(geo, mat(C.lime, { transparent: true, opacity: .4, emissive: C.lime, emissiveIntensity: .25 })); m.rotation.x = Math.PI / 2; g.add(m);
  const b = new THREE.LineSegments(new THREE.EdgesGeometry(geo), new THREE.LineBasicMaterial({ color: C.lime })); b.rotation.x = Math.PI / 2; g.add(b);
  const e = etichetta(nome, C.lime, .9); e.position.y = -3.3; g.add(e);
  const palle = []; for(let i = 0; i < 24; i++){ const p = new THREE.Mesh(new THREE.SphereGeometry(.12, 10, 8), new THREE.MeshBasicMaterial({ color: C.rosso })); p.userData = { a: i * 2.4, r: .4 + (i % 5) * .4, o: i * .13 }; g.add(p); palle.push(p); }
  g.userData = { aggiorna(d){ m.rotation.y = d * .3; b.rotation.y = d * .3; const s = ease(d * 2); g.scale.setScalar(Math.max(.001, s));
    palle.forEach(p => { const u = p.userData, k = ((d + u.o) % 2.4) / 2.4; const z = k < .5 ? 7 - k * 2 * 6.8 : .2 + (k - .5) * 2 * 7, sp = k < .5 ? 1 : 1 + (k - .5) * 5;
      p.position.set(Math.cos(u.a) * u.r * sp, Math.sin(u.a) * u.r * sp, z); }); } };
  return g;
}

/* azioni delle battute */
const AZIONI = {
  grafico(a){ const g = grafico(a.tipo, a.livello); g.position.set(a.x || 0, 0, 0); return g; },
  linea(a){ const g = new THREE.Group(); const l = new THREE.Mesh(new THREE.BoxGeometry(9.4, .06, .06), new THREE.MeshBasicMaterial({ color: C[a.colore || 'lime'] }));
    g.add(l); const e = etichetta(a.testo, C[a.colore || 'lime'], .8); e.position.set(-2.2, .6, 0); g.add(e); g.position.set(a.x || 0, a.y, 0);
    g.userData = { cade: null, aggiorna(d, t){ l.scale.x = Math.max(.001, ease(d * 2)); if(g.userData.cade !== null && t > g.userData.cade){ const k = t - g.userData.cade; g.position.y = a.y - k * k * 6; g.rotation.z = -k * .6; g.visible = k < 1.8; } } };
    return g; },
  gap(a){ const g = new THREE.Group(); const f = new THREE.ArrowHelper(new THREE.Vector3(0, -1, 0), new THREE.Vector3(0, 0, 0), a.da - a.a, C.rosso, .5, .4); g.add(f);
    const e1 = etichetta(a.stop, C.bianco, .55); e1.position.set(-3.2, .55, 0); g.add(e1); const e2 = etichetta(a.eseguito, C.rosso, .7); e2.position.set(-2.6, a.a - a.da, 0); g.add(e2);
    g.position.set(a.x || 4, a.da, .5); g.userData = { aggiorna(d){ f.scale.y = Math.max(.001, ease(d * 1.5)); e2.visible = d > .7; } }; return g; },
  testo(a){ const e = etichetta(a.testo, C[a.colore || 'bianco'], a.alto || 1.4); e.position.set(a.x || 0, a.y || 9, a.z || 1); e.userData.aggiorna = d => { e.material.opacity = ease(d * 3); }; return e; },
  contatore(a){ const e = etichetta(a.prefisso + a.a + a.suffisso, C[a.colore || 'rosso'], a.alto || 1.5); e.position.set(a.x || 0, a.y || 9, 1);
    e.userData.aggiorna = d => { const v = Math.round(a.a * ease(d / (a.durata || 2))); riscrivi(e, a.prefisso + v.toLocaleString('it-IT') + a.suffisso, C[a.colore || 'rosso']); }; return e; },
  palazzi(a){ const g = palazzi(a.nomi); g.position.set(a.x || 0, 0, a.z || 0); return g; },
  crolla(a){ const p = oggetti[a.gruppo]; if(p){ if(p.userData.lista) p.userData.lista[a.nome].userData.crollo = a.t; else p.userData.crollo = a.t; } return null; },
  cade(a){ const p = oggetti[a.chi]; if(p) p.userData.cade = a.t; return null; },
  torre(a){ const g = torre(); g.position.set(a.x || 0, 0, 0); return g; },
  scudo(a){ const g = scudo(a.nome); g.position.set(a.x || 0, a.y || 5, 0); return g; },
  crollo_ora(a){ const g = oggetti[a.chi]; if(g) g.userData.crash = a.t; return null; },
  togli(a){ (a.chi || []).forEach(k => { if(oggetti[k]){ oggetti[k].userData.via = a.t; } }); return null; }
};

window.storia = {
  /* battute: [{t, azione, id, camera:{pos:[x,y,z], guarda:[x,y,z]}, ...parametri}] ordinate per t */
  imposta(b){
    battute = b.map(x => ({ ...x, fatto: false }));
    scena = new THREE.Scene(); oggetti = {};
    scena.add(new THREE.AmbientLight(0xffffff, .65));
    const l = new THREE.DirectionalLight(0xffffff, 1.5); l.position.set(5, 12, 8); scena.add(l);
    const g = new THREE.GridHelper(200, 200, 0x2A3A1A, 0x161A16); g.material.transparent = true; g.material.opacity = .7; scena.add(g);
    inquadrature = [{ t: 0, pos: new THREE.Vector3(0, 6.5, 17), guarda: new THREE.Vector3(0, 6.5, 0) }];
    cam.position.copy(inquadrature[0].pos);
  },
  disegna(t){
    for(const b of battute){
      if(b.fatto || t < b.t) continue; b.fatto = true;
      const o = AZIONI[b.azione] ? AZIONI[b.azione](b) : null;
      if(o && (b.azione === 'testo' || b.azione === 'contatore')){
        o.userData.didascalia = true;
        scena.children.forEach(x => { if(x.userData && x.userData.didascalia && x.userData.via === undefined && Math.abs(x.position.x - o.position.x) < 9
          && Math.abs(x.position.y - o.position.y) < (x.scale.y + o.scale.y) / 2 + .1) x.userData.via = b.t; });
      }
      if(o){ o.userData.nato = b.t; scena.add(o); if(b.id) oggetti[b.id] = o; }
      if(b.camera) inquadrature.push({ t: b.t, pos: new THREE.Vector3(...b.camera.pos), guarda: new THREE.Vector3(...b.camera.guarda) });
    }
    scena.children.forEach(o => { if(o.userData && o.userData.aggiorna){ o.userData.aggiorna(t - o.userData.nato, t); }
      if(o.userData && o.userData.via !== undefined){ const k = t - o.userData.via; if(k > 0){ o.traverse(x => { if(x.material){ x.material.transparent = true; x.material.opacity = Math.max(0, 1 - k * 2); } }); if(k > .6) o.visible = false; } } });
    // camera: va verso l'ultima inquadratura richiesta, con un lieve movimento continuo
    const q = inquadrature[inquadrature.length - 1], prima = inquadrature[Math.max(0, inquadrature.length - 2)];
    const k = ease((t - q.t) / 1.2);
    const pos = prima.pos.clone().lerp(q.pos, k), guarda = prima.guarda.clone().lerp(q.guarda, k);
    pos.x += Math.sin(t * .25) * .5; pos.y += Math.sin(t * .4) * .2;
    cam.position.copy(pos); cam.lookAt(guarda);
    gl.render(scena, cam);
  }
};
window.visPronto = true;
