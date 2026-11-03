"""GIANT PANDA (Zone 2 guardian, Legendary): huge angry giant panda, white with black legs and shoulder band,
black ears, dark eye patches with glowing red angry eyes, a snarling open jaw biting down on a green bamboo stalk,
shaggy shard fur on the cheeks and shoulders, heavy clawed paws. Fierce."""
from cn import *
from detail import *

WHITE, BLACK, PATCH, NOSE, BAMB, BAMB2, LEAFC, CLAWC = (C(240, 240, 236), C(36, 36, 42), C(46, 46, 54), C(28, 28, 32),
                                                       C(120, 190, 70), C(80, 140, 50), C(90, 170, 70), C(230, 225, 210))


def build():
    c = detailed("GiantPanda", height=16)
    sh, L = 4.4, 2.0
    paint = panda_paint(BLACK, sh * 0.72, -L, band=0.95, band_lo=sh * 0.55)
    k = fierce_quad(c, WHITE, belly=WHITE, sh=sh, hip=4.2, L=L, W=1.45, neck=(0.85, 0.55), head=1.6, tail=1,
                    body_r=1.75, leg_r=(0.92, 0.72, 0.62), paw=(0.8, 0.42, 0.95), paw_col=BLACK, paint=paint, hump=0.35)
    hb, cz = k["hb"], k["cz"]
    for s, X in ((-1, "L"), (1, "R")):
        claws3(c, k["paw" + X] + V(0, 0, -0.35), CLAWC, "Fore" + X, size=0.3)
        claws3(c, k["foot" + X] + V(0, 0, -0.35), CLAWC, "Shin" + X, size=0.26)
    # shaggy black shoulder fur
    fur(c, V(0, sh + 0.4, cz + 0.3), (1.75, 1.2, 1.0), BLACK, "Chest", n=70, length=0.8, width=0.6, flow=V(0, -0.8, 0.5), where=lambda u, p: u.y > -0.1, seed=11)
    # head: big round skull, white muzzle, snarling jaw
    E(c, hb + V(0, 0.15, -0.5), (1.35, 1.15, 1.15), WHITE, "Head", seg=(12, 9))
    E(c, hb + V(0, -0.3, -1.4), (0.72, 0.55, 0.6), WHITE, "Head", seg=(10, 7))
    E(c, hb + V(0, -0.02, -1.95), (0.26, 0.17, 0.14), NOSE, "Head", stud=False)
    E(c, hb + V(0, -0.95, -1.25), (0.62, 0.26, 0.62), WHITE, "Jaw", seg=(8, 5))
    maw(c, hb + V(0, -0.62, -1.75), 0.5, 0.65, 0.45, "Head", "Jaw", n=7, tooth=0.17, fangs=2.0)
    fur(c, hb + V(0, -0.2, -0.4), (1.4, 0.9, 1.0), WHITE, "Head", n=60, length=0.7, width=0.55, flow=V(0, -0.6, 0.6), where=lambda u, p: abs(u.x) > 0.55, seed=13)
    for s in (-1, 1):
        E(c, hb + V(s * 0.55, 0.32, -1.32), (0.42, 0.5, 0.22), PATCH, "Head", rot=(0, 0, s * 30), seg=(8, 6), stud=False)
        E(c, hb + V(s * 1.05, 1.1, -0.2), (0.55, 0.52, 0.32), BLACK, "Head", seg=(10, 7))   # round ear
    eyes_pair(c, hb + V(0, 0.38, -1.42), 0.55, 0.27, "Head", glow=C(255, 45, 40), core=C(255, 190, 150), brow=BLACK, slant=26, turn=0.55)
    # bamboo stalk clamped crosswise in the jaws, leaves at both ends
    by_ = hb + V(0, -0.62, -1.55)
    T(c, [by_ + V(-1.9, -0.1, 0.1), by_, by_ + V(1.9, 0.1, -0.1)], [0.17, 0.17, 0.15], BAMB, "Head", seg=10, sub=1)
    for xx in (-1.1, 0.0, 1.1):
        c.torus(B(by_ + V(xx, 0, 0)), 0.18, 0.05, BAMB2, "Head", rot=euler(0, 0, 90), seg=(12, 4))
    for s in (-1, 1):
        tip = by_ + V(s * 1.9, s * 0.1, -s * 0.1)
        for d in (V(s * 0.6, 0.5, 0.3), V(s * 0.7, -0.2, -0.4)):
            c.leaf(B(tip), B(d), B(V(0, 1, 0)), 0.8, 0.3, LEAFC, "Head", thick=0.08, shape="blade")
    E(c, k["tail"][0] + V(0, 0, 0.2), (0.4, 0.38, 0.32), WHITE, "Tail1", seg=(8, 6))
    aura(c, "sparkle", (255, 60, 50), (140, 220, 110), "Legendary")
    c.extra["speed"] = 0.95
    return c


def anims(c):
    fierce_anims(c, tail=1, stride=20, bob=0.18, head_amp=0.7)


VARIANTS = {"Qinling": {BLACK: C(120, 80, 50), PATCH: C(135, 92, 58), WHITE: C(245, 232, 215)}}
