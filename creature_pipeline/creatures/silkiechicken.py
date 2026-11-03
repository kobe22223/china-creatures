"""SILKIE CHICKEN (Epic, Tea Terraces): a round puffball silkie made of soft white fluff puffs, a big fluffy pom
crest, blue-grey face, mulberry comb, turquoise earlobes, fluffy feathered feet. Cute: flat black eyes."""
from cn import *

WHITE, WHITE2, FACE, COMB, LOBE, BEAK, LEGC = (C(250, 250, 252), C(232, 232, 240), C(120, 135, 175), C(110, 50, 90),
                                              C(80, 200, 210), C(130, 140, 170), C(120, 130, 165))


def build():
    c = Creature("SilkieChicken", height=5)
    k = cute_bird(c, WHITE, belly=WHITE, leg_col=LEGC, body=(1.3, 1.2, 1.35), leg_h=0.7, head_r=1.0,
                  head_up=1.0, head_fwd=0.5, wing_col=WHITE, tail=1, foot="toes")
    h, r = k["head"], k["head_r"]
    by, rx, ry, rz = k["by"], k["rx"], k["ry"], k["rz"]
    puffs(c, P(0, by, 0), (rx, ry, rz), WHITE, ["Hips", "Chest"], n=55, size=0.5, seed=4, col2=WHITE2, where=lambda u: u[1] > -0.55)
    c.ellipsoid(h, (r, r * 0.95, r * 0.95), WHITE, "Head", seg=(24, 16))
    puffs(c, h, (r, r * 0.95, r * 0.95), WHITE, "Head", n=40, size=0.36, seed=5, col2=WHITE2, where=lambda u: u[2] > 0.05 or u[1] > 0.6)
    # big pom crest
    puffs(c, h + P(0, r * 0.82, 0.05), (0.62, 0.5, 0.6), WHITE, "Head", n=22, size=0.32, seed=6, col2=WHITE2, sink=0.2)
    # blue-grey face disc, beak, comb, lobes
    c.ellipsoid(h + P(0, -0.05, -r * 0.78), (0.82, 0.7, 0.36), FACE, "Head", seg=(16, 10))
    c.tube([h + P(0, -0.12, -r * 1.06), h + P(0, -0.2, -r * 1.32)], [0.18, 0.04], BEAK, ["Head"], seg=10, sub=1)
    c.ellipsoid(h + P(0, 0.5, -r * 0.92), (0.26, 0.16, 0.16), COMB, "Head", seg=(10, 6))
    for s in (-1, 1):
        c.eye(h + P(s * 0.36, 0.12, -r * 1.08), 0.2, P(s * 0.45, 0.05, -1), "Head", snap=False)
        c.ellipsoid(h + P(s * 0.55, -0.32, -r * 0.82), (0.14, 0.16, 0.08), LOBE, "Head", seg=(10, 6), stud=False)
    # fluffy feathered feet
    for s, S in ((-1, "L"), (1, "R")):
        c.ellipsoid(P(s * k["lx"], 0.42, -0.1), (0.3, 0.3, 0.35), WHITE, "Shin" + S, seg=(12, 8))
    puffs(c, P(0, by + 0.35, rz * 0.85), (0.5, 0.45, 0.45), WHITE, "Tail1", n=12, size=0.3, seed=7, sink=0.2)
    aura(c, "sparkle", (220, 230, 255), (80, 200, 210), "Epic")
    c.extra["speed"] = 1.0
    return c


def anims(c):
    bird_anims(c, tail=1, stride=26, waddle=9, bob=0.12, flap=8)


VARIANTS = {"Ink": {WHITE: C(50, 50, 60), WHITE2: C(70, 70, 84), FACE: C(30, 30, 40), LOBE: C(255, 200, 60)}}
