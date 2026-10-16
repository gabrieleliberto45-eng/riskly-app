# Dispense PDF dei corsi Riskly, una per modulo, generate dai file delle lezioni.
#   python3 dispense.py rischio         → out/rischio/*.html (+ figure ritagliate dalle slide)
#   python3 dispense.py fondamentale
#   node pdf.js rischio                 → out/rischio/*.pdf
# Contenuto: testo di ogni slide + spiegazione (voce originale, senza il "parlato"), esercizi con soluzioni a fine modulo,
# checklist del modulo dai riepiloghi "In breve". Le figure (grafici, disegni, schermate) sono l'ultimo fotogramma della slide.
import sys, os, re, glob, html, importlib.util
from PIL import Image

QUI = os.path.dirname(os.path.abspath(__file__))
CORSI = {
    'rischio': dict(dir='corso-video', nome='Corso di gestione del rischio', breve='Gestione del rischio'),
    'fondamentale': dict(dir='corso-fondamentale', nome='Corso di analisi fondamentale', breve='Analisi fondamentale'),
}
AVVISO = ('Materiale educativo, non consulenza finanziaria. Il trading con leva su forex, CFD e futures comporta un rischio elevato: '
          'puoi perdere tutto il capitale. Numeri, esempi e simulazioni non prevedono risultati futuri.')


def carica(cdir):
    """Come build.carica() del corso, ma senza il parlato: la voce originale è più adatta a un testo da leggere."""
    sys.path.insert(0, f'{cdir}/lezioni')
    L = []
    for f in sorted(glob.glob(f'{cdir}/lezioni/m*.py'), key=lambda p: tuple(int(x) for x in re.findall(r'\d+', os.path.basename(p)))):
        sp = importlib.util.spec_from_file_location('l', f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
        L.append(m.LEZIONE)
    sp = importlib.util.spec_from_file_location('extra', f'{cdir}/lezioni/extra.py'); extra = importlib.util.module_from_spec(sp); sp.loader.exec_module(extra)
    for l in L:
        for anc, sl in getattr(extra, 'INS', {}).get(l['id'], []):
            idx = next((i for i, x in enumerate(l['slide']) if x.get('titolo') == anc), None)
            assert idx is not None, ('ancora non trovata', l['id'], anc)
            l['slide'].insert(idx + 1, sl)
        l['slide'] = [x for x in l['slide'] if x.get('titolo') not in getattr(extra, 'DEL', {}).get(l['id'], [])]
        if l['id'] in extra.EXTRA: l['slide'] = l['slide'][:-1] + [x for e in extra.EXTRA[l['id']] for x in (e if isinstance(e, list) else [e])] + l['slide'][-1:]
    sys.path.pop(0)
    return L


def md(t):
    t = html.escape(str(t))
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)


def puro(t):
    return re.sub(r'\*\*', '', str(t))


def coppia(p):
    if isinstance(p, (list, tuple)):
        a, b = (list(p) + [''])[:2]
        return f'<b>{md(a)}</b>' + (f'<span class="spieg"> — {md(b)}</span>' if b else '')
    return md(p)


def prosa(voce):
    v = [x for x in (voce or []) if x]
    return f'<p class="voce">{md(" ".join(v))}</p>' if v else ''


def figura(cdir, out, lez, si, didascalia):
    fot = sorted(glob.glob(f"{cdir}/out/png/{lez}_{si:02d}_*.png"), key=lambda p: int(p.rsplit('_', 1)[1][:-4]))
    if not fot: return ''
    os.makedirs(f'{out}/fig', exist_ok=True)
    nome = f'fig/{lez}_{si:02d}.jpg'
    if not os.path.exists(f'{out}/{nome}'):
        im = Image.open(fot[-1]).convert('RGB').crop((100, 240, 1820, 885))
        im.thumbnail((1400, 1400)); im.save(f'{out}/{nome}', quality=82)
    return f'<figure><img src="{nome}">' + (f'<figcaption>{md(didascalia)}</figcaption>' if didascalia else '') + '</figure>'


def tabella(intest, righe, cls=''):
    h = ''.join(f'<th>{md(x)}</th>' for x in intest) if intest else ''
    r = ''.join('<tr>' + ''.join(f'<td>{md(c)}</td>' for c in riga) + '</tr>' for riga in righe)
    return f'<table class="{cls}">' + (f'<thead><tr>{h}</tr></thead>' if h else '') + f'<tbody>{r}</tbody></table>'


def lezione(cdir, out, l, esercizi, checklist):
    s_ = l['slide']; h = []
    sotto = next((x.get('sotto') for x in s_ if x['tipo'] == 'titolo'), '')
    h.append(f'<section class="lezione"><div class="lk">LEZIONE {l["id"]}</div><h2>{md(puro(l["titolo"]))}</h2>')
    if sotto: h.append(f'<p class="lead">{md(sotto)}</p>')
    intro = next((x for x in s_ if x['tipo'] == 'titolo'), None)
    if intro and len(' '.join(intro.get('voce') or [])) > 90: h.append(prosa(intro.get('voce')))
    i = 0
    while i < len(s_):
        s = s_[i]; t = s['tipo']; tit = s.get('titolo', '')
        if t == 'titolo': i += 1; continue
        if t == 'esempio' and tit.startswith('Prova tu') and i + 1 < len(s_) and s_[i + 1].get('titolo') == 'Soluzione':
            esercizi.append(dict(lez=l['id'], dom=tit.replace('Prova tu · ', ''), dati=s['righe'], testo=' '.join(s.get('voce') or []),
                                 sol=s_[i + 1]['righe'], ris=s_[i + 1].get('risultato'), spieg=' '.join(s_[i + 1].get('voce') or [])))
            h.append(f'<div class="rimando">✎ Esercizio {len(esercizi)} · {md(tit.replace("Prova tu · ", ""))} — lo trovi in fondo al modulo, con la soluzione.</div>')
            i += 2; continue
        if t == 'punti' and tit == 'In breve':
            punti = [puro(p[0]) + (' — ' + puro(p[1]) if isinstance(p, (list, tuple)) and len(p) > 1 and p[1] else '') if isinstance(p, (list, tuple)) else puro(p) for p in s['punti']]
            checklist.append((l['id'], puro(l['titolo']), punti))
            h.append('<div class="breve"><div class="bk">IN BREVE</div><ul>' + ''.join(f'<li>{md(p)}</li>' for p in punti) + '</ul></div>')
            i += 1; continue
        blocco = f'<h3>{md(tit)}</h3>' if tit else ''
        if t == 'punti':
            blocco += '<ul class="punti">' + ''.join(f'<li>{coppia(p)}</li>' for p in s['punti']) + '</ul>' + prosa(s.get('voce'))
        elif t == 'formula':
            blocco += f'<div class="formula">{md(s["formula"])}</div>'
            if s.get('legenda'): blocco += '<dl class="legenda">' + ''.join(f'<dt>{md(a)}</dt><dd>{md(b)}</dd>' for a, b in s['legenda']) + '</dl>'
            blocco += prosa(s.get('voce'))
        elif t == 'tabella':
            blocco += tabella(s.get('intest'), s['righe']) + (f'<p class="nota">{md(s["nota"])}</p>' if s.get('nota') else '')
        elif t == 'esempio':
            blocco += tabella(None, s['righe'], 'es') + (f'<div class="ris">{md(s["risultato"])}</div>' if s.get('risultato') else '')
        elif t == 'confronto':
            col = lambda d: f'<div class="col"><div class="ct">{md(d["t"])}</div>' + tabella(None, d['punti'], 'es') + '</div>'
            blocco += f'<div class="confronto">{col(s["sx"])}{col(s["dx"])}</div>' + (f'<div class="ris">{md(s["risultato"])}</div>' if s.get('risultato') else '') + prosa(s.get('voce'))
        elif t in ('grafico', 'disegno', 'schermata'):
            blocco += figura(cdir, out, l['id'], i, s.get('didascalia'))
            if t == 'schermata' and s.get('punti'): blocco += '<ul class="punti">' + ''.join(f'<li>{coppia(p)}</li>' for p in s['punti']) + '</ul>'
            blocco += prosa(s.get('voce'))
        elif t == 'numero':
            blocco += f'<div class="numero">{md(s["numero"])}</div>' + (f'<p class="nota">{md(s["testo"])}</p>' if s.get('testo') else '') + prosa(s.get('voce'))
        elif t == 'citazione':
            blocco = f'<blockquote>{md(s["testo"])}</blockquote>'
        elif t == 'avviso':
            blocco += '<div class="avviso">' + ''.join(f'<p>{md(x)}</p>' for x in s['testo']) + '</div>'
        else:
            blocco += prosa(s.get('voce'))
        h.append(f'<div class="blocco">{blocco}</div>')
        i += 1
    h.append('</section>')
    return '\n'.join(h)


CSS = open(f'{QUI}/stile.css').read()


def modulo(corso, cdir, out, lezioni, mod):
    esercizi, checklist = [], []
    m0 = lezioni[0]
    corpo = [lezione(cdir, out, l, esercizi, checklist) for l in lezioni]
    num = re.sub(r'\D', '', m0['modulo']) or '0'
    indice = ''.join(f'<li><span>{l["id"]}</span>{md(puro(l["titolo"]))}</li>' for l in lezioni)
    copertina = f'''<section class="copertina">
<div class="marca">Riskly<span>.trade</span></div>
<div class="kicker">{html.escape(CORSI[corso]["nome"].upper())} · DISPENSA</div>
<div class="modn">{html.escape(m0["modulo"])}</div>
<h1>{md(m0["modTitolo"])}</h1>
<ol class="indice">{indice}</ol>
<div class="contiene"><b>In questa dispensa</b> il testo di ogni lezione, le formule, gli esempi svolti{", " + str(len(esercizi)) + " esercizi con soluzioni" if esercizi else ""} e la checklist del modulo.</div>
<p class="avv">{AVVISO}</p></section>'''
    fine = []
    if esercizi:
        fine.append('<section class="esercizi"><div class="lk">ALLENATI</div><h2>Esercizi</h2><p class="lead">Prova a risolverli senza guardare: le soluzioni sono nella pagina successiva.</p>')
        for n, e in enumerate(esercizi, 1):
            fine.append(f'<div class="esr"><div class="esn">{n}</div><div><div class="est">{md(e["dom"])} <span>· lezione {e["lez"]}</span></div>' + tabella(None, e['dati'], 'es') + '</div></div>')
        fine.append('</section><section class="soluzioni"><div class="lk">SOLUZIONI</div><h2>Soluzioni</h2>')
        for n, e in enumerate(esercizi, 1):
            fine.append(f'<div class="esr"><div class="esn">{n}</div><div><div class="est">{md(e["dom"])}</div>' + tabella(None, e['sol'], 'es')
                        + (f'<div class="ris">{md(e["ris"])}</div>' if e['ris'] else '') + f'<p class="voce">{md(e["spieg"])}</p></div></div>')
        fine.append('</section>')
    if checklist:
        fine.append('<section class="check"><div class="lk">PRIMA DI PASSARE AL MODULO SUCCESSIVO</div><h2>Checklist del modulo</h2><p class="lead">Spunta ogni punto solo se sapresti spiegarlo a voce a un altro trader.</p>')
        for lid, tit, punti in checklist:
            fine.append(f'<div class="cl"><div class="clt">{lid} · {md(tit)}</div><ul>' + ''.join(f'<li>{md(p)}</li>' for p in punti) + '</ul></div>')
        fine.append('</section>')
    if num != '0': fine.append(f'<div class="contiene" style="margin-top:8mm"><b>Quiz del modulo:</b> 5 domande su riskly.trade/quiz. Superati tutti i moduli, scarichi l\'attestato di completamento.</div>')
    fine.append(f'<p class="avv fine">{AVVISO} · riskly.trade</p>')
    doc = f'''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><title>Riskly · {html.escape(CORSI[corso]["breve"])} · {html.escape(m0["modulo"])}</title>
<style>{CSS}</style></head><body>{copertina}{"".join(corpo)}{"".join(fine)}</body></html>'''
    nome = f'modulo-{int(num):02d}'
    open(f'{out}/{nome}.html', 'w').write(doc)
    return nome, len(esercizi)


if __name__ == '__main__':
    corso = sys.argv[1]
    cdir = os.path.join(QUI, '..', CORSI[corso]['dir'])
    out = f'{QUI}/out/{corso}'; os.makedirs(out, exist_ok=True)
    L = carica(cdir)
    gruppi = {}
    for l in L: gruppi.setdefault(l['modulo'], []).append(l)
    for mod, ls in gruppi.items():
        nome, ne = modulo(corso, cdir, out, ls, mod)
        print(nome, mod, len(ls), 'lezioni,', ne, 'esercizi')
