"""SHRIMP SOLDIER (Divine, Dragon King's Palace): a chubby floating coral-pink shrimp guard of the sea palace. A big
round head with eye stalks and flat black eyes, short curling antennae, a plump curled segmented body, little
swimmerets, a fan tail, a gold helmet with a red plume and a tiny gold trident. Cute: flat black eyes."""
from cn import *

PINK, PINK2, BELLY, GOLDS, PLUME, SHAFT = C(255, 130, 110), C(225, 90, 80), C(255, 210, 190), C(255, 200, 60), C(214, 32, 40), C(180, 120, 60)


def build():
    c = Creature("ShrimpSoldier", height=5.5)
    k = cute_swimmer(c, y0=2.4, head_r=1.15, body=(0.95, 0.95, 1.2), length=3.6, n=4)
    y0, hc, r = k["y0"], k["head"], k["head_r"]
    seg_paint = stripes(PINK2, "z", period=0.6, width=0.1, wobble=0.0)
    c.ellipsoid(hc, (r, r * 0.95, r * 1.05), PINK, ["Head", "Spine1"], seg=(24, 16))
    # plump body curling down and under, in segments
    pts = [P(0, y0, 0.1), P(0, y0 - 0.1, 1.0), P(0, y0 - 0.45, 1.8), P(0, y0 - 1.05, 2.3), P(0, y0 - 1.65, 2.2)]
    c.tube(pts, [0.98, 0.85, 0.68, 0.5, 0.35], PINK, ["Spine1", "Spine2", "Spine3", "Spine4"], seg=16, paint=seg_paint)
    c.ellipsoid(P(0, y0 - 0.45, 0.6), (0.7, 0.4, 0.8), BELLY, ["Spine1", "Spine2"], seg=(14, 8))
    for i in range(3):   # little swimmerets
        for s in (-1, 1):
            c.tube([P(s * 0.35, y0 - 0.75, 0.4 + i * 0.45), P(s * 0.45, y0 - 1.2, 0.3 + i * 0.45)], [0.09, 0.05], PINK2, ["Spine1" if i < 2 else "Spine2"], seg=6, sub=1)
    tp = P(0, y0 - 1.75, 2.15)
    for s in (-1, 0, 1):
        c.leaf(tp, P(s * 0.6, -0.4, -0.7), P(1, 0, 0), 0.75, 0.45, PINK2, ["Spine4"], thick=0.1, shape="feather")
    # face: eye stalks with flat black eyes, short curled antennae
    for s in (-1, 1):
        st = hc + P(s * 0.45, r * 0.55, -r * 0.6)
        c.tube([hc + P(s * 0.3, r * 0.3, -r * 0.55), st], [0.14, 0.12], PINK, ["Head"], seg=8, sub=1)
        c.ellipsoid(st + P(0, 0.1, -0.05), (0.26, 0.26, 0.24), PINK, "Head", seg=(12, 8))
        c.eye(st + P(s * 0.05, 0.12, -0.25), 0.2, P(s * 0.3, 0.1, -1), "Head")
        c.tube([hc + P(s * 0.2, -0.1, -r * 0.95), hc + P(s * 0.55, 0.2, -r * 1.5), hc + P(s * 0.9, 0.6, -r * 1.35), hc + P(s * 1.0, 0.85, -r * 0.95)],
               [0.06, 0.05, 0.04, 0.025], PINK2, ["Head"], seg=6)
    # gold helmet with a red plume
    c.ellipsoid(hc + P(0, r * 0.55, 0.15), (r * 0.85, r * 0.45, r * 0.85), GOLDS, "Head", seg=(18, 8), stud=False)
    c.torus(hc + P(0, r * 0.32, 0.15), r * 0.82, 0.08, GOLDS, "Head", seg=(20, 4), stud=False)
    for j in range(3):
        c.leaf(hc + P(0, r * 0.95, 0.15), P((j - 1) * 0.3, 1, 0.55), P(1, 0, 0), 0.8, 0.35, PLUME, "Head", thick=0.12, shape="feather", curl=0.15)
    # tiny trident held at the side
    c.tube([P(0.95, y0 - 1.2, -0.6), P(1.05, y0 + 1.4, -0.75)], [0.06, 0.06], SHAFT, ["FinR"], seg=6, sub=1)
    for dx in (-0.2, 0.0, 0.2):
        c.spike(P(1.05 + dx, y0 + 1.35, -0.75), P(1.05 + dx * 1.3, y0 + 1.85, -0.78), 0.07, GOLDS, "FinR", seg=4, n=3, stud=False)
    c.tube([P(0.85, y0 + 1.35, -0.75), P(1.25, y0 + 1.35, -0.75)], [0.05, 0.05], GOLDS, ["FinR"], seg=6, sub=1, stud=False)
    aura(c, "sparkle", (255, 150, 130), (255, 200, 60), "Divine")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.1
    return c


def anims(c):
    swimmer_anims(c, ["Spine1", "Spine2", "Spine3", "Spine4"], amp=8, axis="pitch", hover=0.35)


VARIANTS = {"Glass": {PINK: C(190, 230, 255), PINK2: C(130, 190, 240), BELLY: C(235, 248, 255), PLUME: C(40, 80, 190)}}
