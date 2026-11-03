"""BACTRIAN CAMEL (Mythic, Great Wall): round sandy Bactrian camel calf on short stubby legs, two fluffy humps with
a red silk-road blanket and gold coins draped between them, a big head with a soft muzzle, small round ears and
woolly tufts on the head, neck and humps. Cute: flat black eyes."""
from cn import *

SAND, SAND2, WOOL, MUZ, NOSE, HOOFC = C(215, 175, 120), C(180, 135, 85), C(150, 105, 65), C(240, 215, 175), C(90, 60, 50), C(110, 80, 60)


def build():
    c = Creature("BactrianCamel", height=7)
    k = cute_quad(c, SAND, belly=MUZ, paw=HOOFC, body=(1.5, 1.2, 1.9), leg_h=1.2, leg_r=0.45, head_r=1.2, head_up=0.7, tail=1)
    h, r = k["head"], k["head_r"]
    by, ry, rz = k["by"], k["ry"], k["rz"]
    # two fluffy humps
    for z in (-0.75, 0.75):
        hp = P(0, by + ry * 0.85, z)
        c.ellipsoid(hp, (0.7, 0.75, 0.62), SAND2, ["Chest"] if z < 0 else ["Hips"], seg=(16, 10))
        puffs(c, hp + P(0, 0.35, 0), (0.62, 0.5, 0.55), WOOL, ["Chest"] if z < 0 else ["Hips"], n=12, size=0.3, seed=int(z * 10) + 20, where=lambda u: u[1] > 0.1)
    # red blanket between the humps with gold trim and coins on the sides
    c.ellipsoid(P(0, by + ry * 0.62, 0), (rx_ := k["rx"] * 1.03, 0.5, 0.62), RED, ["Hips", "Chest"], seg=(18, 8))
    for s in (-1, 1):
        c.ellipsoid(P(s * k["rx"] * 0.82, by + 0.2, 0), (0.18, 0.62, 0.62), RED, ["Hips", "Chest"], seg=(10, 8))
        c.ellipsoid(P(s * k["rx"] * 0.86, by - 0.4, 0), (0.12, 0.08, 0.6), GOLD, ["Hips", "Chest"], seg=(8, 4), stud=False)
        coin(c, P(s * k["rx"] * 0.98, by + 0.15, 0), 0.24, ["Hips", "Chest"], facing=(s, 0, 0))
    c.ellipsoid(h, (r, r * 0.95, r * 1.05), SAND, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.38, -r * 0.7), (0.72, 0.52, 0.6), MUZ, "Head", seg=(16, 10))
    puffs(c, h + P(0, r * 0.7, 0.05), (0.6, 0.35, 0.55), WOOL, "Head", n=10, size=0.26, seed=31, sink=0.2)
    puffs(c, P(0, by + 0.2, -rz * 0.8), (0.9, 0.7, 0.45), WOOL, "Chest", n=14, size=0.32, seed=32, where=lambda u: u[2] < 0)
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.22, -0.3, -r * 1.25), (0.08, 0.12, 0.05), NOSE, "Head", stud=False, smooth=True)
        c.eye(h + P(s * 0.5, 0.2, -r * 0.84), 0.22, P(s * 0.45, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.5, 0.36, -r * 0.82), (0.22, 0.07, 0.1), SAND2, "Head", stud=False)   # sleepy lid
        c.ellipsoid(h + P(s * 0.92, r * 0.5, 0.15), (0.22, 0.2, 0.12), SAND2, "Head", rot=euler(0, s * 30, 0), seg=(10, 8))
    c.tube([P(0, by + 0.1, rz * 0.95), P(0, by - 0.4, rz * 1.1)], [0.12, 0.08], SAND2, ["Tail1"], seg=8, sub=1)
    c.ellipsoid(P(0, by - 0.55, rz * 1.12), (0.16, 0.22, 0.16), WOOL, "Tail1", seg=(8, 6))
    aura(c, "orbit", (255, 200, 90), (214, 32, 40), "Mythic")
    c.extra["speed"] = 0.95
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Head": (4 * sin(2 * p), 0, 6 * sin(p)), "Chest": (2 * sin(2 * p), 3 * sin(p), 0)}
    quad_anims(c, tail=1, stride=22, bob=0.1, extra=extra)


VARIANTS = {"Snowpeak": {SAND: C(245, 242, 235), SAND2: C(215, 210, 200), WOOL: C(200, 195, 185), MUZ: C(255, 250, 240), RED: C(40, 80, 190)}}
