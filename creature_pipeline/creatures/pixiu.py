"""PIXIU (Zone 8 guardian, Celestial): the golden winged treasure beast. A huge powerful golden lion-dragon with
cloud swirl paint, a fiery shard mane, back-swept horns, dragon whiskers and roaring jaws, glowing jade angry eyes,
jade gems on its chest and shoulders, big feathered wings folded along its back and a curled tail tuft. Fierce."""
from cn import *
from detail import *

GOLDP, GOLDP2, GOLDP3, CREAMP, MANEP, MANEP2, JADEG, CLAWC = (C(245, 190, 60), C(205, 145, 35), C(255, 225, 120), C(255, 240, 190),
                                                            C(214, 90, 30), C(255, 160, 40), C(60, 220, 150), C(255, 250, 230))


def build():
    c = detailed("Pixiu", height=17)
    swirl = filigree(GOLDP2, scale=1.1, width=0.06)
    k = fierce_quad(c, GOLDP, belly=CREAMP, sh=4.4, hip=4.1, L=2.1, W=1.4, neck=(0.9, 0.9), head=1.8, tail=3, tail_len=0.9,
                    body_r=1.55, leg_r=(0.9, 0.7, 0.6), paw=(0.8, 0.42, 0.95), paw_col=GOLDP, paint=swirl, hump=0.3)
    hb, sh, cz, mid = k["hb"], k["sh"], k["cz"], k["mid"]
    for s, X in ((-1, "L"), (1, "R")):
        claws3(c, k["paw" + X] + V(0, 0, -0.35), CLAWC, "Fore" + X, size=0.3)
        claws3(c, k["foot" + X] + V(0, 0, -0.35), CLAWC, "Shin" + X, size=0.26)
        E(c, k["sho" + X] + V(s * 0.9, 0.3, 0), (0.12, 0.2, 0.2), JADEG, "Arm" + X, seg=(6, 4), glow=True)
    E(c, V(0, sh - 0.35, cz - 1.25), (0.3, 0.3, 0.14), JADEG, "Chest", seg=(8, 5), glow=True)
    # folded feathered wings along the back
    wing_bones(c, (1.2, sh + 0.9, cz + 0.6), (2.0, sh + 1.9, cz + 1.5), (2.3, sh + 1.6, cz + 3.6))
    feather_wings(c, (1.2, sh + 0.9, cz + 0.6), (2.0, sh + 1.9, cz + 1.5), (2.3, sh + 1.6, cz + 3.6), GOLDP3, GOLDP2, cover=GOLDP, n=8,
                  length=(1.3, 0.9), width=0.85, arm_col=GOLDP2)
    dragon_head(c, hb, 1.25, GOLDP, CREAMP, GOLDP3, CREAMP, MANEP, JADEG, bone="Head", jaw="Jaw", horns="swept", mane_n=6, seed=97,
                brow=GOLDP2, core=C(220, 255, 235), beard=MANEP2)
    fur(c, hb + V(0, -0.1, 0.4), (1.5, 1.4, 1.1), MANEP, ["Neck", "Head"], n=90, length=1.1, width=0.65, flow=lambda p, n: n * 0.4 + V(0, 0.1, 1),
        where=lambda u, p: u.z > -0.3, col2=MANEP2, mix=0.35, seed=98, lift=0.6)
    tp = k["tail"]
    T(c, tp, [0.36, 0.3, 0.24, 0.2], GOLDP, ["Tail1", "Tail2", "Tail3"], seg=8)
    fur(c, tp[-1], (0.55, 0.55, 0.65), MANEP, "Tail3", n=36, length=0.75, width=0.45, flow=lambda p, n: n, col2=MANEP2, seed=99, lift=0.6)
    aura(c, "orbit", (255, 210, 60), (60, 220, 150), "Celestial")
    c.extra["speed"] = 1.1
    return c


def anims(c):
    fierce_anims(c, tail=3, stride=24, bob=0.15, head_amp=0.8, wings=True)


VARIANTS = {"Jade": {GOLDP: C(70, 180, 120), GOLDP2: C(40, 130, 85), GOLDP3: C(150, 230, 180), CREAMP: C(220, 250, 230), JADEG: C(255, 200, 60)}}
