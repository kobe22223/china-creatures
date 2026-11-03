"""STORM PTERODACTYL (Omega, Prehistoric): hovering storm-grey pterosaur with violet membrane wings edged in
glowing electric-yellow, a long swept-back crest, toothy beak, clawed feet tucked under it."""
from dino import *

GREY, GREY2, BELLY, SKIN, SKIN2, CREST, BONE, BOLT = C(96, 104, 128), C(56, 60, 80), C(225, 225, 235), C(120, 70, 190), C(80, 40, 140), C(255, 200, 40), C(235, 230, 215), C(255, 240, 80)


def build():
    c = detailed("StormPterodactyl", height=6)
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    body0, body1 = V(0, 4.2, 0.9), V(0, 4.6, -0.9)
    c.bone("Hips", B(body0), B((body0 + body1) / 2), "Root")
    c.bone("Chest", B((body0 + body1) / 2), B(body1), "Hips")
    nb = body1 + V(0, 0.2, -0.1)
    hb = nb + V(0, 1.1, -0.6)
    c.bone("Neck", B(nb), B(hb), "Chest")
    c.bone("Head", B(hb), B(hb + V(0, 0, -2.0)), "Neck")
    c.bone("Jaw", B(hb + V(0, -0.3, -0.2)), B(hb + V(0, -0.45, -2.2)), "Head")
    wing_bones(c, (0.6, 4.7, -0.6), (3.2, 5.6, -0.2), (6.6, 5.2, 0.6))
    for s, X in ((-1, "L"), (1, "R")):
        c.bone("Thigh" + X, B(V(s * 0.45, 4.1, 0.7)), B(V(s * 0.55, 3.2, 1.0)), "Hips")
        c.bone("Shin" + X, B(V(s * 0.55, 3.2, 1.0)), B(V(s * 0.55, 2.5, 1.4)), "Thigh" + X)
    c.bone("Tail1", B(body0 + V(0, 0, 0.3)), B(body0 + V(0, -0.2, 1.4)), "Hips")
    # body
    T(c, [body0 + V(0, -0.05, 0.6), body0, body1, body1 + V(0, 0.15, -0.35)], [0.45, 0.78, 0.82, 0.55], GREY, ["Hips", "Chest"], seg=8, paint=stripes(GREY2, "z", period=0.45, width=0.1, wobble=0.3))
    E(c, (body0 + body1) / 2 + V(0, -0.35, 0), (0.62, 0.45, 1.05), BELLY, ["Hips", "Chest"], seg=(8, 6))
    fur_line(c, [body1 + V(0, 0.55, 0.2), nb + V(0, 0.45, 0.0)], GREY2, "Chest", length=0.55, width=0.3, out=V(0, 1, 0.6), n_per=3, seed=3)
    T(c, [body1 + V(0, 0.1, 0.1), nb, hb + V(0, -0.1, 0.15)], [0.55, 0.45, 0.4], GREY, ["Chest", "Neck"], seg=7)
    # head: long beak + big swept crest
    T(c, [hb + V(0, 0.05, 0.35), hb + V(0, 0.1, -0.35), hb + V(0, -0.05, -1.3), hb + V(0, -0.2, -2.3)], [0.5, 0.5, 0.3, 0.08], GREY, "Head", seg=6, sub=1, flat=(0.8, 1.0))
    T(c, [hb + V(0, -0.35, -0.15), hb + V(0, -0.45, -1.2), hb + V(0, -0.5, -2.1)], [0.32, 0.2, 0.06], GREY2, "Jaw", seg=6, sub=1, flat=(0.85, 0.6))
    maw(c, hb + V(0, -0.28, -1.5), 0.17, 0.8, 0.22, "Head", "Jaw", n=7, tooth=0.1, fangs=1.2, tongue=False, inner=False)
    crest = [hb + V(0, 0.35, -0.6), hb + V(0, 0.75, 0.1), hb + V(0, 1.2, 1.4), hb + V(0, 0.95, 1.7), hb + V(0, 0.35, 0.45)]
    SHEET(c, crest, CREST, "Head", thick=0.16, stud=False)
    T(c, [crest[1], crest[2]], [0.06, 0.04], BOLT, "Head", seg=4, glow=True)
    eyes_pair(c, hb + V(0, 0.25, -0.35), 0.4, 0.2, "Head", glow=BOLT, core=C(255, 255, 220), brow=GREY2, slant=22, turn=0.9)
    # wings
    bat_wings(c, (0.6, 4.7, -0.6), (3.2, 5.6, -0.2), (6.6, 5.2, 0.6), GREY, SKIN, edge_col=BOLT, fingers=3, glow_edge=True)
    for s, X in ((-1, "L"), (1, "R")):
        m, t = V(s * 3.2, 5.6, -0.2), V(s * 6.6, 5.2, 0.6)
        T(c, [m.lerp(t, 0.1) + V(0, 0.08, 0), t + V(0, 0.05, 0)], [0.07, 0.05], BOLT, "WingTip" + X, seg=4, glow=True)
    # legs tucked + clawed feet
    for s, X in ((-1, "L"), (1, "R")):
        a, b, f = V(s * 0.45, 4.1, 0.7), V(s * 0.55, 3.2, 1.0), V(s * 0.55, 2.5, 1.4)
        T(c, [a, b], [0.28, 0.18], GREY, "Thigh" + X, seg=6)
        T(c, [b, f], [0.18, 0.12], GREY2, "Shin" + X, seg=6)
        for j in (-1, 0, 1):
            S(c, f, f + V(j * 0.2, -0.4, -0.25), 0.08, BONE, "Shin" + X, bend=V(0, 0.1, 0), seg=4, n=3, stud=False)
    T(c, [body0 + V(0, 0, 0.3), body0 + V(0, -0.2, 1.4)], [0.2, 0.05], GREY, "Tail1", seg=5)
    SHEET(c, [body0 + V(0, -0.2, 1.2), body0 + V(0.35, -0.2, 1.6), body0 + V(0, -0.2, 1.95), body0 + V(-0.35, -0.2, 1.6)], SKIN, "Tail1", thick=0.1, stud=False)
    aura(c, "sparkle", (255, 240, 80), (120, 70, 190), "Omega")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.2
    return c


def anims(c):
    def mk(rate, flap):
        def fn(t):
            p = tau * t * rate
            return {
                "Root": ((6 * sin(p - 1.2), 0, 0), (0, 0.45 * sin(p - 1.2), 0)),
                "Chest": (3 * sin(p), 0, 0),
                "Neck": (-4 * sin(p + 0.8), 6 * sin(t * tau) if rate < 2 else 0, 0),
                "Head": (5 * sin(p + 1.4), 0, 0),
                "Jaw": (-4 - 6 * max(0, sin(t * tau * 2)), 0, 0),
                "WingL": (0, 0, flap * sin(p)), "WingR": (0, 0, -flap * sin(p)),
                "WingTipL": (0, 0, flap * 0.6 * sin(p - 0.7)), "WingTipR": (0, 0, -flap * 0.6 * sin(p - 0.7)),
                "ThighL": (-12 + 4 * sin(p), 0, 0), "ThighR": (-12 + 4 * sin(p), 0, 0),
                "ShinL": (18, 0, 0), "ShinR": (18, 0, 0),
                "Tail1": (6 * sin(p - 1.5), 0, 0),
            }
        return fn
    c.animate({"Walk": (24, 1.0, mk(2, 32)), "Idle": (40, 4.0, mk(3, 26))})

