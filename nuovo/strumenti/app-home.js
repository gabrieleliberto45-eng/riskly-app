/* Riskly · "Mettila sul telefono come un'app" (15 novembre 2026, Gabriele: "nelle pagine di journal, strumenti e news
   devi mettere la spiegazione di come farla diventare un'app da telefono nella home").
   Riquadro compatto nella home: una riga sempre in vista, i passi si aprono con "Come fare".
   Riconosce iPhone (Safari o altri browser), Android (con il pulsante Installa quando il browser lo permette) e computer.
   Non compare se il sito è già aperto come app. "Nascondi" lo toglie per 60 giorni.
   Uso: <div data-rapp data-nome="Riskly News"></div> nella home + <script src="/app-home.js" defer></script>.
   Le pagine che disegnano la home da script chiamano window.rAppMonta() dopo averla disegnata. */
(function(){
  var UA = navigator.userAgent || '';
  var IOS = /iPhone|iPad|iPod/.test(UA) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var ANDROID = /Android/.test(UA);
  var DENTRO_APP = /Instagram|FBAN|FBAV|TikTok|musical_ly|Bytedance|Line\//i.test(UA);
  var IOS_ALTRO = /CriOS|FxiOS|EdgiOS/.test(UA);
  var evento = null;
  function giaApp(){ try { return matchMedia('(display-mode: standalone)').matches || navigator.standalone === true; } catch(e) { return false; } }
  function nascosto(){ try { var t = Number(localStorage.getItem('riskly-app-nascosto') || 0); return t && Date.now() - t < 60 * 864e5; } catch(e) { return false; } }
  window.addEventListener('beforeinstallprompt', function(e){ e.preventDefault(); evento = e; monta(); });
  window.addEventListener('appinstalled', function(){ document.querySelectorAll('[data-rapp]').forEach(function(el){ el.innerHTML = ''; el.hidden = true; }); });

  var CSS = '.rapp{display:block;border:1px solid rgba(127,127,127,.28);border-radius:14px;padding:12px 14px;margin:12px 0;font:inherit;font-size:14px;line-height:1.45;background:rgba(127,127,127,.06)}'
    + '.rapp-r{display:flex;align-items:center;gap:8px}.rapp-r img{width:34px;height:34px;border-radius:8px;flex:0 0 34px}'
    + '.rapp-r b{flex:1 1 auto;min-width:0;font-size:14.5px}.rapp button{font:inherit;font-size:13.5px;font-weight:600;cursor:pointer;border-radius:9px;padding:8px 12px;border:1px solid currentColor;background:none;color:inherit}'
    + '.rapp button.pri{background:#F2B33D;border-color:#F2B33D;color:#111}.rapp button.x{border:0;padding:4px 6px;font-size:20px;line-height:1;opacity:.55}'
    + '.rapp ol{margin:10px 0 2px;padding-left:20px}.rapp li{margin:4px 0}.rapp small{display:block;opacity:.7;margin-top:6px;font-size:12.5px}'
    + '.rapp-alt{margin-top:8px;font-size:12.5px;opacity:.8}.rapp-alt button{border:0;padding:0;text-decoration:underline;font-weight:500}';

  function passi(nome, quale, auto){
    var q = quale || (IOS ? 'iphone' : ANDROID ? 'android' : 'pc');
    if(q === 'iphone'){
      if(DENTRO_APP) return '<ol><li>Sei dentro un\'altra app (Instagram, TikTok…): tocca i tre puntini e scegli <b>Apri nel browser</b> o <b>Apri in Safari</b>.</li><li>In Safari tocca <b>Condividi</b> (il quadrato con la freccia in su).</li><li>Scorri e tocca <b>Aggiungi alla schermata Home</b>, poi <b>Aggiungi</b>.</li></ol>';
      return '<ol><li>' + (IOS_ALTRO && auto ? 'Apri questa pagina in <b>Safari</b> (con altri browser su iPhone il comando può mancare).</li><li>' : '') + 'Tocca <b>Condividi</b> (il quadrato con la freccia in su), in basso o in alto a destra.</li><li>Scorri e tocca <b>Aggiungi alla schermata Home</b>.</li><li>Tocca <b>Aggiungi</b>: ' + nome + ' compare tra le app e si apre a schermo intero.</li></ol>';
    }
    if(q === 'android') return '<ol><li>In Chrome tocca i tre puntini <b>⋮</b> in alto a destra.</li><li>Scegli <b>Installa app</b> (o <b>Aggiungi a schermata Home</b>).</li><li>Conferma: ' + nome + ' compare tra le app del telefono.</li></ol>';
    return '<ol><li>In Chrome o Edge clicca l\'icona di installazione nella barra dell\'indirizzo (lo schermo con la freccia), oppure il menu <b>⋮</b> e poi <b>Installa</b>.</li><li>Sul telefono: apri questa pagina e segui i passi per iPhone o Android.</li></ol>';
  }

  function disegna(el){
    if(giaApp() || nascosto()){ el.hidden = true; el.innerHTML = ''; return; }
    var nome = el.getAttribute('data-nome') || 'Riskly';
    el.hidden = false;
    el.innerHTML = '<div class="rapp"><div class="rapp-r"><img src="/apple-touch-icon.png" alt=""><b>Mettila sul telefono come un\'app</b>'
      + (evento ? '<button type="button" class="pri" data-a="installa">Installa</button>' : '')
      + '<button type="button" data-a="apri">Come fare</button><button type="button" class="x" data-a="nascondi" aria-label="Nascondi" title="Nascondi">×</button></div>'
      + '<div data-passi hidden></div></div>';
    el.querySelector('[data-a="apri"]').onclick = function(){ var p = el.querySelector('[data-passi]'); if(p.hidden){ mostra(el, nome); this.textContent = 'Chiudi'; } else { p.hidden = true; this.textContent = 'Come fare'; } };
    el.querySelector('[data-a="nascondi"]').onclick = function(){ try { localStorage.setItem('riskly-app-nascosto', String(Date.now())); } catch(e) {} el.hidden = true; el.innerHTML = ''; };
    var b = el.querySelector('[data-a="installa"]');
    if(b) b.onclick = function(){ try { evento.prompt(); evento.userChoice.then(function(){ evento = null; monta(); }); } catch(e) {} };
  }
  function mostra(el, nome, quale){
    var p = el.querySelector('[data-passi]'), q = quale || (IOS ? 'iphone' : ANDROID ? 'android' : 'pc');
    var altri = ['iphone', 'android', 'pc'].filter(function(x){ return x !== q; });
    var et = { iphone: 'iPhone', android: 'Android', pc: 'computer' };
    p.innerHTML = passi(nome, q, !quale) + '<small>Si apre a schermo intero, senza barra del browser, e ' + (nome === 'Riskly News' ? 'puoi ricevere un avviso a ogni articolo.' : 'ritrovi tutto con un tocco.') + '</small>'
      + '<div class="rapp-alt">Altro dispositivo: ' + altri.map(function(x){ return '<button type="button" data-q="' + x + '">' + et[x] + '</button>'; }).join(' · ') + '</div>';
    p.hidden = false;
    p.querySelectorAll('[data-q]').forEach(function(btn){ btn.onclick = function(){ mostra(el, nome, btn.getAttribute('data-q')); }; });
  }
  function monta(){
    if(!document.getElementById('rapp-stile')){ var s = document.createElement('style'); s.id = 'rapp-stile'; s.textContent = CSS; document.head.appendChild(s); }
    document.querySelectorAll('[data-rapp]').forEach(disegna);
  }
  window.rAppMonta = monta;
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', monta); else monta();
})();
