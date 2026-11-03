"""PENG (Godly, Heavenly Court): the colossal storm bird that the Kun fish becomes. A round storm-blue bird with a
gold-scaled chest, huge spread wings with silver and gold edged feathers, a hooked gold beak, a swept crest, glowing
ice-blue eyes, gold talons tucked under and a wide fanned tail. Hovers. Royal: glowing eyes."""
from cn import *
from detail import V as GV, eyes_pair

STORM, STORM2, SILVER, GOLDP, BEAK, GLOWC, EYE = (C(40, 60, 120), C(25, 38, 85), C(200, 215, 240), C(255, 200, 60),
                                                 C(255, 205, 70), C(150, 230, 255), C(150, 230, 255))


def build():
    c = Creature("Peng", height=8)
    k = flying_bird(c, STORM, belly=GOLDP, leg_col=GOLDP, wing_col=STORM, tip_col=SILVER, body=(1.3, 1.25, 1.5), head_r=1.0,
                    span=(1.1, 3.0, 5.2), n_feathers=12, feather_len=(1.8, 1.4), cover=STORM2, tail=2)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(P(0, k["by"] - 0.1, -k["rz"] * 0.45), (1.0, 0.95, 0.85), GOLDP, ["Chest"], seg=(16, 10), paint=scale_paint(C(214, 150, 30), size=0.35, width=0.08))
    c.ellipsoid(h, (r, r, r * 0.95), STORM, "Head", seg=(24, 16))
    b0 = h + P(0, -0.05, -r * 0.8)
    c.tube([b0, b0 + P(0, 0.02, -0.45), b0 + P(0, -0.22, -0.7), b0 + P(0, -0.45, -0.6)], [0.32, 0.25, 0.13, 0.04], BEAK, ["Head"], seg=10, flat=(0.8, 1.0))
    hg = GV(-h.x, h.z, h.y)
    eyes_pair(c, hg + GV(0, 0.2, -r * 0.8), 0.42, 0.21, "Head", glow=EYE, core=C(230, 250, 255), brow=STORM2, slant=22, turn=0.5)
    for j in range(4):
        c.leaf(h + P((j - 1.5) * 0.18, r * 0.75, 0.2), P((j - 1.5) * 0.2, 0.5, 1), P(1, 0, 0), 1.1, 0.35, SILVER if j % 2 else STORM2, "Head", thick=0.12, shape="feather", curl=-0.15)
    t0 = P(0, k["by"] + 0.05, k["rz"] * 0.85)
    for j in range(7):
        a = (j - 3) * 0.28
        c.leaf(t0, P(a, -0.2, 1), P(1, 0, 0), 1.6, 0.55, STORM2 if j % 2 else STORM, "Tail2" if abs(j - 3) > 1 else "Tail1", thick=0.12, shape="feather")
    aura(c, "orbit", (150, 230, 255), (255, 200, 60), "Godly")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.45
    return c


def anims(c):
    flyer_anims(c, flap=26, tail=2)


VARIANTS = {"Dawn": {STORM: C(240, 150, 60), STORM2: C(200, 90, 40), SILVER: C(255, 240, 200), GLOWC: C(255, 120, 80)}}
