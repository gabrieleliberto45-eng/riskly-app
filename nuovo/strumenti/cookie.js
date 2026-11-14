/* Riskly · banner dei cookie (14 novembre 2026, Gabriele: "aggiungi i cookie").
   I siti Riskly usano solo cookie e memoria del browser tecnici: niente pubblicità né profilazione.
   L'unico contenuto esterno che può usare cookie propri è il calendario di TradingView: si carica solo con il consenso
   ("Contenuti esterni"). La scelta resta nel browser (riskly-consenso) e si cambia dal link "Preferenze cookie".
   Uso: <script src="/cookie.js" defer></script> prima di </body>. Per riaprire: rCookiePreferenze(). */
(function(){
  var CHIAVE = 'riskly-consenso', VERSIONE = 1;
  function leggi(){ try { var c = JSON.parse(localStorage.getItem(CHIAVE) || 'null'); return c && c.v === VERSIONE ? c : null; } catch(e) { return null; } }
  function salva(esterni){
    try {
      localStorage.setItem(CHIAVE, JSON.stringify({ v: VERSIONE, esterni: !!esterni, data: new Date().toISOString() }));
      if(esterni) localStorage.setItem('riskly-tv-ok', '1'); else localStorage.removeItem('riskly-tv-ok');
    } catch(e) {}
    window.rtvOk = !!esterni;
    chiudi();
    try { window.dispatchEvent(new CustomEvent('riskly-consenso', { detail: { esterni: !!esterni } })); } catch(e) {}
  }
  var stile = '#rck{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;max-width:560px;margin:0 auto;background:#fff;color:#0F1B2D;'
    + 'border:1px solid #DCE1E8;border-radius:12px;box-shadow:0 18px 50px -18px rgba(15,27,45,.45);padding:18px 18px 16px;font:400 14px/1.5 "Instrument Sans",system-ui,-apple-system,"Segoe UI",sans-serif}'
    + '#rck .rck-t{font-weight:700;font-size:16px;line-height:1.3;margin:0 0 6px}'
    + '#rck p{margin:0 0 12px;color:#4B5565}#rck a{color:#12263F;text-decoration:underline}'
    + '#rck .rck-b{display:flex;gap:8px;flex-wrap:wrap}'
    + '#rck button{font:600 14px/1 inherit;font-family:inherit;border-radius:8px;padding:11px 14px;cursor:pointer;border:1px solid #12263F;background:#fff;color:#12263F;flex:1 1 auto}'
    + '#rck button.pri{background:#12263F;color:#fff}#rck button.lnk{border-color:transparent;background:none;text-decoration:underline;flex:0 0 auto;padding:11px 6px}'
    + '#rck .rck-v{border-top:1px solid #EBEEF3;padding:10px 0;display:flex;gap:12px;align-items:flex-start;justify-content:space-between}'
    + '#rck .rck-v b{display:block;font-size:14px}#rck .rck-v small{display:block;color:#566273;font-size:12.5px;line-height:1.45}'
    + '#rck input{width:20px;height:20px;margin-top:2px;flex:0 0 20px;accent-color:#12263F}'
    + 'html[data-tema="scuro"] #rck{background:#111926;color:#E7ECF3;border-color:#202C3F}html[data-tema="scuro"] #rck p,html[data-tema="scuro"] #rck .rck-v small{color:#9CA8B8}'
    + 'html[data-tema="scuro"] #rck a,html[data-tema="scuro"] #rck button{color:#E7ECF3;border-color:#E7ECF3}html[data-tema="scuro"] #rck button{background:transparent}'
    + 'html[data-tema="scuro"] #rck button.pri{background:#E7ECF3;color:#0A0F18}html[data-tema="scuro"] #rck .rck-v{border-color:#202C3F}'
    + '@media(max-width:520px){#rck{left:10px;right:10px;bottom:10px;padding:16px 14px 14px}#rck button{flex:1 1 100%}#rck button.lnk{flex:1 1 100%}}';
  var box;
  function chiudi(){ if(box){ box.remove(); box = null; } }
  function mostra(preferenze){
    chiudi();
    if(!document.getElementById('rck-stile')){ var s = document.createElement('style'); s.id = 'rck-stile'; s.textContent = stile; document.head.appendChild(s); }
    var c = leggi();
    box = document.createElement('div'); box.id = 'rck'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-label', 'Cookie');
    var info = '<a href="https://riskly.trade/privacy.html#cookie">Informativa privacy e cookie</a>';
    box.innerHTML = preferenze
      ? '<div class="rck-t">Preferenze cookie</div>'
        + '<div class="rck-v"><div><b>Necessari</b><small>Accesso, preferenze e filtri salvati nel browser. Servono al funzionamento: sempre attivi.</small></div><input type="checkbox" checked disabled aria-label="Necessari, sempre attivi"></div>'
        + '<div class="rck-v"><div><b>Contenuti esterni</b><small>Il calendario economico di TradingView si carica dai suoi server e può usare cookie propri.</small></div><input type="checkbox" id="rck-est"' + (c && c.esterni ? ' checked' : '') + ' aria-label="Contenuti esterni"></div>'
        + '<p style="margin-top:6px">Non usiamo cookie pubblicitari né di profilazione. ' + info + '.</p>'
        + '<div class="rck-b"><button type="button" class="pri" id="rck-salva">Salva le scelte</button><button type="button" id="rck-tutto">Accetta tutto</button></div>'
      : '<div class="rck-t">Cookie</div><p>Usiamo solo cookie tecnici, necessari al funzionamento. Niente pubblicità né profilazione. Alcuni contenuti esterni, come il calendario di TradingView, si caricano solo se li accetti. ' + info + '.</p>'
        + '<div class="rck-b"><button type="button" class="pri" id="rck-tutto">Accetta tutto</button><button type="button" id="rck-no">Solo necessari</button><button type="button" class="lnk" id="rck-pref">Preferenze</button></div>';
    document.body.appendChild(box);
    var q = function(id){ return document.getElementById(id); };
    if(q('rck-tutto')) q('rck-tutto').onclick = function(){ salva(true); };
    if(q('rck-no')) q('rck-no').onclick = function(){ salva(false); };
    if(q('rck-pref')) q('rck-pref').onclick = function(){ mostra(true); };
    if(q('rck-salva')) q('rck-salva').onclick = function(){ salva(q('rck-est').checked); };
  }
  window.rCookiePreferenze = function(){ mostra(true); };
  /* Nelle app (journal app.riskly.trade e siti installati sul telefono) niente banner né link: solo nei siti nel browser. */
  function inApp(){
    try { if(location.hostname === 'app.riskly.trade') return true;
      if(window.navigator.standalone) return true;
      if(window.matchMedia && (matchMedia('(display-mode: standalone)').matches || matchMedia('(display-mode: fullscreen)').matches)) return true;
    } catch(e) {}
    return false;
  }
  function avvia(){
    if(inApp()) return;
    /* un link "Preferenze cookie" in fondo alla pagina, se il sito non ne ha già uno */
    if(!document.querySelector('[data-cookie-pref]')){
      var a = document.createElement('button'); a.type = 'button'; a.setAttribute('data-cookie-pref', '1'); a.textContent = 'Preferenze cookie';
      a.style.cssText = 'display:block;margin:18px auto 90px;background:none;border:0;color:inherit;opacity:.65;font:inherit;font-size:13px;text-decoration:underline;cursor:pointer';
      a.onclick = function(){ mostra(true); };
      document.body.appendChild(a);
    }
    if(!leggi()) mostra(false);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvia); else avvia();
})();
