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
    bl = list(bone) if isinstance(bone, (list, tuple)) else [bone]
    if backing:
        c.tube([ctr - fb * r * 0.25, ctr - fb * r * 0.02], [r * 1.35, r * 1.35], backing, bl, seg=20, sub=1)
    c.tube([ctr - fb * r * 0.1, ctr + fb * r * 0.12], [r, r], col, bl, seg=20, sub=1, stud=False, glow=glow)
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


# ============================================================== FIERCE / GUARDIAN QUADRUPED
def fierce_quad(c, col, belly=None, sh=4.4, hip=None, L=2.0, W=1.3, neck=(0.9, 0.8), head=1.6, tail=3, tail_len=0.9,
                body_r=1.45, leg_r=(0.8, 0.62, 0.52), paw=(0.72, 0.4, 0.9), paw_col=None, paint=None, belly_paint=None,
                hump=0.25):
    """heavy guardian body on detail.beast: thick barrel, muscular legs (about 35-45% of height), wide stance.
    Returns the beast key dict (+ 'body_r'). Head shapes are left to the creature."""
    from detail import beast, leg, T, E, V
    k = beast(c, sh=sh, hip=hip, L=L, W=W, neck=neck, head=head, tail=tail, tail_len=tail_len, tail_lift=0.15)
    sh, hip, cz, hz, mid = k["sh"], k["hip"], k["cz"], k["hz"], k["mid"]
    TB = ["Hips", "Chest"]
    r = body_r
    T(c, [V(0, hip, hz + 0.9), V(0, hip + 0.1, hz), V(0, mid.y + hump * 0.5, 0), V(0, sh + hump, cz + 0.2), V(0, sh + 0.2, cz - 0.6)],
      [r * 0.7, r * 0.98, r * 1.04, r * 1.1, r * 0.85], col, TB, seg=10, paint=paint)
    E(c, V(0, mid.y - r * 0.5, -0.2), (r * 0.78, r * 0.48, L * 1.05), belly or col, TB, seg=(10, 7), paint=belly_paint)
    T(c, [V(0, sh, cz), k["nb"], k["hb"] + V(0, -0.1, 0.25)], [r * 0.9, r * 0.78, r * 0.64], col, ["Chest", "Neck"], seg=9, paint=paint)
    for s, X in ((-1, "L"), (1, "R")):
        for front in (True, False):
            leg(c, k, X, col, r=leg_r, paw_col=paw_col or col, paw=paw, front=front, paint=paint)
    k["body_r"] = r
    return k


def hoof(c, f, r, col, bone):
    """split hoof around a foot point (game Vector)"""
    from detail import E, V
    for s in (-1, 1):
        E(c, f + V(s * r * 0.42, -0.08, -r * 0.45), (r * 0.48, r * 0.42, r * 0.62), col, bone, seg=(8, 5), stud=False)


def fierce_anims(c, tail=3, stride=24, bob=0.14, head_amp=0.8, roar=True, extra=None, wings=False):
    """heavy quad walk + idle with a roar (Jaw) beat"""
    def ex(t, walking):
        p = tau * t
        out = {}
        if walking:
            out = {"Jaw": (-3 - 4 * max(0, sin(2 * p)), 0, 0)} if roar else {}
        elif roar:
            rr = max(0, sin(math.pi * (t - 0.5) / 0.32)) if 0.5 <= t <= 0.82 else 0.0
            out = {"Jaw": (-3 - 24 * rr, 0, 0), "Head": (12 * rr + 3 * sin(2 * p), 0, 4 * sin(p) * (1 - rr)),
                   "Neck": (2 * sin(p) + 6 * rr, 12 * sin(p) * (1 - rr), 0)}
        if extra:
            out.update(extra(t, walking))
        return out
    quad_anims(c, wings=wings, tail=tail, stride=stride, bob=bob, head_amp=head_amp, extra=ex)


# ============================================================== PATTERNS / FLUFF
def panda_paint(col, leg_top, shoulder_z, band=0.6, band_lo=None):
    """panda pattern: black legs (below leg_top) + a black band over the shoulders around z = shoulder_z"""
    def mask(X, Y, Z):
        m = Y < leg_top
        sb = np.abs(Z - shoulder_z) < band
        if band_lo is not None:
            sb &= Y > band_lo
        return m | sb
    return (col, mask)


def puffs(c, ctr, rad, col, bones, n=40, size=0.42, where=None, seed=3, sink=0.45, col2=None, mix=0.3, paint=None):
    """cover an ellipsoid with round fluffy puffs (silkie feathers, clouds, manes). ctr = P() point, rad = game radii"""
    import random as _r
    rng = _r.Random(seed)
    ga = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        y = 1 - 2 * (i + 0.5) / n
        rr = math.sqrt(max(0, 1 - y * y))
        u = (math.cos(ga * i) * rr, y, math.sin(ga * i) * rr)
        if where and not where(u):
            continue
        s = size * (1 + rng.uniform(-0.2, 0.2))
        p = ctr + P(u[0] * (rad[0] - s * sink), u[1] * (rad[1] - s * sink), u[2] * (rad[2] - s * sink))
        cc = col2 if (col2 is not None and rng.random() < mix) else col
        c.ellipsoid(p, (s, s * 0.9, s), cc, bones, seg=(10, 7), paint=paint)


# ============================================================== SWIMMER (cute fish / dolphin, floats)
def cute_swimmer(c, y0=2.2, head_r=1.1, body=(1.0, 1.0, 1.3), length=4.2, n=4, fins=True):
    """floating swimmer skeleton: Root, Head (front), Spine1..n along +z (back), FinL/R at the sides of Spine1.
    Returns dict with spine points (P vectors), chain names, head centre. Shapes are left to the creature."""
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    z0 = -0.2
    pts = [P(0, y0, z0 + length * i / n) for i in range(n + 1)]
    chain = spine(c, pts, parent="Root")
    hc = P(0, y0 + 0.05, z0 - head_r * 0.55)
    c.bone("Head", P(0, y0, z0), hc + P(0, 0, -head_r), "Spine1")
    if fins:
        for s, S in ((-1, "L"), (1, "R")):
            c.bone("Fin" + S, P(s * body[0] * 0.8, y0 - 0.3, z0 + 0.3), P(s * (body[0] + 0.9), y0 - 0.6, z0 + 0.8), "Spine1")
    return dict(y0=y0, pts=pts, chain=chain, head=hc, head_r=head_r, z0=z0)


def swimmer_anims(c, chain, amp=10, axis="yaw", hover=0.35, fins=True, extra=None):
    swim_anims(c, chain, fins=[("FinL", -1), ("FinR", 1)] if fins else (), amp=amp, axis=axis, hover=hover, extra=extra)


# ============================================================== DRAGON HEAD (shared by every dragon-like creature)
def dragon_head(c, hb, s, col, belly, horn, whisk, mane, glow, bone="Head", jaw=None, horns="antler", teeth=True,
                mane_n=4, seed=1, core=C(255, 250, 220), brow=None, snout=1.0, beard=None):
    """Chinese dragon head in game space. hb = back of the skull (detail.V), s = scale, front = -z.
    horns: 'antler' (branched deer horns), 'swept' (smooth back-swept), 'one' (single horn), None.
    jaw = bone for the lower jaw (defaults to the head bone). Returns key points."""
    from detail import E, T, S, V, maw, eyes_pair, fur_line, swept_horn
    jaw = jaw or bone
    E(c, hb + V(0, 0.15 * s, -0.55 * s), (0.95 * s, 0.85 * s, 1.0 * s), col, bone, seg=(12, 9))
    sn = snout
    T(c, [hb + V(0, 0.1 * s, -0.95 * s), hb + V(0, -0.02 * s, -1.7 * s * sn), hb + V(0, -0.08 * s, -2.25 * s * sn)],
      [0.72 * s, 0.56 * s, 0.46 * s], col, bone, seg=10, flat=(1.0, 0.85))
    E(c, hb + V(0, 0.02 * s, -2.32 * s * sn), (0.48 * s, 0.34 * s, 0.28 * s), col, bone, seg=(10, 7))
    for sx in (-1, 1):
        E(c, hb + V(sx * 0.2 * s, 0.12 * s, -2.55 * s * sn), (0.1 * s, 0.08 * s, 0.06 * s), C(30, 20, 20), bone, stud=False)
        S(c, hb + V(sx * 0.45 * s, 0.6 * s, -1.25 * s), hb + V(sx * 0.62 * s, 0.85 * s, -0.55 * s), 0.18 * s, brow or col, bone, seg=4, n=3)
    E(c, hb + V(0, -0.55 * s, -1.55 * s * sn), (0.5 * s, 0.18 * s, 0.85 * s * sn), belly, jaw, seg=(10, 6))
    if teeth:
        maw(c, hb + V(0, -0.35 * s, -2.2 * s * sn), 0.42 * s, 1.0 * s * sn, 0.36 * s, bone, jaw, n=8, tooth=0.12 * s, fangs=1.8)
    eyes_pair(c, hb + V(0, 0.45 * s, -1.05 * s), 0.46 * s, 0.22 * s, bone, glow=glow, core=core, brow=brow or col, slant=22, turn=0.6)
    for sx in (-1, 1):
        b0 = hb + V(sx * 0.42 * s, 0.75 * s, -0.25 * s)
        if horns == "antler":
            main = [b0, b0 + V(sx * 0.2 * s, 0.6 * s, 0.35 * s), b0 + V(sx * 0.35 * s, 1.0 * s, 1.0 * s), b0 + V(sx * 0.4 * s, 1.2 * s, 1.55 * s)]
            swept_horn(c, main, 0.2 * s, horn, bone, seg=6)
            swept_horn(c, [main[1].lerp(main[2], 0.4), main[1].lerp(main[2], 0.4) + V(sx * 0.15 * s, 0.6 * s, -0.1 * s)], 0.12 * s, horn, bone, seg=5)
        elif horns == "swept":
            swept_horn(c, [b0, b0 + V(sx * 0.15 * s, 0.45 * s, 0.6 * s), b0 + V(sx * 0.25 * s, 0.7 * s, 1.4 * s)], 0.24 * s, horn, bone, seg=6, ribs=True)
        # whiskers trailing back from the snout
        T(c, [hb + V(sx * 0.38 * s, -0.05 * s, -2.15 * s * sn), hb + V(sx * 0.95 * s, -0.12 * s, -1.95 * s * sn),
              hb + V(sx * 1.5 * s, -0.5 * s, -1.4 * s), hb + V(sx * 1.75 * s, -0.95 * s, -0.85 * s)],
          [0.09 * s, 0.07 * s, 0.05 * s, 0.03 * s], whisk, bone, seg=5)
    if horns == "one":
        swept_horn(c, [hb + V(0, 0.8 * s, -0.7 * s), hb + V(0, 1.45 * s, -0.8 * s), hb + V(0, 1.9 * s, -0.55 * s)], 0.24 * s, horn, bone, seg=6, ribs=True)
    # mane: shard fur fringe framing the back of the skull and cheeks
    if mane is not None:
        pts = [hb + V(-0.9 * s, -0.4 * s, -0.4 * s), hb + V(-0.85 * s, 0.6 * s, 0.0), hb + V(0, 1.0 * s, 0.25 * s),
               hb + V(0.85 * s, 0.6 * s, 0.0), hb + V(0.9 * s, -0.4 * s, -0.4 * s)]
        fur_line(c, pts, mane, bone, length=0.9 * s, width=0.55 * s, out=lambda p: (p - hb).normalized() + V(0, 0, 0.9), n_per=mane_n, seed=seed)
    if beard is not None:
        fur_line(c, [hb + V(-0.35 * s, -0.75 * s, -1.4 * s), hb + V(0.35 * s, -0.75 * s, -1.4 * s)], beard, jaw, length=0.7 * s, width=0.4 * s, out=V(0, -1, 0.2), n_per=4, seed=seed + 1)
    return dict(nose=hb + V(0, 0, -2.4 * s * sn), top=hb + V(0, 0.9 * s, -0.5 * s))


def scale_paint(col, size=0.55, width=0.08, only=None):
    """overlapping fish / dragon scale arcs painted on (rows along z, offset every other row)"""
    def mask(X, Y, Z):
        b = (Y + X * 0.35) / size
        row = np.floor(b)
        a = Z / size + 0.5 * np.mod(row, 2)
        fx = a - np.floor(a) - 0.5
        fy = b - row
        d = np.sqrt(fx * fx + fy * fy)
        m = np.abs(d - 0.5) < width
        if only is not None:
            m &= only(X, Y, Z)
        return m
    return (col, mask)


# ============================================================== SERPENTINE DRAGON (Kobe's rules)
def serpent_dragon(c, col, belly, mane, claw_col, horn, whisk, glow, L=10.0, n=6, y0=4.0, wave=0.9, rise=0.6,
                   head_scale=None, paint=None, horns="antler", fins=None, legs=True, mane_n=3, seed=1, brow=None, core=C(255, 250, 220)):
    """long floating Chinese dragon: body thickness about 1/8 of its length, head about twice the body width,
    short clawed legs, whiskers and a fur_line mane. Bones: Root, Spine1..n, Head, Jaw, ArmL/R, ThighL/R.
    Animate with swim_anims (yaw) + hover. Returns dict with spine points (game Vectors) and radius."""
    from detail import V, B, T, E, fur_line, claws3, S
    R = L / 16.0                                     # body radius -> thickness = L/8
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append(V(wave * math.sin(t * math.tau * 1.1), y0 + rise * math.sin(t * math.tau * 0.9 + 0.6) - 0.4 * t, t * L))
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    names = spine(c, [B(p) for p in pts], parent="Root")
    hs = head_scale or (2 * R * 2) / (1.9)           # skull width (1.9 s) = twice the body width (4R)
    hb = pts[0] + V(0, 0.25 * hs, -0.35 * hs)
    c.bone("Head", B(pts[0]), B(hb + V(0, 0.1, -2.2 * hs)), "Spine1")
    c.bone("Jaw", B(hb + V(0, -0.4 * hs, -0.3 * hs)), B(hb + V(0, -0.6 * hs, -2.2 * hs)), "Head")
    radii = [R * (1.05 - 0.75 * (i / n) ** 1.6) for i in range(n + 1)]
    T(c, pts, radii, col, names, seg=12, paint=paint)
    T(c, [pts[0] + V(0, 0, 0.3), hb + V(0, -0.1 * hs, 0.1)], [R * 1.05, R * 1.0], col, ["Spine1", "Head"], seg=12, sub=1, paint=paint)
    # belly plates: a lighter strip under the body
    for i in range(n):
        for j in range(3):
            p = pts[i].lerp(pts[i + 1], (j + 0.5) / 3)
            rr = radii[i] + (radii[i + 1] - radii[i]) * (j + 0.5) / 3
            E(c, p + V(0, -rr * 0.62, 0), (rr * 0.72, rr * 0.4, L / n / 3 * 0.6), belly, names[i], seg=(8, 5))
    # mane along the spine
    for i in range(n - 1):
        fur_line(c, [pts[i] + V(0, radii[i] * 0.85, 0), pts[i + 1] + V(0, radii[i + 1] * 0.85, 0)], mane, names[i], length=R * 1.6 * (1 - 0.4 * i / n),
                 width=R * 0.9, out=V(0, 1, 0.7), n_per=mane_n, seed=seed + i)
    if fins is not None:
        for i in range(1, n):
            S(c, pts[i] + V(0, radii[i] * 0.9, 0), pts[i] + V(0, radii[i] * 0.9 + R * 1.2, R * 0.8), R * 0.5, fins, names[i], seg=4, n=3)
    # short clawed legs: front pair on Spine1, back pair on Spine(n-2)
    if legs:
        for li, (si, nm) in enumerate(((1, "Arm"), (n - 2, "Thigh"))):
            p = pts[si]
            for s, X in ((-1, "L"), (1, "R")):
                a = p + V(s * radii[si] * 0.8, -radii[si] * 0.2, 0)
                f = a + V(s * R * 0.9, -R * 1.5, -R * 0.5)
                c.bone(nm + X, B(a), B(f), names[si])
                T(c, [a, a.lerp(f, 0.5) + V(s * 0.1, 0.1, 0), f], [R * 0.45, R * 0.4, R * 0.32], col, nm + X, seg=8)
                E(c, f, (R * 0.42, R * 0.25, R * 0.5), col, nm + X, seg=(8, 5))
                claws3(c, f + V(0, 0.1, R * 0.2), claw_col, nm + X, size=R * 0.35, spread=R * 0.3, z=-R * 0.6)
    k = dragon_head(c, hb, hs, col, belly, horn, whisk, mane, glow, bone="Head", jaw="Jaw", horns=horns, seed=seed + 1, brow=brow, core=core)
    # tail tuft
    fur_line(c, [pts[-2], pts[-1]], mane, names[-1], length=R * 1.4, width=R * 0.8, out=V(0, 0.6, 1), n_per=5, seed=seed + 2)
    return dict(pts=pts, radii=radii, names=names, hb=hb, hs=hs, R=R)


def serpent_anims(c, names, amp=10, hover=0.6, extra=None):
    def ex(t, walking):
        p = tau * t
        out = {"ArmL": (20 * sin(2 * p), 0, 0), "ArmR": (-20 * sin(2 * p), 0, 0),
               "ThighL": (-20 * sin(2 * p), 0, 0), "ThighR": (20 * sin(2 * p), 0, 0),
               "Jaw": (-4 - (8 if walking else 14) * max(0, sin(2 * p)), 0, 0), "Head": (4 * sin(2 * p), 0, 0)}
        if extra:
            out.update(extra(t, walking))
        return out
    swim_anims(c, names, amp=amp, axis="yaw", hover=hover, extra=ex)


# ============================================================== FLYING BIRD (spread wings, hovers)
def flying_bird(c, col, belly, leg_col, wing_col, tip_col, body=(1.2, 1.15, 1.4), head_r=1.0, y_lift=1.6,
                span=(1.0, 2.6, 4.4), n_feathers=10, feather_len=(1.6, 1.2), cover=None, tail=2):
    """cute_bird body lifted into the air with big spread feathered wings (WingL/R + WingTipL/R bones).
    Legs stay short and tucked. Returns the cute_bird key dict."""
    k = cute_bird(c, col, belly=belly, leg_col=leg_col, body=body, leg_h=0.8, head_r=head_r, head_up=1.05, head_fwd=0.5,
                  wing_col=wing_col, tail=tail, foot="toes")
    # drop the folded wings (shapes + bones), add spread wings instead
    c.shapes = [sh for sh in c.shapes if not (set(sh["bones"]) <= {"WingL", "WingR"})]
    c.bones = [b for b in c.bones if b[0] not in ("WingL", "WingR")]
    # lift the whole bird (short tucked legs included) into the air; Root stays on the ground
    up = P(0, y_lift, 0)
    for sh in c.shapes:
        bmesh.ops.translate(sh["bm"], vec=up, verts=sh["bm"].verts)
    c.bones = [(n, h, t, p) if n == "Root" else (n, h + up, t + up, p) for n, h, t, p in c.bones]
    k["by"] += y_lift
    k["head"] = k["head"] + up
    k["nb"] = k["nb"] + up
    by, rx = k["by"], body[0]
    root, mid, tip = (rx * 0.75, by + 0.35, -0.1), (span[1], by + 1.1, 0.2), (span[2], by + 0.9, 0.7)
    wing_bones(c, root, mid, tip)
    feather_wings(c, root, mid, tip, wing_col, tip_col, cover=cover or col, n=n_feathers, length=feather_len, width=0.9, arm_col=wing_col)
    k["wing"] = (root, mid, tip)
    return k


def flyer_anims(c, flap=30, tail=2, extra=None):
    def mk(rate, fl, walking):
        def fn(t):
            p = tau * t * rate
            out = {
                "Root": ((5 * sin(p - 1.2), 0, 0), (0, 0.4 * sin(p - 1.2), 0)),
                "Chest": (3 * sin(p), 0, 0), "Neck": (-3 * sin(p + 0.8), 0, 0), "Head": (4 * sin(p + 1.4), 0, 6 * sin(t * tau)),
                "WingL": (0, 0, fl * sin(p)), "WingR": (0, 0, -fl * sin(p)),
                "WingTipL": (0, 0, fl * 0.6 * sin(p - 0.7)), "WingTipR": (0, 0, -fl * 0.6 * sin(p - 0.7)),
                "ThighL": (-25, 0, 0), "ThighR": (-25, 0, 0), "ShinL": (30, 0, 0), "ShinR": (30, 0, 0),
            }
            for i in range(tail):
                out["Tail%d" % (i + 1)] = (6 * sin(p - 1.5 - i * 0.5), 0, 0)
            if extra:
                out.update(extra(t, walking))
            return out
        return fn
    c.animate({"Walk": (24, 1.0, mk(3, flap, True)), "Idle": (40, 4.0, mk(4, flap * 0.75, False))})
