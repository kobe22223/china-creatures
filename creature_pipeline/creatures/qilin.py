"""QILIN (Zone 9 guardian, Titanic): a huge powerful qilin. A deer-dragon body covered in jade-green scales with
gold scale edges, a blazing orange flame mane down its neck and back, branched gold antlers, a dragon face with
whiskers and roaring jaws, glowing gold angry eyes, flame tufts at its legs, split gold hooves and a flame-tipped tail. Fierce."""
from cn import *
from detail import *

JADEQ, JADEQ2, GOLDQ, CREAMQ, FLAME1, FLAME2, HOOFQ, EYE = (C(50, 160, 120), C(30, 115, 85), C(255, 200, 60), C(240, 235, 190),
                                                          C(255, 120, 30), C(255, 200, 60), C(214, 150, 30), C(255, 220, 60))


def build():
    c = detailed("Qilin", height=17)
    scl = scale_paint(GOLDQ, size=0.55, width=0.07)
    k = fierce_quad(c, JADEQ, belly=CREAMQ, sh=4.6, hip=4.4, L=2.1, W=1.3, neck=(1.0, 1.4), head=1.8, tail=4, tail_len=0.9,
                    body_r=1.45, leg_r=(0.82, 0.62, 0.5), paw=(0.6, 0.35, 0.75), paw_col=JADEQ2, paint=scl, hump=0.2)
    hb, sh, hip, cz, hz, mid = k["hb"], k["sh"], k["hip"], k["cz"], k["hz"], k["mid"]
    for s, X in ((-1, "L"), (1, "R")):
        for f, kn, bone in ((k["paw" + X], k["elb" + X], "Fore" + X), (k["foot" + X], k["knee" + X], "Shin" + X)):
            hoof(c, f, 0.62, HOOFQ, bone)
            for j in range(3):   # flame tufts flowing back from the joints
                c.leaf(B(kn + V(0, -0.1 * j, 0.25)), B(V(s * 0.3, 0.3 - 0.3 * j, 1)), B(V(0, 1, 0)), 0.9, 0.42, FLAME1 if j % 2 else FLAME2, bone, thick=0.1, shape="flame", glow=True)
    # blazing flame mane along the neck and back
    spine_pts = [hb + V(0, 0.9, 0.3), k["nb"] + V(0, 1.4, 0.2), V(0, sh + 1.5, cz + 0.4), V(0, mid.y + 1.5, 0), V(0, hip + 1.3, hz)]
    bones = ["Head", "Neck", "Chest", "Chest", "Hips"]
    for i, p in enumerate(spine_pts):
        for j in range(3):
            d = V((j - 1) * 0.5, 1.0, 0.6)
            c.leaf(B(p + V((j - 1) * 0.3, 0, 0)), B(d), B(V(1, 0, 0)), 1.5 - 0.15 * i, 0.6, FLAME1 if (i + j) % 2 else FLAME2, bones[i], thick=0.12, shape="flame", glow=True)
    dragon_head(c, hb, 1.15, JADEQ, CREAMQ, GOLDQ, CREAMQ, None, EYE, bone="Head", jaw="Jaw", horns="antler", seed=121, brow=JADEQ2, beard=FLAME2)
    tp = k["tail"]
    T(c, tp, [0.36, 0.3, 0.24, 0.2, 0.15], JADEQ, ["Tail%d" % (i + 1) for i in range(4)], seg=8, paint=scl)
    for j in range(4):
        c.leaf(B(tp[-1]), B(V((j - 1.5) * 0.4, 0.4, 1)), B(V(0, 1, 0)), 1.0, 0.5, FLAME1 if j % 2 else FLAME2, "Tail4", thick=0.1, shape="flame", glow=True)
    aura(c, "orbit", (255, 140, 40), (80, 220, 160), "Titanic")
    c.extra["speed"] = 1.2
    return c


def anims(c):
    fierce_anims(c, tail=4, stride=26, bob=0.16, head_amp=0.8)


VARIANTS = {"Celestial": {JADEQ: C(240, 240, 250), JADEQ2: C(190, 200, 225), GOLDQ: C(110, 170, 255), CREAMQ: C(255, 255, 255)}}
