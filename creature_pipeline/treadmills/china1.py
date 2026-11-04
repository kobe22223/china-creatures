"""TIER 1, BAMBOO MAT TREADMILL: a frame of thick bamboo poles with visible nodes, lashed with rope at every joint,
a woven bamboo-mat belt, a little wooden console with a paper scroll screen, and two potted bamboo shoots at the
back corners."""
from tm import *

BAMBOO, NODE, STRAW, STRAW2, ROPE, WOOD, WOOD2, PAPER, INK, POT, LEAF, LEAF2 = (
    C(120, 175, 70), C(85, 135, 50), C(225, 195, 110), C(185, 150, 75), C(140, 95, 55), C(150, 100, 60), C(110, 70, 40),
    C(245, 235, 205), C(70, 60, 50), C(180, 90, 60), C(90, 170, 70), C(60, 130, 50))


def build():
    c = tread("China1")
    deck(c, STRAW, BAMBOO, belt_paint=crosshatch(STRAW2, period=0.7, width=0.2), roller=WOOD, rims=False)
    # side poles (the belt rims) and cross poles under the deck, rope lashed where they meet
    for s in (-1, 1):
        bamboo(c, V(s * 3.12, 0.95, -10.8), V(s * 3.12, 0.95, 10.8), 0.46, BAMBOO, NODE, every=2.6, seg=10)
        bamboo(c, V(s * 3.12, 0.42, -10.4), V(s * 3.12, 0.42, 10.4), 0.3, BAMBOO, NODE, every=2.5)
    for z in (-9.6, 0.0, 9.6):
        bamboo(c, V(-3.6, 0.42, z), V(3.6, 0.42, z), 0.28, BAMBOO, NODE, every=3.0)
        for s in (-1, 1):
            lash(c, V(s * 3.12, 0.62, z), V(0, 1, 0), 0.32, ROPE)
            E(c, V(s * 3.12, 0.12, z), (0.42, 0.14, 0.42), WOOD2, R, seg=(10, 4))   # little wooden foot pads
    # console: bamboo uprights, wooden head, paper scroll screen with dark rods
    for s in (-1, 1):
        bamboo(c, V(s * 2.45, 0.9, -9.6), V(s * 2.45, 6.2, -9.25), 0.36, BAMBOO, NODE, every=1.6)
        lash(c, V(s * 2.45, 0.95, -9.6), V(0, 0, 1), 0.4, ROPE)
        lash(c, V(s * 2.45, 5.9, -9.27), V(1, 0, 0), 0.38, ROPE)
    sc, hc, n = console(c, WOOD, PAPER, posts=False, head_half=(2.95, 0.8, 0.6), y=6.6, z=-9.3, screen_half=(2.0, 0.6),
                        body_paint=bands(WOOD2, "x", period=0.8, width=0.1))
    up = grot(-28, 0, 0) @ V(0, 1, 0)
    for sg in (-1, 1):
        cyl(c, sc + up * sg * 0.66 + n * 0.08 + V(-2.35, 0, 0), sc + up * sg * 0.66 + n * 0.08 + V(2.35, 0, 0), 0.12, WOOD2, seg=10)
        for sx in (-1, 1):
            E(c, sc + up * sg * 0.66 + n * 0.08 + V(sx * 2.4, 0, 0), (0.17, 0.17, 0.17), WOOD2, R, seg=(8, 5))
    # brush-stroke marks on the scroll (abstract ink swirls, no characters)
    for j, dx in enumerate((-1.1, 0.0, 1.1)):
        T(c, [sc + n * 0.1 + V(dx - 0.3, 0.12, 0), sc + n * 0.1 + V(dx, 0.22, 0), sc + n * 0.1 + V(dx + 0.3, 0.02, 0)], [0.05, 0.07, 0.04], INK, R, seg=5, stud=False)
    # bamboo hand rails, lashed at the corners
    rails(c, BAMBOO, r=0.26)
    for s in (-1, 1):
        lash(c, V(s * 3.12, 4.6, -6.0), V(0, 0, 1), 0.28, ROPE)
        lash(c, V(s * 3.12, 4.6, -1.5), V(0, 0, 1), 0.28, ROPE)
    # potted bamboo shoots at the back corners
    for s in (-1, 1):
        pc = V(s * 3.95, 0.0, 11.3)
        T(c, [pc + V(0, 0.25, 0), pc + V(0, 0.8, 0), pc + V(0, 1.5, 0)], [0.6, 0.78, 0.82], POT, R, seg=14, sub=2)
        ring(c, pc + V(0, 1.5, 0), V(0, 1, 0), 0.82, 0.12, C(150, 70, 45), seg=(16, 4))
        E(c, pc + V(0, 1.45, 0), (0.72, 0.1, 0.72), C(90, 60, 40), R, seg=(12, 4))
        for j, (dx, dz, h) in enumerate(((-0.25, 0.1, 4.6), (0.25, -0.15, 3.6), (0.0, 0.3, 2.8))):
            base = pc + V(dx, 1.4, dz)
            top = base + V(-s * 0.15, h, 0)
            bamboo(c, base, top, 0.14, BAMBOO, NODE, every=1.1, seg=6)
            for k, (lx, ly, lz) in enumerate(((-s * 0.9, 0.3, 0.3), (-s * 0.5, 0.2, -0.8), (-s * 0.8, 0.5, 0.0))):
                c.leaf(B(top + V(0, -0.2 * k, 0)), B(V(lx, ly, lz)), B(V(0, 1, 0)), 1.0, 0.32, LEAF if k % 2 else LEAF2, R, thick=0.08, shape="blade")
    return c
