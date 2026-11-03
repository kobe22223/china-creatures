"""CHIWEN (Eternal, Forbidden City): the roof-ridge dragon-fish. A floating glazed-ceramic creature with a dragon
head (glowing eyes, curled whiskers, open jaws) on a plump fish body in green and imperial-yellow glaze, painted
scale bands, a spiny back fin and a big fish tail curling up high behind it like the roof ornaments. Royal: glowing eyes."""
from cn import *
from detail import V as GV, E, T

GREEN_, GREEN2, YELLOW, YELLOW2, CREAM, WHISK, EYE = (C(60, 150, 110), C(35, 110, 80), C(255, 200, 50), C(220, 150, 30),
                                                     C(245, 230, 170), C(255, 220, 120), C(255, 80, 60))


def build():
    c = Creature("Chiwen", height=6.5)
    k = cute_swimmer(c, y0=2.6, head_r=1.0, body=(1.0, 1.0, 1.3), length=4.0, n=4)
    y0 = k["y0"]
    scl = stripes(GREEN2, "z", period=0.5, width=0.12, wobble=0.3)
    # plump fish body, curling up into a high tail
    c.ellipsoid(P(0, y0, 0.5), (1.1, 1.1, 1.45), GREEN_, ["Spine1", "Spine2"], seg=(24, 14), paint=scl)
    c.ellipsoid(P(0, y0 - 0.35, 0.3), (0.85, 0.75, 1.15), CREAM, ["Spine1", "Spine2"], seg=(18, 10))
    c.tube([P(0, y0, 1.4), P(0, y0 + 0.45, 2.4), P(0, y0 + 1.35, 3.1), P(0, y0 + 2.3, 3.2)], [0.85, 0.6, 0.42, 0.25], GREEN_,
           ["Spine2", "Spine3", "Spine4"], seg=16, paint=scl)
    tp = P(0, y0 + 2.3, 3.2)
    for s in (-1, 1):
        c.leaf(tp, P(s * 0.7, 1, -0.35), P(0, 0, 1), 1.3, 0.9, YELLOW if s > 0 else YELLOW2, ["Spine4"], thick=0.12, shape="feather", curl=0.15)
    # spiny back fin in yellow glaze
    for j in range(6):
        z = -0.3 + j * 0.45
        y = y0 + 1.05 + (0.25 if j > 3 else 0) * (j - 3)
        c.spike(P(0, y - 0.15, z), P(0, y + 0.45, z + 0.3), 0.18, YELLOW, ["Spine1"] if j < 3 else ["Spine2"], seg=4, n=3)
    for s, S in ((-1, "L"), (1, "R")):
        c.leaf(P(s * 0.9, y0 - 0.45, 0.0), P(s * 1, -0.4, 0.5), P(0, 0, 1), 1.0, 0.7, YELLOW2, "Fin" + S, thick=0.1, shape="feather")
    # dragon head (cute scale, no separate jaw bone)
    hb = GV(0, y0 + 0.15, -0.2)
    dragon_head(c, hb, 0.72, GREEN_, CREAM, YELLOW, WHISK, YELLOW, EYE, bone="Head", horns="swept", mane_n=3, seed=81, brow=GREEN2)
    aura(c, "sparkle", (255, 210, 60), (80, 200, 140), "Eternal")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.1
    return c


def anims(c):
    swimmer_anims(c, ["Spine1", "Spine2", "Spine3", "Spine4"], amp=9, axis="pitch", hover=0.4)


VARIANTS = {"Imperial": {GREEN_: C(255, 200, 50), GREEN2: C(214, 150, 30), YELLOW: C(214, 32, 40), YELLOW2: C(160, 20, 30)}}
