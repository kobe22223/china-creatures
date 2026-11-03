"""WHITE TIGER (Titanic, Heavenly Court): Baihu, guardian of the west. A round white tiger cub on short stubby legs
with bold charcoal stripes and gold cloud swirls, a big head with the "king" stripe mark on its forehead, white
cheek ruffs, round ears, glowing ice-blue eyes, a gold armour collar and a striped tail. Royal: glowing eyes."""
from cn import *
from detail import V as GV, eyes_pair, fur

WHITE, STRIPE, CREAM, PINK, GOLDW, EYE = C(248, 248, 252), C(50, 52, 62), C(255, 250, 240), C(255, 175, 185), C(255, 205, 70), C(120, 220, 255)


def build():
    c = Creature("WhiteTiger", height=6.5)
    tig = stripes(STRIPE, "z", period=0.75, width=0.18, wobble=0.35)
    k = cute_quad(c, WHITE, belly=CREAM, paw=CREAM, body=(1.5, 1.22, 1.8), leg_h=1.1, leg_r=0.46, head_r=1.32, head_up=0.55, tail=3, paint=tig)
    h, r = k["head"], k["head_r"]
    hg = GV(-h.x, h.z, h.y)
    c.ellipsoid(h, (r * 1.08, r * 0.95, r), WHITE, "Head", seg=(24, 16), paint=stripes(STRIPE, "y", period=0.42, width=0.07, wobble=0.0, only=lambda X, Y, Z: np.abs(X) > 1.05))
    c.ellipsoid(h + P(0, -0.35, -r * 0.75), (0.65, 0.45, 0.45), CREAM, "Head", seg=(16, 10))
    c.ellipsoid(h + P(0, -0.15, -r * 1.1), (0.18, 0.13, 0.1), PINK, "Head", stud=False, smooth=True)
    # "king" mark on the forehead
    fh = h + P(0, 0.62, -r * 0.82)
    for j, w in enumerate((0.3, 0.22, 0.3)):
        c.box(fh + P(0, 0.2 - j * 0.18, 0.02 * j), (w, 0.04, 0.05), STRIPE, "Head", rot=euler(-25, 0, 0), stud=False)
    c.box(fh + P(0, 0.02, 0.02), (0.04, 0.22, 0.05), STRIPE, "Head", rot=euler(-25, 0, 0), stud=False)
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.85, r * 0.62, 0.05), (0.38, 0.36, 0.2), WHITE, "Head", seg=(12, 8))
        c.ellipsoid(h + P(s * 0.85, r * 0.62, -0.08), (0.24, 0.22, 0.08), PINK, "Head", seg=(10, 6), stud=False)
        c.spike(h + P(s * 0.95, -0.25, -0.35), h + P(s * 1.55, -0.45, -0.1), 0.35, CREAM, "Head", seg=6)
    eyes_pair(c, hg + GV(0, 0.2, -r * 0.84), 0.5, 0.26, "Head", glow=EYE, core=C(230, 250, 255), brow=STRIPE, slant=18, turn=0.5)
    # gold armour collar
    bib = P(0, k["by"] - 0.2, -k["rz"] * 0.97)
    c.ellipsoid(bib, (1.12, 0.45, 0.36), GOLDW, "Chest", seg=(16, 8), stud=False, paint=cloud_filigree(C(214, 150, 30), scale=2.5, width=0.08))
    c.ellipsoid(bib + P(0, -0.15, -0.38), (0.2, 0.2, 0.12), EYE, "Chest", seg=(10, 6), glow=True)
    t = P(0, k["by"] + 0.25, k["rz"] * 0.92)
    c.tube([t, t + P(0, 0.4, 0.5), t + P(0, 1.0, 0.65), t + P(0, 1.35, 0.4)], [0.25, 0.25, 0.22, 0.16], WHITE, ["Tail1", "Tail2", "Tail3"],
           seg=12, paint=stripes(STRIPE, "y", period=0.4, width=0.12, wobble=0))
    aura(c, "orbit", (120, 220, 255), (255, 255, 255), "Titanic")
    c.extra["speed"] = 1.3
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (0, 0, 14 * sin(2 * p)), "Tail2": (0, 0, 10 * sin(2 * p - 0.6)), "Head": (4 * sin(2 * p), 0, 6 * sin(p))}
    quad_anims(c, tail=3, stride=28, bob=0.12, extra=extra)


VARIANTS = {"Golden": {WHITE: C(255, 210, 110), CREAM: C(255, 240, 200), STRIPE: C(120, 60, 30), GOLDW: C(255, 255, 255)}}
