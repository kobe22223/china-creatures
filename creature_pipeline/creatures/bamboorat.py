"""BAMBOO RAT (Uncommon, Bamboo Grove): round ginger-grey bamboo rat on short stubby legs, big head with tiny
round ears, chubby cheeks, two cute orange buck teeth, a bamboo-leaf sprig behind one ear, short pink tail.
Cute: flat black eyes."""
from cn import *

FUR, FUR2, BELLY, PINK, TOOTH, LEAF, LEAF2, STALK = (C(196, 150, 110), C(160, 118, 84), C(240, 214, 184), C(255, 170, 170),
                                                     C(255, 170, 60), C(110, 190, 80), C(70, 150, 60), C(150, 200, 90))


def build():
    c = Creature("BambooRat", height=5)
    k = cute_quad(c, FUR, belly=BELLY, paw=PINK, body=(1.5, 1.2, 1.75), leg_h=1.0, leg_r=0.42, head_r=1.25, head_up=0.4, tail=2)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r * 1.08, r * 0.92, r * 0.98), FUR, "Head", seg=(24, 16))
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.6, -0.35, -r * 0.62), (0.58, 0.5, 0.5), BELLY, "Head", seg=(16, 10))   # chubby cheeks
        c.eye(h + P(s * 0.5, 0.3, -r * 0.84), 0.22, P(s * 0.45, 0.05, -1), "Head")
        # tiny round ears, flat against the head
        c.ellipsoid(h + P(s * 0.85, r * 0.62, 0.15), (0.32, 0.3, 0.12), FUR2, "Head", rot=euler(0, s * 30, s * -20), seg=(12, 8))
        c.ellipsoid(h + P(s * 0.86, r * 0.62, 0.08), (0.2, 0.19, 0.06), PINK, "Head", rot=euler(0, s * 30, s * -20), seg=(10, 6), stud=False)
    c.ellipsoid(h + P(0, -0.05, -r * 1.02), (0.2, 0.14, 0.12), C(200, 110, 120), "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.box(h + P(s * 0.09, -0.48, -r * 0.94), (0.08, 0.15, 0.05), TOOTH, "Head", stud=False)
    # bamboo sprig tucked behind the right ear
    b = h + P(0.7, r * 0.6, 0.45)
    c.tube([b, b + P(0.25, 0.2, 0.3)], [0.08, 0.07], STALK, ["Head"], seg=8, sub=1)
    for j, d in enumerate((P(0.8, 0.25, 0.6), P(0.3, 0.45, 1.0), P(1.0, -0.1, 0.5))):
        c.leaf(b + P(0.25, 0.2, 0.3), d, P(0, 1, 0), 0.62, 0.28, LEAF if j != 1 else LEAF2, "Head", thick=0.08, shape="blade", curl=-0.1)
    # short pink tail
    t = P(0, k["by"] - 0.1, k["rz"] * 0.95)
    c.tube([t, t + P(0, -0.4, 0.35), t + P(0.15, -0.85, 0.45)], [0.15, 0.11, 0.06], PINK, ["Tail1", "Tail2"], seg=8)
    aura(c, "sparkle", (150, 220, 110), (255, 220, 150), "Uncommon")
    c.extra["speed"] = 1.05
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Head": (5 * sin(4 * p) if not walking else 3 * sin(2 * p), 0, 5 * sin(p))}   # sniffing nod
    quad_anims(c, tail=2, stride=28, bob=0.12, extra=extra)


VARIANTS = {"Snow": {FUR: C(238, 236, 232), FUR2: C(200, 196, 190), BELLY: C(255, 250, 244), LEAF: C(255, 200, 60), LEAF2: C(214, 32, 40)}}
