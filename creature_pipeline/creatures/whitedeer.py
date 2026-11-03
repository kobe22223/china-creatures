"""WHITE DEER (Divine, Kunlun Immortal Peaks): a round snow-white immortal deer fawn on short stubby legs, cream
spots, a big head with a pale pink nose, soft ears, small branched gold antlers glowing at the tips, a red lucky
knot on a jade collar and a little white tail. Cute: flat black eyes."""
from cn import *

WHITE, WHITE2, CREAM, PINK, ANTLER, GLOWT, HOOFC = (C(250, 250, 248), C(225, 228, 235), C(240, 225, 190), C(255, 185, 190),
                                                   C(255, 205, 80), C(255, 240, 150), C(170, 160, 150))


def build():
    c = Creature("WhiteDeer", height=6.5)
    sp = spots(CREAM, size=0.45, density=0.22, seed=12, only=lambda X, Y, Z: Y > 2.0)
    k = cute_quad(c, WHITE, belly=WHITE2, paw=HOOFC, body=(1.4, 1.15, 1.75), leg_h=1.2, leg_r=0.4, head_r=1.22, head_up=0.65, tail=1, paint=sp)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r * 0.95, r), WHITE, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.35, -r * 0.72), (0.55, 0.42, 0.5), WHITE2, "Head", seg=(16, 10))
    c.ellipsoid(h + P(0, -0.25, -r * 1.12), (0.17, 0.12, 0.1), PINK, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.eye(h + P(s * 0.48, 0.22, -r * 0.84), 0.23, P(s * 0.45, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.78, -0.25, -r * 0.55), (0.18, 0.11, 0.08), PINK, "Head", stud=False)
        e0 = h + P(s * 0.75, r * 0.5, 0.1)
        c.leaf(e0, P(s * 0.6, 0.75, 0.4), P(0, 0, 1), 0.72, 0.5, WHITE, "Head", thick=0.18, shape="blade")
        c.leaf(e0 + P(0, 0.02, -0.08), P(s * 0.6, 0.75, 0.4), P(0, 0, 1), 0.55, 0.3, PINK, "Head", thick=0.1, shape="blade")
        # small branched gold antlers with glowing tips
        a0 = h + P(s * 0.35, r * 0.85, 0.05)
        m = a0 + P(s * 0.2, 0.55, 0.15)
        t1, t2, t3 = m + P(s * 0.25, 0.45, 0.2), m + P(s * 0.05, 0.5, -0.25), a0 + P(s * 0.35, 0.3, 0.3)
        c.tube([a0, m], [0.1, 0.08], ANTLER, ["Head"], seg=8, sub=1)
        for t_ in (t1, t2):
            c.tube([m, t_], [0.07, 0.04], ANTLER, ["Head"], seg=6, sub=1)
            c.ellipsoid(t_, (0.08, 0.08, 0.08), GLOWT, "Head", seg=(8, 5), glow=True)
        c.tube([a0.lerp(m, 0.4), t3], [0.06, 0.03], ANTLER, ["Head"], seg=6, sub=1)
    # jade collar + red lucky knot
    bib = P(0, k["by"] - 0.2, -k["rz"] * 0.97)
    c.ellipsoid(bib, (1.0, 0.3, 0.32), JADE, "Chest", seg=(16, 8))
    lucky_knot(c, bib + P(0, -0.1, -0.35), 0.24, "Chest")
    c.ellipsoid(P(0, k["by"] + 0.35, k["rz"] * 0.97), (0.25, 0.38, 0.2), WHITE, "Tail1", rot=euler(-30, 0, 0), seg=(10, 8))
    aura(c, "sparkle", (255, 240, 150), (230, 240, 255), "Divine")
    c.extra["speed"] = 1.25
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (20 * sin(4 * p), 0, 0), "Head": (4 * sin(2 * p), 0, 7 * sin(p))}
    quad_anims(c, tail=1, stride=28, bob=0.14, extra=extra)


VARIANTS = {"Spirit": {WHITE: C(170, 220, 255), WHITE2: C(140, 190, 240), CREAM: C(240, 250, 255), ANTLER: C(200, 240, 255), JADE: C(255, 200, 60)}}
