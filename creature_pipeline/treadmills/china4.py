"""TIER 4, LANTERN TREADMILL: a red frame; two curved arms rise from the console holding big round red lanterns
with gold caps and gold tassels, and a string of 6 mini lanterns runs along each side from the console to a back
post. Glow: the warm orange lantern insides."""
from tm import *

RED_, RED2, GOLDL, BLACK, GLOWC, CORD = C(205, 30, 35), C(150, 18, 25), C(255, 200, 60), C(40, 30, 30), C(255, 160, 60), C(120, 70, 40)


def build():
    c = tread("China4")
    deck(c, BLACK, RED_, roller=RED2, belt_paint=bands(C(60, 45, 40), "z", period=1.0, width=0.1))
    skirt(c, RED2)
    for s in (-1, 1):
        rbox(c, V(s * 3.1, 1.25, 0), (0.42, 0.08, 10.65), GOLDL, bevel=0.06, seg=1, stud=False)
    sc, hc, n = console(c, RED_, C(60, 20, 20), post=RED2, head_half=(3.0, 0.85, 0.75), body_paint=filigree(GOLDL, scale=1.6, width=0.05))
    # two curved arms rising out of the console, each holding a big lantern
    for s in (-1, 1):
        a0 = V(s * 2.8, 6.8, -9.6)
        arm = [a0, a0 + V(s * 0.8, 1.8, -0.2), a0 + V(s * 1.5, 3.2, 0.0), a0 + V(s * 1.2, 3.9, 0.3)]
        T(c, arm, [0.26, 0.24, 0.2, 0.18], RED2, R, seg=10, sub=3)
        E(c, arm[-1], (0.28, 0.28, 0.28), GOLDL, R, seg=(10, 6), stud=False)
        T(c, [arm[-1], arm[-1] + V(0, -0.6, 0)], [0.05, 0.05], CORD, R, seg=6, sub=1)
        red_lantern(c, arm[-1] + V(0, -1.55, 0), 0.95, GLOWC, body=RED_, cap=GOLDL, tassel_col=GOLDL)
    # back posts + a string of 6 mini lanterns along each side
    for s in (-1, 1):
        x = 3.55
        cyl(c, V(s * x, 0.4, 10.4), V(s * x, 5.4, 10.4), 0.28, RED2, seg=10)
        E(c, V(s * x, 5.5, 10.4), (0.32, 0.32, 0.32), GOLDL, R, seg=(10, 6), stud=False)
        a, b = V(s * x, 5.4, -9.0), V(s * x, 5.4, 10.4)
        pts = [a.lerp(b, t) + V(0, -1.1 * 4 * t * (1 - t), 0) for t in [i / 8 for i in range(9)]]
        T(c, pts, [0.05] * 9, CORD, R, seg=5, sub=2, stud=False)
        for i in range(6):
            t = (i + 1) / 7
            p = a.lerp(b, t) + V(0, -1.1 * 4 * t * (1 - t), 0)
            red_lantern(c, p + V(0, -0.5, 0), 0.32, GLOWC, body=RED_, cap=GOLDL, ribs=0, seg=(10, 6))
        cyl(c, V(s * 2.6, 6.2, -9.25), V(s * x, 5.4, -9.0), 0.08, CORD, seg=6)
    rails(c, RED2, r=0.25)
    return c
