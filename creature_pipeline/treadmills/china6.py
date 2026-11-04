"""TIER 6, GOLDEN PAGODA TREADMILL: a gold frame, red lacquer pillars at the console end holding a 2-tier pagoda
roof with green tiles, gold upturned eave tips and little bells hanging from every corner (over the console only),
and gold dragon-head finials on the rail ends."""
from tm import *

GOLDT, GOLD2T, REDP, GREEN, GREEN2, BLACK, SCREEN, EYE = (C(250, 195, 55), C(205, 145, 30), C(195, 30, 35), C(60, 150, 90),
                                                         C(35, 110, 65), C(40, 32, 30), C(255, 215, 120), C(255, 80, 50))


def build():
    c = tread("China6")
    deck(c, BLACK, GOLDT, roller=GOLD2T, belt_paint=bands(C(70, 55, 40), "z", period=1.0, width=0.1))
    skirt(c, GOLD2T, paint=filigree(GOLDT, scale=1.5, width=0.05))
    sc, hc, n = console(c, GOLDT, C(60, 20, 20), glow=SCREEN, post=GOLD2T, head_half=(3.0, 0.85, 0.75), body_paint=filigree(GOLD2T, scale=1.6, width=0.05))
    # red pillars at the console end (behind the console, z < -7) holding the pagoda roof
    for sx in (-1, 1):
        for z in (-11.0, -7.6):
            cyl(c, V(sx * 3.7, 0.3, z), V(sx * 3.7, 8.9, z), 0.32, REDP, seg=12)
            E(c, V(sx * 3.7, 0.25, z), (0.5, 0.25, 0.5), GOLDT, R, seg=(10, 5))
            E(c, V(sx * 3.7, 8.95, z), (0.45, 0.22, 0.45), GOLDT, R, seg=(10, 5), stud=False)
    rbox(c, V(0, 9.15, -9.3), (4.1, 0.22, 2.0), REDP, bevel=0.12)
    roof(c, V(0, 9.85, -9.3), 4.3, 2.35, 0.95, GREEN, GOLDT, GOLDT, tile2=GREEN2)
    rbox(c, V(0, 10.75, -9.3), (2.4, 0.5, 1.1), REDP, bevel=0.15)
    roof(c, V(0, 11.6, -9.3), 3.0, 1.7, 0.8, GREEN, GOLDT, GOLDT, bell_y=0.5, tile2=GREEN2)
    T(c, [V(0, 12.2, -9.3), V(0, 13.6, -9.3)], [0.18, 0.06], GOLDT, R, seg=8, sub=1, stud=False)
    E(c, V(0, 12.5, -9.3), (0.32, 0.32, 0.32), GOLDT, R, seg=(10, 6), stud=False)
    ends = rails(c, GOLDT, r=0.26)
    # gold dragon-head finials on the rail ends
    for e in ends:
        s = 1 if e.x > 0 else -1
        hd = e + V(0, 0.25, 0.25)
        E(c, hd, (0.36, 0.34, 0.42), GOLDT, R, seg=(10, 7))
        T(c, [hd + V(0, -0.02, 0.25), hd + V(0, -0.08, 0.75)], [0.24, 0.17], GOLDT, R, seg=8, sub=1)
        E(c, hd + V(0, -0.2, 0.55), (0.18, 0.08, 0.28), GOLD2T, R, seg=(8, 4))
        for sx in (-1, 1):
            S(c, hd + V(sx * 0.15, 0.25, -0.05), hd + V(sx * 0.3, 0.6, -0.4), 0.08, GOLD2T, R, seg=4, n=3, stud=False)
            E(c, hd + V(sx * 0.22, 0.12, 0.3), (0.07, 0.07, 0.05), EYE, R, seg=(6, 4), glow=True)
    return c
