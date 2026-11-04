"""Steal an Egg in China: 33 voxel eggs (11 zones x Egg / BigEgg / GiantEgg). One function per zone.
Voxel units (1 = 0.2 studs). Angles: 0 = front (-z). t = height fraction."""
import math
from voxel import *

# ---------------------------------------------------------------- palette
WHITE, IVORY, COBALT, COBALT2, SKY = (245, 247, 252), (238, 232, 214), (36, 72, 176), (78, 120, 210), (150, 190, 240)
GOLD, GOLD2, RED, RED2, JADE, JADE2, JADE3 = (255, 200, 60), (214, 150, 30), (205, 32, 38), (150, 18, 26), (70, 175, 120), (40, 125, 85), (150, 215, 175)
GREEN, GREEN2, GREEN3, STRAW, STRAW2, WATER, WATER2 = (95, 175, 70), (60, 135, 50), (140, 205, 90), (232, 196, 110), (190, 150, 70), (90, 165, 220), (60, 125, 195)
BLACK, GREY, GREY2, GREY3, MORTAR = (35, 35, 40), (140, 140, 145), (105, 105, 112), (175, 175, 180), (70, 68, 66)
MOSS, MOSS2, CELADON, CELADON2, CLAY, CLAY2, CLAY3 = (85, 150, 60), (60, 115, 45), (165, 205, 175), (115, 160, 130), (196, 118, 78), (160, 90, 58), (220, 150, 105)
BRONZE, BRONZE2, YELLOW, PEARL, PEARL2, SEA, SEA2 = (175, 125, 60), (130, 90, 40), (250, 205, 50), (245, 240, 235), (220, 215, 230), (40, 140, 200), (30, 100, 160)
CORAL, CORAL2, SNOW, ROCK, ROCK2, PINE, PINE2 = (255, 120, 110), (230, 80, 90), (250, 252, 255), (120, 125, 135), (90, 95, 105), (45, 120, 70), (30, 90, 55)
BROWN, CREAM, ORANGE, TEA = (110, 75, 45), (250, 240, 215), (255, 140, 40), (90, 150, 60)
# glow colours
SUNG, JADEG, LANTG, TORCHG, AQUAG, EMBERG, WINDG, SPIRITG, BIOG, HALOG, GEMG = (
    (255, 205, 80), (90, 255, 160), (255, 190, 90), (255, 130, 40), (90, 240, 230), (255, 110, 40), (255, 215, 100),
    (160, 210, 255), (100, 255, 230), (255, 235, 150), (80, 255, 170))

SIZES = {"Egg": 3.2, "BigEgg": 4.4, "GiantEgg": 6.0}


def new(zone, kind, base):
    return Egg("China_Z%02d_%s" % (zone, kind), SIZES[kind], base=base, kind=kind)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k, a[2] + b[2] * k)


def norm(v):
    L = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / L for c in v)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


# ================================================================ shared features
def terrace(e, t0, t1, out, col, top=None):
    """flat-topped stepped ring (paddy terrace, battlement base, eave): a disc of radius R(t0) + out between t0 and t1"""
    y0, y1 = t0 * e.h, t1 * e.h
    R = e.R(y0) + out
    e.fill(lambda x, y, z: y0 <= y <= y1 and math.hypot(x, z) <= R, ((-R, R), (y0, y1), (-R, R)),
           (lambda x, y, z: top if (top and y > y1 - 1) else col))


def ring_layer(e, t0, t1, col, d1=1.0, d0=0.0, glow=False):
    """raised ring hugging the egg between heights t0..t1"""
    e.shell_offset(lambda x, y, z, a, t: t0 <= t <= t1, d0, d1, col, glow)


def cap(e, t0, col, thick=1.0, knob=None, knob_r=1.2):
    """lid-like cap: a raised layer over everything above t0, plus an optional knob on top"""
    e.shell_offset(lambda x, y, z, a, t: t >= t0, 0, thick, col)
    if knob:
        e.sphere((0, e.h + thick + knob_r * 0.6, 0), knob_r, knob)


def relief(e, pts, width, col, d1=1.0, glow=False):
    """raise the surface along a path of 3D points (voxel units)"""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; zs = [p[2] for p in pts]
    lo = (min(xs) - width - 2, min(ys) - width - 2, min(zs) - width - 2)
    hi = (max(xs) + width + 2, max(ys) + width + 2, max(zs) + width + 2)
    w2 = (width + 0.5) ** 2

    def region(x, y, z, a, t):
        if not (lo[0] <= x <= hi[0] and lo[1] <= y <= hi[1] and lo[2] <= z <= hi[2]):
            return False
        return any((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2 <= w2 for px, py, pz in pts)
    e.shell_offset(region, 0, d1, col, glow)


def curl_pts(e, ang, t, size, turns=1.3, flip=1, tail=1.5):
    """points of a cloud-scroll spiral on the surface (plus a short tail) centred at (ang, t)"""
    pts = []
    n = 40
    for i in range(n + 1):
        th = i / n * turns * math.tau
        rr = size * (i / n)
        r0 = max(e.R(t * e.h), 1.0)
        a = ang + flip * math.degrees(rr * math.cos(th) / r0)
        tt = t + rr * math.sin(th) / e.h
        pts.append(e.surf(a, tt))
    for i in range(1, 8):
        a = ang + flip * math.degrees((size + tail * size * i / 7) / max(e.R(t * e.h), 1.0))
        pts.append(e.surf(a, t - 0.01 * i))
    return pts


def curls(e, n, t, size, col, d1=1.0, offset=0.0, turns=1.3):
    for k in range(n):
        relief(e, curl_pts(e, offset + k * 360.0 / n, t + (0.04 if k % 2 else -0.04), size, turns=turns, flip=1 if k % 2 else -1), 0.6, col, d1)


def shard(e, ang, t, length, r, col, up=0.35, glow=False):
    """crystal-like column: tapered capsule growing out of the surface"""
    base = e.surf(ang, t, -1.0)
    n = e.normal(ang, t)
    d = norm(add(n, (0, up, 0)))
    tip = add(base, d, length)
    e.capsule(base, tip, r, 0.35, col, glow)
    return tip


def leaf(e, base, d, length, width, col, thick=1.7, glow=False):
    d = norm(d)
    v = cross(d, (0, 1, 0))
    if sum(c * c for c in v) < 1e-4:
        v = (1, 0, 0)
    v = norm(v)
    e.plate(add(base, d, length / 2), d, v, length / 2, width / 2, thick, col, glow)


def torus(e, c, R, r, col, axis="y", glow=False):
    cx, cy, cz = c

    def inside(x, y, z):
        if axis == "y":
            q, h = math.hypot(x - cx, z - cz) - R, y - cy
        elif axis == "z":
            q, h = math.hypot(x - cx, y - cy) - R, z - cz
        else:
            q, h = math.hypot(y - cy, z - cz) - R, x - cx
        return q * q + h * h <= r * r
    m = R + r
    e.fill(inside, ((cx - m, cx + m), (cy - m, cy + m), (cz - m, cz + m)), col, glow)


def disc(e, c, R, thick, col, axis="z", glow=False):
    cx, cy, cz = c

    def inside(x, y, z):
        if axis == "z":
            return math.hypot(x - cx, y - cy) <= R and abs(z - cz) <= thick / 2
        return math.hypot(x - cx, z - cz) <= R and abs(y - cy) <= thick / 2
    e.fill(inside, ((cx - R, cx + R), (cy - R, cy + R), (cz - R, cz + R)), col, glow)


def studs(e, t, n, col, r=0.8, offset=0.0, glow=False, out=0.2):
    for k in range(n):
        e.sphere(e.surf(offset + k * 360.0 / n, t, out), r, col, glow=glow)


def ribs(e, n, col, width=0.7, t0=0.08, t1=0.92, d1=1.0, offset=0.0):
    """vertical raised ribs (lantern ribs, pillars)"""
    def region(x, y, z, a, t):
        if not (t0 <= t <= t1):
            return False
        da = ((a - offset) % (360.0 / n))
        da = min(da, 360.0 / n - da)
        return math.radians(da) * max(math.hypot(x, z), 1) <= width
    e.shell_offset(region, 0, d1, col)


def roof(e, yb, half, rise, col, edge=None, tips=None, thick=1.6, tip_len=2.5, tip_col=None):
    """square pagoda roof tier: sloped pyramid slab of half-size `half` starting at height yb, rising `rise` to the middle,
    with upturned corner tips"""
    def inside(x, y, z):
        m = max(abs(x), abs(z))
        if m > half:
            return False
        ys = yb + (half - m) / half * rise
        return ys <= y <= ys + thick
    e.fill(inside, ((-half, half), (yb, yb + rise + thick), (-half, half)),
           (lambda x, y, z: edge if (edge and max(abs(x), abs(z)) > half - 1.2) else col))
    for sx in (-1, 1):
        for sz in (-1, 1):
            c0 = (sx * (half - 0.5), yb + 0.5, sz * (half - 0.5))
            c1 = (sx * (half + tip_len * 0.5), yb + tip_len, sz * (half + tip_len * 0.5))
            e.capsule(c0, c1, 0.7, 0.4, tip_col or edge or col)


def battlements(e, t, n, col, h=2.5, w=1.6, out=1.2):
    y0 = t * e.h
    R = e.R(y0) + out
    for k in range(n):
        a = math.radians(k * 360.0 / n)
        c = (R * math.sin(a), y0 + h / 2, -R * math.cos(a))
        e.box(c, (w, h / 2, w), col)


def moss(e, t_edge, col, col2, drip=0.12, seed=4, d1=1.0):
    """moss layer over the top with drips hanging down at random angles"""
    def edge(a):
        k = int(a // 15)
        d = hsh(k, seed) * drip
        return t_edge - (d if hsh(k, seed + 1) < 0.55 else 0)
    e.shell_offset(lambda x, y, z, a, t: t >= edge(a), 0, d1,
                   lambda x, y, z, a, t: col2 if hsh(int(x), int(y), int(z), seed) < 0.3 else col)


def windows(e, angs, t, w, h, col, depth=2):
    """glowing rectangular windows / arrow slits carved into the surface"""
    for ang in angs:
        def region(x, y, z, a, tt, ang=ang):
            da = ((a - ang + 180) % 360) - 180
            return abs(math.radians(da) * max(math.hypot(x, z), 1)) <= w / 2 and abs(y - t * e.h) <= h / 2
        e.carve(region, col, depth=depth)


def glow_dots(e, n, col, seed=9, r=0.7, t0=0.1, t1=0.9):
    rng = random.Random(seed)
    for _ in range(n):
        p = e.surf(rng.uniform(0, 360), rng.uniform(t0, t1), 0.3)
        e.sphere(p, r, col, glow=True)


def bow(e, ang, t, col, col2=None, size=2.5):
    """ribbon bow sitting on the surface: two loops + a knot + two tails"""
    c = e.surf(ang, t, 0.6)
    n = e.normal(ang, t)
    side = norm(cross((0, 1, 0), n))
    for s in (-1, 1):
        lc = add(c, side, s * size * 0.75)
        e.plate(lc, side, (0, 1, 0), size * 0.75, size * 0.55, 1.6, col)
        leaf(e, add(c, (0, -0.5, 0)), add((side[0] * s * 0.4, -1, side[2] * s * 0.4), n, 0.2), size * 1.2, size * 0.5, col2 or col)
    e.sphere(add(c, n, 0.5), size * 0.35, col2 or col)


def chips(e, chance, inner, seed=1):
    """chipped blocks: knock out random surface voxels and show a darker colour underneath"""
    for p in e.surface_voxels():
        if p[1] > 1 and hsh(p[0], p[1], p[2], seed) < chance:
            del e.body[p]
            for d in DIRS:
                q = (p[0] + d[0], p[1] + d[1], p[2] + d[2])
                if q in e.body:
                    e.body[q] = inner


def bamboo_stalk(e, base, top, r, col, node, every=3.0):
    e.capsule(base, top, r, r, col)
    d = sub(top, base)
    L = math.sqrt(sum(v * v for v in d))
    k = 1
    while k * every < L:
        p = add(base, d, k * every / L)
        torus(e, p, r, 0.55, node)
        k += 1


# ================================================================ ZONE 1: Rice Paddy Village
def z01():
    a = new(1, "Egg", WHITE)
    a.paint(layers(band(0.40, 0.56, COBALT, wave=1.2, freq=6), band(0.18, 0.24, COBALT2), band(0.74, 0.79, COBALT2)))
    b = new(1, "BigEgg", WHITE)
    b.paint(layers(band(0.10, 0.15, COBALT2), band(0.68, 0.72, COBALT)))
    curls(b, 4, 0.42, 4.5, COBALT)
    cap(b, 0.75, COBALT, thick=1.0, knob=COBALT2, knob_r=1.4)
    ring_layer(b, 0.735, 0.765, GOLD, d1=1.6)
    c = new(1, "GiantEgg", WATER)
    c.paint(layers(stripes([WATER, WATER2], 0.04, 0.0, 0.3), band(0.66, 1.0, SKY)))
    for t0, t1, d, col in [(0.30, 0.37, 3.0, GREEN2), (0.37, 0.44, 2.2, GREEN), (0.44, 0.51, 1.5, GREEN3), (0.51, 0.58, 0.9, GREEN), (0.58, 0.64, 0.5, GREEN2)]:
        terrace(c, t0, t1, d, col, top=WATER)
    top = c.h
    c.fill(lambda x, y, z: top - 3 <= y <= top + 4 and math.hypot(x, z) <= (top + 4 - y) * 1.55,
           ((-12, 12), (top - 3, top + 4), (-12, 12)), lambda x, y, z: STRAW if int(y) % 2 else STRAW2)
    c.fill(lambda x, y, z: top - 3 <= y <= top - 2 and math.hypot(x, z) <= 9.5, ((-10, 10), (top - 3, top - 2), (-10, 10)), RED)
    sp = c.surf(0, 0.79, 0)
    c.carve(lambda x, y, z, ang, t: (x - sp[0]) ** 2 + (y - sp[1]) ** 2 + (z - sp[2]) ** 2 <= 9.5, SUNG, depth=2)
    return [a, b, c]


# ================================================================ ZONE 2: Bamboo Grove
def z02():
    seg = lambda node_every: stripes([GREEN, GREEN3], node_every, 0.0, 1.0)
    nodes = lambda e, n: [ring_layer(e, (k + 1) / (n + 1) - 0.012, (k + 1) / (n + 1) + 0.012, GREEN2, d1=0.9) for k in range(n)]
    a = new(2, "Egg", GREEN)
    a.paint(stripes([GREEN, GREEN3], 0.25))
    nodes(a, 3)
    b = new(2, "BigEgg", GREEN)
    b.paint(stripes([GREEN, GREEN3], 0.2))
    nodes(b, 4)
    for k, (ang, t) in enumerate(((35, 0.6), (165, 0.45), (285, 0.66))):
        base = b.surf(ang, t, 0.3)
        n = b.normal(ang, t)
        for j, s in enumerate((-0.5, 0.5)):
            leaf(b, base, add(n, (s, 0.7, 0)), 7, 3.4, GREEN2 if j else GREEN3, thick=2.0)
    c = new(2, "GiantEgg", GREEN)
    c.paint(layers(stripes([GREEN, GREEN3], 0.16), band(0.30, 0.42, BLACK)))
    nodes(c, 5)
    ring_layer(c, 0.29, 0.43, BLACK, d1=1.2)
    for k, (dx, dz, h) in enumerate(((0.5, 1.0, 13), (-3.0, -1.0, 9), (3.0, -1.5, 7))):
        base = (dx, c.h - 4, dz)
        topp = (dx * 1.6, c.h + h, dz * 1.4)
        bamboo_stalk(c, base, topp, 1.6, GREEN, GREEN2, every=3.0)
        for j, (lx, lz) in enumerate(((1, 0.2), (-1, 0.3))):
            leaf(c, add(topp, (0, -1.5 * j, 0)), (lx, 0.2 - 0.3 * j, lz), 6.5, 2.8, GREEN3 if j % 2 else GREEN2, thick=1.8)
    c.crack(10, 0.55, 22, JADEG, seed=3, branches=2)
    c.crack(200, 0.62, 18, JADEG, seed=8, branches=1)
    return [a, b, c]


# ================================================================ ZONE 3: Tea Terraces
def z03():
    a = new(3, "Egg", CELADON)
    a.paint(crackle(JADE2, cell=3.0, width=0.16))
    b = new(3, "BigEgg", CELADON)
    b.paint(layers(crackle(JADE2, cell=3.5, width=0.13), band(0.12, 0.17, JADE2), band(0.78, 0.82, JADE2)))
    # teapot spout (front-right) and handle (back), lid knob
    s0 = b.surf(70, 0.42, -1)
    b.chain([s0, add(s0, (4, 3, -0.5)), add(s0, (6.5, 6.5, -1))], [1.6, 1.2, 0.8], CELADON2)
    h0, h1 = b.surf(250, 0.66, -0.5), b.surf(250, 0.3, -0.5)
    b.chain([h0, add(h0, (-4.5, -1, 0)), add(h1, (-4.5, 1, 0)), h1], [0.9, 0.9, 0.9, 0.9], CELADON2)
    cap(b, 0.8, JADE2, thick=1.0, knob=JADE, knob_r=1.3)
    c = new(3, "GiantEgg", CELADON)
    c.paint(layers(crackle(JADE2, cell=4.0, width=0.11), band(0.0, 0.12, TEA)))
    # tea leaves round the base
    for k in range(10):
        ang = k * 36
        base = c.surf(ang, 0.1, 0.4)
        leaf(c, base, add(c.normal(ang, 0.1), (0, 0.9, 0)), 5, 2.2, TEA if k % 2 else GREEN2)
    # steam-swirl ridges
    curls(c, 3, 0.45, 5.0, WHITE, offset=60)
    # tiered tea-house roof cap
    roof(c, c.h - 6, 8.5, 3, RED2, edge=GOLD, tip_col=GOLD)
    c.box((0, c.h - 1, 0), (4.5, 1.5, 4.5), RED)
    roof(c, c.h + 0.5, 6, 2.5, RED2, edge=GOLD, tip_col=GOLD)
    c.sphere((0, c.h + 4.5, 0), 1.3, GOLD)
    windows(c, (0, 90, 180, 270), 0.62, 2.6, 3.2, LANTG)
    return [a, b, c]


# ================================================================ ZONE 4: Great Wall
def z04():
    a = new(4, "Egg", GREY)
    a.paint(bricks(GREY, MORTAR, row=2, length=4, jitter=(GREY2, 0.3)))
    b = new(4, "BigEgg", GREY)
    b.paint(bricks(GREY, MORTAR, row=2, length=5, jitter=(GREY2, 0.3)))
    terrace(b, 0.70, 0.76, 1.0, GREY3)
    battlements(b, 0.76, 8, GREY3, h=3, w=1.4, out=0.4)
    c = new(4, "GiantEgg", GREY)
    c.paint(layers(bricks(GREY, MORTAR, row=2, length=5, jitter=(GREY2, 0.35)), band(0.42, 0.5, RED)))
    ring_layer(c, 0.41, 0.51, RED, d1=1.2)
    studs(c, 0.46, 10, GOLD, r=0.8, out=1.0)
    terrace(c, 0.72, 0.78, 1.5, GREY3)
    battlements(c, 0.78, 10, GREY3, h=3.5, w=1.5, out=0.8)
    c.fill(lambda x, y, z: c.h * 0.78 <= y <= c.h + 2 and math.hypot(x, z) <= 4.5, ((-5, 5), (c.h * 0.78, c.h + 2), (-5, 5)), GREY2)
    roof(c, c.h + 2, 5.5, 3, RED, edge=RED2, tip_col=GOLD)
    c.capsule((0, c.h + 4, 0), (0, c.h + 12, 0), 0.5, 0.5, BROWN)
    c.box((2.6, c.h + 10.5, 0), (2.2, 1.4, 0.5), RED)
    moss(c, 0.84, MOSS, MOSS2, drip=0.2, seed=5)
    windows(c, (0, 72, 144, 216, 288), 0.6, 1.0, 3.6, TORCHG)
    return [a, b, c]


# ================================================================ ZONE 5: Jade River
def z05():
    a = new(5, "Egg", JADE)
    a.paint(mottle([JADE2, JADE3], cell=2, chance=0.35, seed=3))
    b = new(5, "BigEgg", JADE)
    b.paint(mottle([JADE2, JADE3], cell=2, chance=0.3, seed=5))
    fc = b.surf(0, 0.48, 1.2)
    torus(b, fc, 3.6, 1.2, JADE3, axis="z")
    ring_layer(b, 0.08, 0.13, GOLD, d1=1.2)
    c = new(5, "GiantEgg", JADE)
    c.paint(mottle([JADE2, JADE3], cell=2, chance=0.3, seed=7))
    for k in range(4):
        t0 = 0.2 + k * 0.14
        pts = [c.surf(a_, t0 + 0.03 * math.sin(math.radians(a_ * 6)), 0) for a_ in range(0, 361, 6)]
        relief(c, pts, 0.7, WATER if k % 2 else WATER2, d1=1.2)
    # koi-fin crest and a pearl on top
    for j, s in enumerate((-1, 0, 1)):
        leaf(c, (s * 1.5, c.h - 2, 1.0 + 0.5 * abs(s)), (s * 0.7, 1, 0.5), 10 - 2.5 * abs(s), 4.5, ORANGE if j != 1 else WHITE, thick=1.8)
    c.sphere((0, c.h + 2.0, -2.0), 2.8, PEARL)
    c.crack(0, 0.5, 26, AQUAG, seed=11, branches=3)
    return [a, b, c]


# ================================================================ ZONE 6: Lantern Night Market
def z06():
    a = new(6, "Egg", RED)
    a.paint(layers(band(0.0, 0.12, GOLD), band(0.86, 1.0, GOLD)))
    b = new(6, "BigEgg", RED)
    b.paint(layers(band(0.0, 0.1, GOLD), band(0.88, 1.0, GOLD)))
    ribs(b, 8, GOLD2, width=0.6, t0=0.1, t1=0.88)
    cap(b, 0.88, GOLD, thick=1.0)
    t0 = b.surf(30, 0.42, 1.0)
    b.chain([t0, add(t0, (0.5, -2.5, -0.5))], [0.5, 0.5], GOLD)
    b.capsule(add(t0, (0.5, -2.5, -0.5)), add(t0, (0.5, -5.5, -0.5)), 0.7, 1.2, RED2)
    c = new(6, "GiantEgg", RED)
    c.paint(layers(band(0.0, 0.08, GOLD), band(0.9, 1.0, GOLD)))
    ribs(c, 10, GOLD2, width=0.6, t0=0.08, t1=0.9)
    # warm light glowing between the ribs (windows in each panel)
    windows(c, [18 + k * 36 for k in range(10)], 0.5, 1.8, 9.0, LANTG, depth=2)
    # gold dragon-coil band spiralling round the egg
    pts = [c.surf(a_, 0.3 + 0.35 * a_ / 720.0, 0) for a_ in range(0, 721, 5)]
    relief(c, pts, 0.9, GOLD, d1=1.6)
    cap(c, 0.9, GOLD, thick=1.2, knob=GOLD2, knob_r=1.4)
    for ang in (60, 180, 300):
        tp = c.surf(ang, 0.33, 1.0)
        c.capsule(tp, add(tp, (0, -3, 0)), 0.5, 0.5, GOLD)
        c.capsule(add(tp, (0, -3, 0)), add(tp, (0, -6, 0)), 0.7, 1.3, RED2)
    # small glowing paper-lantern string round it
    for k in range(9):
        p = c.surf(k * 40, 0.7 - 0.04 * (k % 2), 1.6)
        c.sphere(p, 1.0, LANTG, glow=True)
    pts = [c.surf(a_, 0.73, 1.0) for a_ in range(0, 361, 6)]
    relief(c, pts, 0.3, RED2, d1=1.2)
    return [a, b, c]


# ================================================================ ZONE 7: Terracotta Tomb
def z07():
    a = new(7, "Egg", CLAY)
    a.paint(mottle([CLAY2, CLAY3], cell=2, chance=0.28, seed=4))
    chips(a, 0.06, CLAY2, seed=3)
    b = new(7, "BigEgg", CLAY)
    b.paint(mottle([CLAY2], cell=2, chance=0.15, seed=6))
    b.shell_offset(lambda x, y, z, ang, t: 0.2 <= t <= 0.75 and scales(1, 2, row=3, length=4)(x, y, z, ang, t) == 1, 0, 1, CLAY3)
    c = new(7, "GiantEgg", CLAY)
    c.paint(mottle([CLAY2], cell=2, chance=0.15, seed=8))
    c.shell_offset(lambda x, y, z, ang, t: 0.18 <= t <= 0.72 and scales(1, 2, row=3, length=4)(x, y, z, ang, t) == 1, 0, 1.2, CLAY3)
    studs(c, 0.2, 12, BRONZE, r=0.8, out=1.2)
    studs(c, 0.72, 10, BRONZE, r=0.8, out=1.2)
    cap(c, 0.8, CLAY2, thick=1.2)
    c.sphere((1.5, c.h + 2.5, 0.5), 2.2, CLAY2)                       # topknot
    torus(c, (1.5, c.h + 1.2, 0.5), 2.0, 0.6, RED)                     # ribbon
    c.crack(0, 0.45, 26, EMBERG, seed=21, branches=3)
    c.crack(180, 0.55, 18, EMBERG, seed=22, branches=1)
    return [a, b, c]


# ================================================================ ZONE 8: Forbidden City
def z08():
    a = new(8, "Egg", YELLOW)
    a.paint(band(0.42, 0.56, RED))
    b = new(8, "BigEgg", YELLOW)
    b.paint(scales(YELLOW, GOLD2, row=3, length=4))
    for a_ in (0, 90, 180, 270):
        pts = [b.surf(a_, t, 0) for t in [0.15 + 0.01 * i for i in range(80)]]
        relief(b, pts, 0.7, GOLD, d1=1.3)
    c = new(8, "GiantEgg", YELLOW)
    c.paint(layers(scales(YELLOW, GOLD2, row=3, length=4, t0=0.55), band(0.12, 0.5, RED)))
    ribs(c, 8, RED2, width=0.9, t0=0.12, t1=0.5, d1=1.3)            # red pillars band
    for k in range(4):                                              # gold door studs on the front
        for j in range(3):
            c.sphere(c.surf(-6 + 4 * k, 0.2 + 0.1 * j, 0.6), 0.6, GOLD)
    roof(c, c.h - 7, 9, 3, YELLOW, edge=GOLD2, tip_col=GOLD)
    c.box((0, c.h - 2, 0), (5, 2, 5), RED)
    roof(c, c.h, 7, 3, YELLOW, edge=GOLD2, tip_col=GOLD)
    for sx in (-1, 1):                                                     # dragon finials on the ridge
        c.chain([(sx * 3, c.h + 3.5, 0), (sx * 4.5, c.h + 6, 0), (sx * 3.5, c.h + 7, 0)], [0.9, 0.8, 0.5], GOLD)
    c.capsule((-3, c.h + 3.5, 0), (3, c.h + 3.5, 0), 0.8, 0.8, GOLD)
    windows(c, (0, 90, 180, 270), 0.6, 2.4, 2.4, WINDG)
    return [a, b, c]


# ================================================================ ZONE 9: Kunlun Immortal Peaks
def z09():
    a = new(9, "Egg", SNOW)
    a.paint(mottle([ROCK, ROCK2], cell=2, chance=0.22, seed=9, t1=0.7))
    b = new(9, "BigEgg", ROCK)
    b.paint(layers(mottle([ROCK2], cell=2, chance=0.3, seed=10), band(0.62, 1.0, SNOW)))
    b.shell_offset(lambda x, y, z, ang, t: t >= 0.6 + 0.08 * hsh(int(ang // 20), 3), 0, 1.0, SNOW)
    sp = b.surf(320, 0.7, 0.5)
    b.capsule(sp, add(sp, (-2, 5, -1)), 0.5, 0.4, BROWN)
    for j in range(3):
        leaf(b, add(sp, (-0.7 * j, 1.5 * j + 1, -0.3 * j)), (-1, 0.2, -0.6 + 0.5 * j), 3.5, 1.6, PINE if j % 2 else PINE2)
    c = new(9, "GiantEgg", ROCK)
    c.paint(layers(mottle([ROCK2], cell=2, chance=0.3, seed=11), band(0.7, 1.0, SNOW)))
    for k, (dx, dz, h, r) in enumerate(((0, 0.5, 13, 3.6), (-4.5, 1.5, 9, 2.8), (4.5, 1.0, 10, 2.9), (1.0, -4.5, 7, 2.5))):
        y0 = c.h - 6
        c.fill(lambda x, y, z, dx=dx, dz=dz, h=h, r=r, y0=y0: y0 <= y <= y0 + h and math.hypot(x - dx, z - dz) <= r * (1 - (y - y0) / h) + 0.6,
               ((dx - r - 1, dx + r + 1), (y0, y0 + h), (dz - r - 1, dz + r + 1)),
               lambda x, y, z, y0=y0, h=h: SNOW if y > y0 + h * 0.6 else (ROCK2 if hsh(int(x), int(y), int(z)) < 0.45 else ROCK))
    curls(c, 4, 0.4, 5.0, SNOW, d1=1.2, offset=20)
    for j, s in enumerate((-1.2, -0.4, 0.4, 1.2)):                 # crane feather crest
        leaf(c, (s, c.h + 3, 1.5), (s * 0.5, 1, 0.9), 7, 2.0, BLACK if j in (0, 3) else WHITE, thick=1.0)
    c.crack(0, 0.35, 24, SPIRITG, seed=31, branches=3)
    c.crack(150, 0.5, 18, SPIRITG, seed=32, branches=2)
    return [a, b, c]


# ================================================================ ZONE 10: Dragon King's Palace
def z10():
    a = new(10, "Egg", PEARL)
    a.paint(layers(band(0.38, 0.54, SEA, wave=1.0, freq=5), band(0.3, 0.33, SEA2)))
    b = new(10, "BigEgg", PEARL)
    b.paint(layers(band(0.0, 0.18, SEA, wave=1.0, freq=6), mottle([PEARL2], cell=2, chance=0.2, seed=12, t0=0.18)))
    for k, ang in enumerate((40, 160, 280)):
        base = b.surf(ang, 0.32, -0.5)
        n = b.normal(ang, 0.32)
        t1 = add(base, add(n, (0, 1.4, 0)), 3.5)
        b.capsule(base, t1, 0.9, 0.7, CORAL)
        b.capsule(t1, add(t1, (1.5, 2.5, 0)), 0.7, 0.5, CORAL)
        b.capsule(t1, add(t1, (-1.5, 2.0, 0.5)), 0.6, 0.4, CORAL2)
    for ang in (100, 220, 340):
        b.sphere(b.surf(ang, 0.6, 0.6), 1.3, CORAL2, scale=(1, 0.7, 1))
    c = new(10, "GiantEgg", PEARL)
    c.paint(layers(scales(SEA, SEA2, row=3, length=4, t1=0.45), mottle([PEARL2], cell=2, chance=0.2, seed=13, t0=0.45)))
    for k, ang in enumerate((20, 90, 160, 230, 300)):
        base = c.surf(ang, 0.4, -0.5)
        n = c.normal(ang, 0.4)
        t1 = add(base, add(n, (0, 1.8, 0)), 5)
        c.capsule(base, t1, 1.1, 0.8, CORAL if k % 2 else CORAL2)
        c.capsule(t1, add(t1, (1.6, 3.5, 0)), 0.8, 0.5, CORAL)
        c.capsule(t1, add(t1, (-1.2, 3.0, 0.8)), 0.7, 0.4, CORAL2)
    torus(c, (0, c.h - 1, 0), 3.6, 0.9, GOLD)
    for k in range(6):
        a_ = math.radians(k * 60)
        c.capsule((3.6 * math.sin(a_), c.h - 1, 3.6 * math.cos(a_)), (4.2 * math.sin(a_), c.h + 3, 4.2 * math.cos(a_)), 0.7, 0.35, GOLD)
    c.sphere((0, c.h + 1.5, 0), 2.0, AQUAG, glow=True)
    glow_dots(c, 14, BIOG, seed=4, r=0.6, t0=0.15, t1=0.75)
    return [a, b, c]


# ================================================================ ZONE 11: Heavenly Court
def z11():
    a = new(11, "Egg", WHITE)
    a.paint(layers(band(0.0, 0.18, GOLD), band(0.82, 1.0, GOLD), band(0.42, 0.56, SKY, wave=1.4, freq=5)))
    b = new(11, "BigEgg", WHITE)
    b.paint(layers(band(0.0, 0.12, GOLD), band(0.85, 1.0, GOLD)))
    curls(b, 4, 0.45, 4.5, CREAM, d1=1.2)
    torus(b, (0, b.h * 0.6, 0), b.R(b.h * 0.6) + 3.5, 0.8, GOLD)
    c = new(11, "GiantEgg", WHITE)
    c.paint(layers(band(0.0, 0.1, GOLD), band(0.88, 1.0, GOLD)))
    curls(c, 5, 0.45, 5.5, GOLD, d1=1.3)
    # sun disc halo behind (glowing ring + gold disc rim)
    torus(c, (0, c.h * 0.62, 9.0), 11.0, 0.9, HALOG, axis="z", glow=True)
    torus(c, (0, c.h * 0.62, 9.5), 12.2, 0.6, GOLD, axis="z")
    # phoenix-feather crest
    for j, s in enumerate((-1.5, -0.75, 0, 0.75, 1.5)):
        leaf(c, (s * 0.8, c.h - 1, 0.5), (s * 0.45, 1, 0.6), 9 - 1.5 * abs(s), 2.4, [RED, ORANGE, GOLD, ORANGE, RED][j], thick=1.0)
    for ang in (0, 120, 240):
        c.sphere(c.surf(ang, 0.3, 0.6), 1.2, GEMG, glow=True)
    return [a, b, c]


ZONES = {1: z01, 2: z02, 3: z03, 4: z04, 5: z05, 6: z06, 7: z07, 8: z08, 9: z09, 10: z10, 11: z11}
