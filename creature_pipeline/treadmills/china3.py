"""TIER 3, JADE TREADMILL: a frame carved from pale jade with cloud-scroll reliefs along the sides, white marble
belt rims with soft grey veins, a carved jade bi disc standing on the console, gold studs at the corners and a
soft green glowing screen."""
from tm import *

JADEP, JADED, MARBLE, VEIN, BELT, GOLDJ, SCREEN = (C(150, 215, 175), C(95, 170, 130), C(245, 245, 240), C(185, 190, 195),
                                                  C(70, 120, 100), C(255, 205, 70), C(140, 255, 190))


def build():
    c = tread("China3")
    deck(c, BELT, MARBLE, rim_paint=cracks(VEIN, scale=1.6, width=0.03), roller=JADED, belt_paint=bands(C(60, 105, 88), "z", period=1.2, width=0.12))
    # carved jade side frame with cloud scrolls
    for s in (-1, 1):
        rbox(c, V(s * 3.65, 0.8, 0), (0.42, 0.8, 10.7), JADEP, bevel=0.3)
        for z in (-7.5, -2.5, 2.5, 7.5):
            cloud_scroll(c, V(s * 4.08, 0.85, z - 0.9), 0.62, JADED)
        for z in (-10.6, 10.6):
            E(c, V(s * 3.65, 1.65, z), (0.32, 0.32, 0.32), GOLDJ, R, seg=(10, 6), stud=False)   # gold corner studs
            E(c, V(s * 3.65, 0.15, z), (0.6, 0.15, 0.6), JADED, R, seg=(10, 4))
    rbox(c, V(0, 0.55, 10.85), (3.9, 0.55, 0.3), JADEP, bevel=0.2)
    sc, hc, n = console(c, JADEP, SCREEN, glow=SCREEN, post=JADED, head_half=(3.0, 0.85, 0.75))
    for s in (-1, 1):
        cloud_scroll(c, V(s * 3.05, 6.55, -9.9), 0.5, JADED)
    # carved jade bi disc standing on top of the console
    bi = hc + V(0, 2.0, -0.25)
    c.torus(B(bi), 0.85, 0.3, JADED, R, rot=euler(90, 0, 0), seg=(24, 8))
    c.torus(B(bi + V(0, 0, 0.0)), 0.85, 0.18, JADEP, R, rot=euler(90, 0, 0), seg=(24, 6))
    rbox(c, hc + V(0, 0.95, -0.25), (0.5, 0.2, 0.25), GOLDJ, bevel=0.1, stud=False)
    rails(c, JADED, r=0.25)
    for s in (-1, 1):
        E(c, V(s * 3.05, 4.6, -1.5), (0.3, 0.3, 0.3), GOLDJ, R, seg=(10, 6), stud=False)
    return c
