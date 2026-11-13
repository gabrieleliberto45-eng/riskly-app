#!/usr/bin/env python3
"""Genera le pagine prodotto dei software: software/<slug>.html (14 novembre 2026).
Percorso d'acquisto: home -> esigenza -> confronto (max 3) -> pagina prodotto -> acquisto (Stripe, dal sito) -> dopo l'acquisto.
I dati vengono dalle schede del sito: se cambi un prezzo o una funzione, cambiala qui e rilancia lo script.
uso: python3 nuovo/riskly/pagine_software.py   (il .py non viene pubblicato: il deploy esclude *.py)"""
import html, pathlib

QUI = pathlib.Path(__file__).parent
OUT = QUI / 'software'
OUT.mkdir(exist_ok=True)
e = html.escape

# link dei prodotti su MQL5 (Gabriele, 14 novembre: "tutti e due"): appena c'è il link compare il pulsante principale "Acquista su MQL5" e Stripe resta come seconda scelta
MQL5 = {'riskguard': '', 'trademanager': '', 'scalein': '', 'riskly-pro': '', 'risklycopy': ''}

LIMITI = [
    "Funziona solo con MetaTrader aperto sul computer o su una VPS. Se il computer è spento o MetaTrader è chiuso, il software non agisce: per lasciarlo sempre attivo serve una VPS.",
    "Non funziona dall'app MetaTrader del telefono: lì l'Expert Advisor non gira. Dal telefono puoi vedere lo stato nel journal Riskly.",
    "Con mercato veloce, notizie o gap lo stop può essere eseguito a un prezzo peggiore di quello impostato. Nessun software elimina lo slippage.",
    "Non garantisce profitti e non protegge da tutte le perdite: applica le regole che imposti tu, nei limiti di quello che MetaTrader permette.",
    "Se fai una challenge, controlla sempre il regolamento della prop firm: ogni prop firm decide quali software ammettere.",
]

P = [
  dict(slug='riskguard', nome='RiskGuard', stripe='RiskGuard', prezzo=99, poi=149, conti='2 conti', agg='aggiornamenti inclusi',
       esigenza='Proteggere il conto', titolo='Ti ferma prima che una giornata storta diventi un conto bruciato.',
       sotto="Imposti a mente fredda quante perdite di fila, quante operazioni e quanta perdita al giorno ti concedi. Quando superi un limite, RiskGuard chiude le posizioni e chiude MetaTrader fino a mezzanotte.",
       video='riskguard', didascalia='Massimo 3 perdite di fila: alla terza mette in pausa e la quarta operazione non parte.',
       funzioni=['Pausa obbligatoria dopo una perdita', 'Blocco dopo N perdite consecutive (il numero lo scegli tu)', 'Limite di perdita e di operazioni giornaliere',
                 'Blocco che chiude MetaTrader e resta anche dopo un riavvio', 'Riduce il lotto se rischi più del limite', 'Stop loss obbligatorio',
                 'Chiusura automatica al target giornaliero', 'Operazioni nel journal e stato visibile dal telefono'],
       per='Chi sa di avere un problema con le perdite di fila, il revenge trading o i limiti giornalieri delle prop firm.',
       nonfa='Non gestisce stop, break-even o trailing delle posizioni aperte (lo fa TradeManager) e non entra a scaglioni (lo fa ScaleIn).',
       simili=['riskly-pro', 'trademanager']),
  dict(slug='trademanager', nome='TradeManager', stripe='TradeManager', prezzo=49, poi=79, conti='2 conti', agg='aggiornamenti inclusi',
       esigenza='Gestire le posizioni', titolo='Stop, break-even e trailing, senza toccare il grafico.',
       sotto="Gestisce le posizioni che apri tu: mette stop loss e take profit se mancano, sposta lo stop in pari dopo N pip e poi lo fa seguire il prezzo. Tutto in pip, nessuna formula da ricordare.",
       video='trademanager', didascalia='Stop e take profit automatici, pareggio a +20 pip, poi lo stop segue il prezzo.',
       funzioni=['Stop loss e take profit automatici in pip se mancano: mai una posizione senza stop', 'Break-even automatico dopo N pip, con margine',
                 'Trailing stop in pip: avvio, distanza e passo', 'Filtri per simbolo e magic number', 'Slippage massimo configurabile'],
       per='Chi apre le operazioni a mano e vuole che stop e uscite vengano gestiti sempre allo stesso modo.',
       nonfa='Non blocca il trading dopo le perdite (lo fa RiskGuard) e non apre posizioni aggiuntive (lo fa ScaleIn).',
       simili=['riskly-pro', 'scalein']),
  dict(slug='scalein', nome='ScaleIn', stripe='ScaleIn', prezzo=79, poi=129, conti='2 conti', agg='aggiornamenti inclusi',
       esigenza='Entrare a scaglioni', titolo='Apri una posizione, il software la divide in scaglioni con take profit diversi.',
       sotto="Quando apri un'operazione a mano, ScaleIn apre le altre parti sullo stesso strumento e nella stessa direzione, con take profit scaglionati in pip (per esempio 20, 40, 60). Se il rischio totale supera la soglia, non apre niente.",
       video='scalein', didascalia='Apri una posizione: il software apre le altre parti con take profit scaglionati.',
       funzioni=['Replica la posizione in N scaglioni', 'Take profit diverso per ogni scaglione, in pip', 'Volumi uguali o personalizzati per ogni scaglione',
                 'Ingressi a mercato o con ordini pendenti', "Stop loss automatico in pip se manca sull'originale", 'Blocco se il rischio totale è eccessivo',
                 "Pendenti cancellati da soli se l'originale si chiude"],
       per='Chi esce a parziali e vuole che gli scaglioni partano sempre con le stesse regole, senza calcoli.',
       nonfa="Non apre mai una posizione senza un'operazione tua e non blocca il trading dopo le perdite (lo fa RiskGuard).",
       simili=['riskly-pro', 'trademanager']),
  dict(slug='riskly-pro', nome='Riskly Pro', stripe='Riskly Pro', prezzo=199, poi=299, conti='3 conti', agg='aggiornamenti a vita',
       esigenza='Tutto in uno', titolo='RiskGuard, TradeManager e ScaleIn in un solo software.',
       sotto="I tre moduli lavorano con lo stesso stato: il rischio è calcolato sull'insieme delle posizioni, non su ciascuna separatamente. I pulsanti BUY e SELL hanno già il lotto calcolato.",
       video='risklypro', didascalia='Lotto calcolato sul rischio, niente aperture vicino alle notizie, entrata in 3 parti con pareggio e trailing stop.',
       funzioni=['Tutto di RiskGuard', 'Tutto di TradeManager', 'Tutto di ScaleIn', "Rischio calcolato sull'insieme delle posizioni",
                 'Pulsanti BUY e SELL con il lotto già calcolato (l\'ordine parte solo al tuo clic)', 'Niente aperture con spread largo o vicino alle notizie',
                 'Pannello unico con barre di avanzamento', 'Operazioni nel journal e stato visibile dal telefono', '50% di sconto sul videocorso'],
       per='Chi vuole un solo software per rischio, gestione e uscite, invece di tre separati.',
       nonfa='Non copia le operazioni su altri conti: per quello serve RisklyCopy, che funziona insieme a Riskly Pro.',
       simili=['riskguard', 'trademanager', 'scalein']),
  dict(slug='risklycopy', nome='RisklyCopy', stripe='RisklyCopy', prezzo=69, poi=129, conti='1 conto principale + 2 copie', agg='aggiornamenti inclusi',
       esigenza='Copiare su altri conti', titolo='Apri sul conto principale, gli altri copiano con lo stesso rischio.',
       sotto="Il lotto si ricalcola sul saldo di ogni conto: stesso rischio, non lo stesso lotto. Funziona tra MetaTrader 4 e 5, sullo stesso computer o sulla stessa VPS.",
       video='risklycopy', didascalia='Copia le operazioni dal conto principale agli altri, con il lotto ricalcolato sul saldo di ogni conto.',
       funzioni=['Copia apertura, chiusura, chiusure parziali, stop e take profit', 'Tra MetaTrader 4 e 5, sullo stesso computer o VPS',
                 'Lotto in proporzione al saldo, al rischio %, con moltiplicatore o fisso', 'Conti piccoli: copia al lotto minimo e raggruppa le operazioni',
                 'Se il conto principale si spegne, non chiude niente per sbaglio', 'Si usa insieme a Riskly Pro, ognuno sul suo grafico'],
       per='Chi gestisce più conti propri (per esempio un conto personale e una challenge) e vuole lo stesso rischio su tutti.',
       nonfa='Molte prop firm vietano o limitano la copia tra conti: controlla il regolamento prima di usarlo su un conto prop.',
       simili=['riskly-pro', 'riskguard']),
]
PER = {p['slug']: p for p in P}
CONFRONTO = {  # righe del confronto: (funzione, chi ce l'ha)
  'Blocco dopo le perdite e limiti giornalieri': {'riskguard', 'riskly-pro'},
  'Stop loss automatico se manca': {'trademanager', 'scalein', 'riskly-pro'},
  'Break-even e trailing stop': {'trademanager', 'riskly-pro'},
  'Ingressi a scaglioni con TP diversi': {'scalein', 'riskly-pro'},
  "Rischio calcolato sull'insieme delle posizioni": {'riskly-pro'},
  'Copia su altri conti': {'risklycopy'},
  'Operazioni nel journal in automatico': {'riskguard', 'riskly-pro'},
}

CSS = """
:root{--bg:#F6F6F3;--card:#fff;--ink:#0F1B2D;--ink2:#4B5565;--ink3:#788494;--line:#DCE1E8;--line2:#EBEEF3;--navy:#12263F;--su:#12805A;--att:#A86400}
*{box-sizing:border-box;margin:0;padding:0}html{background:var(--bg)}
body{background:var(--bg);color:var(--ink);font-family:'Instrument Sans',system-ui,-apple-system,'Segoe UI',sans-serif;font-size:16px;line-height:1.6;font-variant-numeric:tabular-nums}
a{color:inherit}.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header{position:sticky;top:0;z-index:5;background:rgba(246,246,243,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header .wrap{display:flex;align-items:center;justify-content:space-between;height:60px;gap:16px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:1.15rem;text-decoration:none}
header nav{display:flex;gap:18px;font-size:15px;overflow-x:auto;scrollbar-width:none}header nav a{text-decoration:none;color:var(--ink2);white-space:nowrap}header nav a.on{color:var(--ink);font-weight:600}
.briciole{font-size:13px;color:var(--ink3);padding:18px 0 0}.briciole a{color:var(--ink2)}
.hero{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:36px;align-items:start;padding:22px 0 30px}
.k{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--att)}
h1{font-family:'Instrument Serif',Georgia,serif;font-weight:400;font-size:clamp(2.1rem,4.4vw,3.2rem);line-height:1.06;margin:8px 0 14px}
.sotto{color:var(--ink2);font-size:1.05rem;margin-bottom:18px}
.compra{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin-bottom:12px}
.prezzo{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}.prezzo b{font-size:2rem;letter-spacing:-.02em}.prezzo s{color:var(--ink3)}
.prezzo small{color:var(--ink2);font-size:14px}
.compra ul{list-style:none;display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13.5px;color:var(--ink2);margin:8px 0 14px}
.compra li::before{content:'✓ ';color:var(--su);font-weight:700}
.btn{display:inline-flex;justify-content:center;align-items:center;gap:8px;border-radius:8px;padding:13px 20px;font-weight:600;font-size:15.5px;text-decoration:none;border:1px solid var(--navy);color:var(--navy);background:transparent;cursor:pointer}
.btn.pri{background:var(--navy);color:#fff;width:100%}
.nota{font-size:12.5px;color:var(--ink3);margin-top:8px}
.video{background:#0B0D0C;border-radius:14px;overflow:hidden;border:1px solid var(--line)}
.video video{display:block;width:100%;aspect-ratio:9/16;max-height:640px;object-fit:contain;background:#0B0D0C}
.video p{color:#C9D3E0;font-size:13.5px;padding:10px 14px;background:#12263F}
.video p em{display:block;font-style:normal;font-size:11.5px;color:#9CA8B8;margin-top:3px}
section{padding:24px 0}h2{font-size:1.3rem;font-weight:700;letter-spacing:-.01em;margin-bottom:12px}
.griglia2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.box{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px}
.box ul{list-style:none;display:grid;gap:7px}.box li{padding-left:22px;position:relative}.box li::before{content:'✓';position:absolute;left:0;color:var(--su);font-weight:700}
.box.lim li::before{content:'!';color:var(--att)}
.box p{color:var(--ink2)}
table{width:100%;border-collapse:collapse;font-size:14.5px;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
th,td{padding:10px 12px;border-bottom:1px solid var(--line2);text-align:center}th:first-child,td:first-child{text-align:left}
thead th{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink2);background:#F2F4F7}
thead th.qui{color:var(--navy);background:#E6ECF5}td.qui{background:#F4F7FB;font-weight:600}
td .si{color:var(--su);font-weight:700}td .no{color:var(--ink3)}
.tab-s{overflow-x:auto;border-radius:12px}
.passi{counter-reset:p;list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.passi li{counter-increment:p;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.passi li::before{content:counter(p);display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;background:var(--navy);color:#fff;font-weight:700;font-size:13px;margin-bottom:8px}
.passi b{display:block}.passi p{color:var(--ink2);font-size:14.5px}
.risorse{display:flex;flex-wrap:wrap;gap:10px}
.altri{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}
.altri a{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;text-decoration:none}
.altri a b{display:block}.altri a span{color:var(--ink2);font-size:14px}.altri a:hover{border-color:var(--navy)}
footer{border-top:1px solid var(--line);margin-top:24px;padding:22px 0 30px;color:var(--ink3);font-size:13px}
@media(max-width:820px){.hero{grid-template-columns:1fr}.griglia2,.passi{grid-template-columns:1fr}.video video{max-height:520px}}
"""

def bottoni(p):
    stripe = f'href="/?compra={e(p["stripe"]).replace(" ", "%20")}#software" data-compra="{e(p["nome"])}"'
    m = MQL5.get(p['slug'], '')
    if m:
        return (f'<a class="btn pri" href="{e(m)}" target="_blank" rel="noopener" data-mql5="{e(p["nome"])}">Acquista su MQL5</a>'
                f'<a class="btn" style="width:100%;margin-top:8px" {stripe}>Oppure paga con carta sul sito · {p["prezzo"]} €</a>'
                '<p class="nota">Su MQL5 la licenza e gli aggiornamenti li gestisce MetaTrader. Sul sito paghi con Stripe: ti serve un account Riskly gratuito e ricevi file, licenza e guida entro 24 ore lavorative.</p>')
    return (f'<a class="btn pri" {stripe}>Acquista {e(p["nome"])} · {p["prezzo"]} €</a>'
            '<p class="nota">Pagamento sicuro con Stripe. Ti serve un account Riskly gratuito: prima del pagamento accetti i termini. Entro 24 ore lavorative ricevi file, licenza e guida.</p>')

def pagina(p):
    s = p['slug']
    confr = [s] + [x for x in p['simili'] if x != s][:2]
    righe = ''.join(f"<tr><td>{e(f)}</td>" + ''.join(f"<td class=\"{'qui' if c == s else ''}\">{'<span class=si>✓</span>' if c in chi else '<span class=no>—</span>'}</td>" for c in confr) + "</tr>"
                    for f, chi in CONFRONTO.items() if any(c in chi for c in confr))
    righe += "<tr><td>Prezzo di lancio</td>" + ''.join(f"<td class=\"{'qui' if c == s else ''}\">{PER[c]['prezzo']} €</td>" for c in confr) + "</tr>"
    righe += "<tr><td>Conti per licenza</td>" + ''.join(f"<td class=\"{'qui' if c == s else ''}\">{e(PER[c]['conti'])}</td>" for c in confr) + "</tr>"
    testa = "<tr><th>Funzione</th>" + ''.join(f"<th class=\"{'qui' if c == s else ''}\">{'<a href=\"/software/' + c + '\">' + e(PER[c]['nome']) + '</a>' if c != s else e(PER[c]['nome'])}</th>" for c in confr) + "</tr>"
    altri = ''.join(f'<a href="/software/{x["slug"]}"><b>{e(x["nome"])}</b><span>{e(x["esigenza"])} · {x["prezzo"]} €</span></a>' for x in P if x['slug'] != s)
    nav = ''.join(f'<a href="/software/{x["slug"]}"{" class=on" if x["slug"] == s else ""}>{e(x["nome"])}</a>' for x in P)
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['nome'])} per MetaTrader 4 e 5 · Riskly</title>
<meta name="description" content="{e(p['sotto'][:155])}">
<link rel="canonical" href="https://riskly.trade/software/{s}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link href="/fonts.css" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header><div class="wrap">
  <a class="brand" href="/"><svg width="26" height="26" viewBox="0 0 44 44" fill="none" aria-hidden="true"><path d="M9 31 L17 19.5 L23.5 25 L35 11" stroke="#B97C00" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 36 H35" stroke="#5E656D" stroke-width="3.4" stroke-linecap="round"/></svg>Riskly</a>
  <nav aria-label="Software">{nav}</nav>
</div></header>
<main class="wrap">
  <div class="briciole"><a href="/">Home</a> › <a href="/#software">Software</a> › {e(p['nome'])}</div>
  <div class="hero">
    <div>
      <div class="k">{e(p['esigenza'])} · MetaTrader 4 e 5</div>
      <h1>{e(p['titolo'])}</h1>
      <p class="sotto">{e(p['sotto'])}</p>
      <div class="compra">
        <div class="prezzo"><b>{p['prezzo']} €</b><s>{p['poi']} €</s><small>prezzo di lancio · paghi una volta</small></div>
        <ul><li>Licenza a vita</li><li>{e(p['conti'])}</li><li>{e(p['agg'])}</li><li>MT4 e MT5</li></ul>
        {bottoni(p)}
      </div>
      <p class="nota"><b>Per chi è:</b> {e(p['per'])}</p>
    </div>
    <figure class="video">
      <video src="/video/{p['video']}.mp4" poster="/video/{p['video']}.jpg" muted loop playsinline preload="none" controls aria-label="Video dimostrativo di {e(p['nome'])}"></video>
      <p>{e(p['didascalia'])}<em>Simulazione illustrativa, non una registrazione di operazioni reali e non rappresentativa di risultati ottenibili.</em></p>
    </figure>
  </div>

  <section class="griglia2">
    <div class="box"><h2>Cosa fa</h2><ul>{''.join(f'<li>{e(f)}</li>' for f in p['funzioni'])}</ul></div>
    <div class="box lim"><h2>Cosa non fa e i limiti</h2><p style="margin-bottom:10px">{e(p['nonfa'])}</p><ul>{''.join(f'<li>{e(x)}</li>' for x in LIMITI)}</ul></div>
  </section>

  <section>
    <h2>Compatibilità</h2>
    <div class="box"><ul>
      <li>MetaTrader 4 e MetaTrader 5, versione per computer (Windows) o VPS. La licenza vale per entrambe.</li>
      <li>Qualsiasi broker che offre MetaTrader 4 o 5, conti reali, demo e prop firm (se il regolamento lo consente).</li>
      <li>Licenza legata ai numeri di conto MetaTrader che ci comunichi: puoi cambiarli scrivendo all'assistenza.</li>
    </ul></div>
  </section>

  <section>
    <h2>Confronto con i software simili</h2>
    <div class="tab-s"><table><thead>{testa}</thead><tbody>{righe}</tbody></table></div>
  </section>

  <section>
    <h2>Dopo l'acquisto</h2>
    <ol class="passi">
      <li><b>Ricevi file e licenza</b><p>Entro 24 ore lavorative ti mandiamo il file per il tuo conto e la licenza.</p></li>
      <li><b>Lo installi con la guida</b><p>Cinque passi, con le immagini. Se serve ti seguiamo noi, anche su Telegram.</p></li>
      <li><b>Lo provi su demo</b><p>Prima di usarlo sul conto vero, provalo qualche giorno su un conto demo.</p></li>
    </ol>
    <div class="risorse" style="margin-top:14px">
      <a class="btn" href="/primi-passi.html">Guida di installazione</a>
      <a class="btn" href="/dichiarazione-prop-firm.pdf" target="_blank" rel="noopener">Dichiarazione per le prop firm (PDF)</a>
      <a class="btn" href="https://app.riskly.trade/?esempio=1">Il journal, con dati di esempio</a>
      <a class="btn" href="mailto:info@riskly.trade?subject={e(p['nome']).replace(' ', '%20')}">Scrivi all'assistenza</a>
    </div>
  </section>

  <section>
    <h2>Gli altri software</h2>
    <div class="altri">{altri}</div>
  </section>
</main>
<footer><div class="wrap">© Riskly · Software di gestione del rischio: non danno segnali e non aprono operazioni da soli. Il trading con leva comporta un alto rischio di perdita. <a href="/privacy.html">Privacy</a> · <a href="/#termini">Termini</a></div></footer>
__TRACCIA__
<script>try{{ tracciaVisita('software/{s}'); }}catch(e){{}}
document.querySelectorAll('[data-compra]').forEach(a => a.addEventListener('click', () => {{ try{{ traccia('clic-acquista-{s}'); }}catch(e){{}} }}));
document.querySelectorAll('[data-mql5]').forEach(a => a.addEventListener('click', () => {{ try{{ traccia('clic-mql5-{s}'); }}catch(e){{}} }}));</script>
<script src="/cookie.js" defer></script>
</body>
</html>
"""

g = (QUI / 'grazie.html').read_text()
traccia = g[g.index('<script>\n/* RISKLY TRACCIA'):g.index("<script>try{ tracciaVisita")]
for p in P:
    (OUT / f"{p['slug']}.html").write_text(pagina(p).replace('__TRACCIA__', traccia.rstrip()))
    print('ok', p['slug'])
