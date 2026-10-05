/* Scene dei reel demo: cosa si vede sul telefono e quando (le chiavi sono parole della voce; "parola#2" = seconda volta). */
const CORSO = '/home/user/riskly-app/marketing/corso-video/out/corso/';
const GRAF = '/home/user/riskly-app/marketing/corso-video/grafici/';
const SENZA_PREZZI = () => { const s = document.createElement('style'); s.textContent = '.bot .price,.bot .price-off,.bot .plabel,#lancioBot,.lancio-bar{visibility:hidden!important;height:0!important;margin:0!important}'; document.head.appendChild(s); };
const BOT_COME = async H => { await H.js(() => { window.visibile = () => false; go('bot'); botTab('come'); }); };
const SIM_Y = k => `#chart${k}`;
const JOURNAL = { 'riskly-metodo': 'generale', 'riskly-metodo-chiesto': '1', 'riskly-saldo-iniziale': '10000', 'riskly-scag-rapido': null, 'riskly-vpip': null };
const avviaJournal = (metodo, vista) => async H => { await H.js(([m, v]) => { utente = { id: 'u1', email: 'demo@riskly.trade', user_metadata: { metodo: m, saldo_iniziale: 10000, nome: 'Trader' } }; profilo = { piano: 'pro' };
  j_trades = j_generaDemo(); aggiornaVista(); jVista(v);
  [...document.querySelectorAll('header a, header button, nav a, nav button, .btn')].filter(e => /registrati|accedi/i.test(e.textContent)).forEach(e => e.style.visibility = 'hidden'); }, [metodo, vista]); };
const verso = sel => async H => H.scorri(sel, .7, 70);

module.exports = {
  /* RiskGuard: la simulazione della giornata che si consuma */
  p01: { init: BOT_COME, passi: [
    [0, async H => H.scorri('#bt-come .sim', .01, 40)],
    ['guarda', async H => { await H.scorri('#chartRG', .6, 140); await H.sim('RG', 7500, 'chiude'); }],
    ['basta', async H => H.velocita(0)],
  ]},
  /* ScaleIn: la replica a scaglioni */
  p04: { init: BOT_COME, passi: [
    [0, async H => H.scorri('#chartSI', .01, 140)],
    ['apri', async H => H.sim('SI', 5000, 'quando')],
    ['esce', async H => H.velocita(0)],
  ]},
  /* TradeManager: break-even e trailing */
  p05: { init: BOT_COME, passi: [
    [0, async H => H.scorri('#chartTM', .01, 140)],
    ['guarda', async H => H.sim('TM', 6000, 'protetto')],
    ['tutto', async H => H.velocita(0)],
  ]},
  /* Riskly Pro: il calcolo del lotto */
  p06: { init: async H => { await H.js(() => { go('calc'); document.getElementById('c-pips').value = ''; document.getElementById('c-bal').value = ''; calcPos(); }); }, passi: [
    [0, async H => H.scorri('.calc-grid', .01, 60)],
    ['diecimila', async H => H.scrivi('#c-bal', '10000', .5)],
    ['venticinque', async H => H.scrivi('#c-pips', '25', .3)],
    ['cinquanta#1', async H => H.scrivi('#c-pips', '50', .3)],
    ['riskly#1', async H => H.scorri('#o-lots', .6, 260)],
  ]},
  /* Journal: statistiche */
  p07: { app: 'jr', storage: JOURNAL, init: avviaJournal('generale', 'statistiche'), passi: [
    ['fascia', async H => H.scorri('#oraMeta', .7, 60)],
    ['stato', async H => H.scorri('#emoStat', .7, 110)],
    ['teoria', async H => H.scorri('#symChart', 1.2, 200)],
  ]},
  /* RiskGuard per le prop firm: tracker gratuito, poi il blocco */
  p08: { init: async H => { await H.js(() => { window.visibile = () => false; go('calc'); ['p-start','p-cur','p-day'].forEach(i => document.getElementById(i).value = ''); calcProp(); }); }, passi: [
    [0, async H => H.scorri('#p-start', .01, 160)],
    ['centomila', async H => { H.scrivi('#p-start', '100000', .5); H.scrivi('#p-day', '100000', .5); }],
    ['tracker', async H => H.scrivi('#p-cur', '96800', .8)],
    ['riskguard#1', async H => { await H.js(() => { go('bot'); botTab('come'); }); await H.scorri('#chartRG', .01, 140); await H.sim('RG', 7500, 'margine'); }],
    ['controlla', async H => H.velocita(0)],
  ]},
  /* Calcolatori: rischio di rovina */
  p09: { init: async H => { await H.js(() => { go('calc'); document.getElementById('r-risk').value = '1'; calcRuin(); }); }, passi: [
    [0, async H => H.scorri('#r-wr', .01, 160)],
    ['winrate', async H => H.scrivi('#r-wr', '50', .3)],
    ['simula', async H => H.scorri('#o-ruin', .7, 200)],
    ['cinque#1', async H => H.scrivi('#r-risk', '5', .2)],
    ['calcolatori', async H => H.scorri('#mcChart', .8, 420)],
  ]},
  /* Journal: chiusura a scaglioni */
  p11: { app: 'jr', storage: JOURNAL, init: avviaJournal('generale', 'nuova'), passi: [
    [0, async H => H.scorri('#add', .01, 70)],
    ['journal', async H => H.scrivi('#f-symbol', 'EURUSD', .5)],
    ['scegli', async H => { await H.scorri('#fScag', .6, 80); H.scrivi('#rp-tot', '1.00', .3); H.scrivi('#rp-stop', '20', .3); }],
    ['scaglioni#2', async H => H.clic('[data-fine="scag"]')],
    ['quanti', async H => H.scrivi('#rp-n', '5', .1)],
    ['ogni', async H => { H.scrivi('#rp-passo', '10', .2); }],
    ['tocchi', async H => H.scorri('.jrap-griglia', .6, 120)],
    ['tre', async H => H.clic('[data-rk="3"]')],
    ['risultato#2', async H => H.scorri('#scagStima', .7, 120)],
  ]},
  /* Bot a confronto: le schede dei quattro bot */
  p12: { init: async H => { await H.js(() => { go('bot'); botTab('scegli'); }); await H.js(SENZA_PREZZI); }, passi: [
    [0, async H => H.scorri('.bot', .01, 90)],
    ['riskguard', verso('.bot@0')],
    ['trademanager', verso('.bot@1')],
    ['scalein', verso('.bot@2')],
    ['riskly#2', verso('.bot@3')],
  ]},
  /* Journal input e conferma con gli screenshot */
  p13: { app: 'jr', storage: Object.assign({}, JOURNAL, { 'riskly-metodo': 'conferma' }), init: avviaJournal('conferma', 'nuova'), passi: [
    [0, async H => H.scorri('#add', .01, 70)],
    ['segni#1', async H => H.scorri('#fMetodo', .7, 60)],
    ['pullback', async H => H.clic('[data-o="P.B. KL"]')],
    ['carichi', async H => { await H.scorri('#jshot1', .6, 260); await H.p.setInputFiles('#f-shot', GRAF + 'trailing.png'); }],
    ['conferma#2', async H => { await H.scorri('[data-posto-shot="conferma"]', .7, 420); await H.clic('[data-o="B.O. KL"] >> nth=1'); }],
    ['screenshot#2', async H => { await H.p.setInputFiles('#f-shot2', GRAF + 'serie.png'); await H.scorri('#jshot2', .6, 260); }],
    ['sessioni', async H => H.scorri('[data-c="sessioni"]', .7, 160)],
    ['dopo', async H => { await H.js(() => jVista('statistiche')); await H.scorri('#gruppiTab', .01, 120); }],
  ]},
  /* Lancio: la home con i prodotti */
  p14: { init: async H => { await H.js(() => go('home')); }, passi: [
    [0, async H => H.scorri(0, .01)],
    ['pensati', async H => H.scorri('.prod-riga', .9, 120)],
    ['fermano', async H => H.scorri('.prod-riga@1', .8, 120)],
    ['journal', async H => H.scorri('.prod-riga@4', .8, 160)],
  ]},
  /* Lista d'attesa */
  p15: { init: async H => { await H.js(() => { go('bot'); botTab('scegli'); }); await H.js(SENZA_PREZZI); }, passi: [
    [0, async H => H.scorri('.bot', .01, 90)],
    ['scegli', async H => { await H.js(() => apriModulo('attesa', 'RiskGuard', 0)); }],
    ['email', async H => { H.scrivi('#m-nome', 'Marco', .4); H.scrivi('#m-email', 'marco@email.it', .9); }],
  ]},
  /* Domani: le tre simulazioni una dopo l'altra */
  p17: { init: BOT_COME, passi: [
    [0, async H => H.scorri('#chartRG', .01, 140)],
    ['riskguard', async H => { await H.scorri('#chartRG', .01, 140); await H.sim('RG', 7500, 'trademanager'); }],
    ['trademanager', async H => { await H.scorri('#chartTM', .5, 140); await H.sim('TM', 6000, 'scalein'); }],
    ['scalein', async H => { await H.scorri('#chartSI', .5, 140); await H.sim('SI', 5000, 'unisce'); }],
    ['oggi', async H => H.velocita(0)],
  ]},
  /* Oggi: la pagina dei bot */
  p18: { init: async H => { await H.js(() => { go('bot'); botTab('scegli'); }); await H.js(SENZA_PREZZI); }, passi: [
    [0, async H => H.scorri(0, .01)],
    ['simulazioni', async H => { await H.js(() => { window.visibile = () => false; botTab('come'); }); await H.scorri('#chartRG', .01, 140); await H.sim('RG', 7500, 'funzionano'); }],
    ['funzionano', async H => { await H.js(() => botTab('scegli')); await H.scorri('.bot', .01, 90); }],
    ['prezzo', async H => H.scorri('.bot@3', 1.2, 90)],
  ]},
  /* Videocorso: spezzoni delle lezioni */
  p03: { corso: [[CORSO + '04_Modulo_4_Dimensionare_la_posizione/4.1_Rischio_fisso_in_percentuale.mp4', 30, ''], [CORSO + '03_Modulo_3_Drawdown_e_perdite/3.4_Le_perdite_si_compongono.mp4', 25, 'perché']] },
  p10: { corso: [[CORSO + '03_Modulo_3_Drawdown_e_perdite/3.2_Perché_recuperare_costa_di_più.mp4', 20, ''], [CORSO + '09_Modulo_9_Tecniche_avanzate/9.2_Il_trailing_stop_loss_in_tutte_le_sue_forme.mp4', 60, 'poi']] },
  p16: { corso: [[CORSO + '09_Modulo_9_Tecniche_avanzate/9.2_Il_trailing_stop_loss_in_tutte_le_sue_forme.mp4', 90, ''], [CORSO + '09_Modulo_9_Tecniche_avanzate/9.4_Uscite_a_scaglioni_e_break_even_sui_restanti.mp4', 40, 'scaglioni']] },
};
