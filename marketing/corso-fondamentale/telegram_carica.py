# Carica il corso Riskly · Analisi fondamentale in un gruppo Telegram con gli Argomenti: un argomento per modulo, video in ordine con didascalia.
# uso: TG_TOKEN=... python3 telegram_carica.py trova          → mostra i gruppi visti dal bot
#      TG_TOKEN=... TG_CHAT=-100... python3 telegram_carica.py carica   (riprende da dove si è fermato: stato in out/telegram_stato.json)
import os, sys, json, re, glob, time, subprocess, requests, build
T = os.environ['TG_TOKEN']; API = f'https://api.telegram.org/bot{T}/'; STATO = build.QUI + '/out/telegram_stato.json'
def call(m, files=None, **p):
    for t in range(6):
        try:
            if files:
                for v in files.values():
                    if hasattr(v[1], 'seek'): v[1].seek(0)
            r = requests.post(API + m, data=p, files=files, timeout=600).json()
        except requests.exceptions.RequestException as e:
            print('rete, riprovo:', type(e).__name__, flush=True); time.sleep(5 * (t + 1)); continue
        if r.get('ok'): return r['result']
        ra = r.get('parameters', {}).get('retry_after')
        if ra: time.sleep(ra + 1); continue
        raise Exception(f"{m}: {r}")
    raise Exception('troppi tentativi ' + m)
def trova():
    for u in call('getUpdates'):
        for k in ('message', 'my_chat_member', 'chat_member'):
            if k in u: c = u[k]['chat']; print(c['id'], c['type'], c.get('title'), 'argomenti' if c.get('is_forum') else 'SENZA argomenti')
pul = lambda t: re.sub(r'\*\*(.+?)\*\*', r'\1', t)
RITOCCHI = {'0.1': ["Il prezzo si muove per un motivo: spesso è una notizia", "L'analisi fondamentale studia contesto, attese e reazioni", "Non è una sfera di cristallo: serve a sapere quando proteggersi"],
            '0.4': ["Quattro domande per ogni notizia: dato, aspettativa, reazione, rischio", "Non chiederti dove andrà il prezzo", "Chiediti cosa fare se si muove molto"],
            '1.2': ["Ogni dato corregge anche quelli dei mesi precedenti", "Una revisione può contare più del dato del mese", "Leggi sempre il dato completo prima di operare"],
            '1.3': ["Quello che tutti si aspettano è già nel prezzo", "Conta la sorpresa, non il dato in sé", "Anche una buona notizia attesa può far scendere il prezzo"],
            '1.4': ["Nei minuti del dato spread, slippage e gap aumentano", "Lo stop può essere eseguito lontano dal livello impostato", "Lotti ridotti e niente ordini stretti a ridosso del dato"]}
TITOLI = {}
def durata(f):
    h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', subprocess.run([build.FF, '-i', f], capture_output=True, text=True).stderr).groups(); return int(h)*3600 + int(m)*60 + float(s)
mm = lambda s: f"{int(s//60)}:{int(round(s%60)):02d}"
def carica(chat):
    L = build.carica(); st = json.load(open(STATO)) if os.path.exists(STATO) else {'topic': {}, 'fatti': []}
    salva = lambda: json.dump(st, open(STATO, 'w'), indent=1)
    mod = {}
    for l in L: mod.setdefault((l['modulo'], l['modTitolo']), []).append(l)
    nomi = ['📌 Inizia da qui'] + [f"📂 {m} · {mt}" if m.startswith('Modulo') else f"📂 {m}" for (m, mt) in mod]
    for n in nomi:
        if n not in st['topic']: st['topic'][n] = call('createForumTopic', chat_id=chat, name=n)['message_thread_id']; salva(); time.sleep(1)
    for i, ((m, mt), ls) in enumerate(mod.items()):
        tid = st['topic'][nomi[i + 1]]
        for l in ls:
            if l['id'] in st['fatti']: continue
            f = glob.glob(f"{build.QUI}/out/corso/*/{l['id']}_*.mp4")[0]; d = durata(f)
            riep = next((s for s in l['slide'] if s.get('titolo') == 'In breve'), None)
            punti = RITOCCHI.get(l['id']) or [pul(p) if isinstance(p, str) else f'{pul(p[0])} — {pul(p[1])}' for p in (riep['punti'] if riep else [])]
            cap = f"🎬 Lezione {l['id']} · {TITOLI.get(l['id'], pul(l['titolo']))} ({mm(d)})" + ("\n\nIn breve:\n" + "\n".join('• ' + p for p in punti) if punti else '')
            with open(f, 'rb') as fh:
                call('sendVideo', files={'video': (os.path.basename(f), fh, 'video/mp4')}, chat_id=chat, message_thread_id=tid, caption=cap,
                     supports_streaming='true', width=1920, height=1080, duration=int(d), protect_content='true')
            st['fatti'].append(l['id']); salva(); print('caricata', l['id'], flush=True); time.sleep(3)
    if 'indice' not in st:
        righe = ['📚 RISKLY · ANALISI FONDAMENTALE', f"{len(L)} lezioni · circa {int(sum(durata(g) for g in glob.glob(build.QUI + '/out/corso/*/*.mp4'))//60)} minuti", '',
                 'Apri gli argomenti in ordine: ogni argomento è un modulo, con le lezioni dalla prima all\'ultima.', '']
        for (m, mt), ls in mod.items(): righe.append(f"▸ {m} · {mt} ({len(ls)} {'lezione' if len(ls) == 1 else 'lezioni'})")
        righe += ['', 'Come usarlo: una lezione alla volta, in ordine. Nei giorni dei dati riguarda la lezione del dato in uscita, e alla fine scrivi il tuo piano macro (modulo 10).', '',
                  '⚠️ Contenuto educativo, non consulenza finanziaria. Il trading con leva comporta un rischio elevato: puoi perdere tutto il capitale. Gli strumenti Riskly citati sono prodotti miei.']
        msg = call('sendMessage', chat_id=chat, message_thread_id=st['topic'][nomi[0]], text='\n'.join(righe), protect_content='true')
        try: call('pinChatMessage', chat_id=chat, message_id=msg['message_id'], disable_notification='true')
        except Exception as e: print('pin non riuscito:', e)
        st['indice'] = msg['message_id']; salva()
    print('FINITO')
if __name__ == '__main__':
    trova() if sys.argv[1] == 'trova' else carica(os.environ['TG_CHAT'])
