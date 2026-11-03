"""STONE GUARDIAN LION (Zone 4 guardian, Cosmic): a huge grey stone guardian lion statue come to life. Rows of
round carved curls for the mane, a square jaw with an open snarl, a carved collar with a bell, heavy paws, the
front right paw resting on a carved embroidered ball, faint stone cracks, glowing jade angry eyes. Fierce."""
from cn import *
from detail import *

STONE, STONE2, STONE3, CRACK, EYE = C(150, 152, 156), C(120, 122, 128), C(178, 180, 184), C(95, 96, 102), C(80, 255, 170)


def build():
    c = detailed("StoneGuardianLion", height=17)
    crk = cracks(CRACK, scale=0.9, width=0.04)
    k = fierce_quad(c, STONE, belly=STONE2, sh=4.4, hip=3.9, L=1.9, W=1.4, neck=(0.8, 1.35), head=1.7, tail=3, tail_len=0.8,
                    body_r=1.5, leg_r=(0.9, 0.72, 0.64), paw=(0.85, 0.45, 1.0), paw_col=STONE3, paint=crk, hump=0.3)
    hb, cz, sh = k["hb"], k["cz"], k["sh"]
    for s, X in ((-1, "L"), (1, "R")):
        for f, bone in ((k["paw" + X], "Fore" + X), (k["foot" + X], "Shin" + X)):
            for j in (-1, 0, 1):
                E(c, f + V(j * 0.32, -0.02, -0.75), (0.17, 0.17, 0.2), STONE3, bone, seg=(6, 4))   # carved toes
    # carved embroidered ball under the front right paw
    ball = k["pawR"] + V(0.2, 0.62, -1.25)
    E(c, ball, (0.78, 0.78, 0.78), STONE3, "ForeR", seg=(12, 9), paint=filigree(STONE2, scale=2.0, width=0.07))
    c.torus(B(ball), 0.8, 0.07, STONE2, "ForeR", seg=(20, 4), stud=False)
    # big square head, curly mane, snarl
    E(c, hb + V(0, 0.1, -0.5), (1.2, 1.1, 1.1), STONE, "Head", seg=(10, 8), paint=crk)
    BOX(c, hb + V(0, -0.3, -1.35), (0.75, 0.5, 0.5), STONE3, "Head")
    BOX(c, hb + V(0, -0.92, -1.25), (0.62, 0.2, 0.55), STONE3, "Jaw")
    maw(c, hb + V(0, -0.6, -1.82), 0.52, 0.65, 0.45, "Head", "Jaw", n=7, tooth=0.17, fangs=2.0, teeth_col=C(220, 222, 226), mouth_col=C(60, 60, 66), tongue_col=STONE2)
    E(c, hb + V(0, 0.0, -1.88), (0.32, 0.2, 0.16), STONE2, "Head", seg=(8, 5))   # broad nose
    eyes_pair(c, hb + V(0, 0.42, -1.4), 0.55, 0.28, "Head", glow=EYE, core=C(220, 255, 235), brow=STONE2, slant=24, turn=0.55)
    # mane: rows of round spiral curls over the head and neck
    for i in range(5):
        for j in range(9):
            a = math.radians(-120 + j * 30)
            rr = 1.25 + 0.12 * i
            p = hb + V(math.sin(a) * rr, 0.95 - i * 0.48, -0.25 + math.cos(a) * rr * 0.75 + i * 0.25)
            if math.cos(a) < -0.6 and i < 3:
                continue          # keep the face clear
            E(c, p, (0.3, 0.3, 0.26), STONE2 if (i + j) % 2 else STONE3, ["Head"] if i < 2 else ["Neck"], seg=(8, 6))
            c.torus(B(p + V(0, 0, 0)), 0.17, 0.06, CRACK, ["Head"] if i < 2 else ["Neck"], seg=(10, 4), stud=False)
    # carved collar + bell
    c.torus(B(V(0, sh + 0.2, cz - 0.4)), 1.25, 0.16, STONE3, "Chest", rot=euler(60, 0, 0), seg=(24, 6), stud=False)
    E(c, V(0, sh - 0.85, cz - 1.15), (0.36, 0.38, 0.36), STONE3, "Chest", seg=(10, 7))
    tp = k["tail"]
    T(c, tp, [0.36, 0.3, 0.24, 0.2], STONE, ["Tail1", "Tail2", "Tail3"], seg=8)
    for j in range(4):
        E(c, tp[-1] + V((j - 1.5) * 0.25, 0.25 * (j % 2), 0.1), (0.3, 0.3, 0.3), STONE2, "Tail3", seg=(8, 6))
    aura(c, "orbit", (80, 255, 170), (200, 205, 210), "Cosmic")
    c.extra["speed"] = 0.85
    return c


def anims(c):
    fierce_anims(c, tail=3, stride=20, bob=0.12, head_amp=0.6)


VARIANTS = {"Jade": {STONE: C(90, 170, 130), STONE2: C(60, 135, 100), STONE3: C(130, 200, 160), CRACK: C(40, 100, 70)}}
