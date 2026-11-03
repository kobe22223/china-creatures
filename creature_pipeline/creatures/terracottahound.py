"""TERRACOTTA HOUND (Cosmic, Terracotta Tomb): a little terracotta clay hound come to life. Round orange-brown
clay body on short stubby legs, big head with a carved muzzle and folded ears, faint cracks and traces of old red
and black paint, a small grey clay armour plate on its back and a curled tail. Cute: flat black eyes."""
from cn import *
from detail import cracks

CLAY, CLAY2, CLAY3, CRACK, PAINT, PLATE, PLATE2 = (C(196, 120, 80), C(160, 92, 60), C(220, 160, 120), C(120, 70, 45),
                                                   C(170, 50, 40), C(140, 130, 120), C(110, 100, 92))


def build():
    c = Creature("TerracottaHound", height=6)
    crk = cracks(CRACK, scale=2.8, width=0.018)
    k = cute_quad(c, CLAY, belly=CLAY3, paw=CLAY2, body=(1.45, 1.2, 1.8), leg_h=1.1, leg_r=0.45, head_r=1.3, head_up=0.55, tail=2, paint=crk)
    h, r = k["head"], k["head_r"]
    by, ry, rz = k["by"], k["ry"], k["rz"]
    c.ellipsoid(h, (r * 1.02, r * 0.95, r), CLAY, "Head", seg=(24, 16), paint=crk)
    c.tube([h + P(0, -0.25, -r * 0.6), h + P(0, -0.3, -r * 1.15)], [0.55, 0.42], CLAY3, ["Head"], seg=16, sub=1)
    c.ellipsoid(h + P(0, -0.12, -r * 1.25), (0.2, 0.14, 0.12), CRACK, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.eye(h + P(s * 0.48, 0.22, -r * 0.84), 0.23, P(s * 0.45, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.75, -0.3, -r * 0.58), (0.2, 0.12, 0.08), PAINT, "Head", stud=False)   # faded red paint cheeks
        # folded ears hanging forward
        e0 = h + P(s * 0.75, r * 0.72, 0.05)
        c.leaf(e0, P(s * 0.7, 0.35, -0.6), P(0, 1, 0), 0.75, 0.55, CLAY2, "Head", thick=0.22, shape="blade", curl=-0.3)
    # small armour plate on the back: clay scales with a black-paint trim
    c.ellipsoid(P(0, by + ry * 0.72, 0.0), (k["rx"] * 0.85, 0.42, rz * 0.62), PLATE, ["Hips", "Chest"], seg=(18, 8),
                paint=stripes(PLATE2, "z", period=0.4, width=0.08, wobble=0))
    c.torus(P(0, by + ry * 0.7, 0.0), k["rx"] * 0.82, 0.07, C(40, 36, 34), ["Hips", "Chest"], rot=Matrix.Diagonal((1, rz * 0.62 / (k["rx"] * 0.82), 1)), seg=(28, 4), stud=False)
    # curled tail
    t = P(0, by + 0.35, rz * 0.95)
    c.tube([t, t + P(0, 0.5, 0.3), t + P(0, 0.85, 0.05), t + P(0, 0.65, -0.2)], [0.22, 0.2, 0.17, 0.12], CLAY, ["Tail1", "Tail2"], seg=10, paint=crk)
    aura(c, "orbit", (230, 140, 80), (255, 220, 160), "Cosmic")
    c.extra["speed"] = 1.15
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (0, 0, 22 * sin(3 * p)), "Head": (4 * sin(2 * p), 0, 8 * sin(p))}
    quad_anims(c, tail=2, stride=28, bob=0.12, extra=extra)


VARIANTS = {"Painted": {CLAY: C(214, 70, 60), CLAY2: C(160, 40, 35), CLAY3: C(250, 225, 190), PLATE: C(40, 40, 45), PLATE2: C(255, 200, 60), PAINT: C(255, 255, 255)}}
