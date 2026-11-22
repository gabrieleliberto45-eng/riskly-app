# Copertina di Riskly News con sfondo creato da Higgsfield (Gabriele, 22/11: "utilizza higgsfield se devi creare qualche immagine copertina").
# Higgsfield fa SOLO l'illustrazione, senza scritte; il testo (logo, categoria, titolo, numero) lo mettiamo noi, così è sempre giusto.
# Budget: 100 crediti Higgsfield al mese (0,75 a immagine con gpt_image_2_6): il registro è in notizie/higgsfield_registro.json.
# uso: python3 notizie/copertina_ia.py ID URL_O_FILE_SFONDO "CATEGORIA" "TITOLO" ["NUMERO"] [--verticale]
#   orizzontale 1600×900 per gli articoli → nuovo/news/copertine/ID.jpg; --verticale 1080×1920 per le copertine dei reel → social/reel/cover/ID.jpg
import io, json, os, sys, urllib.request, datetime as dt
from PIL import Image, ImageDraw, ImageFont, ImageFilter
QUI = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(QUI, '..', 'nuovo', 'riskly', 'fonts')
arg = [a for a in sys.argv[1:] if a != '--verticale']; VERT = '--verticale' in sys.argv
ID, SRC, CAT, TIT = arg[:4]; NUM = arg[4] if len(arg) > 4 else ''
W, H = (1080, 1920) if VERT else (1600, 900)
BLU, ORO, CARTA = (18, 38, 63), (212, 174, 90), (246, 246, 243)
COL = {'Straordinarie': (198, 47, 59), 'Dato appena uscito': (198, 47, 59), 'Fed': (29, 79, 196), 'Tassi e banche centrali': (29, 79, 196), 'Dollaro': (15, 138, 79)}.get(CAT, ORO)

def font(nome, px):
    for n in ([nome] if isinstance(nome, str) else nome):
        p = os.path.join(F, n)
        if os.path.exists(p): return ImageFont.truetype(p, px)
    return ImageFont.load_default()
def trova(*parti):
    fs = sorted(os.listdir(F)); return [f for f in fs if all(x.lower() in f.lower() for x in parti) and f.endswith(('.ttf', '.otf', '.woff2'))] + fs

raw = urllib.request.urlopen(urllib.request.Request(SRC, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read() if SRC.startswith('http') else open(SRC, 'rb').read()
img = Image.open(io.BytesIO(raw)).convert('RGB')
s = max(W / img.width, H / img.height); img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
img = img.crop(((img.width - W) // 2, (img.height - H) // 2, (img.width - W) // 2 + W, (img.height - H) // 2 + H))
# sfumatura scura in basso per il titolo
ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
h0 = int(H * (.55 if VERT else .5))
for y in range(h0, H): d.line([(0, y), (W, y)], fill=(8, 14, 24, int(235 * ((y - h0) / (H - h0)) ** 1.2)))
for y in range(0, int(H * .16)): d.line([(0, y), (W, y)], fill=(8, 14, 24, int(150 * (1 - y / (H * .16)))))
img = Image.alpha_composite(img.convert('RGBA'), ov); d = ImageDraw.Draw(img)
sc = W / 1600 if not VERT else 1.0
ARCH = trova('archivo'); SANS = trova('instrumentsans') + trova('inter'); SER = trova('instrumentserif', '400-normal')
# logo
fl = font(ARCH, int(34 * (1.25 if VERT else 1))); x0, y0 = int(84 * (1 if not VERT else .9)), int(58 if not VERT else 90)
d.rounded_rectangle([x0, y0, x0 + 46, y0 + 46], 10, fill=CARTA); d.line([(x0 + 10, y0 + 32), (x0 + 20, y0 + 20), (x0 + 27, y0 + 26), (x0 + 37, y0 + 13)], fill=(201, 138, 18), width=4)
d.text((x0 + 62, y0 + 23), 'Riskly', font=fl, fill=CARTA, anchor='lm'); wl = d.textlength('Riskly ', font=fl)
d.text((x0 + 62 + wl, y0 + 23), 'NEWS', font=font(ARCH, int(26 * (1.25 if VERT else 1))), fill=ORO, anchor='lm')
# numero chiave
if NUM:
    fn = font(ARCH, int(64 if not VERT else 84)); tw = d.textlength(NUM, font=fn); px, py = 34, 18
    bx1 = W - x0; bx0 = bx1 - tw - 2 * px; by0 = y0 + 4; by1 = by0 + (64 if not VERT else 84) + 2 * py
    d.rounded_rectangle([bx0, by0, bx1, by1], 16, fill=(10, 14, 20, 225), outline=ORO, width=2)
    d.text(((bx0 + bx1) / 2, (by0 + by1) / 2), NUM, font=fn, fill=CARTA, anchor='mm')
# titolo (a capo automatico) e categoria
ft = font([os.path.join(QUI, 'font', 'InstrumentSerif-400-normal-latin.ttf')], int(70 if not VERT else 96)); maxw = W - 2 * x0; righe = []; r = ''
for p in TIT.split():
    t = (r + ' ' + p).strip()
    if d.textlength(t, font=ft) <= maxw: r = t
    else: righe.append(r); r = p
righe.append(r); lh = int((66 if not VERT else 92) * 1.15)
yb = H - int(72 if not VERT else 260) - lh * len(righe)
fc = font(ARCH, int(28 if not VERT else 36)); cw = d.textlength(CAT.upper(), font=fc) + 44; chh = int(50 if not VERT else 62)
d.rounded_rectangle([x0, yb - chh - 24, x0 + cw, yb - 24], chh // 2, fill=COL)
d.text((x0 + cw / 2, yb - 24 - chh / 2), CAT.upper(), font=fc, fill=(12, 12, 12) if COL == ORO else CARTA, anchor='mm')
for i, rr in enumerate(righe): d.text((x0, yb + i * lh), rr, font=ft, fill=CARTA)
out = os.path.join(QUI, '..', 'social', 'reel', 'cover', ID + '.jpg') if VERT else os.path.join(QUI, '..', 'nuovo', 'news', 'copertine', ID + '.jpg')
img.convert('RGB').save(out, quality=88)
# registro dei crediti (0,75 a immagine)
reg = os.path.join(QUI, 'higgsfield_registro.json'); R = json.load(open(reg)) if os.path.exists(reg) else []
if not any(x.get('src') == SRC for x in R): R.append({'data': dt.date.today().isoformat(), 'id': ID, 'src': SRC, 'crediti': 0.75})
json.dump(R, open(reg, 'w'), ensure_ascii=False, indent=0)
mese = dt.date.today().strftime('%Y-%m'); usati = sum(x['crediti'] for x in R if x['data'].startswith(mese))
print(out); print(f'crediti Higgsfield usati questo mese: {usati:.2f} / 100')
