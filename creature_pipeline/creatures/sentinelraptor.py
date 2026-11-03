"""SENTINEL RAPTOR (Secret, armoured): navy beast in white plate armour with steel trims, glowing blue
joints and seams, a huge white blade crest with navy inlay, long jaw lined with teeth, ringed tail, hooked claws."""
from detail import *

NAVY, NAVY2, WHITE, STEEL, GLOW, CLAW = C(40, 50, 110), C(26, 32, 78), C(238, 241, 252), C(150, 165, 210), C(60, 175, 255), C(205, 210, 228)


def build():
    c = detailed("SentinelRaptor", height=10)
    k = beast(c, sh=4.5, hip=4.0, L=1.7, W=1.15, neck=(1.3, 1.6), head=2.0, tail=5, tail_len=1.05, tail_lift=0.4)
    sh, hip, cz, hz, hb = k["sh"], k["hip"], k["cz"], k["hz"], k["hb"]
    TB = ["Hips", "Chest"]
    ribs = stripes(NAVY2, "z", period=0.45, width=0.14, wobble=0.05)
    # ---- body core (navy, ribbed) + belly
    T(c, [V(0, hip + 0.05, hz + 0.9), V(0, hip, hz), V(0, (hip + sh) / 2, 0), V(0, sh, cz), V(0, sh + 0.2, cz - 0.5)], [0.8, 1.12, 1.2, 1.25, 1.0], NAVY, TB, seg=8, flat=(1.0, 1.1), paint=ribs)
    # ---- back plates: overlapping armadillo bands with steel trims, glowing seams between them
    for i in range(5):
        t = i / 4
        z = cz + 0.1 + (hz - cz + 0.3) * t
        y = sh + (hip - sh) * t + 0.15
        shell(c, V(0, y, z), (1.32 - 0.08 * abs(t - 0.4), 1.25, 0.62), WHITE, TB, th=(-180, 180), ph=(8, 90), off=0.02, thick=0.16, seg=(10, 3), trim=STEEL, inset=0.12)
        for s in (-1, 1):
            E(c, V(s * 1.18, y - 0.25, z + 0.48), (0.08, 0.14, 0.2), GLOW, TB, seg=(6, 4), glow=True)
        S(c, V(0, y + 1.25, z), V(0, y + 1.85, z + 0.45), 0.2, WHITE, TB)
    shell(c, V(0, sh - 0.3, cz - 0.25), (1.15, 1.15, 0.95), WHITE, "Chest", th=(-55, 55), ph=(-55, 35), off=0.04, thick=0.14, seg=(5, 4), trim=STEEL)
    # ---- legs: navy, white armour shells, glowing joint rings, hooked claws
    for s, X in ((-1, "L"), (1, "R")):
        for front in (True, False):
            b = leg(c, k, X, NAVY, r=(0.7, 0.52, 0.42) if front else (0.78, 0.56, 0.44), paw_col=WHITE, paw=(0.55, 0.32, 0.75), seg=7, front=front)
            up, lo = ("Arm" + X, "Fore" + X) if front else ("Thigh" + X, "Shin" + X)
            top = k["sho" + X] if front else k["hip" + X]
            ft = k["paw" + X] if front else k["foot" + X]
            shell(c, top + V(s * 0.12, 0.15, 0), (0.88, 0.95, 1.0), WHITE, up, th=(s * 20, s * 165) if s > 0 else (-165, -20), ph=(-25, 80), off=0.04, thick=0.16, seg=(6, 4), trim=STEEL)
            cuff(c, b.lerp(ft, 0.18), b.lerp(ft, 0.75), 0.42, WHITE, lo, thick=0.14, seg=7, flare=0.1)
            c.torus(B(b), 0.5, 0.09, GLOW, lo, rot=euler(0, 0, 90), seg=(12, 4), glow=True)
            claws3(c, ft + V(0, 0, -0.1), CLAW, lo, size=0.36)
    # ---- neck + head: long wedge skull, white helmet plate, navy jaw full of teeth, blade crest
    T(c, [V(0, sh, cz), k["nb"], hb + V(0, -0.1, 0.2)], [1.0, 0.8, 0.62], NAVY, ["Chest", "Neck"], seg=8, paint=ribs)
    fur_line(c, [k["nb"] + V(0, 0.75, 0.6), hb + V(0, 0.55, 0.3)], WHITE, "Neck", length=0.8, width=0.42, out=V(0, 1, 0.8), n_per=3, seed=21)
    E(c, hb + V(0, -0.1, -0.7), (0.78, 0.6, 1.1), NAVY, "Head")
    # angular helmet: diamond-section wedge from the crest base to a pointed snout + cheek plates
    T(c, [hb + V(0, 0.42, 0.35), hb + V(0, 0.38, -0.7), hb + V(0, 0.12, -1.9), hb + V(0, -0.12, -2.75)], [0.82, 0.86, 0.62, 0.2], WHITE, "Head", seg=4, sub=1, flat=(1.0, 0.5), stud=False)
    T(c, [hb + V(0, 0.5, 0.2), hb + V(0, 0.5, -1.2)], [0.3, 0.2], STEEL, "Head", seg=4, sub=1, flat=(0.5, 1.0), stud=False)
    for s in (-1, 1):
        SHEET(c, [hb + V(s * 0.72, 0.15, 0.2), hb + V(s * 0.74, 0.1, -1.1), hb + V(s * 0.62, -0.42, -0.9), hb + V(s * 0.66, -0.5, 0.15)], WHITE, "Head", thick=0.14, stud=False)
        S(c, hb + V(s * 0.66, 0.1, 0.1), hb + V(s * 1.05, 0.25, 0.9), 0.16, STEEL, "Head")
    E(c, hb + V(0, -0.98, -1.4), (0.5, 0.2, 1.0), NAVY, "Jaw", rot=(-14, 0, 0))
    maw(c, hb + V(0, -0.5, -2.45), 0.46, 1.25, 0.6, "Head", "Jaw", n=11, tooth=0.22, fangs=1.5)
    eyes_pair(c, hb + V(0, 0.02, -1.35), 0.6, 0.24, "Head", glow=GLOW, core=C(210, 245, 255), brow=None, slant=24, turn=0.85)
    crest = [hb + V(0, 0.55, -0.9), hb + V(0, 1.6, -0.55), hb + V(0, 3.4, 0.4), hb + V(0, 2.4, 1.3), hb + V(0, 0.5, 0.45)]
    SHEET(c, crest, WHITE, "Head", thick=0.22)
    ctr = sum(crest, V(0, 0, 0)) / len(crest)
    SHEET(c, [ctr + (p - ctr) * 0.55 + V(0, 0.15, 0) for p in crest], NAVY2, "Head", thick=0.3)
    for s in (-1, 1):
        S(c, hb + V(s * 0.45, 0.35, 0.2), hb + V(s * 0.9, 0.7, 1.0), 0.18, WHITE, "Head")
    # ---- tail: navy core with white armour rings, blade tip
    tp = k["tail"]
    radii = [0.72, 0.58, 0.46, 0.36, 0.26, 0.14]
    T(c, tp, radii, NAVY, ["Tail%d" % (i + 1) for i in range(5)], seg=7)
    for i in range(5):
        a, b = tp[i].lerp(tp[i + 1], 0.2), tp[i].lerp(tp[i + 1], 0.7)
        cuff(c, a, b, radii[i] * 0.92, WHITE, "Tail%d" % (i + 1), thick=0.1, seg=7, flare=0.05)
    S(c, tp[-1], tp[-1] + V(0, 0.2, 1.0), 0.22, WHITE, "Tail5")
    aura(c, "sparkle", (60, 175, 255), (230, 240, 255), "Secret")
    c.extra["speed"] = 1.1
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        if walking:
            return {"Jaw": (-4 - 6 * max(0, sin(2 * p)), 0, 0), "Neck": (-6 * sin(2 * p), 0, 0)}
        hiss = max(0, sin(math.pi * (t - 0.55) / 0.3)) if 0.55 <= t <= 0.85 else 0.0
        return {"Jaw": (-3 - 24 * hiss, 0, 0), "Head": (10 * hiss + 3 * sin(2 * p), 0, 5 * sin(p))}
    quad_anims(c, tail=5, stride=26, bob=0.14, head_amp=0.9, extra=extra)

