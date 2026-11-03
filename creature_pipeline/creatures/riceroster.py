"""RICE ROOSTER (Rare, Rice Paddy Village): chubby zodiac rooster, warm chestnut body with a golden neck ruff,
big red comb and wattles, short yellow beak, a compact arc of glossy green-black and gold sickle tail feathers.
Cute: flat black eyes."""
from cn import *

BODY, BODY2, RUFF, CREAM, COMB, BEAK, TAIL, TAIL2, LEGC = (C(205, 92, 40), C(160, 62, 30), C(255, 180, 50), C(255, 226, 170),
                                                          C(225, 30, 40), C(255, 195, 50), C(30, 80, 70), C(255, 190, 50), C(255, 190, 70))


def build():
    c = Creature("RiceRooster", height=5.5)
    k = cute_bird(c, BODY, belly=CREAM, leg_col=LEGC, body=(1.2, 1.18, 1.35), leg_h=0.85, head_r=0.98,
                  head_up=1.1, head_fwd=0.55, wing_col=BODY2, tail=2, foot="toes")
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r, r * 0.95), BODY, "Head", seg=(24, 16))
    # golden neck ruff: a solid collar of gold with short feathers lying flat over the shoulders
    c.ellipsoid(h + P(0, -r * 0.62, 0.08), (r * 0.92, r * 0.5, r * 0.88), RUFF, ["Neck"], seg=(18, 10))
    for i in range(11):
        a = math.radians(-150 + i * 30)
        base = h + P(math.sin(a) * r * 0.72, -r * 0.62, math.cos(a) * r * 0.68 + 0.08)
        c.leaf(base, P(math.sin(a) * 0.35, -1, math.cos(a) * 0.35), P(math.cos(a), 0, -math.sin(a)), 0.6, 0.5,
               RUFF, ["Neck", "Chest"], thick=0.14, shape="feather")
    # beak: short cone + red wattles under it
    c.tube([h + P(0, -0.05, -r * 0.82), h + P(0, -0.12, -r * 1.25)], [0.26, 0.04], BEAK, ["Head"], seg=10, sub=1, flat=(1.0, 0.8))
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.13, -0.5, -r * 0.82), (0.14, 0.24, 0.12), COMB, "Head", seg=(10, 8))
        c.eye(h + P(s * 0.45, 0.2, -r * 0.8), 0.19, P(s * 0.5, 0.05, -1), "Head")
    # comb: five round lobes in an arc along the top of the head
    for j in range(5):
        t = j / 4
        p = h + P(0, r * 0.9 + 0.12 * math.sin(math.pi * t), -r * 0.55 + t * r * 1.05)
        c.ellipsoid(p, (0.12, 0.3 - 0.08 * abs(t - 0.4), 0.2), COMB, "Head", seg=(10, 8))
    # sickle tail: a compact fan of curved feathers arcing up and back over the rump
    t0 = P(0, k["by"] + 0.35, k["rz"] * 0.75)
    for j in range(5):
        side = (j - 2) * 0.16
        up = 1.25 - 0.12 * abs(j - 2)
        pts = [t0 + P(side * 0.5, 0, 0), t0 + P(side, up * 0.7, 0.35), t0 + P(side * 1.2, up, 0.85), t0 + P(side * 1.2, up * 0.75, 1.25)]
        c.tube(pts, [0.24, 0.24, 0.18, 0.05], TAIL if j % 2 == 0 else TAIL2, ["Tail1", "Tail2"], seg=8, flat=(0.4, 1.0))
    aura(c, "sparkle", (255, 120, 60), (255, 210, 80), "Rare")
    c.extra["speed"] = 1.05
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        if walking:   # proud strut: the head pecks forward and back
            return {"Neck": (-10 * sin(2 * p), 0, 0), "Head": (6 * sin(2 * p + 0.8), 0, 0)}
        crow = max(0, sin(math.pi * (t - 0.3) / 0.25)) if 0.3 <= t <= 0.55 else 0.0
        return {"Neck": (-14 * crow + 3 * sin(2 * p), 16 * sin(p) * (1 - crow), 0), "Head": (-12 * crow, 0, 8 * sin(p + 0.5) * (1 - crow)),
                "WingL": (0, 0, -18 * crow), "WingR": (0, 0, 18 * crow)}
    bird_anims(c, tail=2, stride=30, waddle=6, bob=0.12, flap=10, extra=extra)


# Golden rooster: gold body with red-gold tail
VARIANTS = {"Golden": {BODY: C(255, 196, 55), BODY2: C(225, 150, 30), RUFF: C(255, 240, 160), TAIL: C(200, 30, 40), TAIL2: C(255, 230, 120)}}
