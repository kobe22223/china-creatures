"""IMMORTAL CRANE (Eternal, Kunlun Immortal Peaks): a round snow-white red-crowned crane on short tucked legs,
big head with a red crown cap, a black face and neck band, a shortish jade-green beak, folded wings with black
tips, gold cloud swirls on the body, and a soft black tail plume. Cute: flat black eyes."""
from cn import *

WHITE, BLACK, REDC, BEAK, GOLDC, LEGC, CLOUD = (C(252, 252, 250), C(35, 35, 40), C(225, 30, 40), C(120, 170, 130),
                                               C(255, 205, 80), C(70, 70, 80), C(230, 240, 255))


def build():
    c = Creature("ImmortalCrane", height=6)
    swirl = cloud_filigree(GOLDC, scale=1.8, width=0.07, only=lambda X, Y, Z: Z < 0.3)
    k = cute_bird(c, WHITE, belly=WHITE, leg_col=LEGC, body=(1.2, 1.2, 1.5), leg_h=0.85, head_r=0.95,
                  head_up=1.15, head_fwd=0.55, wing_col=WHITE, tail=1, foot="toes", paint=swirl)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r, r * 0.95), WHITE, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, r * 0.75, -0.15), (0.48, 0.25, 0.5), REDC, "Head", seg=(14, 8))                 # red crown
    c.ellipsoid(h + P(0, -0.45, -0.1), (r * 0.82, r * 0.6, r * 0.78), BLACK, "Head", seg=(18, 10))         # black face/throat band
    c.ellipsoid(k["nb"] + P(0, 0.15, -0.05), (0.75, 0.55, 0.65), BLACK, ["Neck", "Chest"], seg=(14, 8))
    c.tube([h + P(0, -0.05, -r * 0.82), h + P(0, -0.15, -r * 1.35), h + P(0, -0.28, -r * 1.65)], [0.2, 0.12, 0.04], BEAK, ["Head"], seg=10)
    for s in (-1, 1):
        c.eye(h + P(s * 0.42, 0.18, -r * 0.82), 0.19, P(s * 0.5, 0.05, -1), "Head")
    # folded wings with black tips and gold swirls (painted on the wing shapes via a second layer)
    for s, S in ((-1, "L"), (1, "R")):
        w = P(s * k["rx"] * 0.82, k["by"] + k["ry"] * 0.12, k["rz"] * 0.15)
        c.ellipsoid(w + P(s * 0.03, 0, 0.05), (k["rx"] * 0.28, k["ry"] * 0.53, k["rz"] * 0.66), WHITE, "Wing" + S, rot=euler(-14, s * -6, s * 4), seg=(16, 10),
                    paint=band(BLACK, 0.55, 9, axis="z"))
    c.ellipsoid(P(0, k["by"] + 0.1, k["rz"] * 0.95), (0.55, 0.42, 0.5), BLACK, "Tail1", rot=euler(-25, 0, 0), seg=(14, 8))   # soft tail plume
    aura(c, "sparkle", (230, 240, 255), (255, 80, 80), "Eternal")
    c.extra["speed"] = 1.2
    return c


def anims(c):
    bird_anims(c, tail=1, stride=28, waddle=5, bob=0.1, flap=14)


VARIANTS = {"Golden": {WHITE: C(255, 225, 140), BLACK: C(150, 60, 40), REDC: C(255, 255, 255), GOLDC: C(214, 32, 40)}}
