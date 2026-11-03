"""FERGHANA HORSE (Cosmic, Great Wall): the "heavenly horse". A round golden-chestnut foal on short stubby legs,
big head, a flowing cream mane and tail, a gold bridle with a red pompom on the forehead, a little jade
saddle cloth with a gold coin and a starry glow on its hooves. Cute: flat black eyes."""
from cn import *

COAT, COAT2, MANE, MANE2, MUZ, NOSE, HOOFC, STAR = (C(225, 150, 70), C(190, 115, 50), C(255, 238, 200), C(250, 220, 160),
                                                   C(245, 205, 165), C(110, 70, 55), C(80, 60, 50), C(170, 220, 255))


def build():
    c = Creature("FerghanaHorse", height=7)
    k = cute_quad(c, COAT, belly=MUZ, paw=HOOFC, body=(1.4, 1.18, 1.85), leg_h=1.25, leg_r=0.42, head_r=1.22, head_up=0.75, tail=3)
    h, r = k["head"], k["head_r"]
    by, rz = k["by"], k["rz"]
    c.ellipsoid(h, (r * 0.95, r, r * 1.05), COAT, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.42, -r * 0.75), (0.62, 0.55, 0.62), MUZ, "Head", seg=(16, 10))
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.22, -0.4, -r * 1.3), (0.08, 0.12, 0.05), NOSE, "Head", stud=False, smooth=True)
        c.eye(h + P(s * 0.48, 0.22, -r * 0.84), 0.23, P(s * 0.45, 0.05, -1), "Head")
        c.leaf(h + P(s * 0.48, r * 0.8, 0.1), P(s * 0.3, 1, 0.15), P(0, 0, 1), 0.65, 0.42, COAT2, "Head", thick=0.18, shape="blade")
    # flowing mane: soft puffs from forelock down the back of the neck
    puffs(c, h + P(0, r * 0.75, 0.25), (0.45, 0.4, 0.75), MANE, "Head", n=14, size=0.32, seed=41, col2=MANE2, sink=0.25)
    puffs(c, P(0, by + 0.75, -rz * 0.55), (0.42, 0.55, 0.65), MANE, "Chest", n=14, size=0.34, seed=42, col2=MANE2, sink=0.25, where=lambda u: u[1] > -0.2)
    # gold bridle + red tassel ornament on the forehead
    c.torus(h + P(0, -0.25, -r * 0.62), 0.78, 0.07, GOLD, "Head", rot=euler(90, 0, 0), seg=(20, 5), stud=False)
    c.ellipsoid(h + P(0, 0.62, -r * 0.92), (0.15, 0.15, 0.12), GOLD, "Head", seg=(10, 6), stud=False)
    c.ellipsoid(h + P(0, 0.88, -r * 0.88), (0.24, 0.22, 0.2), RED, "Head", seg=(12, 8))   # red pompom
    # jade saddle cloth with a coin
    c.ellipsoid(P(0, by + 0.65, 0.1), (k["rx"] * 1.02, 0.55, 0.85), JADE, ["Hips", "Chest"], seg=(18, 8))
    for s in (-1, 1):
        coin(c, P(s * k["rx"] * 0.97, by + 0.35, 0.1), 0.22, ["Hips", "Chest"], facing=(s, 0, 0))
    # flowing tail
    t = P(0, by + 0.35, rz * 0.92)
    c.tube([t, t + P(0, 0.1, 0.5), t + P(0, -0.4, 0.95), t + P(0, -1.0, 1.05)], [0.32, 0.45, 0.4, 0.15], MANE, ["Tail1", "Tail2", "Tail3"], seg=12)
    # starry glow ring above each hoof (Cosmic)
    for s, S in ((-1, "L"), (1, "R")):
        for z, bone in ((k["sz"], "Fore" + S), (k["hz"], "Shin" + S)):
            c.torus(P(s * k["lx"], 0.62, z), 0.42, 0.06, STAR, bone, seg=(16, 4), glow=True)
    aura(c, "orbit", (170, 220, 255), (255, 210, 120), "Cosmic")
    c.extra["speed"] = 1.35
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (0, 0, 12 * sin(2 * p)), "Head": (5 * sin(2 * p), 0, 4 * sin(p))}
    quad_anims(c, tail=3, stride=30, bob=0.16, extra=extra)


VARIANTS = {"Night": {COAT: C(45, 45, 60), COAT2: C(30, 30, 42), MUZ: C(90, 90, 110), MANE: C(170, 200, 255), MANE2: C(130, 160, 240)}}
