"""TIER 10, HEAVENLY CLOUD TREADMILL: no legs, the whole treadmill floats on a base of big fluffy cloud puffs.
White jade pillars wrapped by gold dragons stand at the console end, holding a golden halo ring and a small
celestial gate roof. Gold trim everywhere. Glow: the halo ring, gold accent orbs and a sky-blue screen."""
from tm import *

WHITE, CLOUD2, GOLDH, GOLD2H, BELT, HALO, SKY, ACC = (C(250, 250, 255), C(225, 232, 248), C(255, 205, 70), C(214, 155, 35),
                                                     C(235, 238, 248), C(255, 235, 150), C(150, 210, 255), C(255, 215, 90))


def build():
    c = tread("China10")
    deck(c, BELT, GOLDH, roller=GOLD2H, belt_paint=bands(C(200, 215, 240), "z", period=1.0, width=0.1), rim_paint=filigree(GOLD2H, scale=1.8, width=0.05))
    # floating cloud base: big puffs all round the deck, nothing touching the ground but the lowest puffs
    import random
    rng = random.Random(10)
    for i in range(22):
        z = -10.5 + i
        for s in (-1, 1):
            r = 0.75 + 0.2 * rng.random()
            E(c, V(s * (3.75 + 0.2 * rng.random()), 0.95 + 0.25 * rng.random(), z), (r, r * 0.8, r * 1.1), WHITE if i % 3 else CLOUD2, R, seg=(8, 5))
    for x in (-2.4, -0.8, 0.8, 2.4):
        for z in (-10.9, 10.9):
            r = 0.85 + 0.3 * rng.random()
            E(c, V(x, 0.95, z * 1.04), (r, r * 0.8, r), WHITE, R, seg=(8, 5))
    rbox(c, V(0, 0.55, 0), (2.9, 0.45, 10.5), CLOUD2, bevel=0.3)
    sc, hc, n = console(c, WHITE, SKY, glow=SKY, post=GOLDH, head_half=(3.0, 0.85, 0.75), body_paint=filigree(GOLDH, scale=1.6, width=0.06))
    # white jade pillars wrapped by gold dragons
    for s in (-1, 1):
        p0, p1 = V(s * 3.9, 0.6, -10.8), V(s * 3.9, 9.6, -10.8)
        cyl(c, p0, p1, 0.42, WHITE, seg=12)
        E(c, p0, (0.65, 0.3, 0.65), GOLDH, R, seg=(10, 5), stud=False)
        E(c, p1, (0.6, 0.25, 0.6), GOLDH, R, seg=(10, 5), stud=False)
        helix = [p0 + V(math.cos(t * 0.9 + (0 if s > 0 else math.pi)) * 0.55, 0.3 + t * 0.55, math.sin(t * 0.9 + (0 if s > 0 else math.pi)) * 0.55) for t in range(16)]
        T(c, helix, [0.12 + 0.1 * math.sin(math.pi * i / 15) for i in range(16)], GOLDH, R, seg=7, sub=2, stud=False)
        hd = helix[-1] + V(0, 0.2, 0)
        E(c, hd, (0.3, 0.26, 0.38), GOLDH, R, seg=(8, 6), stud=False)
        for sx in (-1, 1):
            S(c, hd + V(sx * 0.12, 0.2, 0.0), hd + V(sx * 0.2, 0.6, 0.25), 0.07, GOLD2H, R, seg=4, n=3, stud=False)
        E(c, p1 + V(0, 0.45, 0), (0.28, 0.28, 0.28), ACC, R, seg=(10, 6), glow=True)
    # golden halo ring between the pillars + celestial gate roof on top
    ring(c, V(0, 7.4, -11.0), V(0, 0, 1), 3.05, 0.22, HALO, seg=(36, 6), glow=True)
    rbox(c, V(0, 9.95, -10.8), (4.4, 0.25, 0.75), GOLDH, bevel=0.12, stud=False)
    roof(c, V(0, 10.65, -10.8), 4.6, 1.25, 0.75, WHITE, GOLDH, GOLDH, bell_y=0.45, tile2=CLOUD2)
    E(c, V(0, 11.5, -10.8), (0.4, 0.4, 0.4), ACC, R, seg=(10, 6), glow=True)
    ends = rails(c, GOLDH, r=0.25)
    for e in ends:
        E(c, e, (0.3, 0.3, 0.3), ACC, R, seg=(8, 5), glow=True)
    return c
