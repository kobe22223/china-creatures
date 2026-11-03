"""GOLDEN EAGLE (Epic, Great Wall): round chunky golden eagle, dark brown body, golden nape and crown, a big hooked
yellow beak, a proud brow, feathered "trouser" legs, yellow feet and a short fanned tail, red tassel charm at the
neck. Cute: flat black eyes."""
from cn import *

BROWN, BROWN2, GOLDN, CREAM, BEAK, BEAK2, LEGC = (C(110, 72, 45), C(80, 50, 32), C(225, 170, 70), C(235, 200, 140),
                                                  C(255, 200, 60), C(60, 50, 40), C(255, 200, 70))


def build():
    c = Creature("GoldenEagle", height=6)
    k = cute_bird(c, BROWN, belly=BROWN2, leg_col=LEGC, body=(1.3, 1.25, 1.45), leg_h=0.8, head_r=1.0,
                  head_up=1.05, head_fwd=0.5, wing_col=BROWN2, tail=1, foot="toes")
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r * 0.95, r * 0.95), GOLDN, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.3, -r * 0.25), (r * 0.92, r * 0.65, r * 0.75), BROWN, "Head", seg=(18, 10))   # darker cheeks/throat
    # golden nape feathers over the neck
    for i in range(7):
        a = math.radians(-90 + i * 30)
        c.leaf(h + P(math.sin(a) * r * 0.75, -r * 0.35, math.cos(a) * r * 0.7 + 0.1), P(math.sin(a) * 0.3, -1, math.cos(a) * 0.5),
               P(math.cos(a), 0, -math.sin(a)), 0.6, 0.45, GOLDN, ["Neck", "Chest"], thick=0.14, shape="feather")
    # big hooked beak
    b0 = h + P(0, -0.05, -r * 0.8)
    c.tube([b0, b0 + P(0, 0.02, -0.4), b0 + P(0, -0.2, -0.62), b0 + P(0, -0.42, -0.55)], [0.3, 0.24, 0.13, 0.04], BEAK, ["Head"], seg=10, flat=(0.8, 1.0))
    c.ellipsoid(b0 + P(0, 0.08, 0.05), (0.32, 0.2, 0.18), BEAK, "Head", seg=(10, 6))
    for s in (-1, 1):
        c.eye(h + P(s * 0.45, 0.2, -r * 0.8), 0.2, P(s * 0.5, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.45, 0.42, -r * 0.78), (0.3, 0.1, 0.14), BROWN2, "Head", rot=euler(0, 0, s * 15), stud=False)   # proud brow
    # feathered trousers
    for s, S in ((-1, "L"), (1, "R")):
        c.ellipsoid(P(s * k["lx"], 0.75, -0.05), (0.38, 0.4, 0.38), CREAM, "Shin" + S, seg=(12, 8))
    # short fanned tail
    t = P(0, k["by"] + 0.0, k["rz"] * 0.9)
    for j in range(5):
        a = (j - 2) * 0.25
        c.leaf(t, P(a, -0.6, 1), P(1, 0, 0), 0.8, 0.38, BROWN2 if j % 2 else BROWN, "Tail1", thick=0.12, shape="feather")
    lucky_knot(c, P(0, k["by"] + 0.55, -k["rz"] * 1.04), 0.26, "Chest")
    aura(c, "sparkle", (255, 190, 70), (180, 110, 60), "Epic")
    c.extra["speed"] = 1.2
    return c


def anims(c):
    bird_anims(c, tail=1, stride=26, waddle=5, bob=0.1, flap=14)


VARIANTS = {"Imperial": {BROWN: C(40, 40, 50), BROWN2: C(25, 25, 32), GOLDN: C(255, 215, 80), CREAM: C(255, 240, 200)}}
