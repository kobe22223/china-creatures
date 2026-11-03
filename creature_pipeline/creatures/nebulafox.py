"""NEBULA FOX (Cosmic): mystical fox with five fanned galaxy tails, big ears and starry fur."""
from kit import *

FUR, FUR2, CREAM, PAW, GLOW, PINK, STAR = C(95, 70, 190), C(140, 105, 225), C(245, 235, 255), C(50, 35, 110), C(120, 230, 255), C(255, 140, 220), C(255, 250, 210)


def build():
    c = Creature("NebulaFox", height=8.5)
    star = spots(STAR, size=0.36, density=0.16, seed=13)
    k = quad(c, FUR, belly=CREAM, L=1.0, H=0.95, W=0.95, leg=0.95, paw=PAW, tail=0, paint=star)
    h, sh = k["head"], k["sh_y"]
    # fluffy chest
    for j in range(5):
        c.spike(P((j - 2) * 0.35, sh + 0.2, k["chest_z"] - 0.7), P((j - 2) * 0.45, sh - 0.9, k["chest_z"] - 1.0), 0.35, CREAM, "Chest", seg=6)
    # head
    c.ellipsoid(h + P(0, 0.25, -0.45), (1.05, 0.9, 1.0), FUR, "Head", seg=(18, 12), paint=star)
    c.tube([h + P(0, 0.05, -0.85), h + P(0, -0.12, -1.7), h + P(0, -0.22, -2.25)], [0.6, 0.42, 0.3], CREAM, ["Head"], seg=10, flat=(1.0, 0.8))
    c.ellipsoid(h + P(0, -0.12, -2.35), (0.2, 0.14, 0.12), PAW, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.eye(h + P(s * 0.45, 0.45, -1.0), 0.26, P(s * 0.6, 0.15, -1), "Head")
        c.leaf(h + P(s * 0.55, 0.95, -0.3), P(s * 0.4, 1, 0.15), P(1, 0, 0), 1.6, 0.95, FUR2, "Head", thick=0.22, shape="blade")
        c.leaf(h + P(s * 0.55, 1.02, -0.45), P(s * 0.4, 1, 0.15), P(1, 0, 0), 1.2, 0.55, PINK, "Head", thick=0.08, shape="blade")
        c.spike(h + P(s * 0.9, 0.0, -0.6), h + P(s * 1.6, -0.35, -0.2), 0.4, CREAM, "Head", seg=6)   # cheek fluff
        c.ellipsoid(h + P(s * 0.5, 0.8, -0.9), (0.28, 0.08, 0.12), FUR2, "Head", rot=euler(0, s * -20, s * 15))
    c.ellipsoid(h + P(0, 0.85, -1.05), (0.18, 0.18, 0.08), GLOW, "Head", rot=euler(0, 0, 45), glow=True)   # forehead gem
    # five fanned tails, each with its own two bones
    root = P(0, sh + 0.3, k["hip_z"] + 1.0)
    for i in range(5):
        a = math.radians(-60 + i * 30)
        d = P(math.sin(a) * 0.9, 0.75, 0.7)
        m = root + d * 1.6
        e = m + P(math.sin(a) * 1.6, 1.4, 0.9)
        n1, n2 = "TailA%d" % (i + 1), "TailB%d" % (i + 1)
        c.bone(n1, root, m, "Hips"); c.bone(n2, m, e, n1)
        c.tube([root, root.lerp(m, 0.5) + P(0, 0.15, 0), m], [0.32, 0.55, 0.62], FUR, [n1], seg=10, paint=star)
        c.tube([m, m.lerp(e, 0.5), e], [0.62, 0.55, 0.12], FUR2, [n2], seg=10, paint=star)
        c.ellipsoid(e + (m - e) * 0.18, (0.4, 0.4, 0.4), GLOW if i % 2 else PINK, n2, glow=True)
    aura(c, "orbit", (150, 110, 255), (120, 230, 255), "Cosmic")
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        out = {}
        for i in range(5):
            out["TailA%d" % (i + 1)] = (5 * sin(2 * p + i), (12 if walking else 9) * sin(p + i * 0.6), 0)
            out["TailB%d" % (i + 1)] = (6 * sin(2 * p + i + 0.6), (14 if walking else 10) * sin(p + i * 0.6 - 0.8), 0)
        return out
    quad_anims(c, tail=0, stride=26, extra=extra)

