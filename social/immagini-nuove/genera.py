# Genera le sei immagini dei prodotti (1200x675) nello stile nero e oro scelto da Gabriele,
# con testi e disegni veritieri (niente rendimenti, niente funzioni che non esistono).
import json
GOLD='#E2B24A'; GOLD2='#F6D58A'; INK='#0B0D0F'; UP='#3FB27F'; DN='#E5604F'; DIM='#9AA0A6'
CSS='''
@font-face{font-family:IS;src:url(file:///home/user/riskly-app/nuovo/riskly/fonts/InstrumentSans-700-normal-latin.woff2);font-weight:700}
@font-face{font-family:IS;src:url(file:///home/user/riskly-app/nuovo/riskly/fonts/InstrumentSans-500-normal-latin.woff2);font-weight:500}
@font-face{font-family:IS;src:url(file:///home/user/riskly-app/nuovo/riskly/fonts/InstrumentSans-400-normal-latin.woff2);font-weight:400}
@font-face{font-family:JB;src:url(file:///home/user/riskly-app/nuovo/riskly/fonts/JetBrainsMono-500-normal-latin.woff2);font-weight:500}
*{box-sizing:border-box;margin:0}
body{width:1200px;height:675px;background:#0B0D0F;color:#fff;font-family:IS,sans-serif;position:relative;overflow:hidden}
.bg{position:absolute;inset:0;background:radial-gradient(900px 520px at 86% 20%,rgba(226,178,74,.20),transparent 62%),radial-gradient(700px 400px at 0% 100%,rgba(226,178,74,.08),transparent 60%),#0B0D0F}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:60px 60px;mask-image:linear-gradient(90deg,transparent 0,#000 40%)}
.mk{position:absolute;left:64px;top:52px;font-size:21px;letter-spacing:.42em;font-weight:500;color:#fff;opacity:.92}
.tx{position:absolute;left:64px;top:150px;width:560px}
h1{font-size:92px;line-height:.94;letter-spacing:-.025em;font-weight:700}
h1 b{color:'''+GOLD+''';font-weight:700;display:block}
h1.uno{font-size:72px;white-space:nowrap}
h1.uno b{display:inline}
.sub{margin-top:26px;font-size:30px;line-height:1.25;color:#E8EAEC;font-weight:500;width:520px}
ul{list-style:none;padding:0;margin-top:30px;display:grid;gap:14px}
li{display:flex;gap:14px;align-items:center;font-size:25px;color:#E8EAEC}
li i{width:26px;height:26px;border:2px solid '''+GOLD+''';border-radius:50%;flex:none;position:relative}
li i::after{content:"";position:absolute;left:7px;top:4px;width:7px;height:12px;border:solid '''+GOLD+''';border-width:0 2.5px 2.5px 0;transform:rotate(40deg)}
.ft{position:absolute;left:0;right:0;bottom:0;height:62px;border-top:1px solid rgba(226,178,74,.45);background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:space-between;padding:0 64px;font-size:19px;letter-spacing:.28em;color:'''+GOLD+'''}
.ft span:last-child{letter-spacing:.04em;color:#7C838A;font-size:16px}
.il{position:absolute;right:48px;top:96px;width:560px;height:480px}
svg{display:block}
text{font-family:JB,monospace}
.t2{font-family:IS,sans-serif}
'''
def page(nome1,nome2,sub,punti,foot,svg,nota='Immagine illustrativa'):
    li=''.join(f'<li><i></i>{p}</li>' for p in punti)
    return f'''<!doctype html><meta charset=utf-8><style>{CSS}</style><div class="bg"></div><div class="grid"></div>
<div class="mk">RISKLY</div>
<div class="tx"><h1 class="{'uno' if nome1 in ('Risk','Trade','Scale') else ''}">{nome1}<b>{nome2}</b></h1><p class="sub">{sub}</p><ul>{li}</ul></div>
<div class="il">{svg}</div>
<div class="ft"><span>{foot}</span><span>{nota}</span></div>'''
def cndl(x,y,h,w,up,wick=14):
    c=UP if up else DN
    return f'<line x1="{x+w/2}" x2="{x+w/2}" y1="{y-wick}" y2="{y+h+wick}" stroke="{c}" stroke-width="3"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{c}"/>'
def lbl(x,y,t,c=GOLD,a='start',s=18): return f'<text x="{x}" y="{y}" fill="{c}" font-size="{s}" text-anchor="{a}" class="t2" style="font-weight:700;letter-spacing:.06em">{t}</text>'
PANEL='<rect x="2" y="2" width="556" height="476" rx="20" fill="rgba(255,255,255,.035)" stroke="rgba(255,255,255,.14)" stroke-width="2"/>'
# RiskGuard: tre perdite di fila, poi blocco
rg=f'''<svg viewBox="0 0 560 480" width="560" height="480">{PANEL}
<line x1="40" x2="520" y1="150" y2="150" stroke="rgba(255,255,255,.12)" stroke-dasharray="6 8"/>
{cndl(70,170,60,34,True)}{cndl(120,150,70,34,False)}{cndl(170,190,60,34,False)}{cndl(220,215,70,34,False)}
<rect x="285" y="60" width="240" height="360" rx="14" fill="rgba(229,96,79,.10)" stroke="{DN}" stroke-width="2" stroke-dasharray="8 8"/>
<g transform="translate(405 190)" stroke="{DN}" stroke-width="7" fill="none" stroke-linecap="round"><rect x="-30" y="-6" width="60" height="50" rx="10" fill="rgba(229,96,79,.16)"/><path d="M-18 -6 V-26 Q-18 -44 0 -44 Q18 -44 18 -26 V-6"/></g>
{lbl(405,282,'PAUSA',DN,'middle',30)}{lbl(405,314,'fino a mezzanotte','#F2B1A8','middle',19)}
{lbl(70,96,'PERDITE DI FILA',DIM,'start',16)}
<g transform="translate(70 360)"><rect width="46" height="46" rx="10" fill="rgba(229,96,79,.2)" stroke="{DN}" stroke-width="2"/><rect x="62" width="46" height="46" rx="10" fill="rgba(229,96,79,.2)" stroke="{DN}" stroke-width="2"/><rect x="124" width="46" height="46" rx="10" fill="rgba(229,96,79,.2)" stroke="{DN}" stroke-width="2"/>
<text x="23" y="32" fill="{DN}" font-size="22" text-anchor="middle">1</text><text x="85" y="32" fill="{DN}" font-size="22" text-anchor="middle">2</text><text x="147" y="32" fill="{DN}" font-size="22" text-anchor="middle">3</text></g></svg>'''
# TradeManager: stop iniziale, pareggio, trailing
path='M50 380 L110 340 L165 355 L225 285 L280 300 L350 215 L405 232 L480 140'
tm=f'''<svg viewBox="0 0 560 480" width="560" height="480">{PANEL}
<polyline points="50,380 110,340 165,355 225,285 280,300 350,215 405,232 480,140" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
<line x1="50" x2="150" y1="430" y2="430" stroke="{DN}" stroke-width="4"/>
<path d="M150 430 H190 V380 H280 V330 H350 V272 H405 V250 H480" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linejoin="miter"/>
<circle cx="50" cy="380" r="9" fill="#fff"/><circle cx="480" cy="140" r="9" fill="{UP}"/>
{lbl(50,456,'STOP INIZIALE',DN,'start',17)}{lbl(196,408,'PAREGGIO',GOLD,'start',17)}{lbl(350,350,'TRAILING',GOLD,'start',17)}
{lbl(60,100,'LO STOP SEGUE IL PREZZO',DIM,'start',16)}</svg>'''
# ScaleIn: ingresso e scaglioni
si=f'''<svg viewBox="0 0 560 480" width="560" height="480">{PANEL}
{cndl(60,330,40,30,False)}{cndl(100,320,50,30,False)}{cndl(140,290,60,30,True)}{cndl(180,260,50,30,True)}{cndl(220,230,60,30,True)}{cndl(260,190,60,30,True)}{cndl(300,170,40,30,True)}{cndl(340,130,60,30,True)}
<g stroke-dasharray="8 8" stroke-width="2.5"><line x1="40" x2="520" y1="300" y2="300" stroke="{GOLD}"/><line x1="40" x2="520" y1="230" y2="230" stroke="{UP}"/><line x1="40" x2="520" y1="150" y2="150" stroke="{UP}"/><line x1="40" x2="520" y1="90" y2="90" stroke="{UP}"/></g>
{lbl(520,292,'ENTRA',GOLD,'end',16)}{lbl(520,222,'TP 1',UP,'end',16)}{lbl(520,142,'TP 2',UP,'end',16)}{lbl(520,82,'TP 3',UP,'end',16)}
<g font-size="17"><rect x="52" y="394" width="150" height="40" rx="10" fill="rgba(226,178,74,.16)" stroke="{GOLD}"/><text x="127" y="421" fill="{GOLD}" text-anchor="middle">TUA: 0,30</text><rect x="214" y="394" width="150" height="40" rx="10" fill="rgba(226,178,74,.16)" stroke="{GOLD}"/><text x="289" y="421" fill="{GOLD}" text-anchor="middle">SCAGL. 1</text><rect x="376" y="394" width="130" height="40" rx="10" fill="rgba(226,178,74,.16)" stroke="{GOLD}"/><text x="441" y="421" fill="{GOLD}" text-anchor="middle">SCAGL. 2</text></g></svg>'''
# Riskly Pro: tre moduli, un solo rischio
def mod(y,t,s): return f'<rect x="40" y="{y}" width="480" height="78" rx="14" fill="rgba(255,255,255,.05)" stroke="rgba(255,255,255,.16)" stroke-width="2"/><circle cx="82" cy="{y+39}" r="16" fill="rgba(226,178,74,.18)" stroke="{GOLD}" stroke-width="2"/><path d="M74 {y+39} l6 6 l11 -12" stroke="{GOLD}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'+f'<text x="116" y="{y+36}" fill="#fff" font-size="23" class="t2" style="font-weight:700">{t}</text><text x="116" y="{y+62}" fill="{DIM}" font-size="17" class="t2" style="font-weight:500">{s}</text>'
pro=f'''<svg viewBox="0 0 560 480" width="560" height="480">{PANEL}
{mod(34,'RiskGuard','blocca dopo le perdite')}{mod(124,'TradeManager','stop, pareggio, trailing')}{mod(214,'ScaleIn','ingressi a scaglioni')}
<text x="40" y="344" fill="{DIM}" font-size="16" letter-spacing="1.6">RISCHIO TOTALE, TUTTE LE POSIZIONI</text>
<rect x="40" y="360" width="480" height="22" rx="11" fill="rgba(255,255,255,.08)"/><rect x="40" y="360" width="300" height="22" rx="11" fill="{GOLD}"/><line x1="440" x2="440" y1="350" y2="394" stroke="{DN}" stroke-width="3"/>
<text x="340" y="420" fill="{GOLD}" font-size="22" text-anchor="middle">2,4%</text><text x="440" y="420" fill="{DN}" font-size="18" text-anchor="middle">LIMITE 3%</text></svg>'''
# RisklyCopy: stesso rischio su ogni conto
def conto(x,y,t,saldo,lot,c=GOLD): return f'<rect x="{x}" y="{y}" width="200" height="130" rx="14" fill="rgba(255,255,255,.05)" stroke="{c}" stroke-width="2.5"/><text x="{x+100}" y="{y+36}" fill="{c}" font-size="16" text-anchor="middle" letter-spacing="1.5">{t}</text><text x="{x+100}" y="{y+76}" fill="#fff" font-size="26" text-anchor="middle">{saldo}</text><text x="{x+100}" y="{y+108}" fill="{DIM}" font-size="19" text-anchor="middle">{lot}</text>'
cp=f'''<svg viewBox="0 0 560 480" width="560" height="480">{PANEL}
{conto(180,40,'CONTO PRINCIPALE','10.000 $','1,00 lotto')}
<g stroke="{GOLD}" stroke-width="3" fill="none"><path d="M280 170 V220 H140 V262"/><path d="M280 220 H420 V262"/></g><g fill="{GOLD}"><path d="M130 262 l10 14 l10 -14z"/><path d="M410 262 l10 14 l10 -14z"/></g>
{conto(40,282,'COPIA 1','5.000 $','0,50 lotto','#fff')}{conto(320,282,'COPIA 2','2.000 $','0,20 lotto','#fff')}
<rect x="164" y="425" width="232" height="38" rx="19" fill="rgba(226,178,74,.16)" stroke="{GOLD}"/><text x="280" y="450" fill="{GOLD}" font-size="17" text-anchor="middle" letter-spacing="1.2">STESSO RISCHIO</text></svg>'''
# Journal: curva, calendario, win rate (dati dimostrativi)
cal=''.join(f'<rect x="{40+(i%7)*34}" y="{258+(i//7)*34}" width="28" height="28" rx="5" fill="{["rgba(63,178,127,.55)","rgba(229,96,79,.5)","rgba(255,255,255,.08)"][ (i*5+i//3)%3 ]}"/>' for i in range(28))
jr=f'''<svg viewBox="0 0 560 480" width="560" height="480">{PANEL}
<polyline points="40,200 90,170 130,185 190,130 240,150 300,95 350,110 410,70 470,60 520,40" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
<path d="M40 200 L90 170 L130 185 L190 130 L240 150 L300 95 L350 110 L410 70 L470 60 L520 40 V230 H40Z" fill="rgba(226,178,74,.10)"/>
{cal}
<g transform="translate(380 345)"><circle r="68" fill="none" stroke="rgba(255,255,255,.10)" stroke-width="16"/><circle r="68" fill="none" stroke="{GOLD}" stroke-width="16" stroke-dasharray="{2*3.1416*68*.47} 999" transform="rotate(-90)" stroke-linecap="round"/><text y="-2" fill="#fff" font-size="36" text-anchor="middle">47%</text><text y="26" fill="{DIM}" font-size="14" text-anchor="middle">VINTE</text></g>
{lbl(40,246,'CALENDARIO DEL MESE',DIM,'start',14)}{lbl(40,36,'DATI DIMOSTRATIVI',GOLD,'start',15)}</svg>'''
D={
 'bot-riskguard':page('Risk','Guard','Ti ferma prima di perdere il conto.',['Blocco dopo N perdite di fila','Limite di perdita giornaliero','Stop loss sempre presente'],'MENO ERRORI. PIÙ DISCIPLINA.',rg),
 'bot-trademanager':page('Trade','Manager','Gestisce le uscite al posto tuo.',['Stop e take profit in pip','Pareggio automatico','Trailing stop'],'LE USCITE SOTTO CONTROLLO.',tm),
 'bot-scalein':page('Scale','In','Apri una posizione, lui apre le altre.',['Take profit diversi per scaglione','Rischio totale sotto controllo','Stop automatico se manca'],'INGRESSI A SCAGLIONI.',si),
 'bot-riskly-pro':page('Riskly','Pro','Tre software in uno, un solo rischio.',['RiskGuard, TradeManager, ScaleIn','Rischio calcolato su tutte le posizioni','Lotto già calcolato sul rischio'],'IL PIÙ COMPLETO.',pro),
 'bot-risklycopy':page('Riskly','Copy','Stesso rischio su ogni conto.',['Copia da un conto principale','Lotto in proporzione al saldo','Tra MetaTrader 4 e 5'],'DAL TUO CONTO AI TUOI CONTI.',cp),
 'journal':page('Riskly','Journal','Il diario che misura la tua disciplina.',['Operazioni anche dai software','Statistiche per orario e strategia','Regole delle prop firm'],'IMPARA DAI TUOI NUMERI.',jr,'Dati dimostrativi, non reali'),
}
import os
for k,v in D.items(): open(f'/tmp/claude-0/-home-user-riskly-app/ce60a453-0542-5639-9e1e-839dfbd0bd0f/scratchpad/img-{k}.html','w').write(v)
print(list(D))
