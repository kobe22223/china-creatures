"""LION DANCE LION (Zone 6 guardian, Eternal): a giant festival lion-dance lion, costume style. Huge oversized
red and gold costume head with big round glowing eyes under fluffy white brows, a gold forehead mirror and horn,
a wide gold mouth that snaps open with a white fur beard, a body cloth painted with gold scales, white and gold
fur fringe along the back and sides, pom-pom ears and a big fluffy tail. Fierce."""
from cn import *
from detail import *

REDC, REDC2, GOLDC, GOLDC2, WHITEF, GREEN, MIRROR, EYE = (C(215, 35, 40), C(160, 20, 30), C(255, 200, 60), C(220, 150, 30),
                                                        C(252, 250, 245), C(60, 170, 100), C(220, 235, 255), C(255, 230, 80))


def build():
    c = detailed("LionDanceLion", height=17)
    scl = stripes(GOLDC2, "z", period=0.6, width=0.12, wobble=0.35)
    k = fierce_quad(c, REDC, belly=GOLDC, sh=4.35, hip=4.1, L=2.1, W=1.5, neck=(0.9, 1.1), head=2.2, tail=3, tail_len=0.9,
                    body_r=1.6, leg_r=(0.98, 0.8, 0.7), paw=(0.8, 0.42, 0.95), paw_col=GOLDC, paint=scl, hump=0.25)
    hb, sh, hip, cz, hz, mid = k["hb"], k["sh"], k["hip"], k["cz"], k["hz"], k["mid"]
    for s, X in ((-1, "L"), (1, "R")):
        for f, bone in ((k["paw" + X], "Fore" + X), (k["foot" + X], "Shin" + X)):
            fur(c, f + V(0, 0.55, 0), (0.75, 0.3, 0.8), WHITEF, bone, n=26, length=0.55, width=0.42, flow=V(0, -1, 0), where=lambda u, p: abs(u.y) < 0.5, seed=60)
    # fringe along the spine and down the sides
    fur_line(c, [V(0, sh + 1.6, cz - 0.2), V(0, mid.y + 1.6, 0), V(0, hip + 1.4, hz + 0.6)], WHITEF, ["Chest", "Hips"], length=0.9, width=0.6, out=V(0, 1, 0.3), n_per=6, col2=GOLDC, seed=61)
    for s in (-1, 1):
        fur_line(c, [V(s * 1.55, mid.y - 0.6, cz + 0.2), V(s * 1.6, mid.y - 0.7, hz)], GOLDC, ["Chest", "Hips"], length=0.7, width=0.45, out=V(s * 0.5, -1, 0), n_per=7, col2=WHITEF, seed=62 + s)
    # huge costume head
    E(c, hb + V(0, 0.3, -0.75), (2.05, 1.8, 1.75), REDC, "Head", seg=(14, 10))
    for s in (-1, 1):
        E(c, hb + V(s * 1.05, -0.2, -1.55), (0.8, 0.75, 0.65), GOLDC, "Head", seg=(10, 8))
        E(c, hb + V(s * 2.0, 0.95, -0.4), (0.5, 0.5, 0.5), GREEN, "Head", seg=(10, 8))   # pom-pom ear
        fur(c, hb + V(s * 0.75, 1.0, -1.85), (0.62, 0.22, 0.3), WHITEF, "Head", n=24, length=0.55, width=0.4, flow=V(s * 0.6, 0.3, 0.2), where=lambda u, p: u.z < 0.3, seed=63 + s)
    # big round glowing eyes
    for s in (-1, 1):
        E(c, hb + V(s * 0.72, 0.42, -2.05), (0.52, 0.52, 0.25), C(250, 250, 250), "Head", seg=(14, 10), stud=False)
        E(c, hb + V(s * 0.72, 0.42, -2.25), (0.32, 0.32, 0.12), EYE, "Head", seg=(12, 8), glow=True)
        E(c, hb + V(s * 0.72, 0.42, -2.33), (0.14, 0.14, 0.06), C(30, 20, 20), "Head", seg=(10, 6), stud=False)
    # forehead mirror + horn
    T(c, [hb + V(0, 1.3, -2.1), hb + V(0, 1.35, -2.3)], [0.42, 0.42], GOLDC, "Head", seg=14, sub=1)
    E(c, hb + V(0, 1.35, -2.34), (0.3, 0.3, 0.05), MIRROR, "Head", seg=(14, 6), stud=False, glow=True)
    swept_horn(c, [hb + V(0, 1.85, -1.3), hb + V(0, 2.45, -1.4), hb + V(0, 2.85, -1.1)], 0.3, GOLDC, "Head", seg=8)
    # wide gold lips on Head / Jaw + white beard on the jaw
    E(c, hb + V(0, -0.5, -2.0), (1.3, 0.35, 0.7), GOLDC, "Head", seg=(12, 6))
    E(c, hb + V(0, -1.15, -1.75), (1.15, 0.32, 0.65), GOLDC, "Jaw", rot=(-10, 0, 0), seg=(12, 6))
    maw(c, hb + V(0, -0.82, -2.2), 0.95, 0.8, 0.42, "Head", "Jaw", n=10, tooth=0.15, fangs=1.4)
    fur(c, hb + V(0, -1.55, -1.6), (1.05, 0.4, 0.55), WHITEF, "Jaw", n=40, length=0.8, width=0.5, flow=V(0, -1, -0.2), where=lambda u, p: u.y < 0.2, seed=66)
    # big fluffy tail
    tp = k["tail"]
    T(c, tp, [0.35, 0.3, 0.25, 0.2], REDC, ["Tail1", "Tail2", "Tail3"], seg=8)
    fur(c, tp[-1], (0.8, 0.8, 0.9), WHITEF, "Tail3", n=50, length=0.8, width=0.5, flow=lambda p, n: n, col2=GOLDC, mix=0.3, seed=67, lift=0.6)
    aura(c, "sparkle", (255, 60, 50), (255, 220, 80), "Eternal")
    c.extra["speed"] = 1.05
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        if walking:
            return {"Head": (6 * sin(2 * p), 0, 12 * sin(p)), "Jaw": (-4 - 14 * max(0, sin(2 * p)), 0, 0)}
        snap = max(0, sin(math.pi * (t - 0.45) / 0.35)) if 0.45 <= t <= 0.8 else 0.0
        return {"Head": (5 * sin(2 * p) + 8 * snap, 0, 20 * snap * sin(5 * tau * t)), "Jaw": (-3 - 26 * snap, 0, 0)}
    fierce_anims(c, tail=3, stride=24, bob=0.18, head_amp=0.8, roar=False, extra=extra)


VARIANTS = {"Golden": {REDC: C(255, 200, 60), REDC2: C(214, 150, 30), GOLDC: C(214, 32, 40), GOLDC2: C(160, 20, 30), GREEN: C(255, 255, 255)}}
