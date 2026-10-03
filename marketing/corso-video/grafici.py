# Grafici del corso (stile Riskly, sfondo scuro) → grafici/*.png. uso: python3 grafici.py
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
BG,PN,AC,RD,BL,TX,DM,LN='#0B0D0C','#151916','#B6D84F','#F0716B','#6FB1E8','#E6EDF3','#8B98A9','#2A312B'
plt.rcParams.update({'figure.facecolor':PN,'axes.facecolor':PN,'savefig.facecolor':PN,'axes.edgecolor':LN,'axes.labelcolor':DM,'xtick.color':DM,'ytick.color':DM,'text.color':TX,'font.size':19,'axes.grid':True,'grid.color':LN,'grid.linewidth':.8,'axes.spines.top':False,'axes.spines.right':False})
def salva(f,n): f.savefig(f'grafici/{n}.png',dpi=100,bbox_inches='tight',pad_inches=.35); plt.close(f)
rng=np.random.default_rng(5)
# 1 equity A (4%) vs B (1%) sulla stessa serie + istogramma drawdown massimi
r=np.where(rng.random(200)<.45,1.8,-1.0)
f,ax=plt.subplots(1,2,figsize=(17,6.4),gridspec_kw={'width_ratios':[1.5,1]})
for rk,c,l in ((.04,RD,'Rischio 4%'),(.01,AC,'Rischio 1%')):
    eq=np.concatenate([[1],np.cumprod(1+rk*r)]); ax[0].plot(eq*100,color=c,lw=3,label=l)
ax[0].set_yscale('log'); ax[0].set_yticks([50,100,200,500,1000]); ax[0].set_yticklabels(['50','100','200','500','1000']); ax[0].set_xlabel('Operazioni'); ax[0].set_ylabel('Capitale (inizio = 100)'); ax[0].legend(frameon=False,loc='upper left'); ax[0].set_title('Stessa serie di trade, due rischi',color=TX,fontsize=21)
N=40000; rr=np.where(rng.random((N,200))<.45,1.8,-1.0)
for rk,c in ((.04,RD),(.01,AC)):
    eq=np.concatenate([np.ones((N,1)),np.cumprod(1+rk*rr,axis=1)],axis=1); d=(1-eq/np.maximum.accumulate(eq,axis=1)).max(axis=1)*100
    ax[1].hist(d,bins=np.arange(0,100,2.5),color=c,alpha=.75,density=True)
ax[1].set_xlabel('Drawdown massimo (%)'); ax[1].set_yticks([]); ax[1].set_title('Su 40.000 simulazioni',color=TX,fontsize=21); ax[1].grid(False)
salva(f,'equity_ab')
# 2 recupero richiesto
d=np.linspace(0,.9,200); f,ax=plt.subplots(figsize=(14,7)); ax.plot(d*100,(1/(1-d)-1)*100,color=AC,lw=4)
for x in (20,50,70,90): y=(1/(1-x/100)-1)*100; ax.scatter([x],[y],color=RD,s=110,zorder=5); ax.annotate(f'−{x}% → +{y:.0f}%',(x,y),textcoords='offset points',xytext=(-16,14),ha='right',fontsize=19)
ax.set_xlabel('Perdita subita (%)'); ax.set_ylabel('Guadagno necessario per recuperare (%)'); ax.set_ylim(0,950); salva(f,'recupero')
# 3 drawdown mediano per rischio
f,ax=plt.subplots(figsize=(14,6.8)); lab=['0,5%','1%','2%','3%','5%']; v=[5,10,19,28,43]; b=ax.bar(lab,v,color=[AC,AC,'#D9C84F',RD,RD],width=.6)
for x,y in zip(b,v): ax.text(x.get_x()+x.get_width()/2,y+1.2,f'−{y}%',ha='center',fontsize=22,fontweight='bold')
ax.set_xlabel('Rischio per trade'); ax.set_ylabel('Drawdown massimo tipico (%)'); ax.set_ylim(0,52); ax.grid(axis='x',visible=False); salva(f,'dd_rischio')
# 4 win rate di pareggio
rrr=np.linspace(.5,4,200); f,ax=plt.subplots(figsize=(14,7)); ax.plot(rrr,100/(1+rrr),color=AC,lw=4)
for x in (.5,1,2,3): y=100/(1+x); ax.scatter([x],[y],color=RD,s=110,zorder=5); ax.annotate(f'RR {x:g} → {y:.0f}%',(x,y),textcoords='offset points',xytext=(14,10),fontsize=18)
ax.fill_between(rrr,100/(1+rrr),100,color=AC,alpha=.08); ax.text(2.6,75,'Win rate sopra la curva:\nil sistema guadagna',color=AC,fontsize=18); ax.text(2.6,12,'Sotto: perde',color=RD,fontsize=18)
ax.set_xlabel('Rapporto rischio/rendimento (RR)'); ax.set_ylabel('Win rate minimo per non perdere (%)'); ax.set_ylim(0,100); salva(f,'winrate_rr')
# 5 Kelly: crescita vs frazione
W,R=.45,1.8; fs=W-(1-W)/R; fr=np.linspace(0,2.2,300); g=lambda f:W*np.log(1+f*R)+(1-W)*np.log(1-f); gv=np.array([g(fs*c) for c in fr]); gv=gv/g(fs)*100
f,ax=plt.subplots(figsize=(14,7)); ax.plot(fr,gv,color=AC,lw=4); ax.axhline(0,color=DM,lw=1.5)
for c,t in ((.25,'¼ Kelly\n45%'),(.5,'½ Kelly\n76%'),(1,'Kelly pieno\n100%'),(2,'2× Kelly\n≈5%')):
    y=g(fs*c)/g(fs)*100; ax.scatter([c],[y],color=RD,s=120,zorder=5); ax.annotate(t,(c,y),textcoords='offset points',xytext=(-70,-10) if c==2 else (0,16),ha='center',fontsize=17)
ax.set_xlabel('Rischio come multiplo del Kelly pieno'); ax.set_ylabel('Crescita (% del massimo)'); ax.set_ylim(-20,125); salva(f,'kelly')
# 6 ventaglio Monte Carlo (rischio 1%)
N=3000; rr=np.where(rng.random((N,200))<.45,1.8,-1.0); eq=np.concatenate([np.ones((N,1)),np.cumprod(1+.01*rr,axis=1)],axis=1)*100
f,ax=plt.subplots(figsize=(15,7)); 
for i in range(60): ax.plot(eq[i],color=DM,alpha=.25,lw=1)
p10,p50,p90=[np.percentile(eq,q,axis=0) for q in (10,50,90)]; x=np.arange(201)
ax.fill_between(x,p10,p90,color=AC,alpha=.18); ax.plot(x,p50,color=AC,lw=4,label='Mediana'); ax.plot(x,p10,color=BL,lw=2.5,label='10° percentile'); ax.plot(x,p90,color=BL,lw=2.5,label='90° percentile'); ax.axhline(100,color=RD,lw=1.5,ls='--')
ax.set_xlabel('Operazioni'); ax.set_ylabel('Capitale (inizio = 100)'); ax.legend(frameon=False,loc='upper left'); salva(f,'montecarlo')
# 7 composizione: perdite lineari vs composte
n=np.arange(0,16); f,ax=plt.subplots(figsize=(14,7)); ax.plot(n,-5*n,color=DM,lw=3,ls='--',label='Somma semplice (n × 5%)'); ax.plot(n,((.95)**n-1)*100,color=RD,lw=4,label='Perdite composte')
ax.scatter([8],[(.95**8-1)*100],color=AC,s=130,zorder=5); ax.annotate('8 perdite: −33,7%\n(non −40%)',(8,(.95**8-1)*100),textcoords='offset points',xytext=(40,-10),fontsize=19,color=AC); ax.legend(frameon=False,loc='lower left'); ax.set_xlabel('Perdite consecutive (rischio 5%)'); ax.set_ylabel('Variazione del capitale (%)'); salva(f,'composizione')
# 8 trailing drawdown
rng2=np.random.default_rng(3); eq=[100.0]
for i in range(60): eq.append(eq[-1]*(1+0.0035+rng2.normal(0,.012)))
eq=np.array(eq); eq[35:]=eq[35:]-np.linspace(0,eq[35]*.05,len(eq)-35); pk=np.maximum.accumulate(eq)
f,ax=plt.subplots(figsize=(14,7)); ax.plot(eq,color=AC,lw=3.5,label='Equity'); ax.plot(pk*.9,color=RD,lw=3,ls='--',label='Limite trailing (massimo −10%)'); ax.plot(np.full(len(eq),90),color=DM,lw=2,ls=':',label='Limite fisso (capitale iniziale −10%)')
ax.legend(frameon=False,loc='lower right'); ax.set_xlabel('Giorni'); ax.set_ylabel('Equity'); salva(f,'trailing')
# 9 serie di perdite attese
wr=['35%','40%','45%','50%','55%','60%']; v=[10,9,8,7,6,5]; f,ax=plt.subplots(figsize=(14,6.8)); b=ax.bar(wr,v,color=AC,width=.6)
for x,y in zip(b,v): ax.text(x.get_x()+x.get_width()/2,y+.25,str(y),ha='center',fontsize=22,fontweight='bold')
ax.set_xlabel('Win rate'); ax.set_ylabel('Perdite di fila (mediana su 200 trade)'); ax.set_ylim(0,12); ax.grid(axis='x',visible=False); salva(f,'serie')
# 10 equity di due sistemi: expectancy positiva con varianza
rng3=np.random.default_rng(21); f,ax=plt.subplots(figsize=(14,6.8))
for i in range(8):
    rr=np.where(rng3.random(100)<.45,1.8,-1.0); ax.plot(np.concatenate([[0],np.cumsum(rr)]),color=AC if i==0 else DM,alpha=1 if i==0 else .45,lw=3 if i==0 else 1.5)
ax.axhline(0,color=RD,lw=1.5,ls='--'); ax.plot(np.arange(101)*.26,color=BL,lw=3,ls='--',label='Media attesa: +0,26 R a trade'); ax.legend(frameon=False,loc='upper left'); ax.set_xlabel('Operazioni'); ax.set_ylabel('Risultato cumulato (R)'); salva(f,'expectancy')
print('ok')
