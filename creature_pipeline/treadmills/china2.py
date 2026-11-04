"""TIER 2, RED LACQUER TREADMILL: smooth glossy red lacquer side panels with gold cloud-swirl trim, a black belt
with gold edge strips, a red lacquer console with three round gold coin buttons and a square-hole coin emblem,
black lacquer feet and small red tassels hanging off the handle ends."""
from tm import *

RED_, RED2, BLACK, GOLDL, GOLD2_, SCREEN = C(200, 25, 30), C(150, 15, 22), C(30, 26, 28), C(255, 200, 60), C(214, 150, 30), C(40, 30, 32)


def build():
    c = tread("China2")
    swirl = filigree(GOLDL, scale=1.3, width=0.05)
    deck(c, BLACK, RED_, roller=BLACK, rims=False)
    # gold edge strips flush with the belt top
    for s in (-1, 1):
        rbox(c, V(s * 2.6, DECK_TOP - 0.05, 0), (0.1, 0.05, DECK_HL), GOLDL, bevel=0.03, seg=1, stud=False)
    # glossy red lacquer side panels with gold swirl trim and a gold rim along the top
    for s in (-1, 1):
        rbox(c, V(s * 3.25, 0.85, 0), (0.55, 0.85, 10.6), RED_, bevel=0.3, paint=swirl)
        rbox(c, V(s * 3.25, 1.72, 0), (0.6, 0.08, 10.65), GOLDL, bevel=0.06, seg=1, stud=False)
        for z in (-10.2, 10.2):
            E(c, V(s * 3.25, 0.18, z), (0.55, 0.18, 0.55), BLACK, R, seg=(10, 5))   # black lacquer feet
            E(c, V(s * 3.25, 1.85, z), (0.42, 0.3, 0.42), GOLDL, R, seg=(10, 6), stud=False)   # gold corner caps
        for z in (-6.5, -1.0, 4.5):
            cloud_scroll(c, V(s * 3.82, 0.9, z), 0.62, GOLDL, stud=False)
    rbox(c, V(0, 0.4, 10.75), (3.0, 0.4, 0.3), RED_, bevel=0.2, paint=swirl)     # back end cap
    # console: red lacquer uprights + head, dark screen, coin buttons and the coin emblem
    sc, hc, n = console(c, RED_, SCREEN, post=RED2, head_half=(3.0, 0.9, 0.75), body_paint=swirl)
    up = grot(-28, 0, 0) @ V(0, 1, 0)
    for j, dx in enumerate((-0.9, 0.0, 0.9)):
        coin(c, B(sc + n * 0.06 + up * -0.95 + V(dx, 0, 0)), 0.22, R, facing=(n.x, n.y, n.z))
    emb = hc + V(0, 1.6, 0.0)
    coin(c, B(emb), 0.8, R, facing=(0, 0.25, 1))
    coin(c, B(emb), 0.8, R, facing=(0, 0.25, -1))
    for sx in (-1, 1):
        tassel(c, hc + V(sx * 2.9, -0.5, 0.4), RED_, cap=GOLDL, size=0.5)
    rails(c, RED2, r=0.26)
    # little red tassels hanging off the handles
    for s in (-1, 1):
        for z in (-6.0, -1.5):
            tassel(c, V(s * 3.05, 4.4, z), RED_, cap=GOLDL, size=0.42)
    return c
