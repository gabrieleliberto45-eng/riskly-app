import sys, re
src, out = sys.argv[1], sys.argv[2]
L = open(src).read().split('\n')
s = '\n'.join(L)
def righe(a, b): return '\n'.join(L[a-1:b])
def trova(t, da=0):
    for i in range(da, len(L)):
        if t in L[i]: return i + 1
    raise ValueError(t)
css = s[s.index('<style>') + 7: s.index('</style>')]
# pagina strumenti
a = s.index('<div class="page" id="calc">')
def blocco(i):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        d += 1 if m.group() == '<div' else -1
        if d == 0: return i + m.end()
pag = s[a:blocco(a)].replace('<div class="page" id="calc">', '<div class="page on" id="calc">')
pag = pag.replace('''onclick="go('bot')"''', '''onclick="location.href='https://riskly.trade/?da=strumenti'"''')
# script: esc + aiuto + calcolatori + strumenti
e1 = trova('function esc(v){'); js = righe(e1, e1 + 2)
a1 = trova('function aiuto(t){'); a2 = trova('const v=id=>document.getElementById(id).value;')
js += '\n' + righe(a1, a2 + 1)
c1 = trova('calcPos(); calcRuin(); calcProp(); calcBE(); calcComp();')
js += '\ncalcPos(); calcRuin(); calcProp(); calcBE(); calcComp();\n'
f2 = trova('</script>', c1)
js += righe(c1 + 1, f2 - 1)
js = js.replace("if(nome === 'calendario') calDisegna();", "if(nome === 'calendario') calDisegna();\n  history.replaceState(null, '', '#' + nome);")
js += '''
/* sito separato: la pagina è sempre aperta; si può aprire una scheda con #calendario, #montecarlo... */
(function(){ const h = location.hash.slice(1); if(h && document.getElementById('st-' + h)) strTab(h);
  else if(document.getElementById('st-calendario').classList.contains('on')) calDisegna(); })();
'''
html = f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Strumenti gratuiti per il trading · Riskly</title>
<meta name="description" content="Calendario economico in tempo reale e calcolatori gratuiti per il trading: dimensione della posizione, rischio di rovina (Monte Carlo), tracker prop firm, recupero dal drawdown, crescita composta.">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#0B0D0C">
<meta property="og:title" content="Strumenti gratuiti per il trading · Riskly">
<meta property="og:description" content="Calendario economico in tempo reale e 5 calcolatori gratuiti, senza registrazione.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{css}
  /* ═══ sito strumenti: testata e piede propri ═══ */
  .s-testa{{position:sticky;top:0;z-index:30;background:rgba(11,13,12,.86);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}}
  .s-testa .wrap{{display:flex;align-items:center;justify-content:space-between;gap:12px;height:64px}}
  .s-logo{{display:flex;align-items:center;gap:9px;color:var(--text);text-decoration:none;font-weight:600;font-size:1.08rem}}
  .s-logo svg{{width:26px;height:26px}}
  .s-logo small{{color:var(--dim);font-weight:500;font-size:.85rem;margin-left:2px}}
  .s-link{{display:flex;align-items:center;gap:6px;position:static;background:none;border:0;box-shadow:none;padding:0;height:auto;width:auto}}
  .s-link a{{color:var(--dim);text-decoration:none;font-size:.9rem;padding:8px 12px;border-radius:100px}}
  .s-link a:hover{{color:var(--text)}}
  .s-link a.pri{{background:var(--grad);color:#0B0D0C;font-weight:600}}
  #calc .str-nav{{top:76px}}
  .s-piede{{border-top:1px solid var(--line);padding:26px 16px 34px;text-align:center;color:var(--dim2);font-size:.8rem;line-height:1.7;position:relative;z-index:1}}
  .s-piede a{{color:var(--dim)}}
  @media(max-width:620px){{.s-link a:not(.pri){{display:none}}.s-logo small{{display:none}}#calc .str-nav{{top:72px}}}}
</style>
</head>
<body>
<header class="s-testa"><div class="wrap">
  <a class="s-logo" href="https://riskly.trade/?da=strumenti"><svg viewBox="0 0 44 44" aria-hidden="true"><rect width="44" height="44" rx="10" fill="#151916"/><path d="M10 30 L17 20 L23 25 L34 12" stroke="#B6D84F" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/><path d="M10 34.5 H34" stroke="#8B98A9" stroke-width="3.6" stroke-linecap="round"/></svg>Riskly<small>· Strumenti</small></a>
  <nav class="s-link" aria-label="Siti Riskly"><a href="https://riskly.trade/?da=strumenti">Bot e videocorso</a><a href="https://app.riskly.trade">Journal</a><a class="pri" href="https://riskly.trade/?da=strumenti">Scopri Riskly</a></nav>
</div></header>
<main>
{pag}
</main>
<footer class="s-piede">Strumenti gratuiti, senza registrazione. Contenuto informativo ed educativo, non è consulenza finanziaria. Il trading con leva comporta un alto rischio: puoi perdere tutto il capitale.<br>
Riskly · Gabriele Liberto · P. IVA 04948840162 · <a href="https://riskly.trade/privacy">Privacy</a> · <a href="https://riskly.trade/?da=strumenti">riskly.trade</a></footer>
<script>
{js}
</script>
</body>
</html>
'''
open(out, 'w').write(html); print(len(html))
