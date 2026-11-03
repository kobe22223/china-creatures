"""BUFFALO CALF (Epic, Rice Paddy Village): chubby slate-grey water buffalo calf on short stubby legs, big
head with a pale muzzle, two small crescent horns curling back, little droopy ears, a red scarf bib with a
bronze bell and a tufted tail. Cute: flat black eyes."""
from cn import *

GREY, GREY2, BELLY, MUZ, HORN, HOOF, NOSE = (C(110, 118, 135), C(84, 90, 106), C(160, 166, 180), C(196, 188, 190),
                                              C(235, 225, 200), C(55, 55, 66), C(70, 60, 66))


def build():
    c = Creature("BuffaloCalf", height=6.5)
    k = cute_quad(c, GREY, belly=BELLY, paw=HOOF, body=(1.6, 1.28, 1.9), leg_h=1.25, leg_r=0.5, head_r=1.3,
                  head_up=0.5, tail=2)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r * 1.05, r * 0.95, r * 0.95), GREY, "Head", seg=(24, 16))
    # broad pale muzzle with nostrils
    c.ellipsoid(h + P(0, -0.38, -r * 0.72), (0.88, 0.6, 0.52), MUZ, "Head", seg=(20, 12))
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.3, -0.25, -r * 1.12), (0.11, 0.15, 0.05), NOSE, "Head", stud=False, smooth=True)
        c.eye(h + P(s * 0.55, 0.22, -r * 0.8), 0.24, P(s * 0.5, 0.05, -1), "Head")
        # little crescent horns: start on top of the head, curl out and back (short, so the silhouette stays round)
        b0 = h + P(s * 0.5, r * 0.78, 0.0)
        c.tube([b0, b0 + P(s * 0.38, 0.18, 0.08), b0 + P(s * 0.62, 0.22, 0.38), b0 + P(s * 0.6, 0.12, 0.65)],
               [0.22, 0.18, 0.12, 0.05], HORN, ["Head"], seg=10)
        # small droopy ears tucked under the horns
        c.leaf(h + P(s * r * 0.86, 0.32, 0.12), P(s * 1, -0.55, 0.15), P(0, 0, 1), 0.62, 0.42, GREY2, "Head",
               thick=0.16, shape="blade", curl=-0.15)
    # red scarf bib on the chest under the chin, with a bronze bell
    bib = P(0, k["by"] - 0.3, -k["rz"] * 0.97)
    c.ellipsoid(bib, (1.15, 0.62, 0.38), RED, "Chest", seg=(16, 10))
    bell(c, bib + P(0, -0.38, -0.42), 0.36, "Chest")
    # tufted tail
    t = P(0, k["by"] + 0.25, k["rz"] * 0.95)
    c.tube([t, t + P(0, -0.3, 0.35), t + P(0, -0.9, 0.45)], [0.11, 0.09, 0.07], GREY2, ["Tail1", "Tail2"], seg=8)
    c.ellipsoid(t + P(0, -1.05, 0.45), (0.18, 0.26, 0.18), GREY2, "Tail2", seg=(10, 8))
    aura(c, "sparkle", (110, 210, 150), (255, 210, 80), "Epic")
    c.extra["speed"] = 0.95
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (0, 0, 16 * sin(3 * p)), "Head": (4 * sin(2 * p), 0, 6 * sin(p))}
    quad_anims(c, tail=2, stride=24, bob=0.1, extra=extra)


# Ink-and-gold calf: near-black with gold horns and a jade collar
VARIANTS = {"Ink": {GREY: C(52, 52, 62), GREY2: C(34, 34, 42), BELLY: C(96, 96, 110), MUZ: C(150, 140, 150),
                    HORN: C(255, 200, 60), RED: C(70, 180, 120)}}
