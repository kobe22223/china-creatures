"""stack several 3-view sheets into one review image: python3 stack.py out.png id1 id2 ..."""
import sys
from PIL import Image
ids = sys.argv[2:]
S = Image.new("RGB", (1800, 660 * len(ids)), "white")
for k, i in enumerate(ids):
    S.paste(Image.open("out/sheets/%s_views.png" % i), (0, 660 * k))
S.resize((1200, 440 * len(ids))).save(sys.argv[1])
