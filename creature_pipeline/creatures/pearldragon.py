"""PEARL DRAGON (Omega, Dragon King's Palace): a young floating sea dragon. A long pearly-aqua serpentine body with
a pale pink belly, seafoam mane, small swept horns, curling whiskers, short clawed legs, glowing aqua eyes and a
big glowing pearl held in front of its chest. Hovers. Royal: glowing eyes."""
from cn import *
from detail import V, B, E

AQUA, AQUA2, BELLY, FOAM, HORN, WHISK, PEARL, CLAWC = (C(110, 210, 210), C(70, 160, 175), C(255, 215, 220), C(235, 255, 250),
                                                      C(255, 230, 180), C(255, 240, 220), C(250, 245, 255), C(240, 240, 240))


def build():
    c = Creature("PearlDragon", height=7)
    k = serpent_dragon(c, AQUA, BELLY, FOAM, CLAWC, HORN, WHISK, C(120, 255, 240), L=8.0, n=6, y0=3.2, wave=0.7, rise=0.45,
                       paint=scale_paint(AQUA2, size=0.42, width=0.07), horns="swept", seed=151, brow=AQUA2)
    p1 = k["pts"][1]
    E(c, p1 + V(0, -0.2, -1.2), (0.55, 0.55, 0.55), PEARL, ["ArmL", "ArmR"], seg=(14, 10), glow=True)
    aura(c, "orbit", (140, 240, 240), (255, 220, 230), "Omega")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.25
    return c


def anims(c):
    serpent_anims(c, ["Spine%d" % (i + 1) for i in range(6)], amp=10, hover=0.5,
                  extra=lambda t, w: {"ArmL": (-35, 0, 10), "ArmR": (-35, 0, -10)})


VARIANTS = {"Coral": {AQUA: C(255, 140, 120), AQUA2: C(220, 90, 90), BELLY: C(255, 235, 200), FOAM: C(255, 220, 150)}}
