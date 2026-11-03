"""GOLDEN EMPEROR DRAGON (Exclusive, Robux): the emperor's own dragon. A floating long serpentine dragon in
polished gold scales with deep gold edges, an ivory belly, a red and gold mane, a royal gold crown with jade gems,
jade gems running down its spine, branched gold antlers, long whiskers, a big glowing pearl in its claws and
glowing jade eyes. Hovers. Royal: glowing eyes."""
from cn import *
from detail import V, B, E, crown

GOLDE, GOLDE2, IVORY, MANEE, ANTLER, WHISK, JADEE, PEARL, CLAWE = (C(255, 200, 50), C(214, 150, 30), C(255, 245, 220), C(214, 32, 40),
                                                                 C(255, 225, 120), C(255, 240, 200), C(60, 230, 150), C(250, 245, 255), C(255, 250, 235))


def build():
    c = Creature("GoldenEmperorDragon", height=9)
    k = serpent_dragon(c, GOLDE, IVORY, MANEE, CLAWE, ANTLER, WHISK, JADEE, L=9.5, n=7, y0=3.6, wave=0.9, rise=0.6,
                       paint=scale_paint(GOLDE2, size=0.45, width=0.07), horns="antler", seed=191, brow=GOLDE2, core=C(220, 255, 235))
    pts, radii, names, hb, hs = k["pts"], k["radii"], k["names"], k["hb"], k["hs"]
    crown(c, hb + V(0, 0.95 * hs, -0.6 * hs), 0.55 * hs, 0.35 * hs, GOLDE, "Head", n=5, gem=JADEE, tall=1.7, tilt=(-10, 0, 0))
    for i in range(1, len(pts) - 1):
        E(c, pts[i] + V(0, radii[i] * 1.0, 0), (radii[i] * 0.3, radii[i] * 0.3, radii[i] * 0.3), JADEE, names[i], seg=(8, 5), glow=True)
    E(c, pts[1] + V(0, -0.35, -1.15), (0.55, 0.55, 0.55), PEARL, ["ArmL", "ArmR"], seg=(14, 10), glow=True)
    aura(c, "orbit", (255, 215, 60), (60, 230, 150), "Godly")
    c.extra["royal"] = True
    c.extra["hover"] = 1
    c.extra["speed"] = 1.3
    return c


def anims(c):
    serpent_anims(c, ["Spine%d" % (i + 1) for i in range(7)], amp=10, hover=0.55,
                  extra=lambda t, w: {"ArmL": (-35, 0, 10), "ArmR": (-35, 0, -10)})


VARIANTS = {"Jade": {GOLDE: C(70, 190, 130), GOLDE2: C(40, 130, 85), MANEE: C(255, 200, 60), JADEE: C(255, 210, 60)}}
