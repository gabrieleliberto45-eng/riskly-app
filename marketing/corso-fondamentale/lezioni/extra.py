EXTRA = {}
INS = {}
DEL = {}

# grafici con dati veri (lezioni/dati_veri.py)
from dati_veri import GRAFICI
for _id, (_anc, _sl) in GRAFICI.items(): INS.setdefault(_id, []).append((_anc, _sl))
