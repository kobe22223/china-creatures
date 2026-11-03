"""TERRACOTTA HORSE (Divine, Terracotta Tomb): a round little terracotta clay horse come to life. Orange-brown clay
body on short stubby legs, big head with a cropped clay mane and a tied topknot, a painted red and black saddle with
gold studs, a knotted tail and fine hairline cracks. Cute: flat black eyes."""
from cn import *
from detail import cracks

CLAY, CLAY2, CLAY3, CRACK, SADDLE, SADDLE2, BLACKP = (C(200, 125, 82), C(160, 92, 60), C(225, 165, 120), C(120, 70, 45),
                                                     C(185, 45, 40), C(50, 40, 38), C(45, 38, 36))


def build():
    c = Creature("TerracottaHorse", height=7)
    crk = cracks(CRACK, scale=3.2, width=0.012)
    k = cute_quad(c, CLAY, belly=CLAY3, paw=CLAY2, body=(1.4, 1.18, 1.85), leg_h=1.25, leg_r=0.43, head_r=1.22, head_up=0.75, tail=3, paint=crk)
    h, r = k["head"], k["head_r"]
    by, rz = k["by"], k["rz"]
    c.ellipsoid(h, (r * 0.95, r, r * 1.05), CLAY, "Head", seg=(24, 16), paint=crk)
    c.ellipsoid(h + P(0, -0.42, -r * 0.75), (0.62, 0.55, 0.62), CLAY3, "Head", seg=(16, 10))
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.22, -0.4, -r * 1.3), (0.08, 0.12, 0.05), CRACK, "Head", stud=False, smooth=True)
        c.eye(h + P(s * 0.48, 0.22, -r * 0.84), 0.23, P(s * 0.45, 0.05, -1), "Head")
        c.leaf(h + P(s * 0.45, r * 0.82, 0.1), P(s * 0.3, 1, 0.15), P(0, 0, 1), 0.6, 0.4, CLAY2, "Head", thick=0.18, shape="blade")
    # cropped clay mane: a short ridge of blocks, with a tied topknot between the ears
    for j in range(6):
        c.box(h + P(0, r * 0.75 - j * 0.28, 0.35 + j * 0.3), (0.16, 0.2, 0.16), CLAY2, ["Head"] if j < 3 else ["Neck"], stud=False)
    c.ellipsoid(h + P(0, r * 1.05, -0.15), (0.2, 0.25, 0.2), CLAY2, "Head", seg=(10, 8))
    c.torus(h + P(0, r * 0.92, -0.15), 0.18, 0.06, SADDLE, "Head", seg=(12, 4), stud=False)
    # painted saddle with gold studs
    c.ellipsoid(P(0, by + 0.65, 0.1), (k["rx"] * 1.02, 0.55, 0.85), SADDLE, ["Hips", "Chest"], seg=(18, 8), paint=stripes(SADDLE2, "z", period=0.55, width=0.12, wobble=0))
    for j in range(5):
        a = math.radians(-60 + j * 30)
        c.ellipsoid(P(math.sin(a) * k["rx"] * 0.98, by + 0.65 + math.cos(a) * 0.35, 0.1 + 0.75), (0.08, 0.08, 0.08), GOLD, ["Hips"], seg=(8, 5), stud=False)
    # knotted tail: a short tied club
    t = P(0, by + 0.35, rz * 0.92)
    c.tube([t, t + P(0, -0.15, 0.4), t + P(0, -0.6, 0.6)], [0.25, 0.28, 0.22], CLAY2, ["Tail1", "Tail2", "Tail3"], seg=12)
    c.torus(t + P(0, -0.12, 0.38), 0.27, 0.06, SADDLE, "Tail2", rot=euler(70, 0, 0), seg=(12, 4), stud=False)
    aura(c, "sparkle", (255, 220, 120), (200, 125, 82), "Divine")
    c.extra["speed"] = 1.3
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (0, 0, 10 * sin(2 * p)), "Head": (5 * sin(2 * p), 0, 4 * sin(p))}
    quad_anims(c, tail=3, stride=30, bob=0.16, extra=extra)


VARIANTS = {"Painted": {CLAY: C(235, 225, 210), CLAY2: C(60, 55, 52), CLAY3: C(250, 245, 235), SADDLE: C(40, 90, 170), CRACK: C(160, 150, 140)}}
