"""DRAGON KING (Zone 10 guardian, Omega): the Dragon King of the Eastern Sea. A huge long serpentine sea dragon,
deep teal-blue scales with gold edges, a pearl belly, a flowing seafoam mane and spiny gold back fins, branched gold
antlers, a royal gold crown with jade gems, long whiskers, roaring jaws, glowing gold angry eyes and short clawed
legs. Hovers. Fierce."""
from cn import *
from detail import V, B, E, crown

TEAL, TEAL2, BELLY, FOAM, GOLDK, WHISK, JADEK, CLAWC = (C(30, 110, 140), C(18, 75, 100), C(235, 240, 230), C(170, 240, 230),
                                                      C(255, 200, 60), C(255, 240, 200), C(80, 230, 150), C(250, 245, 230))


def build():
    c = Creature("DragonKing", height=18)
    c.stud = c.height / 44 * 0.55
    c.stud_k = 0.65
    k = serpent_dragon(c, TEAL, BELLY, FOAM, CLAWC, GOLDK, WHISK, C(255, 210, 50), L=16.0, n=8, y0=5.5, wave=1.4, rise=0.9,
                       paint=scale_paint(GOLDK, size=0.7, width=0.06), horns="antler", fins=GOLDK, seed=161, brow=TEAL2)
    hb, hs = k["hb"], k["hs"]
    crown(c, hb + V(0, 0.95 * hs, -0.6 * hs), 0.55 * hs, 0.35 * hs, GOLDK, "Head", n=5, gem=JADEK, tall=1.6, tilt=(-10, 0, 0))
    aura(c, "orbit", (80, 230, 200), (255, 210, 60), "Omega")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.1
    return c


def anims(c):
    serpent_anims(c, ["Spine%d" % (i + 1) for i in range(8)], amp=9, hover=0.7)


VARIANTS = {"Crimson": {TEAL: C(170, 30, 40), TEAL2: C(110, 15, 25), FOAM: C(255, 200, 80), BELLY: C(255, 230, 190)}}
