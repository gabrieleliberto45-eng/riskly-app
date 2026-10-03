# Numeri citati nel corso (simulazioni, seme fisso). uso: python3 sim_numeri.py
import numpy as np
rng=np.random.default_rng(11)
def paths(wr,win,loss,rk,n,N=40000):
    r=np.where(rng.random((N,n))<wr,win,-loss); eq=np.cumprod(1+rk*r,axis=1); eq=np.concatenate([np.ones((N,1)),eq],axis=1); return r,eq
def dd(eq): pk=np.maximum.accumulate(eq,axis=1); return (1-eq/pk).max(axis=1)
print('DD mediano / p90, finale mediano, rovina(-30% dall\'inizio), 200 trade, WR45 +1.8/-1')
for rk in (.005,.01,.02,.03,.05):
    r,eq=paths(.45,1.8,1,rk,200); d=dd(eq); print(f'{rk*100:.1f}% DDmed {np.median(d)*100:.1f} p90 {np.percentile(d,90)*100:.1f}  fin med {np.median(eq[:,-1])-1:+.2f} p10 {np.percentile(eq[:,-1],10)-1:+.2f} p90 {np.percentile(eq[:,-1],90)-1:+.2f}  rovina {np.mean(eq.min(axis=1)<=.7)*100:.1f}%  finale<1 {np.mean(eq[:,-1]<1)*100:.1f}%  P(DD>=50%) {np.mean(d>=.5)*100:.1f}')
print('serie di perdite massima (mediana, p90) su 200 trade')
for wr in (.35,.4,.45,.5,.55,.6):
    r=rng.random((40000,200))<wr; run=np.zeros(40000); best=np.zeros(40000)
    for i in range(200): run=np.where(r[:,i],0,run+1); best=np.maximum(best,run)
    print(wr, np.median(best), np.percentile(best,90))
# probabilita di almeno n perdite di fila su 200 trade a WR 45%
r=rng.random((40000,200))<.45; run=np.zeros(40000); best=np.zeros(40000)
for i in range(200): run=np.where(r[:,i],0,run+1); best=np.maximum(best,run)
for n in (5,6,8,10,12): print('>=',n,np.mean(best>=n))
