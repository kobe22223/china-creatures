"""TIER 9, MOON PALACE TREADMILL: a round silver moon gate arch behind the console with a full glowing moon disc
inside it, a little jade rabbit statue sitting on the console, osmanthus sprigs with tiny gold flowers, lavender
lacquer sides with silver cloud scrolls along the rails, all in silver, lavender and pale gold. Glow: the moon disc."""
from tm import *

SILVER, SILVER2, LAV, LAV2, PGOLD, MOON, JADER, JADER2, BRANCH, LEAFO, BELT = (
    C(215, 220, 235), C(170, 175, 195), C(180, 160, 220), C(140, 120, 190), C(240, 215, 140), C(255, 245, 205),
    C(170, 230, 200), C(110, 190, 150), C(110, 80, 60), C(80, 150, 90), C(70, 60, 95))


def osmanthus(c, base, d, s):
    """branch sprig with leaves and clusters of tiny gold flowers"""
    tip = base + d
    T(c, [base, base.lerp(tip, 0.5) + V(0, 0.25, 0), tip], [0.1, 0.08, 0.04], BRANCH, R, seg=6, sub=2)
    for k in range(4):
        p = base.lerp(tip, 0.3 + 0.2 * k)
        c.leaf(B(p), B(V(s * 0.6, 0.5 - 0.3 * (k % 2), 0.3)), B(V(0, 1, 0)), 0.55, 0.25, LEAFO, R, thick=0.06, shape="blade")
        for m in range(3):
            E(c, p + V(s * 0.1 * m, 0.12 + 0.08 * m, 0.1 * (m - 1)), (0.07, 0.07, 0.07), PGOLD, R, seg=(6, 4), stud=False)


def build():
    c = tread("China9")
    deck(c, BELT, SILVER, roller=SILVER2, belt_paint=bands(C(90, 80, 120), "z", period=1.1, width=0.1))
    for s in (-1, 1):
        rbox(c, V(s * 3.55, 0.75, 0), (0.45, 0.75, 10.7), LAV, bevel=0.3)
        for z in (-6.0, 1.0, 8.0):
            cloud_scroll(c, V(s * 4.02, 0.85, z - 0.9), 0.6, SILVER, stud=False)
    rbox(c, V(0, 0.5, 10.9), (3.9, 0.5, 0.3), LAV, bevel=0.2)
    # moon gate arch + glowing full moon behind the console
    gc = V(0, 6.3, -11.4)
    ring(c, gc, V(0, 0, 1), 4.0, 0.48, SILVER, seg=(42, 5))
    ring(c, gc + V(0, 0, 0.3), V(0, 0, 1), 4.0, 0.16, PGOLD, seg=(36, 5), stud=False)
    E(c, gc + V(0, 0, -0.15), (3.45, 3.45, 0.12), MOON, R, seg=(28, 6), glow=True)
    for s in (-1, 1):
        rbox(c, V(s * 3.7, 1.0, -11.4), (0.75, 1.0, 0.75), SILVER2, bevel=0.25)
        E(c, V(s * 3.7, 2.1, -11.4), (0.55, 0.2, 0.55), PGOLD, R, seg=(10, 5), stud=False)
    sc, hc, n = console(c, LAV, C(60, 55, 90), post=SILVER2, head_half=(3.0, 0.85, 0.72), body_paint=filigree(SILVER, scale=1.6, width=0.05))
    # little jade rabbit statue sitting on the console
    rb = hc + V(0.9, 1.0, -0.1)
    E(c, rb + V(0, 0.45, 0), (0.48, 0.55, 0.55), JADER, R, seg=(12, 8))
    E(c, rb + V(0, 1.15, 0.1), (0.4, 0.38, 0.38), JADER, R, seg=(12, 8))
    for sx in (-1, 1):
        T(c, [rb + V(sx * 0.15, 1.4, 0.1), rb + V(sx * 0.2, 2.0, 0.25)], [0.1, 0.06], JADER2, R, seg=6, sub=1)
        E(c, rb + V(sx * 0.15, 1.2, 0.42), (0.05, 0.06, 0.03), C(40, 60, 50), R, seg=(6, 4), stud=False)
    E(c, rb + V(0, 0.2, -0.5), (0.18, 0.18, 0.18), JADER2, R, seg=(8, 5))
    E(c, rb + V(0, -0.05, 0), (0.6, 0.12, 0.6), PGOLD, R, seg=(12, 4), stud=False)
    # osmanthus sprigs at the console and the back corners
    for s in (-1, 1):
        osmanthus(c, V(s * 3.0, 6.9, -9.4), V(s * 1.0, 1.2, 0.3), s)
        osmanthus(c, V(s * 3.8, 1.4, 10.6), V(s * 0.6, 2.2, 0.4), s)
    rails(c, SILVER, r=0.25)
    for s in (-1, 1):
        for z in (-5.0, -2.5):
            cloud_scroll(c, V(s * 3.3, 4.6, z), 0.42, SILVER2, stud=False)
    return c
