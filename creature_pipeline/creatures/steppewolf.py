"""STEPPE WOLF (Legendary, Great Wall): round grey steppe wolf pup on short stubby legs, big head with a cream
muzzle and cheeks, short pointed ears, a fluffy cream chest ruff, a red bandana and a bushy grey tail. Cute: flat black eyes."""
from cn import *

GREY, GREY2, CREAM, NOSE, PINK = C(150, 155, 168), C(105, 110, 124), C(240, 232, 218), C(35, 32, 36), C(250, 170, 170)


def build():
    c = Creature("SteppeWolf", height=6)
    k = cute_quad(c, GREY, belly=CREAM, paw=CREAM, body=(1.45, 1.2, 1.8), leg_h=1.15, leg_r=0.44, head_r=1.28, head_up=0.55, tail=3)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r * 1.04, r * 0.95, r), GREY, "Head", seg=(24, 16))
    c.tube([h + P(0, -0.25, -r * 0.55), h + P(0, -0.32, -r * 1.12)], [0.56, 0.42], CREAM, ["Head"], seg=16, sub=1)   # short muzzle
    c.ellipsoid(h + P(0, -0.15, -r * 1.25), (0.2, 0.14, 0.12), NOSE, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.72, -0.35, -r * 0.45), (0.5, 0.42, 0.45), CREAM, "Head", seg=(14, 8))
        c.eye(h + P(s * 0.48, 0.25, -r * 0.84), 0.23, P(s * 0.45, 0.05, -1), "Head")
        e0 = h + P(s * 0.7, r * 0.7, 0.05)
        c.leaf(e0, P(s * 0.35, 1, 0.1), P(0, 0, 1), 0.78, 0.68, GREY2, "Head", thick=0.22, shape="blade")
        c.leaf(e0 + P(0, 0.04, -0.1), P(s * 0.35, 1, 0.1), P(0, 0, 1), 0.55, 0.42, PINK, "Head", thick=0.1, shape="blade")
    # fluffy chest ruff
    puffs(c, P(0, k["by"] + 0.1, -k["rz"] * 0.75), (1.05, 0.7, 0.55), CREAM, "Chest", n=18, size=0.38, seed=8, where=lambda u: u[2] < 0.2)
    # red scarf: a knotted bandana on the chest under the chin
    sc = P(0, k["by"] - 0.25, -k["rz"] * 0.97)
    c.ellipsoid(sc, (1.12, 0.62, 0.38), RED, "Chest", seg=(16, 10))
    c.ellipsoid(sc + P(0, -0.45, -0.25), (0.32, 0.42, 0.18), RED2, "Chest", rot=euler(20, 0, 0), seg=(10, 8))
    # bushy tail sweeping up
    t = P(0, k["by"] + 0.2, k["rz"] * 0.9)
    c.tube([t, t + P(0, 0.45, 0.5), t + P(0, 1.0, 0.62), t + P(0, 1.4, 0.4)], [0.36, 0.5, 0.44, 0.22], GREY, ["Tail1", "Tail2", "Tail3"], seg=16, sub=5)
    c.ellipsoid(t + P(0, 1.32, 0.45), (0.34, 0.34, 0.32), CREAM, "Tail3", seg=(12, 8))
    aura(c, "sparkle", (200, 210, 255), (214, 32, 40), "Legendary")
    c.extra["speed"] = 1.2
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (0, 0, 14 * sin(2 * p)), "Tail2": (0, 0, 10 * sin(2 * p - 0.6))}
    quad_anims(c, tail=3, stride=28, bob=0.12, extra=extra)


VARIANTS = {"Midnight": {GREY: C(55, 58, 75), GREY2: C(35, 38, 52), CREAM: C(150, 160, 190), RED: C(255, 200, 60), RED2: C(214, 150, 30)}}
