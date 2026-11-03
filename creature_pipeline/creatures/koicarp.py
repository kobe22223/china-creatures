"""KOI CARP (Cosmic, Jade River): a chubby floating koi with a big round head, white body with bold red-orange
patches, flowing veil fins, little whiskers, a gold crown-spot and a fanned double tail. Hovers and swims through
the air. Cute: flat black eyes."""
from cn import *

WHITE, RED_, ORANGE, FIN, FIN2, LIP, GOLDS = (C(250, 248, 244), C(220, 40, 30), C(255, 120, 40), C(255, 235, 225),
                                             C(255, 170, 120), C(255, 170, 160), C(255, 205, 60))


def build():
    c = Creature("KoiCarp", height=5.5)
    k = cute_swimmer(c, y0=2.3, head_r=1.15, body=(1.05, 1.05, 1.4), length=4.4, n=4)
    y0, pts, hc, r = k["y0"], k["pts"], k["head"], k["head_r"]
    patches = spots(RED_, size=1.5, density=0.5, seed=5)
    # head + body + tail stalk, blended over the spine
    c.ellipsoid(hc, (r, r * 0.95, r), WHITE, ["Head", "Spine1"], seg=(24, 16), paint=spots(RED_, size=1.3, density=0.5, seed=9, only=lambda X, Y, Z: Y > y0 + 0.1))
    c.ellipsoid(P(0, y0, -0.25), (1.02, 1.0, 0.95), WHITE, ["Head", "Spine1"], seg=(20, 12), paint=patches)   # fills the head/body join
    c.ellipsoid(P(0, y0, 0.7), (1.08, 1.05, 1.45), WHITE, ["Spine1", "Spine2"], seg=(24, 14), paint=patches)
    c.tube([P(0, y0, 1.3), P(0, y0 + 0.02, 2.3), P(0, y0 + 0.04, 3.3)], [0.88, 0.55, 0.3], WHITE, ["Spine2", "Spine3", "Spine4"], seg=16, flat=(0.8, 1.0), paint=patches)
    # gold spot on the crown
    c.ellipsoid(hc + P(0, r * 0.85, 0.1), (0.3, 0.1, 0.3), GOLDS, "Head", seg=(12, 6), stud=False)
    # face: lips, whiskers, eyes
    c.ellipsoid(hc + P(0, -0.3, -r * 0.95), (0.35, 0.22, 0.18), LIP, "Head", seg=(12, 8))
    for s in (-1, 1):
        c.eye(hc + P(s * 0.6, 0.22, -r * 0.72), 0.22, P(s * 0.7, 0.05, -1), "Head")
        c.tube([hc + P(s * 0.25, -0.35, -r * 1.0), hc + P(s * 0.55, -0.6, -r * 1.1), hc + P(s * 0.7, -0.85, -r * 1.0)], [0.06, 0.05, 0.03], LIP, ["Head"], seg=6)
    # pectoral veil fins
    for s, S in ((-1, "L"), (1, "R")):
        c.leaf(P(s * 0.85, y0 - 0.4, 0.2), P(s * 1, -0.5, 0.6), P(0, 0, 1), 1.1, 0.75, FIN, "Fin" + S, thick=0.08, shape="feather")
    # dorsal fin along the back
    c.leaf(P(0, y0 + 0.95, 0.3), P(0, 0.4, 1), P(0, 0, 1), 1.6, 0.7, FIN2, ["Spine2"], thick=0.08, shape="fin")
    # fanned double tail
    tp = P(0, y0 + 0.04, 3.2)
    for s in (-1, 1):
        c.leaf(tp, P(s * 0.25, s * 0.6, 1), P(0, 1, 0), 1.6, 1.1, FIN if s > 0 else FIN2, ["Spine4"], thick=0.08, shape="feather", curl=0.1)
    aura(c, "orbit", (255, 140, 80), (255, 230, 140), "Cosmic")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.1
    return c


def anims(c):
    swimmer_anims(c, ["Spine1", "Spine2", "Spine3", "Spine4"], amp=11, axis="yaw", hover=0.35)


VARIANTS = {"Ogon": {WHITE: C(255, 210, 80), RED_: C(255, 245, 200), FIN: C(255, 235, 170), FIN2: C(255, 200, 90)}}
