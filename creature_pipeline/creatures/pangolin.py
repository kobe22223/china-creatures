"""PANGOLIN (Mythic, Tea Terraces): round little pangolin on short stubby legs, covered in overlapping bronze
scales tipped with gold, big round head with scale cap, a soft pink face and long scaled tail curled up behind.
Cute: flat black eyes."""
from cn import *
from detail import shard, fibo, V as GV, B
from mathutils import Matrix

SKIN, BRONZE, BRONZE2, GOLDT, FACE, NOSE, CLAWC = (C(210, 160, 120), C(170, 110, 60), C(130, 80, 45), C(255, 200, 70),
                                                   C(250, 200, 180), C(120, 70, 70), C(90, 60, 40))


def scales(c, ctr, rad, bones, rows=7, size=0.62, z_range=(-0.85, 0.95), arc=105, seed=1, mix=0.3):
    """overlapping armour scales in neat rows over the top of an ellipsoid (game ctr / radii), each lying back (+z)"""
    import random as _r
    rng = _r.Random(seed)
    for i in range(rows):
        t = z_range[0] + (z_range[1] - z_range[0]) * i / (rows - 1)
        ring = math.sqrt(max(0.05, 1 - t * t))
        n = max(3, int(arc / 180 * math.pi * ring * max(rad[0], rad[1]) / (size * 0.62)))
        for j in range(n):
            a = math.radians(-arc + 2 * arc * (j + 0.5 * (i % 2)) / n)
            u = GV(math.sin(a) * ring, math.cos(a) * ring, t)
            p = GV(ctr) + GV(u.x * rad[0], u.y * rad[1], u.z * rad[2])
            nrm = GV(u.x / rad[0], u.y / rad[1], u.z / rad[2]).normalized()
            f = GV(0, 0, 1)
            f = (f - nrm * f.dot(nrm)).normalized()
            side = nrm.cross(f).normalized()
            M = Matrix((side, nrm, f)).transposed()          # local x = side, y = normal, z = flow (game axes)
            ctr_p = p + nrm * 0.05 + f * size * 0.25
            c.ellipsoid(B(ctr_p), (size * 0.62, size * 0.16, size * 0.6), GOLDT if rng.random() < mix else BRONZE, bones,
                        rot=G @ M @ G, seg=(10, 6))


def build():
    c = Creature("Pangolin", height=5.5)
    k = cute_quad(c, BRONZE2, belly=SKIN, paw=SKIN, body=(1.45, 1.2, 1.85), leg_h=1.0, leg_r=0.42, head_r=1.2, head_up=0.35, tail=3)
    h, r = k["head"], k["head_r"]
    by, rx, ry, rz = k["by"], k["rx"], k["ry"], k["rz"]
    scales(c, (0, by, 0), (rx, ry, rz), ["Hips", "Chest"], rows=8, size=0.66, seed=2, mix=0.18)
    c.ellipsoid(h, (r, r * 0.92, r), BRONZE2, "Head", seg=(24, 16))
    scales(c, (-h.x, h.z, h.y), (r, r * 0.92, r), "Head", rows=4, size=0.5, z_range=(-0.35, 0.8), arc=75, seed=3, mix=0.18)
    # soft pink face + small snout
    c.ellipsoid(h + P(0, -0.18, -r * 0.55), (0.88, 0.72, 0.62), FACE, "Head", seg=(18, 12))
    c.ellipsoid(h + P(0, -0.32, -r * 1.05), (0.3, 0.24, 0.3), FACE, "Head", seg=(12, 8))
    c.ellipsoid(h + P(0, -0.3, -r * 1.33), (0.13, 0.1, 0.06), NOSE, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.eye(h + P(s * 0.42, 0.05, -r * 0.92), 0.2, P(s * 0.45, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.8, 0.1, -r * 0.2), (0.16, 0.14, 0.08), FACE, "Head", stud=False)
    for s, S in ((-1, "L"), (1, "R")):
        for z, bone in ((k["sz"], "Fore" + S), (k["hz"], "Shin" + S)):
            claws(c, s * k["lx"], z - 0.45, CLAWC, bone, n=3, size=0.2)
    # long scaled tail curling up behind
    t = P(0, by + 0.0, rz * 0.85)
    pts = [t, t + P(0, -0.2, 0.9), t + P(0, 0.3, 1.6), t + P(0, 1.1, 1.75), t + P(0, 1.5, 1.3)]
    c.tube(pts, [0.65, 0.5, 0.38, 0.26, 0.12], BRONZE, ["Tail1", "Tail2", "Tail3"], seg=12)
    for i in range(len(pts) - 1):
        for j in range(3):
            p = pts[i].lerp(pts[i + 1], (j + 0.5) / 3)
            rr = 0.62 - 0.12 * (i + j / 3)
            c.ellipsoid(p + P(0, rr * 0.55, 0), (rr * 0.85, rr * 0.35, rr * 0.55), GOLDT if (i + j) % 2 else BRONZE, ["Tail1", "Tail2", "Tail3"][min(2, i * 3 // 4)], seg=(10, 6))
    aura(c, "orbit", (255, 200, 70), (170, 110, 60), "Mythic")
    c.extra["speed"] = 1.0
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (0, 6 * sin(p), 0), "Tail3": (8 * sin(2 * p), 0, 0), "Head": (4 * sin(2 * p), 0, 5 * sin(p))}
    quad_anims(c, tail=3, stride=22, bob=0.08, extra=extra)


VARIANTS = {"Jade": {BRONZE: C(60, 160, 110), BRONZE2: C(35, 110, 75), GOLDT: C(220, 250, 220), SKIN: C(220, 235, 220)}}
