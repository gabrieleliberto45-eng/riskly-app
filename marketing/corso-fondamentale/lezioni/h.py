# Scorciatoie per scrivere le lezioni
def T(kick, titolo, sotto, voce): return dict(tipo='titolo', kicker=kick, titolo=titolo, sotto=sotto, voce=[voce])
def P(titolo, punti, voce, k=None): return dict(tipo='punti', titolo=titolo, punti=punti, voce=voce, k=k)
def F(titolo, formula, legenda, voce, k=None): return dict(tipo='formula', titolo=titolo, formula=formula, legenda=legenda, voce=voce, k=k)
def TB(titolo, intest, righe, voce, nota=None, k=None): return dict(tipo='tabella', titolo=titolo, intest=intest, righe=righe, nota=nota, voce=voce, k=k)
def EX(titolo, righe, voce, risultato=None, k=None): return dict(tipo='esempio', titolo=titolo, righe=righe, risultato=risultato, voce=voce, k=k)
def CF(titolo, sx, dx, voce, risultato=None, k=None): return dict(tipo='confronto', titolo=titolo, sx=sx, dx=dx, risultato=risultato, voce=voce, k=k)
def G(titolo, img, voce, didascalia=None): return dict(tipo='grafico', titolo=titolo, img=img + '.png', didascalia=didascalia, voce=voce)
def N(titolo, numero, voce, testo=None): return dict(tipo='numero', titolo=titolo, numero=numero, testo=testo, voce=voce)
def Q(testo, voce): return dict(tipo='citazione', testo=testo, voce=[voce])
def L(id, mod, modt, titolo, slide): return dict(id=id, modulo=mod, modTitolo=modt, titolo=titolo, slide=slide)
def ES(domanda, dati, soluz, risultato, voce):
    """Esercizio: slide domanda (dati) + slide soluzione. voce = [testo domanda, testo soluzione]"""
    n1 = len(dati); n2 = len(soluz) + 1
    return [dict(tipo='esempio', titolo='Prova tu · ' + domanda, righe=[[a, b] for a, b in dati], voce=[voce[0]], risultato=None, k=[n1]),
            dict(tipo='esempio', titolo='Soluzione', righe=[[a, b] for a, b in soluz], risultato=risultato, voce=[voce[1]], k=[n2])]
def RIEP(punti, voce): return dict(tipo='punti', titolo='In breve', punti=punti, voce=voce)
def D(titolo, diag, passi, voce, didascalia=None, k=None): return dict(tipo='disegno', titolo=titolo, diag=diag, passi=passi, voce=voce, didascalia=didascalia, k=k)
def SC(titolo, img, punti, voce, k=None): return dict(tipo='schermata', titolo=titolo, img=img, punti=punti, voce=voce, k=k)
