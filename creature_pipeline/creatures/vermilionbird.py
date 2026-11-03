"""VERMILION BIRD (Omega, Heavenly Court): Zhuque, guardian of the south. A round flame-red firebird hovering on
big spread wings with orange and gold tips, a flame crest, a short gold beak, glowing gold eyes, a gold cloud swirl
on its chest and long glowing flame tail plumes. Hovers. Royal: glowing eyes."""
from cn import *
from detail import V as GV, eyes_pair

RED_, RED3, ORANGE, GOLDV, BEAK, FLAME1, FLAME2, EYE = (C(225, 40, 35), C(170, 25, 25), C(255, 130, 30), C(255, 200, 60),
                                                       C(255, 205, 80), C(255, 110, 30), C(255, 210, 70), C(255, 220, 80))


def build():
    c = Creature("VermilionBird", height=7)
    k = flying_bird(c, RED_, belly=ORANGE, leg_col=GOLDV, wing_col=RED_, tip_col=ORANGE, body=(1.15, 1.1, 1.35), head_r=0.95,
                    span=(1.0, 2.4, 4.0), n_feathers=10, feather_len=(1.4, 1.1), cover=RED3, tail=2)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r, r * 0.95), RED_, "Head", seg=(24, 16))
    c.ellipsoid(P(0, k["by"] + 0.1, -k["rz"] * 0.85), (0.75, 0.6, 0.3), GOLDV, "Chest", seg=(14, 8), paint=cloud_filigree(RED3, scale=3, width=0.08))
    c.tube([h + P(0, -0.08, -r * 0.82), h + P(0, -0.2, -r * 1.25)], [0.22, 0.04], BEAK, ["Head"], seg=10, sub=1)
    hg = GV(-h.x, h.z, h.y)
    eyes_pair(c, hg + GV(0, 0.15, -r * 0.82), 0.4, 0.2, "Head", glow=EYE, core=C(255, 250, 220), brow=RED3, slant=16, turn=0.5)
    for j in range(5):
        c.leaf(h + P((j - 2) * 0.15, r * 0.8, 0.0), P((j - 2) * 0.25, 1, 0.6), P(1, 0, 0), 0.9 - 0.1 * abs(j - 2), 0.35, FLAME1 if j % 2 else FLAME2, "Head", thick=0.1, shape="flame", glow=True)
    t0 = P(0, k["by"] + 0.1, k["rz"] * 0.85)
    for j in range(5):
        a = (j - 2) * 0.35
        pts = [t0, t0 + P(a * 0.6, -0.3, 0.9), t0 + P(a, -0.9, 1.7), t0 + P(a * 1.2, -1.6, 2.1)]
        c.tube(pts, [0.2, 0.22, 0.16, 0.04], RED_ if j % 2 else ORANGE, ["Tail1", "Tail2"], seg=8, flat=(1.0, 0.45))
        c.leaf(pts[-1], P(a * 0.3, -0.6, 0.6), P(1, 0, 0), 0.6, 0.35, FLAME2, "Tail2", thick=0.08, shape="flame", glow=True)
    aura(c, "orbit", (255, 110, 40), (255, 220, 80), "Omega")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.35
    return c


def anims(c):
    flyer_anims(c, flap=30, tail=2)


VARIANTS = {"Bluefire": {RED_: C(40, 90, 210), RED3: C(25, 55, 150), ORANGE: C(120, 200, 255), GOLDV: C(220, 240, 255)}}
