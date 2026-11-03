"""GOLDEN PHEASANT (Rare, Bamboo Grove): round scarlet pheasant with a golden crest, an orange cape barred with
dark lines, a green back, blue wings and a compact arc of long barred tail feathers. Cute: flat black eyes."""
from cn import *

RED_, GOLDC, CAPE, BAR, GREEN, BLUE, TAILC, LEGC, BEAK = (C(220, 40, 40), C(255, 200, 40), C(255, 140, 30), C(60, 40, 30),
                                                         C(40, 140, 80), C(50, 80, 180), C(205, 160, 80), C(220, 200, 150), C(255, 220, 120))


def build():
    c = Creature("GoldenPheasant", height=5.5)
    k = cute_bird(c, RED_, belly=C(240, 90, 60), leg_col=LEGC, body=(1.15, 1.12, 1.4), leg_h=0.8, head_r=0.95,
                  head_up=1.08, head_fwd=0.55, wing_col=BLUE, tail=2, foot="toes")
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r, r * 0.95), GOLDC, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.3, -r * 0.35), (r * 0.9, r * 0.62, r * 0.7), RED_, "Head", seg=(18, 10))   # red face/throat
    c.tube([h + P(0, -0.05, -r * 0.82), h + P(0, -0.12, -r * 1.22)], [0.22, 0.04], BEAK, ["Head"], seg=10, sub=1)
    for s in (-1, 1):
        c.eye(h + P(s * 0.42, 0.12, -r * 0.82), 0.18, P(s * 0.5, 0.05, -1), "Head")
    # golden crest swept back over the head
    for j in range(5):
        a = (j - 2) * 0.16
        c.leaf(h + P(a, r * 0.7, -0.35 + abs(a)), P(a * 0.5, 0.45, 1), P(1, 0, 0), 1.0, 0.36, GOLDC, "Head", thick=0.14, shape="feather", curl=-0.15)
    # barred orange cape around the neck, solid collar + short feathers lying flat
    barred = stripes(BAR, "y", period=0.28, width=0.07, wobble=0.0)
    c.ellipsoid(h + P(0, -r * 0.65, 0.12), (r * 0.95, r * 0.5, r * 0.9), CAPE, ["Neck"], seg=(18, 10), paint=barred)
    # green back patch
    c.ellipsoid(P(0, k["by"] + k["ry"] * 0.55, k["rz"] * 0.15), (k["rx"] * 0.65, k["ry"] * 0.45, k["rz"] * 0.7), GREEN, ["Hips", "Chest"], seg=(16, 10))
    # long barred tail: three feathers arcing back and down, compact
    t0 = P(0, k["by"] + 0.25, k["rz"] * 0.8)
    tb = stripes(BAR, "z", period=0.32, width=0.08, wobble=0.0)
    for j in range(3):
        side = (j - 1) * 0.22
        pts = [t0 + P(side * 0.4, 0, 0), t0 + P(side, 0.85, 0.45), t0 + P(side * 1.2, 1.15, 1.1), t0 + P(side * 1.3, 0.75, 1.65)]
        c.tube(pts, [0.24, 0.24, 0.17, 0.05], TAILC, ["Tail1", "Tail2"], seg=8, flat=(0.45, 1.0), paint=tb)
    aura(c, "sparkle", (255, 200, 40), (220, 40, 40), "Rare")
    c.extra["speed"] = 1.1
    return c


def anims(c):
    bird_anims(c, tail=2, stride=30, waddle=6, bob=0.12, flap=12)


VARIANTS = {"Silver": {RED_: C(240, 240, 248), C(240, 90, 60): C(210, 215, 230), GOLDC: C(200, 210, 230), CAPE: C(150, 160, 190),
                       GREEN: C(60, 70, 110), BLUE: C(30, 40, 80), TAILC: C(170, 175, 195)}}
