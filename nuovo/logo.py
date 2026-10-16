# Logo Riskly uniforme: linea a zigzag oro (#B97C00) e base grigia (#5E656D), riquadro chiaro (#FBFBF9) dove c'è.
# uso: python3 nuovo/logo.py file.html ...   (riscrive i colori di ogni logo trovato, anche nei data URI)
import re, sys
ORO, GRIGIO, FONDO = 'B97C00', '5E656D', 'FBFBF9'
ZIG = r"M\s?(?:9|10) (?:31|30) L17 (?:19\.5|20) L(?:23\.5|23) 25 L(?:35|34) (?:11|12)"
BASE = r"M\s?(?:9|10) (?:36|34\.5) H\s?(?:35|34)"
def colora(svg):
    def path(m, col):
        p = m.group(0)
        return re.sub(r"stroke=(['\"])(?:#|%23)?[^'\"]*\1", lambda s: f"stroke={s.group(1)}{'%23' if '%23' in svg else '#'}{col}{s.group(1)}", p)
    svg = re.sub(r"<path[^>]*d=['\"]" + ZIG + r"['\"][^>]*>", lambda m: path(m, ORO), svg)
    svg = re.sub(r"<path[^>]*d=['\"]" + BASE + r"['\"][^>]*>", lambda m: path(m, GRIGIO), svg)
    svg = re.sub(r"(<rect[^>]*fill=(['\"]))(?:#|%23)[0-9A-Fa-f]{3,6}(\2)", lambda m: m.group(1) + ('%23' if '%23' in svg else '#') + FONDO + m.group(3), svg)
    if '<rect' not in svg:  # sempre la stessa forma dell'icona: riquadro chiaro arrotondato
        q = "'" if "viewBox='" in svg else '"'
        svg = re.sub(r"(<svg[^>]*>(?:<defs>.*?</defs>)?)", lambda m: m.group(1) + f"<rect width={q}44{q} height={q}44{q} rx={q}10{q} fill={q}{'%23' if '%23' in svg else '#'}{FONDO}{q}/>", svg, count=1, flags=re.S)
    return svg
for f in sys.argv[1:]:
    s = open(f).read()
    n = re.sub(r"<svg[^>]*>(?:(?!</svg>).){0,1500}?(?:" + ZIG + r").{0,1500}?</svg>", lambda m: colora(m.group(0)), s, flags=re.S)
    if n != s: open(f, 'w').write(n); print('aggiornato', f)
