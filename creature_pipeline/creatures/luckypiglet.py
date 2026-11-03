"""LUCKY PIGLET (Common, Rice Paddy Village): round pink piglet on short stubby legs, big head, floppy ears,
red lucky bib with a gold coin, curly tail. Cute: plain flat black eyes."""
from kit import *

PINK, PINK2, BELLY, SNOUT, RED, GOLD, HOOF = C(255, 176, 186), C(240, 140, 158), C(255, 205, 212), C(255, 158, 172), C(214, 32, 40), C(255, 200, 60), C(140, 85, 92)


def build():
    c = Creature("LuckyPiglet", height=6)
    k = cute_quad(c, PINK, belly=BELLY, paw=HOOF, body=(1.5, 1.25, 1.8), leg_h=1.2, leg_r=0.45, head_r=1.3, head_up=0.5, tail=2)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r * 1.05, r * 0.95, r * 0.95), PINK, "Head", seg=(24, 16))
    # snout: short flat disc on the front of the face
    c.tube([h + P(0, -0.15, -r * 0.8), h + P(0, -0.2, -r * 1.12)], [0.55, 0.52], SNOUT, ["Head"], seg=18, sub=1)
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.2, -0.2, -r * 1.2), (0.09, 0.15, 0.04), C(150, 70, 85), "Head", stud=False, smooth=True)
        c.eye(h + P(s * 0.5, 0.3, -r * 0.82), 0.24, P(s * 0.45, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.85, -0.25, -r * 0.62), (0.24, 0.14, 0.1), C(255, 130, 150), "Head", stud=False)
        # floppy ears: start on top of the head, fold forward over the brow
        e0 = h + P(s * 0.55, r * 0.82, -0.3)
        c.leaf(e0, P(s * 0.75, -0.55, -0.55), P(0, 0, 1), 1.05, 0.85, PINK2, "Head", thick=0.22, shape="blade", curl=-0.25)
    # red lucky bib + gold coin, sitting on the chest under the chin
    bib = P(0, k["by"] + 0.15, -k["rz"] * 0.88)
    c.ellipsoid(bib, (1.0, 0.75, 0.3), RED, "Chest", seg=(16, 10))
    coin = bib + P(0, -0.1, -0.3)
    c.torus(coin, 0.3, 0.08, GOLD, "Chest", rot=euler(90, 0, 0), seg=(16, 6))
    c.box(coin, (0.1, 0.1, 0.07), GOLD, "Chest", stud=False)
    # curly tail
    t = P(0, k["by"] + 0.3, k["rz"] * 0.95)
    pts = [t, t + P(0.3, 0.3, 0.25), t + P(0.0, 0.55, 0.15), t + P(-0.2, 0.35, 0.0), t + P(0.05, 0.25, -0.05)]
    c.tube(pts, [0.15, 0.14, 0.12, 0.1, 0.07], PINK2, ["Tail1", "Tail2"], seg=8)
    aura(c, "sparkle", (255, 200, 60), (255, 120, 120), "Common")
    c.extra["speed"] = 1.0
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (0, 0, 18 * sin(4 * p)), "Head": (4 * sin(2 * p), 0, 6 * sin(p))}
    quad_anims(c, tail=2, stride=26, bob=0.12, extra=extra)


# palette-swapped texture (same mesh + UVs): Jade piglet with a gold bib
VARIANTS = {"Jade": {PINK: C(120, 205, 160), PINK2: C(80, 170, 125), BELLY: C(185, 235, 205), SNOUT: C(150, 220, 180),
                     HOOF: C(50, 105, 80), RED: C(255, 200, 60), GOLD: C(214, 32, 40)}}
