"""GIANT WATER BUFFALO (Zone 1 guardian, Epic): huge slate water buffalo with massive ribbed crescent horns
sweeping back, glowing red angry eyes, a gold nose ring, a red festival saddle cloth with gold trim and coins,
shard-fur ridge over the shoulders, heavy split hooves. Fierce."""
from cn import *
from detail import *

GREY, GREY2, BELLY, MUZ, HORN, HORN2, HOOFC = (C(84, 92, 108), C(56, 62, 76), C(120, 126, 140), C(150, 140, 146),
                                               C(225, 212, 180), C(170, 150, 120), C(40, 40, 48))


def build():
    c = detailed("GiantWaterBuffalo", height=16)
    k = fierce_quad(c, GREY, belly=BELLY, sh=4.3, hip=4.1, L=2.1, W=1.35, neck=(0.95, 0.75), head=1.7, tail=3,
                    body_r=1.6, leg_r=(0.86, 0.66, 0.56), paw=(0.66, 0.36, 0.78), paw_col=GREY2, hump=0.45)
    sh, hip, cz, hz, hb, mid = k["sh"], k["hip"], k["cz"], k["hz"], k["hb"], k["mid"]
    TB = ["Hips", "Chest"]
    for s, X in ((-1, "L"), (1, "R")):
        hoof(c, k["paw" + X], 0.62, HOOFC, "Fore" + X)
        hoof(c, k["foot" + X], 0.62, HOOFC, "Shin" + X)
    # red festival saddle cloth with gold trim + three coins along the back
    shell(c, V(0, mid.y + 0.2, 0.0), (1.66, 1.62, 1.9), RED, TB, th=(-180, 180), ph=(38, 90), seg=(12, 3), trim=GOLD, thick=0.12, inset=0.1)
    for s in (-1, 1):
        shell(c, V(0, mid.y + 0.2, 0.0), (1.66, 1.62, 1.9), RED, TB, th=(55, 125) if s > 0 else (-125, -55), ph=(-15, 40), seg=(5, 3), thick=0.1)
        shell(c, V(0, mid.y + 0.2, 0.0), (1.7, 1.66, 1.94), GOLD, TB, th=(55, 125) if s > 0 else (-125, -55), ph=(-20, -12), seg=(5, 1), thick=0.1)
        coin(c, B(V(s * 1.78, mid.y + 0.75, 0)), 0.3, TB, facing=(s, 0.2, 0))
    # shard fur ridge over the shoulder hump
    fur_line(c, [V(0, sh + 1.85, cz + 0.9), V(0, sh + 2.0, cz), V(0, sh + 1.5, cz - 0.6)], GREY2, "Chest", length=0.8, width=0.6, out=V(0, 1, 0.5), n_per=4, seed=5)
    # head: broad skull, pale muzzle, jaw, gold nose ring
    E(c, hb + V(0, 0.05, -0.55), (1.05, 0.95, 1.1), GREY, "Head", seg=(10, 8))
    E(c, hb + V(0, -0.3, -1.45), (0.8, 0.62, 0.62), MUZ, "Head", seg=(10, 7))
    E(c, hb + V(0, -0.85, -1.15), (0.62, 0.25, 0.6), MUZ, "Jaw", seg=(8, 5))
    maw(c, hb + V(0, -0.62, -1.75), 0.42, 0.6, 0.35, "Head", "Jaw", n=6, tooth=0.14, fangs=1.2, lower_teeth=False)
    for s in (-1, 1):
        E(c, hb + V(s * 0.32, -0.15, -2.02), (0.13, 0.17, 0.08), C(30, 26, 30), "Head", stud=False)
    c.torus(B(hb + V(0, -0.42, -2.08)), 0.3, 0.07, GOLD, "Head", rot=euler(0, 0, 90), seg=(14, 5), stud=False)
    eyes_pair(c, hb + V(0, 0.32, -1.05), 0.62, 0.26, "Head", glow=C(255, 50, 40), core=C(255, 180, 140), brow=GREY2, slant=24, turn=0.6)
    # massive ribbed crescent horns sweeping out and back, tips curling up
    for s in (-1, 1):
        b0 = hb + V(s * 0.75, 0.75, -0.35)
        pts = [b0, b0 + V(s * 1.0, 0.25, 0.1), b0 + V(s * 2.0, 0.2, 0.7), b0 + V(s * 2.5, 0.55, 1.6), b0 + V(s * 2.3, 1.15, 2.2)]
        swept_horn(c, pts, 0.52, HORN, "Head", seg=8, ribs=True)
        E(c, b0, (0.5, 0.42, 0.5), HORN2, "Head", seg=(8, 5))
        c.leaf(B(hb + V(s * 0.95, 0.3, -0.15)), B(V(s * 1, -0.6, 0.2)), B(V(0, 0, 1)), 0.8, 0.5, MUZ, "Head", thick=0.18, shape="blade")   # droopy ear under the horn
    # tail with a dark tuft
    tp = k["tail"]
    T(c, tp, [0.28, 0.22, 0.17, 0.12], GREY, ["Tail1", "Tail2", "Tail3"], seg=7)
    fur(c, tp[-1] + V(0, -0.1, 0.1), (0.35, 0.5, 0.35), GREY2, "Tail3", n=24, length=0.6, width=0.4, flow=V(0, -1, 0.3), seed=9)
    aura(c, "sparkle", (255, 70, 50), (255, 200, 60), "Epic")
    c.extra["speed"] = 0.9
    return c


def anims(c):
    fierce_anims(c, tail=3, stride=22, bob=0.16, head_amp=0.7)


VARIANTS = {"Bronze": {GREY: C(120, 82, 50), GREY2: C(80, 52, 30), BELLY: C(160, 120, 80), MUZ: C(190, 160, 130), RED: C(40, 110, 80), HORN: C(255, 215, 120)}}
