"""TIER 8, PHOENIX FIRE TREADMILL: the phoenix's head and flame crest form the console, looking back at the
runner with glowing eyes; its wings spread along both sides as the rails with long layered feathers tipped in
flame; its tail feathers fan up high behind the belt. Glow: flame-feather tips and the eyes."""
from tm import *

ORANGE, RED_, RED2, GOLDF, YELLOW, BELT, EYE, FLAME = (C(255, 130, 30), C(215, 45, 35), C(160, 25, 25), C(255, 200, 60),
                                                      C(255, 225, 90), C(60, 30, 25), C(255, 120, 30), C(255, 230, 90))


def build():
    c = tread("China8")
    deck(c, BELT, RED_, roller=RED2, belt_paint=bands(C(90, 40, 30), "z", period=0.9, width=0.12))
    skirt(c, RED2, paint=filigree(GOLDF, scale=1.6, width=0.05))
    # the console: a red plate the phoenix rests its chest on
    sc, hc, n = console(c, RED_, C(50, 20, 20), post=ORANGE, head_half=(2.8, 0.75, 0.7), y=5.8, z=-9.3,
                        body_paint=scale_paint(GOLDF, size=0.35, width=0.08))
    # head + flame crest, built facing -z then turned to look at the runner
    hb = V(0, 7.6, -10.4)
    n0 = len(c.shapes)
    E(c, hb + V(0, 0, -0.4), (1.25, 1.2, 1.25), ORANGE, R, seg=(16, 12))
    E(c, hb + V(0, -0.45, -0.75), (1.0, 0.7, 0.95), YELLOW, R, seg=(14, 8))
    T(c, [hb + V(0, 0.0, -1.5), hb + V(0, -0.2, -2.2), hb + V(0, -0.55, -2.55)], [0.42, 0.22, 0.05], GOLDF, R, seg=10, sub=2)
    eyes_pair(c, hb + V(0, 0.3, -1.35), 0.55, 0.26, R, glow=EYE, core=C(255, 245, 200), brow=RED2, slant=22, turn=0.5)
    for j in range(7):
        a = (j - 3) * 0.28
        base = hb + V(a * 0.6, 1.0, -0.3 + abs(a) * 0.3)
        tip = base + V(a * 1.2, 1.9 - 0.25 * abs(j - 3), 1.1)
        T(c, [base, base.lerp(tip, 0.5) + V(0, 0.2, -0.2), tip], [0.16, 0.13, 0.05], RED_ if j % 2 else ORANGE, R, seg=6, sub=2)
        c.leaf(B(tip), B(V(a, 0.7, 0.6)), B(V(1, 0, 0)), 0.75, 0.35, FLAME, R, thick=0.08, shape="flame", glow=True)
    turn_around(c, n0, hb)
    T(c, [V(0, 5.6, -9.6), hb + V(0, -0.6, 0.2)], [0.9, 0.85], ORANGE, R, seg=12, sub=1)   # neck into the console
    # wings spread along both sides as the rails: a wing arm + long layered feathers with flame tips
    for s in (-1, 1):
        arm = [V(s * 2.4, 6.0, -9.0), V(s * 3.2, 5.6, -7.5), V(s * 3.4, 4.8, -4.0), V(s * 3.45, 4.2, 0.5), V(s * 3.5, 3.4, 4.0)]
        T(c, arm, [0.42, 0.4, 0.36, 0.3, 0.2], RED_, R, seg=10, sub=3, paint=scale_paint(GOLDF, size=0.3, width=0.08))
        for i in range(10):
            t = i / 9
            p = arm[1].lerp(arm[-1], t)
            ln = 2.4 - 0.9 * t
            d = V(s * 0.7, -1.0, 0.55 + 0.4 * t)
            c.leaf(B(p), B(d), B(V(0, 0, 1)), ln, 0.75, [ORANGE, RED_, GOLDF][i % 3], R, thick=0.12, shape="feather")
            tipp = p + d.normalized() * ln * 0.95
            c.leaf(B(tipp), B(d), B(V(0, 0, 1)), 0.45, 0.35, FLAME, R, thick=0.08, shape="flame", glow=True)
        cyl(c, V(s * 3.5, 3.4, 4.0), V(s * 3.5, 1.3, 4.6), 0.18, RED2, seg=8)
    # tail feathers fanning up high behind the belt (all of it at z >= 10.3)
    t0 = V(0, 1.2, 10.9)
    for j in range(7):
        a = math.radians(-60 + j * 20)
        tip = t0 + V(math.sin(a) * 3.4, 4.2 + 2.6 * math.cos(a), 1.0)
        mid = t0.lerp(tip, 0.5) + V(0, 0.4, 0.5)
        T(c, [t0, mid, tip], [0.22, 0.2, 0.08], [RED_, ORANGE, GOLDF][j % 3], R, seg=8, sub=3, flat=(1.0, 0.5))
        c.leaf(B(tip), B(V(math.sin(a) * 0.4, 1, 0.3)), B(V(1, 0, 0)), 1.0, 0.55, FLAME, R, thick=0.08, shape="flame", glow=True)
        E(c, tip + V(0, -0.35, 0), (0.28, 0.32, 0.12), GOLDF, R, seg=(10, 6), stud=False)
    return c
