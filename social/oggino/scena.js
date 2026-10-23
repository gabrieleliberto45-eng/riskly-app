/* "Oggi no." — scena 3D: il terminale del trader, il pulsante BUY e il robot di Riskly che si mette in mezzo.
   Le azioni partono sulle parole della voce: window.ep.imposta(battute) · window.ep.disegna(t) */
import * as THREE from './three/three.module.min.js';

const C = { lime: 0xF2B83A, verde: 0x22C55E, rosso: 0xEF4444, oro: 0xE8B84A, bianco: 0xF3F1EA, grafite: 0x1E241F };
const hex = c => '#' + new THREE.Color(c).getHexString();
const cv = document.getElementById('gl');
const gl = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, preserveDrawingBuffer: true });
gl.setPixelRatio(1); gl.setSize(cv.width, cv.height, false); gl.setClearColor(0, 0);
const cam = new THREE.PerspectiveCamera(50, cv.width / cv.height, .1, 200);
const CAM = new THREE.Vector3(0, 6.2, 17), GUARDA = new THREE.Vector3(0, 6.4, 0);
const ease = x => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);
const easeIn = x => Math.pow(Math.min(1, Math.max(0, x)), 2.2);
const fra = (t, a, d) => Math.min(1, Math.max(0, (t - a) / d));
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .4, metalness: .35, ...o });
const luce = (c, i = 1) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false, transparent: true, opacity: i });

const scena = new THREE.Scene();
scena.add(new THREE.AmbientLight(0xffffff, .55));
const key = new THREE.DirectionalLight(0xffffff, 1.5); key.position.set(4, 10, 9); scena.add(key);
const rim = new THREE.PointLight(C.lime, 18, 12); rim.position.set(0, 5.5, -.5); scena.add(rim);
const sotto = new THREE.PointLight(C.lime, 6, 5); scena.add(sotto);
const fronte = new THREE.DirectionalLight(0xdfe8d8, .9); fronte.position.set(-2, 6, 16); scena.add(fronte);

/* ─── il terminale: grafico su una tela che si ridisegna quando cambia lo stato ─── */
const tela = document.createElement('canvas'); tela.width = 1024; tela.height = 540;
const tx = tela.getContext('2d'), texSchermo = new THREE.CanvasTexture(tela); texSchermo.colorSpace = THREE.SRGBColorSpace;
const schermo = new THREE.Mesh(new THREE.PlaneGeometry(7.6, 4.0), new THREE.MeshBasicMaterial({ map: texSchermo, toneMapped: false }));
schermo.position.set(0, 9.6, 0); scena.add(schermo);
const cornice = new THREE.Mesh(new THREE.BoxGeometry(7.85, 4.25, .18), mat(0x101410, { metalness: .6 }));
cornice.position.set(0, 9.6, -.11); scena.add(cornice);
const BASE = []; { let p = 300; for(let i = 0; i < 22; i++){ const o = p; p += Math.sin(i * 1.7) * 9 - 2.2; BASE.push([o, p]); } }
let chiaveSchermo = '';
function disegnaSchermo(perdite, rabbia, spento){
  const k = perdite.toFixed(2) + '|' + rabbia.toFixed(2) + '|' + spento.toFixed(2);
  if(k === chiaveSchermo) return; chiaveSchermo = k;
  const W = tela.width, H = tela.height, x = tx;
  x.fillStyle = '#0c100d'; x.fillRect(0, 0, W, H);
  x.strokeStyle = 'rgba(255,255,255,.05)'; x.lineWidth = 1;
  for(let g = 70; g < H; g += 60){ x.beginPath(); x.moveTo(0, g); x.lineTo(W, g); x.stroke(); }
  x.font = '600 26px "Martian Mono"'; x.fillStyle = '#8B98A9'; x.fillText('XAUUSD · M5', 26, 42);
  const n = Math.floor(perdite), conto = -(Math.min(3, n) * 1.0);
  x.textAlign = 'right'; x.fillStyle = n ? '#EF4444' : '#8B98A9'; x.font = '700 30px "Martian Mono"';
  x.fillText('CONTO ' + (n ? conto.toFixed(1).replace('.', ',') + '%' : '0,0%'), W - 26, 44); x.textAlign = 'left';
  const cw = 28, gap = 10, x0 = 40, y = v => 120 + (v - 240) * -2.0 + 200;
  const tutte = BASE.slice();
  let p = BASE[BASE.length - 1][1];
  for(let i = 0; i < 3; i++){ const o = p; p -= 28 + i * 6; tutte.push([o, p, i]); }
  tutte.forEach((c, i) => {
    let vis = 1;
    if(c.length === 3){ vis = Math.min(1, Math.max(0, perdite - c[2])); if(vis <= 0) return; }
    const su = c[1] >= c[0], X = x0 + i * (cw + gap);
    const top = y(Math.max(c[0], c[1])), bot = y(Math.min(c[0], c[1]));
    const h = Math.max(4, (bot - top) * vis);
    x.fillStyle = su ? '#22C55E' : '#EF4444';
    x.fillRect(X + cw / 2 - 1.5, top - 10, 3, h + 20); x.fillRect(X, top, cw, h);
    if(c.length === 3 && vis > .9){ x.fillStyle = '#EF4444'; x.font = '700 22px "Martian Mono"'; x.fillText('−1%', X - 6, top + h + 40); }
  });
  if(rabbia > 0){ x.fillStyle = `rgba(239,68,68,${.32 * rabbia})`; x.fillRect(0, 0, W, H); }
  if(spento > 0){ x.fillStyle = `rgba(4,5,4,${.82 * spento})`; x.fillRect(0, 0, W, H);
    x.globalAlpha = spento; x.textAlign = 'center'; x.fillStyle = '#5D6B7D'; x.font = '700 40px "Martian Mono"'; x.fillText('PIATTAFORMA CHIUSA', W / 2, H / 2 + 14); x.textAlign = 'left'; x.globalAlpha = 1; }
  texSchermo.needsUpdate = true;
}

/* ─── il pulsante BUY ─── */
const telaB = document.createElement('canvas'); telaB.width = 512; telaB.height = 150;
const bx = telaB.getContext('2d'), texB = new THREE.CanvasTexture(telaB); texB.colorSpace = THREE.SRGBColorSpace;
let chiaveB = '';
function disegnaBottone(testo, colore, testoColore){
  const k = testo + colore; if(k === chiaveB) return; chiaveB = k;
  bx.fillStyle = colore; bx.fillRect(0, 0, 512, 150);
  bx.fillStyle = testoColore; bx.font = '900 76px Archivo'; bx.textAlign = 'center'; bx.textBaseline = 'middle'; bx.fillText(testo, 256, 80);
  texB.needsUpdate = true;
}
const latoB = mat(C.lime, { emissive: C.lime, emissiveIntensity: .25 });
const bottone = new THREE.Mesh(new THREE.BoxGeometry(3.0, .88, .34),
  [latoB, latoB, latoB, latoB, new THREE.MeshBasicMaterial({ map: texB, toneMapped: false }), latoB]);
bottone.position.set(0, 6.45, .4); scena.add(bottone);

/* ─── il cursore del mouse ─── */
const forma = new THREE.Shape(); forma.moveTo(0, 0); forma.lineTo(0, -1.0); forma.lineTo(.27, -.76); forma.lineTo(.46, -1.18);
forma.lineTo(.6, -1.11); forma.lineTo(.42, -.7); forma.lineTo(.76, -.7); forma.lineTo(0, 0);
const cursore = new THREE.Mesh(new THREE.ExtrudeGeometry(forma, { depth: .08, bevelEnabled: false }), new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false }));
const bordoC = new THREE.LineSegments(new THREE.EdgesGeometry(cursore.geometry), new THREE.LineBasicMaterial({ color: 0x000000 }));
cursore.add(bordoC); cursore.visible = false; scena.add(cursore);
const CURS_DA = new THREE.Vector3(3.6, 2.2, 1.4), CURS_A = new THREE.Vector3(.55, 6.35, .8);

/* ─── il robot ─── */
const robot = new THREE.Group(), corpoMat = mat(0x2B322C, { metalness: .55, roughness: .3 });
const corpo = new THREE.Mesh(new THREE.CapsuleGeometry(.78, .72, 8, 28), corpoMat); corpo.position.y = 4.3; corpo.scale.x = 1.04; robot.add(corpo);
const fascia = new THREE.Mesh(new THREE.TorusGeometry(.8, .035, 8, 48), luce(C.lime)); fascia.rotation.x = Math.PI / 2; fascia.position.y = 3.85; robot.add(fascia);
const stemma = new THREE.Mesh(new THREE.CylinderGeometry(.27, .27, .05, 6), luce(C.lime)); stemma.rotation.x = Math.PI / 2; stemma.position.set(0, 4.5, .79); robot.add(stemma);
const testa = new THREE.Group(); testa.position.y = 5.78; robot.add(testa);
const cranio = new THREE.Mesh(new THREE.SphereGeometry(.8, 32, 24), corpoMat); cranio.scale.set(1.18, .9, 1); testa.add(cranio);
const visiera = new THREE.Mesh(new THREE.SphereGeometry(.8, 32, 20), mat(0x030403, { metalness: .9, roughness: .1 }));
visiera.scale.set(1.0, .52, .36); visiera.position.set(0, .02, .52); testa.add(visiera);
const occhi = [-.27, .27].map(x => { const o = new THREE.Mesh(new THREE.CapsuleGeometry(.075, .13, 4, 12), luce(C.lime)); o.position.set(x, .03, .86); testa.add(o); return o; });
const antenna = new THREE.Mesh(new THREE.CylinderGeometry(.03, .03, .45), corpoMat); antenna.position.set(0, .88, 0); testa.add(antenna);
const punta = new THREE.Mesh(new THREE.SphereGeometry(.1, 16, 12), luce(C.lime)); punta.position.set(0, 1.14, 0); testa.add(punta);
function braccio(lato){
  const spalla = new THREE.Group(); spalla.position.set(.9 * lato, 4.72, 0);
  const sup = new THREE.Mesh(new THREE.CapsuleGeometry(.13, .62, 4, 12), corpoMat); sup.position.y = -.42; spalla.add(sup);
  const mano = new THREE.Mesh(new THREE.BoxGeometry(.36, .42, .14), corpoMat); mano.position.y = -.92; spalla.add(mano);
  const palmo = new THREE.Mesh(new THREE.PlaneGeometry(.26, .3), luce(C.lime, .9)); palmo.position.set(0, -.92, .075); spalla.add(palmo);
  spalla.rotation.z = .12 * lato; robot.add(spalla); return spalla;
}
const bracSx = braccio(-1), bracDx = braccio(1);
const anello = new THREE.Mesh(new THREE.TorusGeometry(.62, .05, 8, 48), luce(C.lime)); anello.rotation.x = Math.PI / 2; anello.position.y = 3.05; robot.add(anello);
const alone = new THREE.Mesh(new THREE.CircleGeometry(1.1, 40), luce(C.lime, .22)); alone.rotation.x = -Math.PI / 2; alone.position.y = 2.6; robot.add(alone);
const SR = 1.3, YR = -1.45;
robot.position.set(0, YR, 2.7); robot.visible = false; scena.add(robot);

/* ─── etichette ─── */
function etichetta(testo, colore, alto = .7){
  const c = document.createElement('canvas'), x = c.getContext('2d'), f = 120;
  x.font = `900 ${f}px Archivo`; const w = Math.ceil(x.measureText(testo).width) + 80; c.width = w; c.height = f + 60;
  x.fillStyle = 'rgba(0,0,0,.72)'; x.fillRect(0, 0, w, c.height); x.font = `900 ${f}px Archivo`;
  x.fillStyle = hex(colore); x.textBaseline = 'middle'; x.fillText(testo, 40, c.height / 2 + 6);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthTest: false, toneMapped: false }));
  s.scale.set(alto * w / c.height, alto, 1); s.userData.base = s.scale.clone(); s.renderOrder = 10; return s;
}

/* ─── battute → istanti ─── */
let B = {}, etichette = [];
const COLORI = { rosso: C.rosso, oro: C.oro, lime: C.lime, bianco: C.bianco };
window.ep = {
  imposta(battute){
    B = {}; etichette.forEach(e => scena.remove(e.s)); etichette = [];
    for(const b of battute){
      if(b.azione === 'etichetta'){ const s = etichetta(b.testo, COLORI[b.colore] || C.bianco); s.position.set(b.x || 0, b.y || 12.4, 1.5); s.visible = false; scena.add(s); etichette.push({ s, t: b.t }); }
      else if(B[b.azione] === undefined) B[b.azione] = b.t;
    }
  },
  disegna(t){
    const T = k => (B[k] === undefined ? Infinity : B[k]);
    const tP = T('perdite'), tL = T('lotto'), tCu = T('cursore'), tE = T('entra'), tTi = T('timbro'), tR = T('rabbia'), tCh = T('chiudi'), tK = T('calma'), tF = T('fine');
    // schermo e pulsante
    const perdite = t < tP ? 0 : Math.min(3, (t - tP) / .42 * 1.0 + .0);
    const rabbia = t < tR ? 0 : Math.max(0, 1 - Math.abs((t - tR - .35) / .55));
    const spento = ease(fra(t, tCh + .4, .7));
    disegnaSchermo(perdite, rabbia, spento);
    const lotto = t >= tL ? '0,80' : '0,40';
    if(t >= tCh + .4) disegnaBottone('CHIUSO', '#2A302A', '#5D6B7D');
    else disegnaBottone('BUY ' + lotto, t >= tL && t < tL + .25 ? '#F3F1EA' : '#F2B83A', '#0B0D0C');
    const sopra = t >= tCu + 1.0 && t < tE;
    latoB.emissiveIntensity = sopra ? .6 + .3 * Math.sin(t * 18) : (t >= tCh + .4 ? 0 : .25);
    latoB.color.set(t >= tCh + .4 ? 0x2A302A : C.lime);
    // cursore: arriva sul pulsante, viene respinto dal robot, se ne va quando si chiude
    cursore.visible = t >= tCu && t < tCh + 1.4;
    if(cursore.visible){
      const p = new THREE.Vector3().lerpVectors(CURS_DA, CURS_A, ease(fra(t, tCu, 1.0)));
      if(t >= tE + .42) p.add(new THREE.Vector3(.9, -.7, 0).multiplyScalar(ease(fra(t, tE + .42, .25))));
      if(t >= tCh) p.add(new THREE.Vector3(3, -4, 0).multiplyScalar(easeIn(fra(t, tCh, 1.2))));
      cursore.position.copy(p);
    }
    // robot: cade dall'alto, atterra, ferma il pulsante
    robot.visible = t >= tE;
    let y = 0, sq = 1;
    if(robot.visible){
      y = 12 * (1 - easeIn(fra(t, tE, .42)));
      const atterra = fra(t, tE + .42, .3); if(atterra > 0 && atterra < 1) sq = 1 - .16 * Math.sin(atterra * Math.PI);
      y += Math.sin(t * 2.2) * .06 * fra(t, tE + .8, .5);
    }
    robot.position.y = YR + y; robot.scale.set(SR * (1 + (1 - sq) * .6), SR * sq, SR * (1 + (1 - sq) * .6));
    sotto.position.set(0, 2.4 + y, 3.6); sotto.intensity = robot.visible ? 6 + Math.sin(t * 6) * 1.5 : 0;
    const blocco = ease(fra(t, tTi - .05, .22)) * (1 - ease(fra(t, tCh + .2, .5)));
    bracDx.rotation.z = .12 + 2.35 * blocco; bracDx.rotation.x = -.25 * blocco;
    const calma = ease(fra(t, tK, .6));
    bracSx.rotation.x = -.15 * calma; bracSx.rotation.z = -.12 - .1 * calma;
    testa.rotation.x = Math.sin(fra(t, tK, .9) * Math.PI * 2) * .12 * (t < tK + .9 ? 1 : 0);
    testa.rotation.y = robot.visible ? Math.sin(t * .9) * .06 : 0;
    // occhi: lampeggio, si stringono sulla rabbia
    const lamp = ((t % 3.3) < .1) ? .12 : 1, stretti = t >= tR && t < tR + 1.5 ? .45 : 1;
    occhi.forEach(o => o.scale.y = lamp * stretti);
    punta.material.opacity = .55 + .45 * Math.abs(Math.sin(t * 3));
    // etichette
    etichette.forEach(e => { e.s.visible = t >= e.t && t < tCh + .3; const k = ease(fra(t, e.t, .25)); e.s.scale.set(e.s.userData.base.x * (.6 + .4 * k), e.s.userData.base.y * (.6 + .4 * k), 1); e.s.material.opacity = k; });
    // camera: leggera spinta in avanti e scossa all'atterraggio
    const scossa = t >= tE + .42 && t < tE + .8 ? (1 - fra(t, tE + .42, .38)) * .14 : 0;
    const spinta = .9 * ease(fra(t, 0, 4)) + 1.0 * ease(fra(t, tK, 3));
    cam.position.set(CAM.x + Math.sin(t * 61) * scossa, CAM.y + Math.cos(t * 47) * scossa, CAM.z - spinta);
    cam.lookAt(GUARDA);
    // overlay HTML: timbro, rosso, finale
    const tb = document.getElementById('timbro');
    const kT = fra(t, tTi, .18), via = fra(t, tTi + 2.0, .4);
    tb.style.opacity = t < tTi ? 0 : (1 - via); tb.style.transform = `scale(${1.6 - .6 * ease(kT)}) rotate(${-4 + 4 * ease(kT)}deg)`;
    document.getElementById('rosso').style.opacity = rabbia;
    document.getElementById('fine').style.opacity = ease(fra(t, tF + .9, .5));
    gl.render(scena, cam);
  }
};
document.fonts.load('900 120px Archivo').then(() => document.fonts.load('700 30px "Martian Mono"')).then(() => { chiaveSchermo = ''; chiaveB = ''; window.visPronto = true; });
