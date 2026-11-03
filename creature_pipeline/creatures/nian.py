"""NIAN (Special, Nian Night Raids): the New Year beast that raids at night. A huge heavy red beast with gold scale
paint, a shaggy gold and orange mane, one great curved gold horn on its brow, a broad lion-ox face with a roaring
jaw of fangs, glowing gold angry eyes, gold cloud markings on its legs, clawed paws and a spiked tail with a flame
tuft. Fierce."""
from cn import *
from detail import *

REDN, REDN2, GOLDN, GOLDN2, MANEN, MANEN2, CREAMN, CLAWN, EYE = (C(200, 30, 35), C(140, 15, 25), C(255, 200, 60), C(214, 150, 30),
                                                               C(255, 170, 40), C(255, 110, 30), C(250, 225, 170), C(250, 245, 230), C(255, 215, 60))


def build():
    c = detailed("Nian", height=16)
    scl = scale_paint(GOLDN2, size=0.6, width=0.06)
    k = fierce_quad(c, REDN, belly=CREAMN, sh=4.9, hip=4.6, L=2.1, W=1.45, neck=(0.85, 0.85), head=1.8, tail=4, tail_len=0.95,
                    body_r=1.6, leg_r=(0.95, 0.75, 0.62), paw=(0.85, 0.42, 1.0), paw_col=REDN2, paint=scl, hump=0.4)
    hb, sh, cz = k["hb"], k["sh"], k["cz"]
    for s, X in ((-1, "L"), (1, "R")):
        claws3(c, k["paw" + X] + V(0, 0, -0.35), CLAWN, "Fore" + X, size=0.32)
        claws3(c, k["foot" + X] + V(0, 0, -0.35), CLAWN, "Shin" + X, size=0.28)
        for f, bone in ((k["elb" + X], "Fore" + X), (k["knee" + X], "Shin" + X)):
            fur_line(c, [f + V(0, 0.1, 0.2), f + V(0, -0.3, 0.4)], MANEN, bone, length=0.6, width=0.42, out=V(0, -0.3, 1), n_per=3, seed=181 + s)
    # head: broad lion-ox face
    E(c, hb + V(0, 0.15, -0.55), (1.25, 1.1, 1.15), REDN, "Head", seg=(12, 9), paint=scl)
    E(c, hb + V(0, -0.3, -1.45), (0.85, 0.58, 0.65), REDN2, "Head", seg=(10, 7))
    E(c, hb + V(0, -0.02, -2.02), (0.36, 0.22, 0.16), C(40, 15, 15), "Head", stud=False)
    E(c, hb + V(0, -1.0, -1.3), (0.7, 0.26, 0.7), CREAMN, "Jaw", seg=(8, 5))
    maw(c, hb + V(0, -0.62, -1.85), 0.58, 0.75, 0.55, "Head", "Jaw", n=9, tooth=0.2, fangs=2.4)
    eyes_pair(c, hb + V(0, 0.45, -1.45), 0.58, 0.3, "Head", glow=EYE, core=C(255, 250, 210), brow=REDN2, slant=26, turn=0.55)
    # one great curved gold horn
    swept_horn(c, [hb + V(0, 1.0, -1.0), hb + V(0, 1.8, -1.15), hb + V(0, 2.6, -0.85), hb + V(0, 3.0, -0.2)], 0.42, GOLDN, "Head", seg=8, ribs=True)
    for s in (-1, 1):
        S(c, hb + V(s * 0.95, 0.75, -0.2), hb + V(s * 1.5, 1.2, 0.3), 0.32, REDN2, "Head", seg=4, n=3)   # ears
    # shaggy gold and orange mane
    mc = hb + V(0, 0.0, 0.0)
    fur(c, mc, (1.7, 1.6, 1.3), MANEN, ["Neck", "Head"], n=170, length=1.3, width=0.7, flow=lambda p, n: (p - mc).normalized() * 0.5 + V(0, -0.1, 1),
        where=lambda u, p: u.z > -0.45, col2=MANEN2, mix=0.35, seed=183, lift=0.6)
    fur(c, k["nb"] + V(0, -0.2, 0.1), (1.3, 1.2, 1.1), MANEN, ["Chest", "Neck"], n=60, length=1.0, width=0.6, flow=V(0, -0.6, 0.6), where=lambda u, p: u.y < 0.3, col2=GOLDN, seed=184)
    # spiked tail with a flame tuft
    tp = k["tail"]
    T(c, tp, [0.42, 0.36, 0.3, 0.24, 0.18], REDN, ["Tail%d" % (i + 1) for i in range(4)], seg=8, paint=scl)
    for i in range(1, 4):
        S(c, tp[i] + V(0, 0.3, 0), tp[i] + V(0, 0.85, 0.3), 0.18, GOLDN, "Tail%d" % (i + 1), seg=4, n=3)
    for j in range(4):
        c.leaf(B(tp[-1]), B(V((j - 1.5) * 0.4, 0.5, 1)), B(V(0, 1, 0)), 1.1, 0.5, MANEN if j % 2 else MANEN2, "Tail4", thick=0.1, shape="flame", glow=True)
    aura(c, "orbit", (255, 60, 40), (255, 210, 60), "Secret")
    c.extra["speed"] = 1.15
    return c


def anims(c):
    fierce_anims(c, tail=4, stride=24, bob=0.18, head_amp=0.8)


VARIANTS = {"Shadow": {REDN: C(45, 40, 60), REDN2: C(28, 25, 40), MANEN: C(170, 80, 255), MANEN2: C(110, 50, 200), GOLDN: C(220, 220, 240)}}
