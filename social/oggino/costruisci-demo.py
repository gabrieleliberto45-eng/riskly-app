# Costruisce demo-bot.json: per ogni bot una scaletta coerente con il percorso del prezzo.
# Il prezzo qui è calcolato come in demo.html, così stop, take profit e break-even scattano davvero quando il prezzo li tocca.
import json, math
def mk(K, r):
    def p(t):
        if t <= K[0][0]: v = K[0][1]
        elif t >= K[-1][0]: v = K[-1][1]
        else:
            for (a, x), (b, y) in zip(K, K[1:]):
                if a <= t <= b: k = (t - a) / (b - a); s = k * k * (3 - 2 * k); v = x + (y - x) * s; break
        return v + (math.sin(t * 9.1) * .35 + math.sin(t * 4.3 + 1) * .4 + math.sin(t * 17.3 + 2) * .25) * r
    return p
def primo(p, da, cond, fino=60):
    t = da
    while t < fino:
        if cond(p(t)): return round(t, 2)
        t += .01
    raise ValueError('mai')
SPR, R = .29, .35
F = lambda x: f"{x:.2f}"
D = []

# ---------------- TradeManager ----------------
K = [(-20, 4189.6), (0, 4189.8), (2, 4190.0), (6, 4192.6), (8, 4193.4), (12.5, 4195.6), (14, 4195.8), (17, 4192.6), (19, 4192.4)]
p = mk(K, R); tap = 1.6; e = round(p(tap) + SPR, 2); sl0, tp = round(e - 3.0, 2), round(e + 6.0, 2)
tbe = primo(p, tap, lambda v: v >= e + 2.0); be = round(e + .1, 2)
moves = [[tbe, be, .4]]; sl = be; mx = 0; t = tbe; ttr = None
while True:
    t = round(t + .02, 2); v = p(t); mx = max(mx, v)
    if mx - e >= 3.0:
        nuovo = round(e + math.floor((mx - e - 2.0) / .5) * .5, 2)
        if nuovo > sl + 1e-9: moves.append([t, nuovo, .3]); sl = nuovo; ttr = ttr or t
    if t > tbe + .5 and v <= sl: tch = t; break
assert max(p(x / 100) for x in range(0, int(tch * 100))) < tp, 'TP colpito'
pip = round((sl - e) / .1)
D.append({"id": "b-trademanager", "bot": "TradeManager", "simbolo": "XAUUSD", "ora": "10:12", "scala": [4186.0, 4198.0], "prezzo": K, "rumore": R,
  "lotto": [[0, "0.40"]], "tocchi": [[tap]],
  "linee": [{"tipo": "entrata", "etichetta": "buy 0.40", "prezzo": e, "da": tap + .1, "a": tch + .6},
            {"tipo": "sl", "etichetta": "SL", "prezzo": sl0, "da": tap + .6, "a": tch + .6, "colpo": True, "sposta": moves},
            {"tipo": "tp", "etichetta": "TP", "prezzo": tp, "da": tap + .6, "a": tch + .6}],
  "notifiche": [[tap + .6, "Stop loss e take profit impostati in automatico: 30 e 60 pip"], [tbe, "+20 pip: stop spostato a pareggio"],
                [ttr, "Trailing stop attivo: lo stop segue il prezzo a 20 pip"], [tch, f"Posizione chiusa allo stop a {F(sl)} · +{pip} pip"]],
  "didascalie": [[.3, "1", "Apri una posizione. Anche senza stop loss."], [tbe - 1.1, "2", "A +20 pip lo stop va a pareggio."],
                 [ttr - .4, "3", "Poi lo stop segue il prezzo."], [tch + .1, "4", f"Chiusa in profitto (+{pip} pip). Senza toccare niente."]],
  "pannello": [[0, "attivo", 0, [["Stop auto", "30 pip"], ["Break-even", "a +20 pip"], ["Trailing", "20 pip"], ["Passo", "5 pip"]]],
               [tbe, "pareggio ✓", 0, [["Stop auto", "30 pip"], ["Break-even", "fatto", "#B6D84F"], ["Trailing", "20 pip"], ["Passo", "5 pip"]]],
               [ttr, "trailing", 0, [["Stop auto", "30 pip"], ["Break-even", "fatto", "#B6D84F"], ["Trailing", "attivo", "#B6D84F"], ["Passo", "5 pip"]]],
               [tch, "chiusa +" + str(pip) + " pip", 0, [["Stop auto", "30 pip"], ["Break-even", "fatto", "#B6D84F"], ["Trailing", "fatto", "#B6D84F"], ["Risultato", f"+{pip} pip", "#00C853"]]]],
  "punti": ["Stop e take profit automatici se mancano", "Break-even dopo i pip che scegli", "Trailing stop: avvio, distanza e passo"],
  "quando": "Per MT4 e MT5 · dal 23 ottobre", "fine": round(tch + 2.8, 2), "durata": round(tch + 8.6, 2)})

# ---------------- RiskGuard ----------------
K = [(-20, 4191.6), (0, 4192.0), (1.4, 4192.2), (3.8, 4189.0), (4.6, 4189.4), (5.0, 4189.5), (7.4, 4186.3), (8.2, 4186.8), (8.6, 4186.9), (11.0, 4183.6), (12.5, 4184.2), (15, 4186.8), (18, 4188.2)]
p = mk(K, R); taps = [1.2, 4.8, 8.4]; lin = []; hits = []; pan = [[0, "attivo", 0, [["Perdite di fila", "0 / 3"], ["Perdita oggi", "0,0% / 3,0%"], ["Trade oggi", "0 / 5"], ["Stop obbligatorio", "sì"]]]]
notif = []
for i, tp_ in enumerate(taps):
    e = round(p(tp_) + SPR, 2); sl = round(e - 2.5, 2); tpp = round(e + 5.0, 2)
    h = primo(p, tp_ + .3, lambda v: v <= sl); hits.append(h)
    lin += [{"tipo": "entrata", "etichetta": "buy 0.40", "prezzo": e, "da": tp_ + .1, "a": h + .6},
            {"tipo": "sl", "etichetta": "SL", "prezzo": sl, "da": tp_ + .2, "a": h + .6, "colpo": True},
            {"tipo": "tp", "etichetta": "TP", "prezzo": tpp, "da": tp_ + .2, "a": h + .6}]
    n = i + 1
    pan.append([h, "in pausa" if n == 3 else "attivo", 1 if n == 3 else 0, [["Perdite di fila", f"{n} / 3", "#ff6b61"], ["Perdita oggi", f"{n},0% / 3,0%", "#ff6b61"], ["Trade oggi", f"{n} / 5"], ["Stop obbligatorio", "sì"]]])
    notif.append([h, f"Stop loss · −1,0% · perdite di fila: {n} su 3"] if n < 3 else [h, "3 perdite di fila: pausa attiva fino alle 18:00"])
t4 = round(hits[2] + 2.4, 2)
notif.append([t4 + .05, "Operazione bloccata: la pausa è attiva"])
D.append({"id": "b-riskguard", "bot": "RiskGuard", "simbolo": "XAUUSD", "ora": "15:40", "scala": [4180.5, 4195.5], "prezzo": K, "rumore": R,
  "lotto": [[0, "0.40"]], "tocchi": [[x] for x in taps] + [[t4]], "linee": lin, "notifiche": notif, "blocco": [t4 + .05, t4 + 2.4],
  "didascalie": [[.2, "1", "La regola: massimo 3 perdite di fila."], [hits[0] + .2, "2", "Ogni stop viene contato."],
                 [hits[2] + .1, "3", "Alla terza: pausa. Niente quarta."], [t4 - .6, "4", "Anche se ci riprovi."]],
  "pannello": pan, "punti": ["Ti ferma dopo le perdite di fila che scegli", "Limite di perdita giornaliero con margine", "Stop loss obbligatorio e massimo di trade al giorno"],
  "quando": "Per MT4 e MT5 · dal 23 ottobre", "fine": round(t4 + 2.9, 2), "durata": round(t4 + 8.7, 2)})

# ---------------- ScaleIn ----------------
K = [(-20, 4189.6), (0, 4189.8), (2, 4190.1), (5.5, 4192.9), (7, 4192.5), (9.5, 4194.9), (11, 4194.5), (13.5, 4196.9), (15, 4196.6), (17, 4196.2)]
p = mk(K, R); tap = 1.5; e = round(p(tap) + SPR, 2); sl = round(e - 3.0, 2)
tps = [round(e + 2.0 * k, 2) for k in (1, 2, 3)]; th = []; da = tap
for x in tps: h = primo(p, da, lambda v: v >= x); th.append(h); da = h
assert min(p(x / 100) for x in range(int(tap * 100), int(th[2] * 100))) > sl
lin = [{"tipo": "entrata", "etichetta": "buy 0.10 ×3", "prezzo": e, "da": tap + .1, "a": th[2] + .6},
       {"tipo": "sl", "etichetta": "SL", "prezzo": sl, "da": tap + .6, "a": th[2] + .6}]
lin += [{"tipo": "tp", "etichetta": f"TP{k + 1}", "prezzo": x, "da": tap + .6, "a": th[k] + .6, "colpo": True} for k, x in enumerate(tps)]
pan = [[0, "pronto", 0, [["Take profit", "20 · 40 · 60 pip"], ["Volumi", "uguali"], ["Stop auto", "30 pip"], ["Posizioni", "—"]]],
       [tap + .6, "3 posizioni", 0, [["Take profit", "20 · 40 · 60 pip"], ["Volumi", "uguali"], ["Stop auto", "30 pip"], ["Posizioni", "3 aperte"]]]]
for k, h in enumerate(th):
    pan.append([h, "chiuse tutte" if k == 2 else f"{2 - k} aperte", 0, [["Take profit", "20 · 40 · 60 pip"], ["Volumi", "uguali"], ["Incassati", f"+{20 * (k + 1)} pip", "#00C853"], ["Posizioni", f"{2 - k} aperte"]]])
D.append({"id": "b-scalein", "bot": "ScaleIn", "simbolo": "XAUUSD", "ora": "09:31", "scala": [4185.5, 4198.5], "prezzo": K, "rumore": R,
  "lotto": [[0, "0.10"]], "tocchi": [[tap]], "linee": lin, "pannello": pan,
  "notifiche": [[tap + .6, "Aperte altre 2 posizioni · take profit a 20, 40 e 60 pip · stop 30 pip"]] + [[h, f"TP{k + 1} raggiunto · +{20 * (k + 1)} pip" + (" · tutte chiuse" if k == 2 else "")] for k, h in enumerate(th)],
  "didascalie": [[.3, "1", "Apri una posizione a mano."], [tap + .7, "2", "ScaleIn apre le altre, con take profit scaglionati."],
                 [th[0] + .1, "3", "Ogni parte esce al suo livello."], [th[2] + .1, "4", "Una entrata, tre uscite. Tutto automatico."]],
  "punti": ["Take profit scaglionati in pip", "Volumi uguali o personalizzati", "Stop automatico e controllo del rischio totale"],
  "quando": "Per MT4 e MT5 · dal 23 ottobre", "fine": round(th[2] + 2.8, 2), "durata": round(th[2] + 8.6, 2)})

# ---------------- Riskly Pro ----------------
# lotto dal rischio + filtro notizie, poi entra in 3 parti (scaglionamento): TP1 e pareggio, trailing, TP2, l'ultima parte esce col trailing
K = [(-20, 4189.8), (0, 4190.0), (3, 4190.3), (8.6, 4189.8), (8.9, 4187.6), (9.3, 4189.4), (10.0, 4189.0), (10.4, 4189.2),
     (12.6, 4191.7), (13.3, 4191.4), (15.6, 4193.8), (16.3, 4193.5), (18.2, 4194.7), (18.8, 4194.5), (20.2, 4192.2), (22, 4192.0)]
p = mk(K, R); tap1, tap2 = 4.7, 10.2; e = round(p(tap2) + SPR, 2); sl0 = round(e - 2.5, 2)
tps = [round(e + 2.0 * k, 2) for k in (1, 2, 3)]
t1 = primo(p, tap2, lambda v: v >= tps[0]); be = round(e + .1, 2)
moves = [[t1, be, .4]]; sl = be; mx = 0; t = t1; ttr = None; t2 = None
while True:
    t = round(t + .02, 2); v = p(t); mx = max(mx, v)
    if t2 is None and v >= tps[1]: t2 = t
    if mx - e >= 3.0:
        nuovo = round(e + math.floor((mx - e - 2.0) / .5) * .5, 2)
        if nuovo > sl + 1e-9: moves.append([t, nuovo, .3]); sl = nuovo; ttr = ttr or t
    if t > t1 + .5 and v <= sl: tch = t; break
assert t2 and ttr < t2 < tch, (ttr, t2, tch)
assert max(p(x / 100) for x in range(int(tap2 * 100), int(tch * 100))) < tps[2], 'TP3 colpito'
assert min(p(x / 100) for x in range(int(tap2 * 100), int(t1 * 100))) > sl0
pip = round((sl - e) / .1); tot = 20 + 40 + pip
R4 = lambda a, b, c, d: [a, b, c, d]
D.append({"id": "b-risklypro", "bot": "Riskly Pro", "simbolo": "XAUUSD", "ora": "14:28", "scala": [4185.0, 4197.0], "prezzo": K, "rumore": R,
  "lotto": [[0, "—"], [1.6, "0.40"]], "tocchi": [[tap1], [tap2]], "blocco": [tap1 + .05, tap1 + 2.2],
  "banner": {"testo": "CPI USA · 14:30", "secondi": 120, "da": 3.0, "a": 8.6},
  "linee": [{"tipo": "entrata", "etichetta": "buy 0.40 · 3 parti", "prezzo": e, "da": tap2 + .1, "a": tch + .6},
            {"tipo": "sl", "etichetta": "SL", "prezzo": sl0, "da": tap2 + .2, "a": tch + .6, "colpo": True, "sposta": moves},
            {"tipo": "tp", "etichetta": "TP1", "prezzo": tps[0], "da": tap2 + .2, "a": t1 + .6, "colpo": True},
            {"tipo": "tp", "etichetta": "TP2", "prezzo": tps[1], "da": tap2 + .2, "a": t2 + .6, "colpo": True},
            {"tipo": "tp", "etichetta": "TP3", "prezzo": tps[2], "da": tap2 + .2, "a": tch + .6}],
  "notifiche": [[1.6, "Rischio 1% con stop a 25 pip: lotto calcolato 0.40"], [tap1 + .05, "Notizia tra 2 minuti: apertura bloccata"],
                [tap2 + .2, "BUY 0.40 in 3 parti · take profit a 20, 40 e 60 pip · stop 25 pip"],
                [t1, "TP1 +20 pip · stop delle altre parti a pareggio"], [ttr, "Trailing stop attivo: lo stop segue il prezzo a 20 pip"],
                [t2, "TP2 +40 pip · resta l'ultima parte"], [tch, f"Ultima parte chiusa dal trailing · +{pip} pip"]],
  "didascalie": [[.3, "1", "Scegli quanto rischiare. Il lotto lo calcola lui."], [3.3, "2", "Notizia in arrivo? Non apre."],
                 [9.0, "3", "Dopo il dato entra in 3 parti, con il lotto giusto."], [t1 - .6, "4", "Prima uscita: lo stop va a pareggio."],
                 [ttr - .2, "5", "Poi lo stop segue il prezzo."], [tch + .1, "6", f"+20, +40, +{pip} pip. Senza toccare niente."]],
  "pannello": [[0, "attivo", 0, R4(["Rischio", "1,0%"], ["Lotto", "—"], ["Scaglioni", "20 · 40 · 60 pip"], ["Filtro notizie", "on"])],
               [1.6, "attivo", 0, R4(["Rischio", "1,0%"], ["Lotto", "0.40", "#B6D84F"], ["Scaglioni", "20 · 40 · 60 pip"], ["Filtro notizie", "on"])],
               [3.0, "notizia", 1, R4(["Rischio", "1,0%"], ["Lotto", "0.40", "#B6D84F"], ["Scaglioni", "20 · 40 · 60 pip"], ["Filtro notizie", "blocca", "#ff6b61"])],
               [8.6, "attivo", 0, R4(["Rischio", "1,0%"], ["Lotto", "0.40", "#B6D84F"], ["Scaglioni", "20 · 40 · 60 pip"], ["Filtro notizie", "on"])],
               [tap2 + .2, "3 parti", 0, R4(["Rischio", "1,0%"], ["Parti aperte", "3"], ["Break-even", "a +20 pip"], ["Trailing", "20 pip"])],
               [t1, "pareggio ✓", 0, R4(["Rischio", "0% (pareggio)", "#B6D84F"], ["Parti aperte", "2"], ["Break-even", "fatto", "#B6D84F"], ["Trailing", "20 pip"])],
               [ttr, "trailing", 0, R4(["Rischio", "0% (pareggio)", "#B6D84F"], ["Parti aperte", "2"], ["Break-even", "fatto", "#B6D84F"], ["Trailing", "attivo", "#B6D84F"])],
               [t2, "trailing", 0, R4(["Incassati", "+60 pip", "#00C853"], ["Parti aperte", "1"], ["Break-even", "fatto", "#B6D84F"], ["Trailing", "attivo", "#B6D84F"])],
               [tch, "chiusa", 0, R4(["Incassati", f"+{tot} pip", "#00C853"], ["Parti aperte", "0"], ["Break-even", "fatto", "#B6D84F"], ["Trailing", "fatto", "#B6D84F"])]],
  "punti": ["Lotto calcolato sul rischio e filtro notizie", "Entrata in più parti con take profit scaglionati", "Break-even e trailing stop automatici"],
  "quando": "Per MT4 e MT5 · dal 23 ottobre", "fine": round(tch + 2.8, 2), "durata": round(tch + 8.6, 2)})

# ---------------- RisklyCopy ----------------
# apri sul principale, la copia parte sugli altri conti con il lotto ricalcolato sul saldo; stop spostato e chiusura copiati
K = [(-20, 4189.6), (0, 4189.8), (2, 4190.0), (5.5, 4192.2), (6.3, 4191.9), (9.5, 4193.6), (10.3, 4193.3), (13.2, 4195.4), (14.5, 4195.2), (16, 4195.0)]
p = mk(K, R); tap = 1.6; e = round(p(tap) + SPR, 2); sl0, tp = round(e - 2.5, 2), round(e + 5.0, 2)
tc = round(tap + .9, 2); tbe = primo(p, tap, lambda v: v >= e + 2.0); tm = round(tbe + .6, 2)
th = primo(p, tm, lambda v: v >= tp)
assert min(p(x / 100) for x in range(int(tap * 100), int(tm * 100))) > sl0 and min(p(x / 100) for x in range(int(tm * 100), int(th * 100))) > e + .1
C = lambda a, b, c, d, col=None: [["10 000 €", a] + ([col] if col else []), ["2 000 €", b] + ([col] if col else []), ["1 000 €", c] + ([col] if col else []), ["Rischio", d]]
D.append({"id": "b-risklycopy", "bot": "RisklyCopy", "simbolo": "XAUUSD", "ora": "11:04", "scala": [4186.0, 4197.0], "prezzo": K, "rumore": R,
  "lotto": [[0, "0.40"]], "tocchi": [[tap]],
  "linee": [{"tipo": "entrata", "etichetta": "buy 0.40", "prezzo": e, "da": tap + .1, "a": th + .6},
            {"tipo": "sl", "etichetta": "SL", "prezzo": sl0, "da": tap + .2, "a": th + .6, "sposta": [[tm, round(e + .1, 2), .5]]},
            {"tipo": "tp", "etichetta": "TP", "prezzo": tp, "da": tap + .2, "a": th + .6, "colpo": True}],
  "notifiche": [[tc, "Copiata su 2 conti · lotto ricalcolato sul saldo: 0.08 e 0.04"], [tm, "Stop spostato sul principale · aggiornato su 2 conti"],
                [th, "Take profit sul principale · chiuse anche le 2 copie"]],
  "didascalie": [[.3, "1", "Apri sul conto principale."], [tc + .1, "2", "Gli altri conti copiano. Il lotto si ricalcola: stesso rischio."],
                 [tm - .5, "3", "Sposti lo stop? Si sposta ovunque."], [th + .1, "4", "Chiudi sul principale: si chiude su tutti. +2% su ogni conto."]],
  "pannello": [[0, "invia a 2 conti", 0, C("—", "—", "—", "1% ovunque")],
               [tc, "copiata ✓", 0, C("BUY 0.40", "BUY 0.08", "BUY 0.04", "1% ovunque"), ],
               [tm, "stop copiato ✓", 0, C("SL pareggio", "SL pareggio", "SL pareggio", "0% ovunque")],
               [th, "chiuse ✓", 0, C("+200 €", "+40 €", "+20 €", "+2% ovunque", "#00C853")]],
  "punti": ["Copia tra conti MT4 e MT5", "Lotto in proporzione al saldo o al rischio", "Conti piccoli: lotto minimo e raggruppamento"],
  "quando": "Per MT4 e MT5 · dal 23 ottobre", "fine": round(th + 2.8, 2), "durata": round(th + 8.6, 2)})

json.dump(D, open('demo-bot.json', 'w'), ensure_ascii=False, indent=1)
for d in D: print(d['id'], 'durata', d['durata'])
