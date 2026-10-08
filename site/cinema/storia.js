/* Riskly · "il grafico cinematografico"
   Un grafico a candele 3D che, mentre scorri, racconta cosa fanno i bot:
   rischio deciso prima, stop che ferma la caduta, break-even, trailing, uscite a scaglioni, journal.
   È una simulazione illustrativa: i prezzi sono generati, la logica (stop, BE, trailing) è quella vera. */
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const sez = document.getElementById('storia');
const cv = document.getElementById('storia-gl');
if (sez && cv) avvia();

function avvia(){
  const fermo = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const piccolo = innerWidth < 760;
  let gl;
  try { gl = new THREE.WebGLRenderer({ canvas: cv, antialias: !piccolo, powerPreference: 'high-performance' }); }
  catch(e){ sez.classList.add('senza-3d'); return; }
  gl.setPixelRatio(Math.min(devicePixelRatio || 1, piccolo ? 1.5 : 2));
  const P = window.PAL || { bg:'#0D0E10', acc:'#C9C5BC', accHi:'#F2EFE9', accLo:'#6E6B66', line:'#2A2D32', up:'#5FAE8A', down:'#CC6A61' };
  gl.setClearColor(P.bg, 1);

  const scena = new THREE.Scene();
  scena.background = new THREE.Color(P.bg);
  scena.fog = new THREE.FogExp2(P.bg, piccolo ? .022 : .019);
  const cam = new THREE.PerspectiveCamera(42, 1, .1, 400);

  /* ── prezzi: caos, poi trade A (stop preso), poi trade B (break-even, trailing, uscita in guadagno) ── */
  let seme = 7;
  const rnd = () => (seme = (seme * 16807) % 2147483647) / 2147483647;
  const N = 96, U = 3.1;                       // 1 unità di prezzo = 25 pip = 2,2 in scena
  const chiusure = new Array(N);
  let p = 0;
  for(let i = 0; i < 40; i++){ p += (rnd() - .5) * 1.1 - p * .06; chiusure[i] = p; }
  const shift = chiusure[39]; for(let i = 0; i < 40; i++) chiusure[i] -= shift;
  const E = -.55;
  const punti = [[39,0],[42,-.3],[44,-.15],[47,-.45],[49,-.72],[50,-1.18],[52,-.85],[55,E],
    [57,E+.32],[59,E+.18],[62,E+.98],[65,E+1.45],[67,E+1.22],[71,E+2.15],[73,E+1.86],[77,E+2.95],[80,E+3.35],
    [82,E+2.95],[84,E+2.0],[86,E+1.75],[90,E+2.15],[95,E+1.95]];
  for(let k = 0; k < punti.length - 1; k++){
    const [a, va] = punti[k], [b, vb] = punti[k+1];
    for(let i = a; i <= b; i++) chiusure[i] = va + (vb - va) * (i - a) / (b - a) + (i === a || i === b ? 0 : (rnd() - .5) * .22);
  }
  const C = chiusure.map((c, i) => {
    const o = i ? chiusure[i-1] : c - .2;
    let h = Math.max(o, c) + rnd() * .22 + .04, l = Math.min(o, c) - rnd() * .22 - .04;
    if(i >= 40 && i < 50) l = Math.max(l, -.93);   // il trade A non tocca lo stop prima della candela 50
    if(i === 50) l = -1.32;
    return { o, c, h, l };
  });
  // trade B: stop iniziale E−1, a +0,8 (20 pip) va a break-even, poi segue il massimo a 1 unità di distanza
  const stopB = new Array(N).fill(null);
  let st = E - 1, be = -1, uscita = -1, maxH = -Infinity;
  for(let i = 56; i < N; i++){
    if(uscita < 0 && C[i].l <= st && i > 56){ uscita = i; }
    if(uscita >= 0){ stopB[i] = stopB[uscita - 1]; continue; }
    maxH = Math.max(maxH, C[i].h);
    if(be < 0 && maxH >= E + .8){ be = i; st = Math.max(st, E); }
    if(be >= 0) st = Math.max(st, E, maxH - 1);
    stopB[i] = st;
  }
  const prezzoUscita = uscita > 0 ? stopB[uscita - 1] : st;
  const pipUscita = Math.round((prezzoUscita - E) * 25);

  const X = i => (i - 48) * 1.0;
  const Y = v => v * U;

  /* ── candele: corpi e stoppini in due InstancedMesh ── */
  const geoC = new THREE.BoxGeometry(.62, 1, .62);
  const geoS = new THREE.BoxGeometry(.07, 1, .07);
  const matC = new THREE.MeshBasicMaterial({ toneMapped: false });
  const corpi = new THREE.InstancedMesh(geoC, matC, N);
  const stoppini = new THREE.InstancedMesh(geoS, new THREE.MeshBasicMaterial({ toneMapped: false }), N);
  const SU = new THREE.Color(P.up), GIU = new THREE.Color(P.down);
  for(let i = 0; i < N; i++){
    const col = (C[i].c >= C[i].o ? SU : GIU).clone().multiplyScalar(i < 40 ? .4 : .95);
    corpi.setColorAt(i, col); stoppini.setColorAt(i, col.clone().multiplyScalar(.8));
  }
  scena.add(corpi, stoppini);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), vs = new THREE.Vector3(), vp = new THREE.Vector3();
  function posaCandele(rivelate, t){
    for(let i = 0; i < N; i++){
      const v = THREE.MathUtils.clamp(rivelate - i, 0, 1), e = 1 - Math.pow(1 - v, 3);
      const k = C[i], alto = Math.max(Math.abs(k.c - k.o) * U, .06);
      const respiro = i < 40 && !fermo ? Math.sin(t * .8 + i * .45) * .04 : 0;
      vp.set(X(i), Y((k.c + k.o) / 2) + respiro, 0); vs.set(1, Math.max(alto * e, .0001), 1);
      corpi.setMatrixAt(i, m4.compose(vp, q, vs));
      vp.set(X(i), Y((k.h + k.l) / 2) + respiro, 0); vs.set(1, Math.max((k.h - k.l) * U * e, .0001), 1);
      stoppini.setMatrixAt(i, m4.compose(vp, q, vs));
    }
    corpi.instanceMatrix.needsUpdate = stoppini.instanceMatrix.needsUpdate = true;
  }

  /* ── pavimento a griglia e polvere nello spazio ── */
  const fondo = Y(Math.min(...C.map(k => k.l))) - 4;
  const griglia = new THREE.GridHelper(700, 175, new THREE.Color(P.accLo), new THREE.Color(P.line));
  griglia.material.transparent = true; griglia.material.opacity = .55; griglia.material.depthWrite = false;
  griglia.position.y = fondo; scena.add(griglia);
  const nP = piccolo ? 500 : 1400, posP = new Float32Array(nP * 3);
  for(let i = 0; i < nP; i++){ posP[i*3] = (rnd() - .5) * 220; posP[i*3+1] = fondo + rnd() * 60; posP[i*3+2] = (rnd() - .5) * 160; }
  const polvere = new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(posP, 3)),
    new THREE.PointsMaterial({ color: new THREE.Color(P.acc), size: .14, transparent: true, opacity: .55, depthWrite: false, toneMapped: false }));
  scena.add(polvere);

  /* ── lastre laser: stop (rosso), break-even/trailing (ghiaccio), ingressi e take profit ── */
  function lastra(colore){
    const g = new THREE.Group();
    const piano = new THREE.Mesh(new THREE.PlaneGeometry(1, 7), new THREE.MeshBasicMaterial({ color: colore, transparent: true, opacity: .16, side: THREE.DoubleSide, depthWrite: false, toneMapped: false, blending: THREE.AdditiveBlending }));
    piano.rotation.x = -Math.PI / 2;
    const bordo = new THREE.Mesh(new THREE.BoxGeometry(1, .06, .06), new THREE.MeshBasicMaterial({ color: colore, toneMapped: false }));
    bordo.scale.set(1, 1, 1);
    const bordo2 = bordo.clone(); bordo.position.z = 3.5; bordo2.position.z = -3.5;
    const fronte = new THREE.Mesh(new THREE.BoxGeometry(1, .09, .09), new THREE.MeshBasicMaterial({ color: new THREE.Color(colore).multiplyScalar(2), toneMapped: false }));
    g.add(piano, bordo, bordo2, fronte); g.userData = { piano, mats: [piano.material, bordo.material, bordo2.material, fronte.material] };
    scena.add(g); return g;
  }
  function stendi(g, x0, x1, y, alfa){
    const w = Math.max(x1 - x0, .001);
    g.position.set((x0 + x1) / 2, y, 0); g.scale.set(w, 1, 1);
    g.visible = alfa > .01;
    g.userData.mats.forEach((m, k) => { m.transparent = true; m.opacity = (k === 0 ? .16 : 1) * alfa; });
  }
  const stopA = lastra(P.down), ingressoA = lastra(P.accLo), stopBL = lastra(P.down), ingressoB = lastra(P.accLo);
  const tp = [lastra(P.accHi), lastra(P.accHi), lastra(P.accHi)];
  [ingressoA, ingressoB].forEach(g => g.userData.piano.visible = false);
  tp.forEach(g => g.userData.piano.visible = false);

  /* ── esplosione quando lo stop ferma il prezzo ── */
  const nE = 260, posE = new Float32Array(nE * 3), dirE = [];
  for(let i = 0; i < nE; i++){ const a = rnd() * Math.PI * 2, b = rnd() * Math.PI - Math.PI / 2, v = .4 + rnd();
    dirE.push(new THREE.Vector3(Math.cos(a) * Math.cos(b) * v, Math.abs(Math.sin(b)) * v * .7, Math.sin(a) * Math.cos(b) * v)); }
  const scintille = new THREE.Points(new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(posE, 3)),
    new THREE.PointsMaterial({ color: new THREE.Color(P.down), size: .22, transparent: true, opacity: 0, depthWrite: false, toneMapped: false, blending: THREE.AdditiveBlending }));
  scena.add(scintille);
  let tEsplosione = -1;

  /* ── post-produzione: bagliore ── */
  const comp = new EffectComposer(gl);
  comp.addPass(new RenderPass(scena, cam));
  const bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), piccolo ? .35 : .45, .35, .45);
  comp.addPass(bloom);
  comp.addPass(new OutputPass());

  /* ── etichette HTML agganciate ai punti 3D ── */
  const etich = {};
  sez.querySelectorAll('[data-etichetta]').forEach(el => etich[el.dataset.etichetta] = el);
  const proj = new THREE.Vector3();
  function aggancia(nome, x, y, visibile, testo){
    const el = etich[nome]; if(!el) return;
    if(testo && el.textContent !== testo) el.textContent = testo;
    proj.set(x, y, 0).project(cam);
    const dentro = proj.z < 1 && Math.abs(proj.x) < 1.1 && Math.abs(proj.y) < 1.1;
    el.style.transform = `translate(${((proj.x + 1) / 2 * W).toFixed(1)}px,${((1 - proj.y) / 2 * H).toFixed(1)}px)`;
    el.classList.toggle('on', visibile && dentro);
  }

  /* ── regia: una inquadratura per capitolo, interpolata con lo scorrimento ── */
  const yE = Y(E);
  const regia = [
    { pos: [-25, 5.5, 27], guarda: [-11, .4, 0] },
    { pos: [-22, 4.5, 18], guarda: [-15, -1, 0] },
    { pos: [-10, 2, 15], guarda: [-9, -2.4, 0] },
    { pos: [4, 9, 28], guarda: [13, yE + 4.6, 0] },
    { pos: [30, 13, 30], guarda: [12, yE + 5, 0] },
    { pos: [-6, 40, 64], guarda: [-8, 0, 0] }
  ];
  const liscio = t => t * t * (3 - 2 * t);
  const posT = new THREE.Vector3(), guardaT = new THREE.Vector3(), guardaC = new THREE.Vector3(-4, 0, 0);
  function inquadra(f){
    const k = Math.min(Math.floor(f), regia.length - 2), u = liscio(THREE.MathUtils.clamp(f - k, 0, 1));
    const a = regia[k], b = regia[k + 1];
    posT.set(...a.pos).lerp(vp.set(...b.pos), u);
    guardaT.set(...a.guarda).lerp(vp.set(...b.guarda), u);
    if(W < H){                       // telefono: azione al centro e camera più indietro
      guardaT.x += 6;
      posT.sub(guardaT).multiplyScalar(1.35).add(guardaT);
    }
  }
  cam.position.set(...regia[0].pos);

  // quante candele sono visibili per ogni punto della storia
  function rivela(f){
    if(f < 1.6) return 40;
    if(f < 2.6) return 40 + (f - 1.6) * 16.5;          // trade A fino allo stop
    if(f < 3.7) return 56.5 + (f - 2.6) / 1.1 * 31;    // trade B: break-even, trailing, uscita
    return 87.5 + Math.min(1, (f - 3.7) / 1.3) * 8.5;
  }

  let W = 1, H = 1;
  function misura(){
    const r = cv.getBoundingClientRect(); W = r.width; H = r.height;
    gl.setSize(W, H, false); comp.setSize(W, H); bloom.setSize(W, H);
    cam.aspect = W / H; cam.fov = W < H ? 60 : 42;
    if(W < H) cam.setViewOffset(W, H, 0, H * .2, W, H); else cam.clearViewOffset();
    cam.updateProjectionMatrix();
  }
  misura(); addEventListener('resize', misura);

  const mouse = { x: 0, y: 0 };
  addEventListener('pointermove', e => { mouse.x = e.clientX / innerWidth - .5; mouse.y = e.clientY / innerHeight - .5; }, { passive: true });

  const capitoli = [...sez.querySelectorAll('.cap')];
  const tacche = [...sez.querySelectorAll('.storia-tacche i')];
  let capOn = -1, visibile = true, ultimoRiv = 0;
  new IntersectionObserver(v => { visibile = v[0].isIntersecting; }).observe(sez);

  function progresso(){
    const r = sez.getBoundingClientRect();
    return THREE.MathUtils.clamp(-r.top / Math.max(r.height - innerHeight, 1), 0, 1);
  }

  const orologio = new THREE.Clock();
  function fotogramma(){
    requestAnimationFrame(fotogramma);
    if(!visibile || !sez.closest('.page.on')) return;
    const t = orologio.getElapsedTime();
    const pr = progresso(), f = pr * 5;
    const cap = Math.min(5, Math.round(f));
    if(cap !== capOn){
      capitoli.forEach((c, i) => c.classList.toggle('on', i === cap));
      tacche.forEach((c, i) => c.classList.toggle('on', i <= cap));
      capOn = cap;
    }

    const riv = rivela(f);
    posaCandele(riv, t);

    // trade A: ingresso e stop, poi lo stop preso
    const aA = THREE.MathUtils.clamp((f - .55) * 2.2, 0, 1) * (1 - THREE.MathUtils.clamp((f - 3.2) * 2, 0, 1));
    const fineA = Math.min(Math.max(riv, 41), 50.6);
    stendi(stopA, X(39.5), X(fineA), Y(-1), aA);
    stendi(ingressoA, X(39.5), X(fineA), Y(0), aA * .55);
    const preso = riv >= 50.5;
    if(preso && tEsplosione < 0) tEsplosione = t;
    if(!preso) tEsplosione = -1;
    if(tEsplosione >= 0){
      const k = Math.min(1, (t - tEsplosione) / 1.4), e = 1 - Math.pow(1 - k, 3);
      for(let i = 0; i < nE; i++){ posE[i*3] = X(50) + dirE[i].x * e * 6; posE[i*3+1] = Y(-1) + dirE[i].y * e * 5; posE[i*3+2] = dirE[i].z * e * 6; }
      scintille.geometry.attributes.position.needsUpdate = true;
      scintille.material.opacity = (1 - k) * (fermo ? 0 : 1);
    } else scintille.material.opacity = 0;

    // trade B: lo stop sale a break-even e poi segue il prezzo
    const iB = Math.min(Math.floor(riv - .5), N - 1);
    const aB = THREE.MathUtils.clamp((riv - 56.6) * 1.5, 0, 1);
    const sB = iB >= 56 ? stopB[iB] : E - 1;
    const prima = sB < E - .001;
    stopBL.userData.mats.forEach(m => m.color && m.color.set(prima ? P.down : P.acc));
    stopBL.userData.mats[3].color.multiplyScalar(2);
    const yS = stopBL.position.y || Y(E - 1);
    stendi(stopBL, X(55.5), X(Math.max(riv, 56.6)), THREE.MathUtils.lerp(yS, Y(sB), fermo ? 1 : .18), aB);
    const fineB = uscita > 0 ? Math.min(riv, uscita + .5) : riv;
    stendi(ingressoB, X(55.5), X(Math.max(fineB, 56.6)), Y(E), aB * .5);

    // scaglioni: tre take profit a 20, 40 e 60 pip
    const aT = THREE.MathUtils.clamp((f - 3.35) * 2.2, 0, 1) * (1 - THREE.MathUtils.clamp((f - 4.6) * 2.5, 0, 1));
    tp.forEach((g, k) => stendi(g, X(56), X(86), Y(E + .8 * (k + 1)), aT));

    // etichette
    aggancia('stop', X(40.5), Y(-1), aA > .5 && f < 2.9, preso ? 'STOP PRESO · −1% · −100 €' : 'STOP · −1% = −100 €');
    aggancia('ingresso', X(40.5), Y(0), aA > .5 && f > .7 && f < 1.9, 'INGRESSO · 0,40 LOTTI');
    aggancia('be', X(be), Y(E), riv > be + .6 && f < 3.45, 'BREAK-EVEN');
    aggancia('trail', X(Math.min(riv, uscita > 0 ? uscita : riv)), Y(sB), riv > be + 3 && f < 3.45, uscita > 0 && riv > uscita + .5 ? `USCITA · +${pipUscita} PIP` : 'TRAILING STOP');
    ['tp1','tp2','tp3'].forEach((n, k) => aggancia(n, X(66 + k * 5), Y(E + .8 * (k + 1)), aT > .5, `TP${k+1} · +${20 * (k + 1)} PIP`));

    // camera: insegue l'inquadratura con un po' di inerzia, il mouse aggiunge parallasse
    inquadra(f);
    const morb = fermo ? 1 : .06;
    posT.x += mouse.x * 4; posT.y -= mouse.y * 2.5;
    if(!fermo && f < .5) { posT.x += Math.sin(t * .15) * 6; posT.z += Math.cos(t * .15) * 3; }
    cam.position.lerp(posT, morb);
    guardaC.lerp(guardaT, morb);
    cam.lookAt(guardaC);
    polvere.rotation.y = fermo ? 0 : t * .006;

    comp.render();
    if(!ultimoRiv){ sez.classList.add('pronto'); ultimoRiv = 1; }
  }
  fotogramma();
}
