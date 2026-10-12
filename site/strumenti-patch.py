import sys, re
p = sys.argv[1]; s = open(p).read()

def blocco(s, i):
    """restituisce la fine del <div ...> che inizia in i (div bilanciati)"""
    d = 0; j = i
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        d += 1 if m.group() == '<div' else -1
        if d == 0: return i + m.end()
    raise ValueError

# --- etichette del menu: Calcolatori -> Strumenti
s = s.replace('<span>Calcolatori</span></button>', '<span>Strumenti</span></button>')
s = s.replace('stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8.5 7h7"/><path d="M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01M8.5 15h.01M12 15h.01M15.5 15h.01M8.5 18h.01M12 18h.01M15.5 18h.01"/></svg>Calcoli</button>',
              'stroke-linejoin="round"><rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8.5 7h7"/><path d="M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01M8.5 15h.01M12 15h.01M15.5 15h.01M8.5 18h.01M12 18h.01M15.5 18h.01"/></svg>Strumenti</button>')
s = s.replace('''<button onclick="go('calc',this)">Calcolatori</button>''', '''<button onclick="go('calc',this)">Strumenti</button>''')
s = s.replace('''<a onclick="go('calc')">Calcolatori</a>''', '''<a onclick="go('calc')">Strumenti</a>''')

# --- pagina
a = s.index('<div class="page" id="calc">'); fine_pag = blocco(s, a)
pag = s[a:fine_pag]
pag = pag.replace('<span class="sez-num">CALCOLATORI</span>', '<span class="sez-num">STRUMENTI</span>')
pag = pag.replace('<h2>Calcola prima, <em>non dopo</em></h2>', '<h2>Tutto quello che serve <em>prima del trade</em></h2>')
pag = pag.replace('<p class="lead">Cinque strumenti gratuiti, senza registrazione. Girano nel tuo browser: nessun dato viene inviato.</p>',
                  '<p class="lead">Calendario economico in tempo reale e cinque calcolatori gratuiti, senza registrazione. I calcolatori girano nel tuo browser: nessun dato viene inviato.</p>')

def carta(titolo):
    i = pag.index('<h3>' + titolo + '</h3>'); i = pag.rindex('<div class="card"', 0, i); return i, blocco(pag, i)
nomi = [('posizione', 'Dimensione della posizione'), ('montecarlo', 'Rischio di rovina'), ('prop', 'Tracker challenge prop firm'),
        ('recupero', 'Recupero dopo una perdita'), ('crescita', 'Crescita composta')]
carte = {}
for k, t in nomi:
    i, j = carta(t); c = pag[i:j]
    c = c.replace('<div class="card" style="margin-top:13px">', '<div class="card">', 1)
    carte[k] = c
ini = pag.index('<div class="calc-grid">'); fin = pag.index('<div class="capture"')
ic = lambda d: f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'
tab = [('calendario', 'Calendario', ic('<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>')),
       ('posizione', 'Posizione', ic('<path d="M12 3v18M5 8h14M7 13h10M9 18h6"/>')),
       ('montecarlo', 'Monte Carlo', ic('<path d="M3 17c3-1 4-8 7-8s3 6 6 6 3-9 5-10"/><path d="M3 21h18"/>')),
       ('prop', 'Prop firm', ic('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>')),
       ('recupero', 'Recupero', ic('<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/>')),
       ('crescita', 'Crescita', ic('<path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/>'))]
navh = '<div class="str-nav" role="tablist" aria-label="Strumenti">' + ''.join(
    f'<button role="tab" data-st="{k}" class="{"on" if k == "calendario" else ""}" onclick="strTab(\'{k}\')">{svg}<span>{n}</span></button>' for k, n, svg in tab) + '</div>\n'
cal = '''<div class="str-pannello on" id="st-calendario">
        <div class="card cal-card">
          <div class="card-head"><h3>Calendario economico</h3><span class="meta cal-live"><i></i>in tempo reale</span></div>
          <p class="cal-sotto">I dati che muovono forex, oro e indici. Il valore effettivo compare appena il dato esce; gli orari sono nella tua ora locale.</p>
          <div class="cal-filtri">
            <div class="cal-gruppo" id="calImp"><span>Importanza</span>
              <button class="cal-chip alta" data-v="1"><span class="tori"><b></b><b></b><b></b></span>Alta</button>
              <button class="cal-chip media" data-v="0"><span class="tori"><b></b><b></b><b></b></span>Media</button>
              <button class="cal-chip bassa" data-v="-1"><span class="tori"><b></b><b></b><b></b></span>Bassa</button></div>
            <div class="cal-gruppo" id="calPaesi"><span>Paesi</span>
              <button class="cal-chip" data-v="us">🇺🇸 USA</button><button class="cal-chip" data-v="eu">🇪🇺 Area euro</button><button class="cal-chip" data-v="it">🇮🇹 Italia</button>
              <button class="cal-chip" data-v="de">🇩🇪 Germania</button><button class="cal-chip" data-v="gb">🇬🇧 Regno Unito</button><button class="cal-chip" data-v="jp">🇯🇵 Giappone</button>
              <button class="cal-chip" data-v="ch">🇨🇭 Svizzera</button><button class="cal-chip" data-v="ca">🇨🇦 Canada</button><button class="cal-chip" data-v="au">🇦🇺 Australia</button>
              <button class="cal-chip" data-v="nz">🇳🇿 Nuova Zelanda</button><button class="cal-chip" data-v="cn">🇨🇳 Cina</button></div>
            <div class="cal-rapidi"><button data-preset="forex">Solo quello che muove il forex</button><button data-preset="usa">Solo USA, alta importanza</button><button data-preset="tutto">Mostra tutto</button></div>
          </div>
          <div class="cal-cornice" id="calCornice"></div>
          <p class="cal-nota">Dati forniti da <a href="https://it.tradingview.com/economic-calendar/" rel="noopener" target="_blank">TradingView</a>. Orari e valori possono cambiare: verifica sempre prima di operare. Nei minuti intorno ai dati importanti spread e slippage possono farti perdere più del previsto: Riskly Pro non apre operazioni vicino alle notizie.</p>
        </div>
      </div>
'''
corpo = navh + cal + ''.join(f'      <div class="str-pannello" id="st-{k}">\n        {carte[k]}\n      </div>\n' for k, _ in nomi) + '\n      '
pag = pag[:ini] + corpo + pag[fin:]
s = s[:a] + pag + s[fine_pag:]

# --- stile
css = '''
  /* ═══ STRUMENTI: barra delle sotto-pagine e calendario ═══ */
  .str-nav{display:flex;gap:6px;justify-content:center;margin:0 auto 22px;position:sticky;top:76px;z-index:20;width:max-content;max-width:100%;
    padding:6px;background:rgba(16,19,17,.96);border:1px solid rgba(182,216,79,.35);border-radius:100px;backdrop-filter:blur(10px);
    box-shadow:0 10px 30px rgba(0,0,0,.5),0 0 0 4px rgba(182,216,79,.05)}
  .str-nav button{display:inline-flex;align-items:center;gap:8px;background:none;border:none;color:var(--text);font-family:inherit;font-size:.95rem;font-weight:600;
    padding:11px 18px;border-radius:100px;cursor:pointer;white-space:nowrap;transition:background-color .15s ease,transform .1s ease}
  .str-nav button svg{width:17px;height:17px;opacity:.85}
  .str-nav button:active{transform:scale(.97)}
  @media (hover:hover) and (pointer:fine){.str-nav button:hover{background:rgba(255,255,255,.06)}}
  .str-nav button.on{background:var(--grad);color:#0B0D0C}
  .str-pannello{display:none;max-width:760px;margin:0 auto}
  .str-pannello.on{display:block}
  #st-calendario{max-width:none}
  @media(max-width:760px){
    .str-nav{width:100%;justify-content:flex-start;overflow-x:auto;scrollbar-width:none;border-radius:16px;top:calc(8px + env(safe-area-inset-top))}
    .str-nav::-webkit-scrollbar{display:none}
    .str-nav button{flex:0 0 auto;flex-direction:column;gap:4px;padding:8px 12px;font-size:.78rem;border-radius:12px}
  }
  .cal-live{display:inline-flex;align-items:center;gap:7px;color:var(--accent)}
  .cal-live i{width:7px;height:7px;border-radius:50%;background:var(--accent);animation:calPulsa 2s infinite}
  @keyframes calPulsa{0%{box-shadow:0 0 0 0 rgba(182,216,79,.6)}70%{box-shadow:0 0 0 8px rgba(182,216,79,0)}100%{box-shadow:0 0 0 0 rgba(182,216,79,0)}}
  @media (prefers-reduced-motion:reduce){.cal-live i{animation:none}}
  .cal-sotto{color:var(--dim);font-size:.92rem;margin:-2px 0 14px}
  .cal-filtri{display:grid;gap:12px;padding:14px;border:1px solid var(--line);border-radius:12px;background:rgba(255,255,255,.015);margin-bottom:12px}
  .cal-gruppo{display:flex;flex-wrap:wrap;align-items:center;gap:7px}
  .cal-gruppo>span{font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--dim2);font-weight:600;min-width:92px}
  .cal-chip{appearance:none;border:1px solid var(--line);background:transparent;color:var(--dim);font:500 .85rem inherit;font-family:inherit;padding:6px 11px;border-radius:999px;
    cursor:pointer;display:inline-flex;align-items:center;gap:7px;transition:background-color .15s ease,color .15s ease,border-color .15s ease,transform .1s ease}
  .cal-chip:active{transform:scale(.97)}
  @media (hover:hover) and (pointer:fine){.cal-chip:hover{color:var(--text);border-color:#3A423B}}
  .cal-chip[aria-pressed="true"]{background:var(--accent-soft);color:var(--text);border-color:rgba(182,216,79,.5)}
  .cal-chip .tori{display:inline-flex;gap:2px}.cal-chip .tori b{width:5px;height:11px;border-radius:1px;background:var(--dim2)}
  .cal-chip.alta .tori b{background:var(--down)}.cal-chip.media .tori b:nth-child(-n+2){background:var(--gold)}.cal-chip.bassa .tori b:first-child{background:var(--dim)}
  .cal-rapidi{display:flex;flex-wrap:wrap;gap:4px 14px;border-top:1px solid var(--line);padding-top:10px}
  .cal-rapidi button{appearance:none;border:0;background:none;color:var(--accent);font:500 .84rem inherit;font-family:inherit;cursor:pointer;padding:3px 0}
  .cal-rapidi button:hover{text-decoration:underline}
  .cal-cornice{height:min(74vh,780px);min-height:480px;border:1px solid var(--line);border-radius:12px;overflow:hidden;position:relative}
  .cal-cornice .vuoto{position:absolute;inset:0;display:grid;place-items:center;color:var(--dim);text-align:center;padding:24px}
  .cal-cornice .tradingview-widget-container,.cal-cornice .tradingview-widget-container__widget{height:100%}
  .cal-nota{color:var(--dim2);font-size:.78rem;line-height:1.55;margin-top:10px}
  .cal-nota a{color:var(--dim)}
  @media(max-width:620px){.cal-gruppo>span{min-width:100%}.cal-cornice{height:70vh}}
'''
k = s.index('</style>'); s = s[:k] + css + s[k:]

# --- script
js = '''
/* ═══ STRUMENTI: sotto-pagine e calendario economico ═══ */
function strTab(nome){
  document.querySelectorAll('.str-pannello').forEach(x => x.classList.toggle('on', x.id === 'st-' + nome));
  document.querySelectorAll('.str-nav button').forEach(b => { const on = b.dataset.st === nome; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); });
  const nav = document.querySelector('.str-nav'), b = nav && nav.querySelector('button.on');
  if(b && nav.scrollWidth > nav.clientWidth) nav.scrollTo({ left: b.offsetLeft - nav.clientWidth / 2 + b.offsetWidth / 2, behavior: 'smooth' });
  const menu = document.querySelector('nav');
  const sopra = (menu && getComputedStyle(menu).position === 'sticky') ? menu.offsetHeight + 16 : 16;
  if(nav && nav.getBoundingClientRect().top < sopra) window.scrollTo({ top: Math.max(0, nav.getBoundingClientRect().top + window.scrollY - sopra), behavior: 'smooth' });
  try { localStorage.setItem('riskly-strumento', nome); } catch(e) {}
  if(nome === 'calendario') calDisegna();
}
const CAL_PREDEF = { imp: ['1', '0'], paesi: ['us', 'eu', 'gb', 'jp', 'ch', 'ca', 'au', 'nz', 'cn', 'de', 'it'] };
const CAL_PRESET = { forex: { imp: ['1', '0'], paesi: ['us', 'eu', 'gb', 'jp', 'ch', 'ca', 'au', 'nz'] }, usa: { imp: ['1'], paesi: ['us'] },
                     tutto: { imp: ['1', '0', '-1'], paesi: CAL_PREDEF.paesi } };
let calStato = CAL_PREDEF, calChiave = '', calAttesa;
try { calStato = JSON.parse(localStorage.getItem('riskly-calendario')) || CAL_PREDEF; } catch(e) {}
function calSegna(){
  document.querySelectorAll('#calImp .cal-chip').forEach(b => b.setAttribute('aria-pressed', calStato.imp.includes(b.dataset.v)));
  document.querySelectorAll('#calPaesi .cal-chip').forEach(b => b.setAttribute('aria-pressed', calStato.paesi.includes(b.dataset.v)));
}
function calDisegna(){
  const box = document.getElementById('calCornice'); if(!box) return;
  const chiave = calStato.imp.join(',') + '|' + calStato.paesi.join(',');
  if(chiave === calChiave && box.childElementCount) return;      // già caricato con questi filtri
  clearTimeout(calAttesa);
  calAttesa = setTimeout(() => {
    try { localStorage.setItem('riskly-calendario', JSON.stringify(calStato)); } catch(e) {}
    calChiave = chiave; box.innerHTML = '';
    if(!calStato.imp.length || !calStato.paesi.length){ box.innerHTML = '<div class="vuoto">Scegli almeno un livello di importanza e un paese.</div>'; return; }
    const c = document.createElement('div'); c.className = 'tradingview-widget-container';
    const w = document.createElement('div'); w.className = 'tradingview-widget-container__widget'; c.appendChild(w);
    const sc = document.createElement('script'); sc.src = 'https://s3.tradingview.com/external-embedding/embed-widget-events.js'; sc.async = true;
    sc.text = JSON.stringify({ colorTheme: 'dark', isTransparent: true, width: '100%', height: '100%', locale: 'it',
                               importanceFilter: calStato.imp.join(','), countryFilter: calStato.paesi.join(',') });
    c.appendChild(sc); box.appendChild(c);
  }, 250);
}
(function(){
  const cambia = (id, chiave) => { const g = document.getElementById(id); if(!g) return;
    g.addEventListener('click', e => { const b = e.target.closest('.cal-chip'); if(!b) return; const v = b.dataset.v, l = calStato[chiave];
      calStato = { ...calStato, [chiave]: l.includes(v) ? l.filter(x => x !== v) : [...l, v] }; calSegna(); calDisegna(); }); };
  cambia('calImp', 'imp'); cambia('calPaesi', 'paesi');
  document.querySelectorAll('.cal-rapidi button').forEach(b => b.addEventListener('click', () => { calStato = { ...CAL_PRESET[b.dataset.preset] }; calSegna(); calDisegna(); }));
  calSegna();
  let ultimo = 'calendario'; try { ultimo = localStorage.getItem('riskly-strumento') || 'calendario'; } catch(e) {}
  if(!document.getElementById('st-' + ultimo)) ultimo = 'calendario';
  document.querySelectorAll('.str-pannello').forEach(x => x.classList.toggle('on', x.id === 'st-' + ultimo));
  document.querySelectorAll('.str-nav button').forEach(b => { const on = b.dataset.st === ultimo; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); });
  /* il calendario si carica solo quando apri la pagina Strumenti */
  const pag = document.getElementById('calc');
  if(pag) new MutationObserver(() => { if(pag.classList.contains('on') && document.getElementById('st-calendario').classList.contains('on')) calDisegna(); })
            .observe(pag, { attributes: true, attributeFilter: ['class'] });
})();
'''
k = s.rindex('calcPos(); calcRuin(); calcProp(); calcBE(); calcComp();')
k = s.index('\n', k) + 1
s = s[:k] + js + s[k:]
open(p, 'w').write(s)
print('ok')
