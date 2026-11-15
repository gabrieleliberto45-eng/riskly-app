import json,urllib.request,sys
def post(body):
    r=urllib.request.Request("https://api.resend.com/emails",data=json.dumps(body).encode(),headers={"Authorization":"Bearer proxy-injected","Content-Type":"application/json","User-Agent":"riskly"})
    try: return 200, urllib.request.urlopen(r,timeout=30).read().decode()
    except urllib.error.HTTPError as e: return e.code, e.read().decode()
DA="Riskly <noreply@mail.riskly.trade>"
if sys.argv[1]=="prova":
    c,t=post({"from":DA,"to":["delivered@resend.dev"],"subject":"verifica","text":"verifica dominio"})
    print(c,t[:150]); sys.exit(0 if c==200 else 1)
def testo(nome): return f"""Ciao {nome},

ti scriviamo per un'informazione sul tuo account del journal Riskly (app.riskly.trade).

La tua prova gratuita è terminata. Le operazioni che hai registrato restano salvate fino al 15 dicembre 2026: dopo quella data, se non è attivo un piano, l'account e i dati collegati verranno eliminati, come previsto per gli account in prova scaduta.

Se vuoi continuare a usare il journal, puoi scegliere un piano qui: https://riskly.trade/#prezzi
Se vuoi tenere una copia delle tue operazioni, puoi esportarle dal journal prima di quella data.
Se invece vuoi che eliminiamo l'account subito, rispondi a questa email.

Il team Riskly

—
Email di servizio relativa al tuo account. Riskly · Gabriele Liberto, ditta individuale · P. IVA 04948840162 · info@riskly.trade"""
for nome,email in [(n, e) for n, e in [tuple(x.split(":",1)) for x in sys.argv[2:]]]:
    c,t=post({"from":DA,"to":[email],"reply_to":"info@riskly.trade","subject":"Il tuo account Riskly: prova terminata","text":testo(nome)})
    print(nome,c,t[:120])
