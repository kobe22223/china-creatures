"""MONEY TOAD (Mythic, Lantern Night Market): the lucky three-legged money toad. A round golden toad on short
stubby legs (two in front, one in back), a big wide head with a gold coin held in its smile, jade and red gem
warts on its back and a red ribbon. Cute: flat black eyes."""
from cn import *

GOLDT, GOLDT2, BELLY, JADEG, REDG, LIPC = C(240, 190, 60), C(205, 150, 40), C(255, 230, 150), C(60, 190, 120), C(220, 50, 50), C(180, 110, 40)


def build():
    c = Creature("MoneyToad", height=5)
    k = cute_quad(c, GOLDT, belly=BELLY, paw=GOLDT2, body=(1.7, 1.15, 1.6), leg_h=0.85, leg_r=0.48, head_r=1.35, head_up=0.35, tail=1, spread=0.62)
    # three legs: drop the two hind legs and add one centred hind leg on the right-hind bones
    c.shapes = [sh for sh in c.shapes if not (set(sh["bones"]) <= {"ThighL", "ShinL", "ThighR", "ShinR"})]
    by, ry, hz, lr = k["by"], k["ry"], k["hz"], 0.5
    c.ellipsoid(P(0, by - ry * 0.5, hz), (lr * 1.5, ry * 0.55, lr * 1.5), GOLDT, "ThighR", seg=(16, 12))
    c.ellipsoid(P(0, k["leg_h"] * 0.5 + 0.1, hz + 0.1), (lr, k["leg_h"] * 0.55, lr * 1.05), GOLDT, "ShinR", seg=(16, 10))
    c.ellipsoid(P(0, 0.27, hz - lr * 0.2), (lr * 1.2, 0.28, lr * 1.35), GOLDT2, "ShinR", seg=(14, 8))
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r * 1.15, r * 0.85, r), GOLDT, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.45, -r * 0.3), (r * 0.95, r * 0.42, r * 0.7), C(250, 212, 105), "Head", seg=(18, 10))
    # wide smile holding a coin
    c.tube([h + P(-0.95, -0.2, -r * 0.72), h + P(0, -0.38, -r * 0.98), h + P(0.95, -0.2, -r * 0.72)], [0.06, 0.07, 0.06], LIPC, ["Head"], seg=6)
    coin(c, h + P(0, -0.32, -r * 1.02), 0.38, "Head", facing=(0, 0.1, -1))
    for s in (-1, 1):
        # bulging eye mounds on top, flat black eyes on their fronts
        c.ellipsoid(h + P(s * 0.6, r * 0.6, -0.3), (0.5, 0.45, 0.48), GOLDT, "Head", seg=(14, 10))
        c.eye(h + P(s * 0.62, r * 0.66, -0.72), 0.29, P(s * 0.3, 0.15, -1), "Head")
    # gem warts on the back
    for j, (x, z) in enumerate(((-0.6, -0.4), (0.55, -0.2), (0.0, 0.3), (-0.45, 0.7), (0.5, 0.75), (0.0, -0.75))):
        c.ellipsoid(P(x, by + ry * 0.9, z), (0.17, 0.12, 0.17), JADEG if j % 2 else REDG, ["Hips", "Chest"], seg=(10, 6), stud=False)
    # red ribbon bow on the back
    c.ellipsoid(P(0, by + ry * 0.75, -0.95), (0.5, 0.18, 0.2), RED, "Chest", seg=(12, 6))
    aura(c, "orbit", (255, 210, 60), (220, 50, 50), "Mythic")
    c.extra["speed"] = 0.9
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        if walking:   # little hops
            return {"Root": ((0, 0, 0), (0, 0.35 * abs(sin(p)), 0)), "ArmL": (25 * sin(p), 0, 0), "ArmR": (25 * sin(p), 0, 0),
                    "ThighR": (-25 * sin(p), 0, 0), "ThighL": (0, 0, 0)}
        return {"Head": (3 * sin(2 * p), 0, 6 * sin(p)), "Chest": (3 * max(0, sin(4 * p)), 0, 0)}
    quad_anims(c, tail=1, stride=0, bob=0.0, extra=extra)


VARIANTS = {"Jade": {GOLDT: C(80, 190, 130), GOLDT2: C(50, 140, 95), BELLY: C(200, 245, 215), JADEG: C(255, 210, 60)}}
