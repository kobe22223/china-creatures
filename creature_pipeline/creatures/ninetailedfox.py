"""NINE-TAILED FOX (Titanic, Kunlun Immortal Peaks): a round white-and-gold fox on short stubby legs, big head
with tall soft ears, a red forehead mark and gold cheek tufts, and nine fluffy tails fanned out behind it, each
tipped with a glowing blue fox-fire. Cute: flat black eyes."""
from cn import *

WHITE, CREAM, GOLDF, PINK, NOSE, MARK, FIRE = (C(252, 250, 245), C(250, 232, 190), C(255, 200, 90), C(255, 175, 190),
                                              C(40, 30, 35), C(220, 40, 50), C(120, 220, 255))


def build():
    c = Creature("NineTailedFox", height=6.5)
    k = cute_quad(c, WHITE, belly=CREAM, paw=GOLDF, body=(1.4, 1.15, 1.75), leg_h=1.1, leg_r=0.42, head_r=1.25, head_up=0.6, tail=0)
    h, r = k["head"], k["head_r"]
    by, rz = k["by"], k["rz"]
    c.ellipsoid(h, (r * 1.05, r * 0.92, r), WHITE, "Head", seg=(24, 16))
    c.tube([h + P(0, -0.25, -r * 0.6), h + P(0, -0.32, -r * 1.15)], [0.5, 0.32], CREAM, ["Head"], seg=16, sub=1)
    c.ellipsoid(h + P(0, -0.2, -r * 1.22), (0.16, 0.12, 0.1), NOSE, "Head", stud=False, smooth=True)
    c.ellipsoid(h + P(0, 0.62, -r * 0.85), (0.1, 0.22, 0.05), MARK, "Head", stud=False)
    for s in (-1, 1):
        c.eye(h + P(s * 0.48, 0.2, -r * 0.84), 0.22, P(s * 0.45, 0.05, -1), "Head")
        c.spike(h + P(s * 0.9, -0.15, -0.4), h + P(s * 1.5, -0.4, -0.1), 0.32, GOLDF, "Head", seg=6)   # cheek tuft
        e0 = h + P(s * 0.6, r * 0.75, 0.05)
        c.leaf(e0, P(s * 0.35, 1, 0.1), P(0, 0, 1), 0.95, 0.68, WHITE, "Head", thick=0.2, shape="blade")
        c.leaf(e0 + P(0, 0.05, -0.1), P(s * 0.35, 1, 0.1), P(0, 0, 1), 0.7, 0.42, PINK, "Head", thick=0.1, shape="blade")
    puffs(c, P(0, by + 0.1, -rz * 0.8), (0.95, 0.65, 0.5), CREAM, "Chest", n=14, size=0.34, seed=111, where=lambda u: u[2] < 0.2)
    # nine fanned tails, each with two bones, a gold band and a glowing fox-fire tip
    root = P(0, by + 0.3, rz * 0.85)
    for i in range(9):
        a = math.radians(-90 + i * 22.5)
        m = root + P(math.sin(a) * 0.95, 0.85 + 0.35 * math.cos(a), 0.55 + 0.2 * (i % 2))
        e = m + P(math.sin(a) * 1.15, 1.15 * math.cos(a * 0.6), 0.25 + 0.55 * (i % 2) + 0.3 * abs(math.sin(a)))
        n1, n2 = "TailA%d" % (i + 1), "TailB%d" % (i + 1)
        c.bone(n1, root, m, "Hips"); c.bone(n2, m, e, n1)
        c.tube([root, root.lerp(m, 0.5) + P(0, 0.1, 0), m], [0.22, 0.33, 0.37], WHITE if i % 2 else CREAM, [n1], seg=10)
        c.tube([m, m.lerp(e, 0.5), e], [0.37, 0.34, 0.12], WHITE if i % 2 else CREAM, [n2], seg=10)
        c.ellipsoid(e + (m - e) * 0.12, (0.26, 0.26, 0.26), FIRE, n2, seg=(10, 6), glow=True)
    aura(c, "orbit", (120, 220, 255), (255, 200, 90), "Titanic")
    c.extra["speed"] = 1.3
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        out = {"Head": (4 * sin(2 * p), 0, 6 * sin(p))}
        for i in range(9):
            out["TailA%d" % (i + 1)] = (4 * sin(2 * p + i), (10 if walking else 7) * sin(p + i * 0.5), 0)
            out["TailB%d" % (i + 1)] = (5 * sin(2 * p + i + 0.6), (12 if walking else 8) * sin(p + i * 0.5 - 0.8), 0)
        return out
    quad_anims(c, tail=0, stride=26, bob=0.12, extra=extra)


VARIANTS = {"Shadow": {WHITE: C(60, 50, 80), CREAM: C(110, 95, 140), GOLDF: C(200, 120, 255), FIRE: C(200, 120, 255), PINK: C(180, 120, 220)}}
