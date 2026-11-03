"""TYRANT REX (Godly, Prehistoric guardian + pet): massive forest-green T-Rex with dark tiger stripes,
cream belly, bone-white back spikes, scarred brow ridges, a huge open jaw lined with teeth, tiny arms,
glowing amber eyes and a molten-amber gem crest."""
from dino import *

GRN, GRN2, BELLY, BONE, CLAW, AMBER, AMBER2 = C(62, 120, 58), C(30, 64, 34), C(232, 214, 160), C(240, 232, 205), C(60, 50, 44), C(255, 170, 30), C(255, 230, 120)


def build():
    c = detailed("TyrantRex", height=12)
    k = theropod(c, hip=5.0, L=2.3, W=1.25, neck=(1.0, 1.25), head=3.2, tail=6, tail_len=1.35, arm=0.75, upright=0.25)
    hb, ch, mid, hip, hz = k["hb"], k["chest"], k["mid"], k["hip"], k["hz"]
    stripes_ = stripes(GRN2, "z", period=0.75, width=0.2, wobble=0.35)
    TB = ["Hips", "Chest"]
    # ---- body: deep barrel chest tapering into the hips + cream belly
    T(c, [V(0, hip + 0.1, hz + 1.0), V(0, hip + 0.2, hz), mid, ch + V(0, -0.2, 0.3), ch + V(0, 0.05, -0.35)],
      [1.25, 1.6, 1.85, 1.75, 1.3], GRN, TB, seg=10, flat=(0.9, 1.05), paint=stripes_)
    E(c, mid + V(0, -1.05, -0.3), (1.25, 0.9, 2.0), BELLY, TB, seg=(10, 7), paint=stripes(C(205, 185, 130), "y", period=0.35, width=0.08, wobble=0))
    # ---- neck + head
    T(c, [ch + V(0, 0.1, 0.2), k["nb"] + V(0, 0, -0.1), hb + V(0, -0.15, 0.25)], [1.35, 1.2, 1.05], GRN, ["Chest", "Neck"], seg=9, paint=stripes_)
    E(c, k["nb"] + V(0, -0.7, -0.25), (0.9, 0.8, 0.9), BELLY, "Neck", seg=(8, 6))
    # skull: boxy and deep, long snout
    T(c, [hb + V(0, 0.2, 0.5), hb + V(0, 0.25, -0.6), hb + V(0, 0.1, -1.9), hb + V(0, -0.05, -3.0)], [1.05, 1.08, 0.88, 0.62],
      GRN, "Head", seg=8, sub=1, flat=(0.9, 0.95), paint=stripes_)
    E(c, hb + V(0, -0.05, -3.0), (0.62, 0.5, 0.45), GRN, "Head", seg=(8, 6))
    # lower jaw, dropped open
    T(c, [hb + V(0, -0.85, 0.2), hb + V(0, -1.4, -1.3), hb + V(0, -1.7, -2.75)], [0.85, 0.7, 0.5], GRN, "Jaw", seg=8, sub=1, flat=(0.95, 0.6))
    E(c, hb + V(0, -1.65, -1.3), (0.65, 0.35, 1.3), BELLY, "Jaw", seg=(8, 6))
    maw(c, hb + V(0, -1.05, -2.85), 0.58, 2.4, 0.6, "Head", "Jaw", n=13, tooth=0.34, fangs=1.5)
    # brow ridges, nostrils, scars
    for s in (-1, 1):
        S(c, hb + V(s * 0.55, 0.85, -0.7), hb + V(s * 0.75, 1.25, 0.2), 0.22, GRN2, "Head", seg=4, n=3)
        E(c, hb + V(s * 0.3, 0.32, -3.2), (0.12, 0.08, 0.1), C(20, 30, 20), "Head", stud=False)
        T(c, [hb + V(s * 0.95, 0.4, -1.55), hb + V(s * 0.98, -0.05, -1.25)], [0.05, 0.05], BELLY, "Head", seg=4, stud=False)
    eyes_pair(c, hb + V(0, 0.55, -0.85), 0.86, 0.34, "Head", glow=AMBER, core=AMBER2, brow=GRN2, slant=22, turn=0.95)
    # amber crest gem + bone horns on the skull
    E(c, hb + V(0, 1.15, -0.55), (0.32, 0.4, 0.45), AMBER, "Head", glow=True, seg=(6, 4))
    for s in (-1, 1):
        S(c, hb + V(s * 0.45, 0.9, 0.15), hb + V(s * 0.75, 1.5, 0.95), 0.25, BONE, "Head", bend=V(0, 0.2, 0), seg=4, n=4)
    # ---- back spikes running from the skull down to the tail tip
    pts = [hb + V(0, 0.95, 0.5), k["nb"] + V(0, 1.15, 0.2), ch + V(0, 1.6, 0.4), mid + V(0, 1.8, -0.4), mid + V(0, 1.85, 0.6), V(0, hip + 1.55, hz + 0.1)]
    bones = ["Head", "Neck", "Chest", "Chest", "Hips", "Hips"]
    for i, p in enumerate(pts):
        sz = 0.42 if 1 < i < 5 else 0.3
        S(c, p, p + V(0, sz * 1.7, sz * 0.7), sz * 0.5, BONE, bones[i], seg=4, n=3)
    # ---- legs + arms + tail
    theropod_legs(c, k, GRN, CLAW, r=(1.0, 0.68, 0.4), paint=stripes_, toe_col=GRN2)
    tiny_arms(c, k, GRN, CLAW, r=0.3)
    radii = dino_tail(c, k, GRN, 1.3, paint=stripes_)
    tp = k["tail"]
    for i in range(1, len(tp) - 1):
        sz = 0.36 * (1 - i / len(tp)) + 0.1
        S(c, tp[i] + V(0, radii[i] * 0.85, 0), tp[i] + V(0, radii[i] * 0.85 + sz * 1.6, sz * 0.7), sz * 0.5, BONE, "Tail%d" % (i + 1 if i < len(tp) - 1 else i), seg=4, n=3)
    aura(c, "sparkle", (255, 170, 30), (255, 240, 180), "Godly")
    c.extra["speed"] = 0.9
    return c


def anims(c):
    theropod_anims(c, tail=6, stride=28, bob=0.22, head_amp=0.8)

