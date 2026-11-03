"""contact sheet: python3 sheet.py out.png id1 id2 ... (top row: out/<id>/<Name>_30.png, bottom row: variant)"""
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont
out, ids = sys.argv[1], sys.argv[2:]
try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except OSError:
    FONT = ImageFont.load_default()
cols = len(ids)
S = Image.new("RGB", (cols * 500, 1000), "white")
dr = ImageDraw.Draw(S)
for k, i in enumerate(ids):
    for row, pat in ((0, "*_30.png"), (1, "*_var_*.png")):
        f = sorted(glob.glob(f"out/{i}/{pat}"))
        if not f:
            continue
        S.paste(Image.open(f[0]).resize((500, 500)), (k * 500, row * 500))
        label = i if row == 0 else os.path.basename(f[0]).split("_var_")[1][:-4] + " variant"
        dr.text((k * 500 + 10, row * 500 + 10), label, fill=(0, 0, 0), font=FONT)
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
S.save(out)
print("CONTACT", out)
