# Costruisce demo.html (versione dimostrativa del journal) per app.riskly.trade dal sito principale.
# uso: python3 nuovo/demo_journal.py <index del sito> <uscita>
import sys, re
src, out = sys.argv[1], sys.argv[2]
s = open(src).read()
css = s[s.index('<style>') + 7: s.index('</style>')]
a = s.index('<div class="page" id="app">')
def blocco(i):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        d += 1 if m.group() == '<div' else -1
        if d == 0: return i + m.end()
pag = s[a:blocco(a)].replace('<div class="page" id="app">', '<div class="page on" id="app">')
# via i piani (si comprano sul sito principale): al loro posto un invito
p1 = pag.index('<div class="plans"'); p2 = pag.index('</p>', pag.index('class="nota-fine"')) + 4
pag = pag[:p1] + '''<div class="jfine">
        <h3>Ti piace? Crea il tuo journal</h3>
        <p>Con un account ritrovi le operazioni da qualsiasi dispositivo e le sincronizzi da MetaTrader. 7 giorni di prova, poi da 29 € l'anno.</p>
        <div class="jfine-az"><a class="btn pri" href="/">Crea un account</a><a class="btn" href="https://riskly.trade/?vai=journal">Vedi i piani</a></div>
      </div>''' + pag[p2:]
j1 = s.index('/* ═══ JOURNAL ═══ */'); j2 = s.index('/* ---------- Rifiniture interfaccia ---------- */')
js = s[s.index('function esc(v){'):s.index('function botTab(nome){')] + s[j1:j2]
html = f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Journal di trading, versione dimostrativa · Riskly</title>
<meta name="description" content="Prova il journal di trading di Riskly con dati di esempio: metriche, curva del capitale, calendario e stato d'animo per ogni operazione.">
<link rel="icon" href="/favicon.ico">
<style>{css}
.jfine{{margin-top:28px;padding:26px;border:1px solid var(--line);border-radius:var(--r);background:var(--panel)}}
.jfine h3{{font-size:1.5rem;margin-bottom:8px}} .jfine p{{color:var(--dim);max-width:60ch}}
.jfine-az{{display:flex;gap:12px;flex-wrap:wrap;margin-top:16px}}
.dtesta{{position:sticky;top:0;z-index:20;border-bottom:1px solid var(--line);background:var(--bg)}}
.dtesta .wrap{{display:flex;align-items:center;justify-content:space-between;height:64px;gap:12px}}
.dtesta a.marchio{{display:flex;gap:10px;align-items:center;font-weight:700;font-size:19px;color:var(--text);text-decoration:none}}
.dtesta nav{{display:flex;gap:18px;align-items:center;position:static;border:0;background:none}}
.dtesta nav a{{font-size:15px;color:var(--dim);text-decoration:none}}
footer.dpiede{{border-top:1px solid var(--line);padding:28px 0;margin-top:40px;font-size:13px;color:var(--dim)}}
</style>
</head>
<body>
<header class="dtesta"><div class="wrap">
  <a class="marchio" href="/"><svg width="28" height="28" viewBox="0 0 44 44" fill="none" aria-hidden="true"><path d="M9 31 L17 19.5 L23.5 25 L35 11" stroke="#15181B" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 36 H35" stroke="#E9A10F" stroke-width="3.6" stroke-linecap="round"/></svg>Riskly journal</a>
  <nav><a href="https://riskly.trade">Bot e corso</a><a class="btn pri" href="/">Accedi</a></nav>
</div></header>
<main>
{pag}
</main>
<footer class="dpiede"><div class="wrap">Versione dimostrativa: i dati restano nel tuo browser e non vengono inviati. Contenuto educativo, non consulenza finanziaria. Riskly · Gabriele Liberto · P. IVA 04948840162 · <a href="https://riskly.trade/privacy.html">Privacy</a></div></footer>
<script>
{js}
avviaJournal();
</script>
</body>
</html>
'''
open(out, 'w').write(html); print('ok', len(html))
