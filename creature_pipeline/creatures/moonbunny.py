"""MOON BUNNY (Cosmic): chunky lavender star bunny, huge ears, crescent moon on the forehead, comet puff tail."""
from kit import *

FUR, FUR2, CREAM, PINK, MOON, STAR = C(190, 170, 245), C(150, 125, 225), C(250, 245, 255), C(255, 160, 210), C(255, 230, 120), C(255, 250, 215)


def build():
    c = Creature("MoonBunny", height=8)
    star = spots(STAR, size=0.35, density=0.14, seed=23)
    k = quad(c, FUR, belly=CREAM, L=0.8, H=0.82, W=1.3, leg=1.15, paw=CREAM, tail=1, paint=star, chunk=1.15)
    h, sh = k["head"], k["sh_y"]
    c.ellipsoid(h + P(0, 0.3, -0.4), (1.35, 1.2, 1.2), FUR, "Head", seg=(22, 14), paint=star)
    c.ellipsoid(h + P(0, -0.1, -1.35), (0.7, 0.5, 0.45), CREAM, "Head")
    c.ellipsoid(h + P(0, 0.08, -1.78), (0.18, 0.12, 0.1), PINK, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.eye(h + P(s * 0.55, 0.5, -1.3), 0.32, P(s * 0.5, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.9, 0.0, -1.1), (0.25, 0.16, 0.12), PINK, "Head", stud=False)
        # huge ears (one bent at the tip)
        e0 = h + P(s * 0.5, 1.2, -0.2)
        e1 = e0 + P(s * 0.3, 1.6, 0.25)
        e2 = e1 + (P(s * 0.9, 0.6, 0.5) if s > 0 else P(s * 0.2, 1.3, 0.2))
        c.tube([e0, e1, e2], [0.42, 0.45, 0.25], FUR, ["Head"], seg=10, flat=(1.0, 0.55))
        c.tube([e0 + P(0, 0.2, -0.22), e1 + P(0, 0, -0.22), e2 + P(0, 0, -0.18)], [0.22, 0.27, 0.12], PINK, ["Head"], seg=8, flat=(1.0, 0.4))
    # crescent moon mark on the forehead (glowing)
    pts = [h + P(math.sin(math.radians(a)) * 0.45, 0.95 + math.cos(math.radians(a)) * 0.35, -1.1 - 0.15 * math.cos(math.radians(a))) for a in range(-100, 101, 25)]
    c.tube(pts, [0.04, 0.08, 0.11, 0.12, 0.12, 0.12, 0.11, 0.08, 0.04], MOON, ["Head"], seg=6, glow=True)
    # chubby chest fluff + comet puff tail
    for j in range(5):
        c.spike(P((j - 2) * 0.4, sh + 0.1, k["chest_z"] - 0.9), P((j - 2) * 0.5, sh - 0.8, k["chest_z"] - 1.2), 0.38, CREAM, "Chest", seg=6)
    tail = P(0, sh + 0.3, k["hip_z"] + 1.2)
    c.ellipsoid(tail, (0.75, 0.75, 0.7), CREAM, "Tail1", seg=(16, 10))
    for j in range(3):
        c.leaf(tail + P(0, 0.2, 0.3), P((j - 1) * 0.5, 0.3, 1), P(1, 0, 0), 1.3, 0.5, MOON if j == 1 else STAR, "Tail1", thick=0.2, shape="flame", glow=True)
    aura(c, "orbit", (200, 170, 255), (255, 230, 140), "Cosmic")
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        if walking:   # bunny hop: back legs together, front legs together
            return {"Root": ((0, 0, 0), (0, 0.45 * abs(sin(p)), 0)), "ArmL": (30 * sin(p), 0, 0), "ArmR": (30 * sin(p), 0, 0),
                    "ThighL": (-30 * sin(p), 0, 0), "ThighR": (-30 * sin(p), 0, 0), "Chest": (-6 * sin(p), 0, 0)}
        return {"Head": (5 * sin(2 * p), 0, 10 * sin(p))}
    quad_anims(c, tail=1, stride=0, bob=0.0, extra=extra)

