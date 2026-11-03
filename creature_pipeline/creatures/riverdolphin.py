"""RIVER DOLPHIN (Secret, Jade River): a chubby floating Yangtze river dolphin, pale blue-grey with a white belly,
a big round head with a short rounded beak, a small dorsal fin, wide flippers, a fluked tail and a little jade
pearl pendant. Hovers and swims through the air. Cute: flat black eyes."""
from cn import *

GREY, GREY2, BELLY, BLUSH, PEARL = C(170, 190, 210), C(125, 145, 170), C(240, 245, 250), C(255, 180, 190), C(140, 230, 180)


def build():
    c = Creature("RiverDolphin", height=6)
    k = cute_swimmer(c, y0=2.4, head_r=1.2, body=(1.1, 1.05, 1.5), length=4.6, n=4)
    y0, hc, r = k["y0"], k["head"], k["head_r"]
    belly = band(BELLY, -10, y0 - 0.35)
    c.ellipsoid(hc, (r, r * 0.95, r), GREY, ["Head", "Spine1"], seg=(24, 16), paint=belly)
    c.ellipsoid(P(0, y0, 0.75), (1.1, 1.05, 1.5), GREY, ["Spine1", "Spine2"], seg=(24, 14), paint=belly)
    c.ellipsoid(P(0, y0, -0.25), (1.08, 1.04, 0.95), GREY, ["Head", "Spine1"], seg=(20, 12), paint=belly)   # fills the head/body join
    c.tube([P(0, y0, 1.4), P(0, y0 + 0.05, 2.5), P(0, y0 + 0.1, 3.6)], [0.9, 0.55, 0.28], GREY, ["Spine2", "Spine3", "Spine4"], seg=16, flat=(1.0, 0.85), paint=belly)
    # short rounded beak + melon forehead
    c.tube([hc + P(0, -0.25, -r * 0.8), hc + P(0, -0.32, -r * 1.35)], [0.42, 0.3], GREY2, ["Head"], seg=14, sub=1)
    for s in (-1, 1):
        c.eye(hc + P(s * 0.58, 0.15, -r * 0.74), 0.22, P(s * 0.7, 0.05, -1), "Head")
        c.ellipsoid(hc + P(s * 0.78, -0.25, -r * 0.5), (0.18, 0.1, 0.08), BLUSH, "Head", stud=False)
    # flippers, dorsal fin, flukes
    for s, S in ((-1, "L"), (1, "R")):
        c.leaf(P(s * 0.85, y0 - 0.5, 0.2), P(s * 1, -0.6, 0.5), P(0, 0, 1), 1.0, 0.6, GREY2, "Fin" + S, thick=0.16, shape="blade")
    c.leaf(P(0, y0 + 1.0, 0.8), P(0, 0.7, 1), P(0, 0, 1), 0.8, 0.7, GREY2, ["Spine2"], thick=0.14, shape="fin")
    tp = P(0, y0 + 0.1, 3.5)
    for s in (-1, 1):
        c.leaf(tp + P(0, 0, -0.15), P(s * 1, 0, 0.75), P(0, 0, 1), 0.95, 0.85, GREY2, ["Spine4"], thick=0.16, shape="feather")
    # jade pearl pendant on a red cord
    c.torus(P(0, y0 - 0.3, -0.35), 0.95, 0.06, RED, ["Spine1"], rot=euler(90, 0, 0), seg=(20, 4))
    c.ellipsoid(P(0, y0 - 1.05, -0.62), (0.22, 0.22, 0.22), PEARL, ["Spine1"], seg=(12, 8), glow=True)
    aura(c, "orbit", (170, 220, 255), (140, 230, 180), "Secret")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.15
    return c


def anims(c):
    swimmer_anims(c, ["Spine1", "Spine2", "Spine3", "Spine4"], amp=12, axis="pitch", hover=0.4)


VARIANTS = {"Pink": {GREY: C(255, 185, 200), GREY2: C(240, 140, 170), BELLY: C(255, 235, 240)}}
