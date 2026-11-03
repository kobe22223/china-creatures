"""Steal an Egg in China: shared helpers for the China roster.

- cute_bird + bird_anims: Kobe's bird proportions (round body, head about 35% of height, short legs tucked
  under at about 15%, wings folded against the body).
- festival motifs: gold coin, lucky knot with tassel, bronze bell, paper lantern, cloud swirl filigree.
Game coords via P: x right, y up, z back, front = -z.
"""
from kit import *

GOLD = C(255, 200, 60)
GOLD2 = C(214, 150, 30)
RED = C(214, 32, 40)
RED2 = C(160, 18, 30)
JADE = C(70, 180, 120)
JADE2 = C(35, 120, 80)
PORCELAIN = C(245, 245, 250)
COBALT = C(40, 80, 190)


# ============================================================== BIRD (cute)
def cute_bird(c, col, belly=None, leg_col=C(255, 150, 40), body=(1.25, 1.2, 1.45), leg_h=0.75, head_r=1.0,
              head_up=0.95, head_fwd=0.55, wing_col=None, tail=1, paint=None, foot="web", leg_x=0.48):
    """round bird body on short tucked legs, big head sitting up and forward, folded wings.
    Bones: Root, Hips, Chest, Neck, Head, ThighL/R, ShinL/R, WingL/R, Tail1.. Returns key points."""
    rx, ry, rz = body
    by = leg_h + ry * 0.82                       # body centre: the bottom of the body sinks over the legs
    hc = P(0, by + ry * head_up, -rz * head_fwd)  # head centre
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    c.bone("Hips", P(0, by, rz * 0.5), P(0, by, 0), "Root")
    c.bone("Chest", P(0, by, 0), P(0, by + ry * 0.4, -rz * 0.45), "Hips")
    nb = P(0, by + ry * 0.45, -rz * 0.4)
    c.bone("Neck", nb, hc + P(0, -head_r * 0.4, 0), "Chest")
    c.bone("Head", hc + P(0, -head_r * 0.4, 0), hc + P(0, 0.1, -head_r), "Neck")
    lx = rx * leg_x
    for s, S in ((-1, "L"), (1, "R")):
        c.bone("Thigh" + S, P(s * lx, by - ry * 0.45, 0.05), P(s * lx, leg_h * 0.55, -0.02), "Hips")
        c.bone("Shin" + S, P(s * lx, leg_h * 0.55, -0.02), P(s * lx, 0.1, -0.12), "Thigh" + S)
        c.bone("Wing" + S, P(s * rx * 0.8, by + ry * 0.35, -rz * 0.25), P(s * rx * 0.95, by - ry * 0.1, rz * 0.6), "Chest")
    t0, prev = P(0, by + ry * 0.15, rz * 0.85), "Hips"
    for i in range(tail):
        t1 = t0 + P(0, 0.35, 0.5)
        c.bone("Tail%d" % (i + 1), t0, t1, prev)
        prev, t0 = "Tail%d" % (i + 1), t1
    belly = belly or col
    wing_col = wing_col or col
    c.ellipsoid(P(0, by, 0), (rx, ry, rz), col, ["Hips", "Chest"], seg=(24, 16), paint=paint)
    c.ellipsoid(P(0, by - ry * 0.3, -rz * 0.3), (rx * 0.78, ry * 0.68, rz * 0.72), belly, ["Hips", "Chest"], seg=(18, 12))
    # neck filler so the head sits on the body with no gap
    c.ellipsoid(nb.lerp(hc, 0.45), (head_r * 0.72, head_r * 0.75, head_r * 0.72), col, ["Chest", "Neck"], seg=(16, 10), paint=paint)
    # folded wings: flattened teardrops hugging the sides of the body
    for s, S in ((-1, "L"), (1, "R")):
        w = P(s * rx * 0.8, by + ry * 0.12, rz * 0.15)
        c.ellipsoid(w, (rx * 0.26, ry * 0.5, rz * 0.62), wing_col, "Wing" + S, rot=euler(-14, s * -6, s * 4), seg=(16, 10), paint=paint)
    # legs: short thigh stub sunk in the body, thin shin, flat foot
    for s, S in ((-1, "L"), (1, "R")):
        c.ellipsoid(P(s * lx, by - ry * 0.55, 0.0), (0.36, 0.42, 0.4), belly, "Thigh" + S, seg=(12, 8))
        c.tube([P(s * lx, leg_h * 0.95, -0.02), P(s * lx, leg_h * 0.5, -0.04), P(s * lx, 0.2, -0.1)], [0.17, 0.15, 0.14], leg_col, ["Shin" + S], seg=10, sub=1)
        if foot == "web":
            c.ellipsoid(P(s * lx, 0.1, -0.38), (0.36, 0.09, 0.42), leg_col, "Shin" + S, seg=(12, 6))
        else:   # three toes
            for t in (-1, 0, 1):
                c.tube([P(s * lx, 0.12, -0.1), P(s * lx + t * 0.22, 0.08, -0.5)], [0.08, 0.06], leg_col, ["Shin" + S], seg=6, sub=1)
            c.tube([P(s * lx, 0.12, -0.05), P(s * lx, 0.08, 0.25)], [0.07, 0.05], leg_col, ["Shin" + S], seg=6, sub=1)
    return dict(by=by, rx=rx, ry=ry, rz=rz, head=hc, head_r=head_r, leg_h=leg_h, nb=nb, lx=lx)


def bird_anims(c, tail=1, stride=30, waddle=7, bob=0.1, flap=10, extra=None):
    """waddle walk (body rolls side to side, head bobs) + idle (looks around, ruffles wings)"""
    def walk(t):
        p = tau * t
        out = {
            "Root": ((0, 0, waddle * sin(p)), (0, bob * abs(sin(p)), 0)),
            "Chest": (3 * sin(2 * p), 0, 0),
            "Neck": (-6 * sin(2 * p), 0, 0), "Head": (5 * sin(2 * p + 0.6), 0, -waddle * 0.6 * sin(p)),
            "ThighL": (-stride * sin(p), 0, 0), "ThighR": (stride * sin(p), 0, 0),
            "ShinL": (20 * max(0, sin(p + 0.5)), 0, 0), "ShinR": (20 * max(0, -sin(p + 0.5)), 0, 0),
            "WingL": (0, 0, -flap * 0.5 * max(0, sin(2 * p))), "WingR": (0, 0, flap * 0.5 * max(0, sin(2 * p))),
        }
        for i in range(tail):
            out["Tail%d" % (i + 1)] = (0, 14 * sin(p - 0.6 * i), 0)
        if extra:
            out.update(extra(t, True))
        return out

    def idle(t):
        p = tau * t
        flut = max(0, sin(math.pi * (t - 0.6) / 0.2)) if 0.6 <= t <= 0.8 else 0.0
        out = {
            "Root": ((0, 0, 0), (0, 0.05 * sin(2 * p), 0)),
            "Chest": (2 * sin(2 * p), 0, 0),
            "Neck": (3 * sin(2 * p), 18 * sin(p), 0), "Head": (4 * sin(2 * p + 1), 0, 10 * sin(p + 0.5)),
            "WingL": (0, 0, -flap * 2 * flut), "WingR": (0, 0, flap * 2 * flut),
        }
        for i in range(tail):
            out["Tail%d" % (i + 1)] = (0, 10 * sin(3 * p - 0.6 * i), 0)
        if extra:
            out.update(extra(t, False))
        return out
    c.animate({"Walk": (24, 1.0, walk), "Idle": (40, 4.0, idle)})


# ============================================================== MOTIFS
def coin(c, ctr, r, bone, facing=(0, 0, -1), col=GOLD, hole=C(120, 70, 20), glow=False, backing=None):
    """round Chinese coin with a square hole: a flat disc + raised rim. facing: outward direction in game axes.
    backing = colour of a slightly bigger disc behind it (contrast on same-coloured bodies)"""
    f = Vector(facing).normalized()
    fb = P(f.x, f.y, f.z)
    ax = Vector((0, 1, 0)).rotation_difference(Vector((f.x, f.y, f.z))).to_matrix()
    rot = G @ ax @ G
    if backing:
        c.tube([ctr - fb * r * 0.25, ctr - fb * r * 0.02], [r * 1.35, r * 1.35], backing, [bone], seg=20, sub=1)
    c.tube([ctr - fb * r * 0.1, ctr + fb * r * 0.12], [r, r], col, [bone], seg=20, sub=1, stud=False, glow=glow)
    c.torus(ctr + fb * r * 0.12, r * 0.88, r * 0.12, col, bone, rot=rot, seg=(20, 5), stud=False, glow=glow)
    c.box(ctr + fb * r * 0.13, (r * 0.26, r * 0.26, r * 0.26), hole, bone, rot=rot, stud=False)


def lucky_knot(c, top, size, bone, col=RED, tassel=RED2, bead=GOLD):
    """red Chinese knot (diamond of loops) with a gold bead and a tassel hanging below `top`"""
    s = size
    c.box(top + P(0, -s * 0.6, 0), (s * 0.42, s * 0.42, s * 0.16), col, bone, rot=euler(0, 0, 45), stud=False)
    for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
        c.ellipsoid(top + P(dx * s * 0.62, -s * 0.6 + dy * s * 0.62, 0), (s * 0.22, s * 0.22, s * 0.14), col, bone, seg=(10, 6), stud=False)
    c.ellipsoid(top + P(0, -s * 1.35, 0), (s * 0.2, s * 0.2, s * 0.2), bead, bone, seg=(10, 6), stud=False)
    c.tube([top + P(0, -s * 1.45, 0), top + P(0, -s * 2.4, 0.02)], [s * 0.16, s * 0.3], tassel, [bone], seg=10, sub=1)


def bell(c, ctr, r, bone, col=GOLD2, rim=GOLD):
    """small bronze collar bell"""
    c.ellipsoid(ctr, (r, r * 1.05, r), col, bone, seg=(14, 8), stud=False)
    c.torus(ctr + P(0, -r * 0.45, 0), r * 0.92, r * 0.18, rim, bone, seg=(14, 5), stud=False)
    c.ellipsoid(ctr + P(0, -r * 0.65, -r * 0.55), (r * 0.25, r * 0.25, r * 0.2), C(60, 40, 20), bone, seg=(8, 5), stud=False)


def lantern(c, ctr, r, bone, col=RED, cap=GOLD, glow=C(255, 190, 80), tassel=True):
    """round red paper lantern with gold caps, ribs and a glowing core band"""
    c.ellipsoid(ctr, (r, r * 0.85, r), col, bone, seg=(16, 10), stud=False)
    for k in range(6):
        a = k / 6 * math.tau
        pts = [ctr + P(math.sin(a) * r * 1.01 * math.cos(math.radians(e)), r * 0.85 * math.sin(math.radians(e)), math.cos(a) * r * 1.01 * math.cos(math.radians(e))) for e in range(-70, 71, 35)]
        c.tube(pts, [0.035 * r / 0.5] * len(pts), cap, [bone], seg=5, sub=1, stud=False)
    for sgn in (-1, 1):
        c.tube([ctr + P(0, sgn * r * 0.72, 0), ctr + P(0, sgn * r * 0.95, 0)], [r * 0.42, r * 0.38], cap, [bone], seg=12, sub=1, stud=False)
    c.ellipsoid(ctr, (r * 0.55, r * 0.2, r * 0.55), glow, bone, seg=(10, 4), glow=True)
    if tassel:
        c.tube([ctr + P(0, -r * 0.95, 0), ctr + P(0, -r * 1.7, 0)], [r * 0.08, r * 0.18], col, [bone], seg=8, sub=1)


def cloud_filigree(col, scale=1.2, width=0.08, only=None):
    """cloud swirl trim paint for royal creatures (wrapper so creature files only import cn)"""
    from detail import filigree
    return filigree(col, scale=scale, width=width, only=only)
