# Genera la modalità scura di strumenti.riskly.trade.
# Legge gli stili di index.html e, per ogni regola che usa un colore chiaro (fondi) o scuro (testi),
# scrive la stessa regola sotto html[data-tema="scuro"] con il colore scambiato.
# Il risultato va nel blocco <style id="tema-scuro"> (rigenerato ogni volta).
# Si rilancia dopo aver cambiato gli stili (serve: pip install tinycss2):
#   python3 nuovo/strumenti/tema_scuro.py              -> strumenti.riskly.trade
#   python3 nuovo/strumenti/tema_scuro.py index.html   -> il journal (app.riskly.trade, index.html nella radice)
import os, re, sys, tinycss2
QUI = os.path.dirname(os.path.abspath(__file__))
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(QUI, 'index.html')
COLORI = {  # chiaro -> scuro
  '#F3F4F1': '#0E1110', '#ECEEEA': '#171B19', '#FBFBF9': '#161A18', '#FFFFFF': '#1C211F', '#FFF': '#1C211F',
  '#E1E4E6': '#262C29', '#D7DADC': '#2E3532', '#CDD1D4': '#2E3532', '#C9CDD1': '#36403B',
  '#15181B': '#ECEEEA', '#0E1012': '#F3F4F1', '#2B3036': '#D5DBD7', '#3A4047': '#C3CAC5',
  '#4B525A': '#B9C0BB', '#5E656D': '#A3ABA6', '#59637A': '#9AA39E',
  '#B97C00': '#F2B83A', '#9A6700': '#F2B83A', '#8A5D00': '#F2B83A',
  '#1E7F45': '#3FCB7E', '#C2361F': '#FF6B5A',
  'RGBA(21,24,27,.015)': 'rgba(255,255,255,.03)', 'RGBA(21,24,27,.06)': 'rgba(255,255,255,.07)',
}
RX = re.compile('|'.join(sorted((re.escape(k) for k in COLORI), key=len, reverse=True)) + r'(?![0-9A-Fa-f])', re.I)
def scambia(v): return RX.sub(lambda m: COLORI[m.group(0).upper().replace(' ', '')], v)

def prefissa(sel):
  out = []
  for s in sel.split(','):
    s = s.strip()
    if not s: continue
    if s in (':root', 'html'): out.append('html[data-tema="scuro"]')
    elif s.startswith('html'): out.append('html[data-tema="scuro"]' + s[4:])
    elif s.startswith(':root'): out.append('html[data-tema="scuro"]' + s[5:])
    else: out.append('html[data-tema="scuro"] ' + s)
  return ','.join(out)

def regole(nodi):
  out = []
  for n in nodi:
    if n.type == 'qualified-rule':
      sel = tinycss2.serialize(n.prelude).strip()
      dich = tinycss2.parse_declaration_list(n.content, skip_comments=True, skip_whitespace=True)
      nuove = []
      for d in dich:
        if d.type != 'declaration': continue
        v = tinycss2.serialize(d.value).strip()
        if RX.search(v): nuove.append(f'{d.name}:{scambia(v)}!important' if not d.name.startswith('--') else f'{d.name}:{scambia(v)}')
      if nuove: out.append(prefissa(sel) + '{' + ';'.join(nuove) + '}')
    elif n.type == 'at-rule' and n.lower_at_keyword == 'media' and n.content:
      dentro = regole(tinycss2.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True))
      if dentro: out.append('@media ' + tinycss2.serialize(n.prelude).strip() + '{' + ''.join(dentro) + '}')
  return out

s = open(P, encoding='utf-8').read()
s = re.sub(r'\n?<style id="tema-scuro">.*?</style>', '', s, flags=re.S)
css = ''.join(re.findall(r'<style>(.*?)</style>', s, flags=re.S))
out = regole(tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True))
extra = '''
html[data-tema="scuro"]{color-scheme:dark}
html[data-tema="scuro"] body{background:#0E1110!important;color:#ECEEEA}
html[data-tema="scuro"] input,html[data-tema="scuro"] select,html[data-tema="scuro"] textarea{background:#171B19!important;color:#ECEEEA!important;border-color:#36403B!important}
html[data-tema="scuro"] .s-logo rect{fill:#FBFBF9}
html[data-tema="scuro"] .cal-info{background:rgba(242,184,58,.12)!important;color:#ECEEEA!important}
html[data-tema="scuro"] .cal-giorno{background:#171B19!important;color:#ECEEEA!important}
html[data-tema="scuro"] .str-nav{background:rgba(22,26,24,.92)!important;border-color:#36403B!important;box-shadow:0 10px 30px -14px rgba(0,0,0,.8)!important}
html[data-tema="scuro"] .str-nav button{color:#C3CAC5!important}
html[data-tema="scuro"] .str-nav button.on{background:#F2B83A!important;color:#1C1700!important}
html[data-tema="scuro"] .s-testa .s-tema{border-color:#ECEEEA!important;color:#ECEEEA!important;background:rgba(255,255,255,.04)!important}
'''
blocco = '<style id="tema-scuro">\n/* generato da tema_scuro.py: non modificare a mano */\n' + '\n'.join(out) + extra + '</style>'
s = s.replace('</head>', blocco + '\n</head>', 1)
open(P, 'w', encoding='utf-8').write(s)
print(len(out), 'regole scure')
