"""MANDARIN DUCK (Rare, Tea Terraces): round drake mandarin duck, chestnut-purple breast with white bars, a
cream-white eye stripe, orange cheek whiskers, a green and copper crest, small orange sail feathers folded on the
back, red bill. Cute: flat black eyes."""
from cn import *

PURP, CHEST, CREAM, ORANGE, GREEN, COPPER, BILL, SAIL, BACK, LEGC = (
    C(120, 70, 120), C(150, 70, 60), C(250, 240, 220), C(255, 140, 40), C(40, 120, 90), C(190, 100, 50),
    C(220, 40, 40), C(255, 150, 50), C(135, 98, 70), C(255, 160, 60))


def build():
    c = Creature("MandarinDuck", height=5)
    k = cute_bird(c, BACK, belly=CREAM, leg_col=LEGC, body=(1.2, 1.1, 1.4), leg_h=0.75, head_r=1.0,
                  head_up=1.05, head_fwd=0.52, wing_col=C(150, 120, 90), tail=1)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r * 0.95, r * 0.95), GREEN, "Head", seg=(24, 16))
    # cream eye stripe band wrapping back from the eyes + orange whisker cheeks
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.62, 0.42, -0.25), (0.3, 0.2, 0.7), CREAM, "Head", rot=euler(-12, 0, 0), seg=(14, 8))
        c.ellipsoid(h + P(s * 0.6, -0.36, -0.42), (0.4, 0.4, 0.5), ORANGE, "Head", seg=(14, 8))
        c.eye(h + P(s * 0.42, 0.18, -r * 0.84), 0.19, P(s * 0.5, 0.05, -1), "Head")
    c.ellipsoid(h + P(0, -0.2, -r * 0.98), (0.3, 0.14, 0.4), BILL, "Head", seg=(14, 8))
    # copper crest swept back
    for j in range(3):
        c.leaf(h + P((j - 1) * 0.2, r * 0.7, 0.2), P((j - 1) * 0.2, 0.25, 1), P(1, 0, 0), 0.9, 0.4, COPPER if j != 1 else GREEN, "Head", thick=0.14, shape="feather", curl=-0.2)
    # purple-chestnut breast with white bars
    bars = stripes(CREAM, "z", period=0.6, width=0.08, wobble=0.0, only=lambda X, Y, Z: (Z > -1.2) & (Z < -0.6))
    c.ellipsoid(P(0, k["by"] + 0.1, -k["rz"] * 0.45), (k["rx"] * 0.92, k["ry"] * 0.72, k["rz"] * 0.62), CHEST, ["Chest"], seg=(18, 12), paint=bars)
    # orange sail feathers folded flat on the back (small accents, angled back)
    for s, S in ((-1, "L"), (1, "R")):
        c.ellipsoid(P(s * 0.62, k["by"] + k["ry"] * 0.72, k["rz"] * 0.3), (0.13, 0.48, 0.45), SAIL, "Wing" + S, rot=euler(-20, 0, s * -12), seg=(12, 8))
    c.ellipsoid(P(0, k["by"] + 0.3, k["rz"] * 0.92), (0.35, 0.28, 0.45), BACK, "Tail1", rot=euler(-25, 0, 0), seg=(12, 8))
    aura(c, "sparkle", (255, 150, 60), (150, 100, 200), "Rare")
    c.extra["speed"] = 1.05
    return c


def anims(c):
    bird_anims(c, tail=1, stride=30, waddle=7, bob=0.1, flap=10)


VARIANTS = {"Hen": {BACK: C(140, 130, 120), GREEN: C(150, 140, 130), CHEST: C(170, 160, 150), ORANGE: C(190, 180, 170),
                    SAIL: C(160, 150, 140), COPPER: C(130, 120, 110), BILL: C(120, 110, 100)}}
