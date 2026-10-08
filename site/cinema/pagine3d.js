/* Riskly · una scena 3D per ogni pagina, dietro al titolo.
   Si attenua mentre scorri e si ferma quando la pagina non è visibile.
   I colori arrivano da window.PAL (grafite o blu notte). */
import * as THREE from 'three';

avvia();

function avvia(){
  const P = window.PAL || { bg:'#0D0E10', panel:'#1B1E22', acc:'#C9C5BC', accHi:'#F2EFE9', accLo:'#8F8C86', up:'#5FAE8A', down:'#CC6A61', line:'#2A2D32' };
  const piccolo = innerWidth < 760;
  const fermo = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const cv = document.createElement('canvas');
  cv.id = 'scena3d'; cv.setAttribute('aria-hidden', 'true');
  document.body.prepend(cv);
  let gl;
  try { gl = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, powerPreference: 'high-performance' }); }
  catch(e){ cv.remove(); return; }
  gl.setPixelRatio(Math.min(devicePixelRatio || 1, piccolo ? 1.5 : 2));
  gl.setClearColor(0x000000, 0);

  let seme = 11;
  const rnd = () => (seme = (seme * 16807) % 2147483647) / 2147483647;
  const col = c => new THREE.Color(c);
  const linea = (c, o = 1) => new THREE.LineBasicMaterial({ color: col(c), transparent: o < 1, opacity: o });
  function bordi(geo, c, o){ return new THREE.LineSegments(new THREE.EdgesGeometry(geo), linea(c, o)); }
  function base(fog = .045){
    const scena = new THREE.Scene();
    scena.fog = new THREE.Fog(col(P.bg), 18, 60);
    scena.add(new THREE.AmbientLight(0xffffff, .9));
    const sole = new THREE.DirectionalLight(0xffffff, 1.4); sole.position.set(6, 12, 8); scena.add(sole);
    const cam = new THREE.PerspectiveCamera(40, 1, .1, 200);
    return { scena, cam };
  }
  const solido = (o = .92) => new THREE.MeshStandardMaterial({ color: col(P.panel).lerp(col(P.acc), .16), metalness: .25, roughness: .55, transparent: o < 1, opacity: o });

  /* ── BOT: tre moduli e una lastra-limite che ferma ciò che cade ── */
  function bot(){
    const { scena, cam } = base();
    const g = new THREE.GridHelper(60, 30, col(P.accLo), col(P.line)); g.position.y = -.01; scena.add(g);
    [-4, 0, 4].forEach((x, i) => {
      const geo = new THREE.BoxGeometry(2.2, 5.6 + i * .5, .55);
      const m = new THREE.Mesh(geo, solido()); m.position.set(x, (5.6 + i * .5) / 2, 0); scena.add(m);
      const b = bordi(geo, P.acc, .9); b.position.copy(m.position); scena.add(b);
    });
    const limite = new THREE.Mesh(new THREE.PlaneGeometry(15, 6), new THREE.MeshBasicMaterial({ color: col(P.down), transparent: true, opacity: .1, side: THREE.DoubleSide, depthWrite: false }));
    limite.rotation.x = -Math.PI / 2; limite.position.y = 1.6; scena.add(limite);
    const bl = bordi(new THREE.BoxGeometry(15, .001, 6), P.down, .9); bl.position.y = 1.6; scena.add(bl);
    const N = piccolo ? 14 : 24, cubi = [];
    const geoC = new THREE.BoxGeometry(.34, .34, .34);
    for(let i = 0; i < N; i++){
      const m = new THREE.Mesh(geoC, new THREE.MeshStandardMaterial({ color: col(rnd() < .5 ? P.down : P.up), metalness: .3, roughness: .4, transparent: true }));
      m.userData = { v: 0, ferma: 0 }; riparti(m, true); scena.add(m); cubi.push(m);
    }
    function riparti(m, primo){ m.position.set((rnd() - .5) * 13, 7 + rnd() * (primo ? 9 : 3), (rnd() - .5) * 5); m.userData.v = 0; m.userData.ferma = 0; m.material.opacity = 1; }
    return { scena, cam, guarda: new THREE.Vector3(0, 2.6, 0), orbita: [24, 9, 0.1],
      agg(t, dt){
        cubi.forEach(m => {
          const u = m.userData;
          if(u.ferma){ u.ferma += dt; m.material.opacity = Math.max(0, 1 - u.ferma / 1.4); if(u.ferma > 1.6) riparti(m); return; }
          u.v += 9.8 * dt * .35; m.position.y -= u.v * dt; m.rotation.x += dt; m.rotation.y += dt * .7;
          if(m.position.y <= 1.6 + .17 && Math.abs(m.position.x) < 7.5 && Math.abs(m.position.z) < 3){ m.position.y = 1.77; u.ferma = .001; }
        });
      } };
  }

  /* ── CALCOLATORI: Monte Carlo nello spazio ── */
  function calc(){
    const { scena, cam } = base();
    const S = piccolo ? 70 : 110, NP = piccolo ? 36 : 64, linee = [];
    for(let k = 0; k < NP; k++){
      const pos = new Float32Array(S * 3); let y = 0;
      for(let i = 0; i < S; i++){
        y += (rnd() < .5 ? .16 : -.08) + (rnd() - .5) * .05;   // winrate 50%, rapporto 2:1
        pos[i*3] = -10 + 20 * i / (S - 1); pos[i*3+1] = y * .55; pos[i*3+2] = -6 + 12 * k / (NP - 1);
      }
      const geo = new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(pos, 3));
      const finale = pos[(S-1)*3+1];
      const l = new THREE.Line(geo, linea(finale < -1.4 ? P.down : P.acc, finale < -1.4 ? .7 : .28)); scena.add(l); linee.push(l);
    }
    const med = linee[Math.floor(NP / 2)]; med.material = linea(P.accHi, 1);
    const pav = new THREE.Mesh(new THREE.PlaneGeometry(22, 14), new THREE.MeshBasicMaterial({ color: col(P.down), transparent: true, opacity: .07, side: THREE.DoubleSide, depthWrite: false }));
    pav.rotation.x = -Math.PI / 2; pav.position.y = -1.65; scena.add(pav);
    const pb = bordi(new THREE.BoxGeometry(22, .001, 14), P.down, .5); pb.position.y = -1.65; scena.add(pb);
    let ciclo = 0;
    return { scena, cam, guarda: new THREE.Vector3(0, .8, 0), orbita: [19, 7, .07],
      agg(t, dt){
        ciclo += dt; const k = fermo ? 1 : Math.min(1, ciclo / 6);
        if(ciclo > 9) ciclo = 0;
        linee.forEach(l => l.geometry.setDrawRange(0, Math.max(2, Math.floor(S * (1 - Math.pow(1 - k, 2))))));
      } };
  }

  /* ── JOURNAL: uno skyline di dati ── */
  function app(){
    const { scena, cam } = base();
    const NX = piccolo ? 16 : 24, NZ = piccolo ? 7 : 10, n = NX * NZ;
    const mesh = new THREE.InstancedMesh(new THREE.BoxGeometry(.7, 1, .7), new THREE.MeshStandardMaterial({ metalness: .45, roughness: .4 }), n);
    const alt = [], m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), s = new THREE.Vector3();
    for(let i = 0; i < NX; i++) for(let j = 0; j < NZ; j++){
      const h = .4 + i * .16 + Math.sin(i * .7 + j) * .6 + rnd() * .8;
      const k = i * NZ + j; alt[k] = Math.max(.2, h);
      mesh.setColorAt(k, col(rnd() < .22 ? P.down : (rnd() < .5 ? P.up : P.panel)).multiplyScalar(rnd() < .22 ? .9 : 1));
    }
    scena.add(mesh);
    const g = new THREE.GridHelper(60, 60, col(P.accLo), col(P.line)); scena.add(g);
    let nato = 0;
    return { scena, cam, guarda: new THREE.Vector3(0, 1.6, 0), orbita: [20, 11, .06],
      agg(t, dt){
        nato = fermo ? 1 : Math.min(1, nato + dt / 1.6);
        for(let i = 0; i < NX; i++) for(let j = 0; j < NZ; j++){
          const k = i * NZ + j, e = 1 - Math.pow(1 - Math.min(1, Math.max(0, nato * 1.6 - i / NX * .6)), 3);
          const h = alt[k] * e * (1 + (fermo ? 0 : Math.sin(t * .8 + i * .4 + j) * .04));
          v.set((i - NX / 2) * .95, h / 2, (j - NZ / 2) * .95); s.set(1, Math.max(h, .001), 1);
          mesh.setMatrixAt(k, m4.compose(v, q, s));
        }
        mesh.instanceMatrix.needsUpdate = true;
      } };
  }

  /* ── PREZZI: tre piedistalli ── */
  function prezzi(){
    const { scena, cam } = base();
    const g = new THREE.GridHelper(60, 30, col(P.accLo), col(P.line)); scena.add(g);
    const pezzi = [];
    [[-4, 1.6], [0, 2.6], [4, 3.6]].forEach(([x, h], i) => {
      const geo = new THREE.CylinderGeometry(1.5, 1.5, h, 6);
      const m = new THREE.Mesh(geo, solido()); m.position.set(x, h / 2, 0); scena.add(m);
      const b = bordi(geo, i === 1 ? P.accHi : P.acc, .9); b.position.copy(m.position); scena.add(b);
      const gem = new THREE.Mesh(new THREE.OctahedronGeometry(.55), new THREE.MeshStandardMaterial({ color: col(i === 1 ? P.accHi : P.acc), metalness: .8, roughness: .2 }));
      gem.position.set(x, h + 1.1, 0); scena.add(gem); pezzi.push({ gem, y: h + 1.1, i });
    });
    return { scena, cam, guarda: new THREE.Vector3(0, 2.2, 0), orbita: [21, 7, .1],
      agg(t){ pezzi.forEach(p => { p.gem.rotation.y = t * .8 + p.i; p.gem.position.y = p.y + (fermo ? 0 : Math.sin(t * 1.4 + p.i) * .18); }); } };
  }

  /* ── CORSO: dieci moduli come lastre a ventaglio ── */
  function corso(){
    const { scena, cam } = base();
    const lastre = [];
    for(let i = 0; i < 10; i++){
      const geo = new THREE.BoxGeometry(6, 3.6, .06);
      const gr = new THREE.Group();
      gr.add(new THREE.Mesh(geo, solido(.88)), bordi(geo, i % 3 === 0 ? P.accHi : P.acc, .75));
      gr.position.set((i - 4.5) * .35, 2.2, (i - 4.5) * .7); gr.rotation.y = -.5 + i * .03;
      scena.add(gr); lastre.push(gr);
    }
    const g = new THREE.GridHelper(60, 30, col(P.accLo), col(P.line)); scena.add(g);
    return { scena, cam, guarda: new THREE.Vector3(0, 2.2, 0), orbita: [20, 6, .08],
      agg(t){
        const att = Math.floor(t / 1.6) % 10;
        lastre.forEach((l, i) => { const su = i === att && !fermo ? 1 : 0; l.position.y += ((2.2 + su * .9) - l.position.y) * .08; });
      } };
  }

  /* ── METODO: un terreno topografico sorvolato ── */
  function metodo(){
    const { scena, cam } = base();
    const geo = new THREE.PlaneGeometry(60, 60, piccolo ? 60 : 100, piccolo ? 60 : 100); geo.rotateX(-Math.PI / 2);
    const p = geo.attributes.position;
    const z = (x, y) => Math.sin(x * .18) * 1.6 + Math.cos(y * .15) * 1.4 + Math.sin((x + y) * .07) * 2.2;
    for(let i = 0; i < p.count; i++) p.setY(i, z(p.getX(i), p.getZ(i)));
    geo.computeVertexNormals();
    scena.add(new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: col(P.panel), metalness: .2, roughness: .9 })));
    const w = new THREE.LineSegments(new THREE.WireframeGeometry(geo), linea(P.accLo, .35)); w.position.y = .01; scena.add(w);
    const pts = []; for(let k = 0; k <= 80; k++){ const x = -24 + k * .6, y = Math.sin(k * .18) * 6; pts.push(new THREE.Vector3(x, z(x, y) + .15, y)); }
    scena.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), linea(P.accHi)));
    return { scena, cam, guarda: new THREE.Vector3(0, 1, 0), orbita: [20, 10, .04], agg(){} };
  }

  /* ── FAQ: una sfera geodetica ── */
  function faq(){
    const { scena, cam } = base();
    const geo = new THREE.IcosahedronGeometry(3.6, 2);
    const gr = new THREE.Group();
    gr.add(new THREE.Mesh(new THREE.IcosahedronGeometry(3.45, 2), solido(.85)), bordi(geo, P.acc, .55));
    gr.add(new THREE.Points(geo, new THREE.PointsMaterial({ color: col(P.accHi), size: .09 })));
    gr.position.y = 3.6; scena.add(gr);
    const g = new THREE.GridHelper(60, 30, col(P.accLo), col(P.line)); scena.add(g);
    return { scena, cam, guarda: new THREE.Vector3(0, 3.4, 0), orbita: [21, 5, .05],
      agg(t){ if(!fermo){ gr.rotation.y = t * .12; gr.rotation.x = Math.sin(t * .2) * .15; } } };
  }

  const COSTRUTTORI = { bot, calc, app, journal: prezzi, corso, metodo, faq };
  const pronte = {};
  let attiva = null, pagina = '';

  let W = 1, H = 1;
  function misura(){
    W = innerWidth; H = innerHeight;
    gl.setSize(W, H, false);
    Object.values(pronte).forEach(inquadra);
  }
  function inquadra(sc){
    sc.cam.aspect = W / H; sc.cam.fov = W < H ? 55 : 40;
    if(W < H) sc.cam.setViewOffset(W, H, 0, H * .14, W, H);          // telefono: scena più in alto
    else sc.cam.setViewOffset(W, H, -W * .24, 0, W, H);              // computer: scena a destra del titolo
    sc.cam.updateProjectionMatrix();
  }
  addEventListener('resize', misura);

  function scegli(){
    const on = document.querySelector('.page.on'); const id = on ? on.id : '';
    if(id === pagina) return; pagina = id;
    const f = COSTRUTTORI[id];
    if(f && !pronte[id]){ pronte[id] = f(); inquadra(pronte[id]); }
    attiva = f ? pronte[id] : null;
    cv.dataset.pagina = id;
    document.body.classList.toggle('con3d', !!attiva);
  }
  new MutationObserver(scegli).observe(document.body, { subtree: true, attributes: true, attributeFilter: ['class'] });
  misura(); scegli();

  const mouse = { x: 0, y: 0 };
  addEventListener('pointermove', e => { mouse.x = e.clientX / innerWidth - .5; mouse.y = e.clientY / innerHeight - .5; }, { passive: true });

  const orologio = new THREE.Clock(); let ultimo = 0;
  function giro(){
    requestAnimationFrame(giro);
    if(!attiva || document.hidden) return;
    const t = orologio.getElapsedTime(), dt = Math.min(.05, t - ultimo); ultimo = t;
    const sbiadito = Math.max(.22, 1 - scrollY / (innerHeight * .85)) * (pagina === 'app' ? .45 : 1);
    cv.style.opacity = sbiadito.toFixed(3);
    const [r, h, vel] = attiva.orbita;
    const a = fermo ? .7 : .7 + t * vel;
    attiva.cam.position.set(Math.sin(a) * r + mouse.x * 2.5, h - mouse.y * 1.5, Math.cos(a) * r);
    attiva.cam.lookAt(attiva.guarda);
    attiva.agg(t, dt);
    gl.render(attiva.scena, attiva.cam);
  }
  giro();
}
