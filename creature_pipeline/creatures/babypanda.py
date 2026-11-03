"""BABY PANDA (Legendary, Bamboo Grove): round baby giant panda on short black stubby legs, big white head with
grey eye patches, round black ears, a black shoulder band, a red bib with a gold lucky coin and a little bamboo
shoot in one paw-hand. Cute: flat black eyes."""
from cn import *

WHITE, BLACK, PATCH, NOSE, PINK, SHOOT, SHOOT2 = (C(248, 248, 244), C(40, 40, 46), C(118, 118, 134), C(30, 30, 34),
                                                  C(255, 175, 180), C(150, 205, 90), C(95, 165, 70))


def build():
    c = Creature("BabyPanda", height=6)
    body, leg_h = (1.55, 1.3, 1.8), 1.15
    by = leg_h + body[1] * 0.75
    paint = panda_paint(BLACK, by - body[1] * 0.38, -body[2] * 0.55, band=0.55, band_lo=by - body[1] * 0.2)
    k = cute_quad(c, WHITE, belly=WHITE, paw=BLACK, body=body, leg_h=leg_h, leg_r=0.48, head_r=1.38, head_up=0.5, tail=1, paint=paint)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r * 1.08, r * 0.95, r * 0.98), WHITE, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.38, -r * 0.78), (0.6, 0.42, 0.42), WHITE, "Head", seg=(16, 10))
    c.ellipsoid(h + P(0, -0.2, -r * 1.1), (0.2, 0.13, 0.1), NOSE, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        # eye patch: a tilted grey oval, eye sits on it
        c.ellipsoid(h + P(s * 0.5, 0.18, -r * 0.82), (0.36, 0.46, 0.2), PATCH, "Head", rot=euler(0, 0, s * -25), seg=(14, 8), stud=False)
        c.eye(h + P(s * 0.5, 0.22, -r * 0.86), 0.25, P(s * 0.45, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.85, -0.25, -r * 0.62), (0.2, 0.12, 0.08), PINK, "Head", stud=False)
        # round black ears
        c.ellipsoid(h + P(s * 0.88, r * 0.72, 0.05), (0.42, 0.4, 0.22), BLACK, "Head", seg=(14, 10))
    # red bib with a gold coin
    bib = P(0, k["by"] - 0.2, -k["rz"] * 0.97)
    c.ellipsoid(bib, (1.1, 0.6, 0.36), RED, "Chest", seg=(16, 10))
    coin(c, bib + P(0, -0.25, -0.38), 0.3, "Chest", facing=(0, 0.1, -1))
    # tiny bamboo shoot held against the chest by the right foreleg
    sp = P(0.85, k["by"] - 0.35, -k["rz"] * 0.9)
    c.tube([sp, sp + P(0.05, 1.0, -0.1)], [0.14, 0.12], SHOOT, ["ForeR"], seg=10, sub=1)
    c.torus(sp + P(0.02, 0.5, -0.05), 0.14, 0.04, SHOOT2, "ForeR", seg=(12, 4))
    c.leaf(sp + P(0.05, 1.0, -0.1), P(0.5, 1, -0.2), P(0, 0, 1), 0.5, 0.22, SHOOT2, "ForeR", thick=0.08, shape="blade")
    # tiny tail
    c.ellipsoid(P(0, k["by"] + 0.2, k["rz"] * 0.98), (0.3, 0.28, 0.2), WHITE, "Tail1", seg=(10, 8))
    aura(c, "sparkle", (255, 215, 80), (255, 255, 255), "Legendary")
    c.extra["speed"] = 1.0
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Head": (4 * sin(2 * p), 0, 8 * sin(p))}
    quad_anims(c, tail=1, stride=22, bob=0.14, extra=extra)


VARIANTS = {"Golden": {WHITE: C(255, 236, 190), BLACK: C(150, 95, 40), PATCH: C(175, 120, 60), RED: C(70, 180, 120)}}
