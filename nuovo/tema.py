# Converte una pagina del vecchio tema scuro/lime nel tema chiaro "manuale" (carta, inchiostro, ambra).
# uso: python3 tema.py <file.html> [<file.html> ...]   (modifica i file sul posto, idempotente grazie al marcatore)
import re, sys
MARK = '/* TEMA CHIARO RISKLY */'
HEX = {
  '#0B0D0C':'#F3F4F1', '#101311':'#ECEEEA', '#121614':'#FBFBF9', '#151916':'#FBFBF9', '#1B201C':'#FFFFFF',
  '#252B26':'#CDD1D4', '#0B0F19':'#F3F4F1', '#08110c':'#FBFBF9', '#04121C':'#FBFBF9', '#0A0E14':'#F3F4F1',
  '#E6EDF3':'#15181B', '#8B98A9':'#5E656D', '#5D6B7D':'#5E656D', '#7C887E':'#5E656D', '#6B788A':'#5E656D',
  '#B6D84F':'#B97C00', '#C6E36A':'#E9A10F', '#CBE46E':'#15181B', '#A9D14A':'#15181B', '#7DBE4A':'#15181B',
  '#22C55E':'#1E7F45', '#16A34A':'#166B3A', '#EF4444':'#C2361F', '#F59E0B':'#B97C00', '#0EA5E9':'#1F5FD6',
}
def rgba(m):
    r,g,b,a = m.group(1),m.group(2),m.group(3),m.group(4)
    a = a or '1'
    key=(r.strip(),g.strip(),b.strip())
    if key==('255','255','255'): return f'rgba(21,24,27,{a})'
    if key==('0','0','0'): return f'rgba(21,24,27,{float(a)*.35:.3f})'
    if key==('182','216','79'): return f'rgba(233,161,15,{a})'
    if key==('34','197,94'.split(',')[0],'197') : pass
    if key==('34','197','94'): return f'rgba(30,127,69,{a})'
    if key==('239','68','68'): return f'rgba(194,54,31,{a})'
    if key in (('4','8','12'),('4','6','12'),('9','13','22')): return f'rgba(21,24,27,{min(float(a),.55)})'
    if key in (('16','19','17'),('9','11','10'),('11','13','12'),('20','23','21'),('45','55','80')): return f'rgba(243,244,241,{a})'
    return m.group(0)
def converti(t):
    if MARK in t: return t
    for k,v in HEX.items(): t = re.sub(re.escape(k)+r'(?![0-9A-Fa-f])', v, t, flags=re.I)
    t = re.sub(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)', rgba, t)
    return t
if __name__=='__main__':
    for f in sys.argv[1:]:
        t=open(f).read(); n=converti(t); open(f,'w').write(n); print('convertito',f)
