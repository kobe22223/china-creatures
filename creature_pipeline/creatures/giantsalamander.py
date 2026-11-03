"""GIANT SALAMANDER (Zone 5 guardian, Secret): a huge Chinese giant salamander, broad and heavy, mottled brown
skin with dark spots and wrinkled side folds, a wide flat head with a huge gaping mouth of small sharp teeth, tiny
glowing teal angry eyes, thick sprawling legs with stubby toes and a long flat paddle tail. Fierce."""
from cn import *
from detail import *

SKIN, SKIN2, BELLY, SPOT, TOES, EYE = C(120, 90, 60), C(90, 66, 44), C(175, 150, 110), C(60, 44, 32), C(150, 120, 85), C(60, 255, 220)


def build():
    c = detailed("GiantSalamander", height=15)
    mot = spots(SPOT, size=0.55, density=0.4, seed=3)
    k = fierce_quad(c, SKIN, belly=BELLY, sh=3.4, hip=3.3, L=2.4, W=1.9, neck=(0.9, 0.0), head=1.9, tail=5, tail_len=1.1,
                    body_r=1.35, leg_r=(0.85, 0.66, 0.58), paw=(0.85, 0.32, 0.95), paw_col=SKIN2, paint=mot, hump=0.0)
    hb, sh, hip, cz, hz = k["hb"], k["sh"], k["hip"], k["cz"], k["hz"]
    TB = ["Hips", "Chest"]
    # wide flattened body overlay + wrinkled side folds
    E(c, V(0, (sh + hip) / 2, 0), (2.0, 1.15, 2.6), SKIN, TB, seg=(14, 9), paint=mot)
    for s in (-1, 1):
        for j in range(5):
            z = cz + 0.3 + j * (hz - cz) / 4
            E(c, V(s * 1.95, (sh + hip) / 2 - 0.45, z), (0.28, 0.32, 0.55), SKIN2, TB, seg=(8, 5))
    for s, X in ((-1, "L"), (1, "R")):
        for f, bone in ((k["paw" + X], "Fore" + X), (k["foot" + X], "Shin" + X)):
            for j in (-1.5, -0.5, 0.5, 1.5):
                E(c, f + V(j * 0.28, -0.05, -0.85), (0.15, 0.13, 0.25), TOES, bone, seg=(6, 4))
    # wide flat head with a gaping mouth
    E(c, hb + V(0, 0.0, -0.9), (1.75, 0.75, 1.45), SKIN, "Head", seg=(14, 8), paint=mot)
    E(c, hb + V(0, -0.85, -0.85), (1.6, 0.32, 1.35), BELLY, "Jaw", seg=(12, 6))
    maw(c, hb + V(0, -0.45, -2.2), 1.35, 1.3, 0.55, "Head", "Jaw", n=14, tooth=0.12, fangs=1.4)
    for s in (-1, 1):
        E(c, hb + V(s * 0.38, 0.35, -2.3), (0.09, 0.06, 0.06), SPOT, "Head", stud=False)   # nostrils
    eyes_pair(c, hb + V(0, 0.62, -1.4), 0.85, 0.2, "Head", glow=EYE, core=C(220, 255, 250), brow=SKIN2, slant=18, turn=0.8)
    # long flat paddle tail with a fin ridge
    tp = k["tail"]
    T(c, tp, [1.0, 0.85, 0.65, 0.45, 0.28, 0.1], SKIN, ["Tail%d" % (i + 1) for i in range(5)], seg=10, flat=(0.45, 1.0), paint=mot)
    for i in range(1, 5):
        c.leaf(B(tp[i] + V(0, 0.55 - 0.08 * i, 0)), B(V(0, 0.3, 1)), B(V(0, 0, 1)), 1.1, 0.45, SKIN2, "Tail%d" % (i + 1), thick=0.1, shape="fin")
    aura(c, "orbit", (60, 255, 220), (120, 90, 60), "Secret")
    c.extra["speed"] = 0.85
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        out = {"Root": ((0, 6 * sin(p), 0), (0, 0.06 * abs(sin(2 * p)), 0))} if walking else {}
        for i in range(5):
            out["Tail%d" % (i + 1)] = (0, (8 + 4 * i) * sin(p * (2 if walking else 1) - 0.7 * i), 0)
        return out
    fierce_anims(c, tail=5, stride=18, bob=0.06, head_amp=0.5, extra=extra)


VARIANTS = {"Albino": {SKIN: C(245, 215, 200), SKIN2: C(225, 180, 165), BELLY: C(255, 235, 225), SPOT: C(240, 160, 150), TOES: C(255, 200, 190)}}
