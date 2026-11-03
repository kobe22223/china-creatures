"""FISHING CORMORANT (Legendary, Jade River): round glossy black-green cormorant on short webbed feet, big head
with a white throat, a long hooked yellow beak holding a little silver fish, a woven straw neck ring and a
tiny red tassel. Cute: flat black eyes."""
from cn import *

BLACK, BLACK2, CHEEK, BEAK, BEAK2, STRAW, FISH, FISH2, LEGC = (C(40, 52, 50), C(30, 70, 62), C(240, 240, 230), C(255, 200, 70),
                                                             C(230, 160, 40), C(220, 180, 100), C(190, 205, 220), C(140, 160, 185), C(50, 50, 55))


def build():
    c = Creature("FishingCormorant", height=6)
    k = cute_bird(c, BLACK, belly=BLACK2, leg_col=LEGC, body=(1.2, 1.25, 1.45), leg_h=0.8, head_r=1.0,
                  head_up=1.12, head_fwd=0.5, wing_col=BLACK2, tail=1)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r * 0.95, r * 0.95), BLACK, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.52, -r * 0.55), (0.62, 0.36, 0.38), CHEEK, "Head", seg=(14, 8))   # white throat
    for s in (-1, 1):
        c.eye(h + P(s * 0.42, 0.2, -r * 0.82), 0.19, P(s * 0.5, 0.05, -1), "Head")
    # long hooked beak + a little fish held crosswise
    b0 = h + P(0, -0.1, -r * 0.82)
    c.tube([b0, b0 + P(0, -0.05, -0.55), b0 + P(0, -0.12, -0.95), b0 + P(0, -0.28, -1.05)], [0.22, 0.16, 0.1, 0.04], BEAK, ["Head"], seg=10)
    f0 = b0 + P(0, -0.15, -0.6)
    c.ellipsoid(f0, (0.62, 0.2, 0.16), FISH, "Head", seg=(14, 8))
    c.leaf(f0 + P(0.55, 0, 0), P(1, 0, 0), P(0, 1, 0), 0.32, 0.36, FISH2, "Head", thick=0.06, shape="fin")
    c.ellipsoid(f0 + P(-0.42, 0.04, -0.12), (0.05, 0.05, 0.03), C(20, 20, 25), "Head", stud=False)
    # woven straw neck ring
    c.torus(h + P(0, -r * 0.85, 0.15), 0.7, 0.11, STRAW, ["Neck"], rot=euler(-15, 0, 0), seg=(20, 6))
    lucky_knot(c, h + P(0, -r * 0.95, -0.55), 0.18, "Neck")
    c.leaf(P(0, k["by"] + 0.1, k["rz"] * 0.9), P(0, -0.3, 1), P(1, 0, 0), 0.75, 0.6, BLACK2, "Tail1", thick=0.14, shape="feather")
    aura(c, "sparkle", (90, 200, 170), (255, 220, 120), "Legendary")
    c.extra["speed"] = 1.1
    return c


def anims(c):
    bird_anims(c, tail=1, stride=28, waddle=8, bob=0.1, flap=12)


VARIANTS = {"Ivory": {BLACK: C(235, 235, 228), BLACK2: C(200, 205, 200), CHEEK: C(255, 220, 120), STRAW: C(214, 32, 40)}}
