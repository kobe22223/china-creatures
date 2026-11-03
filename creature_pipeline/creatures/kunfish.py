"""KUN FISH (Titanic, Dragon King's Palace): the legendary giant fish of the northern sea. A huge chubby floating
whale-fish, deep ocean blue with a pale belly, glowing cloud swirl markings, a big round head with a gentle smile,
wing-like pectoral fins (it will one day become the Peng), a crest fin and a wide crescent tail. Cute: flat black eyes."""
from cn import *

BLUE, BLUE2, BELLY, FIN, GLOWC, BLUSH = C(40, 80, 170), C(25, 55, 130), C(210, 230, 250), C(70, 130, 220), C(120, 230, 255), C(255, 170, 190)


def build():
    c = Creature("KunFish", height=7)
    k = cute_swimmer(c, y0=2.8, head_r=1.4, body=(1.35, 1.3, 1.7), length=5.0, n=4)
    y0, hc, r = k["y0"], k["head"], k["head_r"]
    belly = band(BELLY, -10, y0 - 0.45)
    c.ellipsoid(hc, (r, r * 0.95, r), BLUE, ["Head", "Spine1"], seg=(24, 16), paint=belly)
    c.ellipsoid(P(0, y0, -0.2), (1.35, 1.3, 1.1), BLUE, ["Head", "Spine1"], seg=(22, 14), paint=belly)
    c.ellipsoid(P(0, y0, 0.9), (1.4, 1.32, 1.7), BLUE, ["Spine1", "Spine2"], seg=(24, 16), paint=belly)
    c.tube([P(0, y0, 1.8), P(0, y0 + 0.05, 3.0), P(0, y0 + 0.12, 4.2)], [1.05, 0.62, 0.3], BLUE, ["Spine2", "Spine3", "Spine4"], seg=16, flat=(0.85, 1.0), paint=belly)
    # glowing cloud swirl markings along the back
    for j, (x, z) in enumerate(((0.0, -0.3), (0.6, 0.6), (-0.6, 0.9), (0.0, 1.9))):
        p = P(x, y0 + 1.15 - 0.15 * abs(x), z)
        c.torus(p, 0.28, 0.06, GLOWC, ["Spine1"] if z < 1 else ["Spine2"], rot=euler(-10, 0, x * 25), seg=(14, 4), glow=True)
    # face
    for s in (-1, 1):
        c.eye(hc + P(s * 0.68, 0.18, -r * 0.72), 0.24, P(s * 0.7, 0.05, -1), "Head")
        c.ellipsoid(hc + P(s * 0.85, -0.25, -r * 0.5), (0.2, 0.12, 0.08), BLUSH, "Head", stud=False)
    c.tube([hc + P(-0.4, -0.45, -r * 0.88), hc + P(0, -0.55, -r * 0.98), hc + P(0.4, -0.45, -r * 0.88)], [0.04, 0.05, 0.04], BLUE2, ["Head"], seg=6)
    # wing-like pectoral fins, crest fin, crescent tail
    for s, S in ((-1, "L"), (1, "R")):
        c.leaf(P(s * 1.15, y0 - 0.2, 0.2), P(s * 1, 0.1, 0.55), P(0, 0, 1), 1.9, 1.0, FIN, "Fin" + S, thick=0.14, shape="feather", curl=0.1)
    c.leaf(P(0, y0 + 1.25, 0.6), P(0, 0.5, 1), P(0, 0, 1), 1.3, 0.9, FIN, ["Spine2"], thick=0.12, shape="fin")
    tp = P(0, y0 + 0.12, 4.1)
    for s in (-1, 1):
        c.leaf(tp, P(0, s * 0.9, 0.55), P(1, 0, 0), 1.5, 0.75, FIN, ["Spine4"], thick=0.14, shape="feather", curl=-0.15 * s)
    aura(c, "orbit", (120, 230, 255), (40, 80, 170), "Titanic")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.0
    return c


def anims(c):
    swimmer_anims(c, ["Spine1", "Spine2", "Spine3", "Spine4"], amp=9, axis="pitch", hover=0.45)


VARIANTS = {"Abyss": {BLUE: C(30, 30, 45), BLUE2: C(15, 15, 25), BELLY: C(80, 70, 120), FIN: C(90, 60, 160), GLOWC: C(200, 120, 255)}}
