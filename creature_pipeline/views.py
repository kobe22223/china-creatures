"""3-view sheet per creature: python3 views.py <id> [<id> ...] -> out/sheets/<id>_views.png
(front 30, back 150, walk frame) with the measured proportions written under the title."""
import sys, os, glob, json
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "out", "sheets"), exist_ok=True)
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
except OSError:
    FONT = ImageFont.load_default()
for cid in sys.argv[1:]:
    d = os.path.join(HERE, "out", cid)
    ims = []
    for suf in ("_30.png", "_150.png", "_walk.png"):
        f = glob.glob(os.path.join(d, "*" + suf))
        ims.append(Image.open(f[0]).resize((600, 600)) if f else Image.new("RGB", (600, 600), "grey"))
    S = Image.new("RGB", (1800, 660), "white")
    for i, im in enumerate(ims):
        S.paste(im, (i * 600, 60))
    pj = os.path.join(d, "proportions.json")
    txt = cid
    if os.path.exists(pj):
        p = json.load(open(pj))
        txt += "   height %.1f   legs %d%%   head %d%%" % (p["height"], round(p["legs"] * 100), round(p["head"] * 100))
    ImageDraw.Draw(S).text((14, 14), txt + "      front / back / walk", fill=(0, 0, 0), font=FONT)
    S.save(os.path.join(HERE, "out", "sheets", cid + "_views.png"))
    print("SHEET", cid)
