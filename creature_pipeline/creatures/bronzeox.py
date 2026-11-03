"""BRONZE OX (Eternal, Terracotta Tomb): a round little ox cast in ancient bronze. Green-teal patina body with
gold cloud swirl relief, polished gold horns, hooves and muzzle, a jade nose ring and a jade disc pendant on a red
cord. Cute: flat black eyes."""
from cn import *

PATINA, PATINA2, BRONZE, GOLDB, JADEC, NOSE = C(70, 150, 135), C(45, 110, 100), C(185, 130, 60), C(240, 190, 80), C(120, 220, 160), C(35, 70, 65)


def build():
    c = Creature("BronzeOx", height=6.5)
    relief = cloud_filigree(GOLDB, scale=1.5, width=0.07)
    k = cute_quad(c, PATINA, belly=PATINA2, paw=GOLDB, body=(1.6, 1.28, 1.85), leg_h=1.15, leg_r=0.5, head_r=1.3, head_up=0.45, tail=2, paint=relief)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r * 1.08, r * 0.95, r * 0.95), PATINA, "Head", seg=(24, 16), paint=relief)
    c.ellipsoid(h + P(0, -0.4, -r * 0.72), (0.85, 0.58, 0.5), GOLDB, "Head", seg=(20, 12))
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.3, -0.3, -r * 1.12), (0.1, 0.13, 0.05), NOSE, "Head", stud=False, smooth=True)
        c.eye(h + P(s * 0.55, 0.22, -r * 0.8), 0.24, P(s * 0.5, 0.05, -1), "Head")
        b0 = h + P(s * 0.6, r * 0.72, -0.05)
        c.tube([b0, b0 + P(s * 0.5, 0.15, 0.0), b0 + P(s * 0.75, 0.55, -0.1)], [0.22, 0.17, 0.06], GOLDB, ["Head"], seg=10)
        c.leaf(h + P(s * r * 0.9, 0.2, 0.1), P(s * 1, -0.45, 0.2), P(0, 0, 1), 0.6, 0.38, PATINA2, "Head", thick=0.16, shape="blade")
    c.torus(h + P(0, -0.55, -r * 1.15), 0.24, 0.06, JADEC, "Head", rot=euler(0, 0, 90), seg=(14, 5), stud=False)
    # jade bi disc pendant under the chin
    bib = P(0, k["by"] - 0.3, -k["rz"] * 0.98)
    c.ellipsoid(bib, (1.1, 0.42, 0.32), RED, "Chest", seg=(16, 8))
    c.torus(bib + P(0, -0.35, -0.38), 0.28, 0.12, JADEC, "Chest", rot=euler(90, 0, 0), seg=(16, 6), stud=False)
    t = P(0, k["by"] + 0.2, k["rz"] * 0.95)
    c.tube([t, t + P(0, -0.35, 0.3), t + P(0, -0.85, 0.4)], [0.11, 0.09, 0.07], PATINA2, ["Tail1", "Tail2"], seg=8)
    c.ellipsoid(t + P(0, -1.0, 0.4), (0.18, 0.25, 0.18), GOLDB, "Tail2", seg=(10, 8))
    aura(c, "sparkle", (120, 220, 190), (240, 190, 80), "Eternal")
    c.extra["speed"] = 0.95
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (0, 0, 16 * sin(3 * p)), "Head": (4 * sin(2 * p), 0, 6 * sin(p))}
    quad_anims(c, tail=2, stride=22, bob=0.1, extra=extra)


VARIANTS = {"Polished": {PATINA: C(205, 140, 60), PATINA2: C(160, 100, 40), GOLDB: C(255, 225, 140)}}
