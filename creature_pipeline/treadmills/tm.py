"""Shared building blocks for the China treadmills (game space via detail.V: x right, y up, front/console = -z).

Hard rules from the brief (make_tm.py checks them):
- origin = centre of the belt on the ground, units = studs
- belt deck: flat walkable top 20 long x 5.4 wide, top at y = 1.2
- air above the deck (|x| < 2.7, -6 < z < 10) stays clear above y = 3
- footprint <= 10 wide x 25 long x 17 tall, console at about z = -9 with a slanted screen facing +z at about y = 7
Every shape is bound to the single Root bone; the treadmill never animates.
"""
import math
import bmesh
from mathutils import Matrix
from cn import *
from detail import V, B, E, T, S, BOX, SHEET, filigree, cracks, crown, swept_horn, eyes_pair, fur_line, maw, grot, claws3, fur, shard

R = "Root"
DECK_TOP, DECK_HW, DECK_HL = 1.2, 2.7, 10.0


def tread(name, stud=0.9):
    """a Creature set up as a static treadmill: one Root bone, 1024 px texture, studs about half a stud wide"""
    c = Creature(name, height=12, stud=stud)
    c.tex_size = 1024
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    return c


def rbox(c, ctr, half, col, bevel=0.2, seg=2, rot=None, **kw):
    """rounded (bevelled) box in game space: chunky sculpted look instead of a sharp part"""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal((half[0], half[2], half[1], 1.0)), verts=bm.verts)
    b = min(bevel, min(half) * 0.95)
    if b > 0.01:
        bmesh.ops.bevel(bm, geom=list(bm.edges) + list(bm.verts), offset=b, offset_type="OFFSET", segments=seg,
                        profile=0.5, affect="EDGES")
    m = Matrix.Identity(4)
    if rot is not None:
        m = euler(*rot).to_4x4()
    bmesh.ops.transform(bm, matrix=Matrix.Translation(B(ctr)) @ m, verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return c._add(bm, col, [R], **kw)


def cyl(c, a, b, r, col, seg=12, **kw):
    """straight capped cylinder between two game points"""
    return T(c, [a, b], [r, r], col, R, seg=seg, sub=1, **kw)


def deck(c, belt, rim, belt_paint=None, rim_paint=None, roller=None, rim_w=0.38, rims=True):
    """the walkable belt (exact size, flat top at y = 1.2), end rollers and the two side rims"""
    rbox(c, V(0, DECK_TOP - 0.3, 0), (DECK_HW, 0.3, DECK_HL), belt, bevel=0.06, seg=1, paint=belt_paint)
    for z in (-DECK_HL, DECK_HL):
        cyl(c, V(-DECK_HW - 0.05, DECK_TOP - 0.42, z), V(DECK_HW + 0.05, DECK_TOP - 0.42, z), 0.4, roller or rim, seg=12)
    if rims:
        for s in (-1, 1):
            rbox(c, V(s * (DECK_HW + rim_w), DECK_TOP - 0.45, 0), (rim_w, 0.6, DECK_HL + 0.6), rim, bevel=0.18, paint=rim_paint)


def skirt(c, col, paint=None, h=0.55, out=0.0):
    """low base under the deck (fills the gap to the ground)"""
    rbox(c, V(0, h * 0.5, 0), (DECK_HW + 0.65 + out, h * 0.5, DECK_HL + 0.8), col, bevel=0.2, paint=paint)


def console(c, body, screen, glow=None, post=None, post_r=0.38, head_half=(3.0, 0.85, 0.75), tilt=-28, y=6.6, z=-9.3,
            screen_half=(2.1, 0.62), post_paint=None, body_paint=None, posts=True):
    """console end: two uprights + a slanted head with the screen facing +z (towards the runner) at about y = 7.
    Returns the screen centre and the head centre."""
    if posts:
        for s in (-1, 1):
            cyl(c, V(s * 2.45, DECK_TOP - 0.1, z - 0.3), V(s * 2.45, y - 0.3, z + 0.05), post_r, post or body, seg=12, paint=post_paint)
    hc = V(0, y, z)
    rbox(c, hc, head_half, body, bevel=0.3, rot=(tilt, 0, 0), paint=body_paint)
    # screen: thin panel on the +z face of the head, tilted the same way
    M = grot(tilt, 0, 0)
    n = M @ V(0, 0, 1)
    sc = hc + n * (head_half[2] + 0.02)
    rbox(c, sc, (screen_half[0], screen_half[1], 0.06), glow or screen, bevel=0.05, seg=1, rot=(tilt, 0, 0), glow=bool(glow), stud=False)
    return sc, hc, n


def rails(c, col, r=0.24, y=4.6, x=3.05, z_end=-1.5, paint=None, seg=10):
    """hand rails: from the console uprights forward along each side, then down into the frame (outside the deck)"""
    for s in (-1, 1):
        pts = [V(s * 2.45, 6.0, -9.2), V(s * x, 5.0, -8.0), V(s * x, y, -6.0), V(s * x, y, z_end), V(s * x, 2.6, z_end + 1.2), V(s * x, 1.3, z_end + 1.6)]
        T(c, pts, [r] * len(pts), col, R, seg=seg, sub=3, paint=paint)
    return [V(s * x, y, z_end) for s in (-1, 1)]


def feet(c, col, zs=(-9.5, -3.2, 3.2, 9.5), x=3.2, r=0.55, h=0.32):
    for z in zs:
        for s in (-1, 1):
            E(c, V(s * x, h * 0.5, z), (r, h, r * 1.1), col, R, seg=(12, 6))


def tassel(c, top, col, cap=None, size=0.35):
    """small hanging tassel: gold bead + cord + flared skirt"""
    E(c, top + V(0, -size * 0.3, 0), (size * 0.38,) * 3, cap or C(255, 200, 60), R, seg=(8, 6), stud=False)
    T(c, [top + V(0, -size * 0.6, 0), top + V(0, -size * 2.2, 0)], [size * 0.18, size * 0.45], col, R, seg=8, sub=1)


def red_lantern(c, ctr, r, glow_col, body=C(214, 32, 40), cap=C(255, 200, 60), ribs=6, tassel_col=None, seg=(16, 10)):
    """round paper lantern; the inside is a separate Glow mesh peeking through the open bottom and the gaps"""
    E(c, ctr, (r, r * 0.86, r), body, R, seg=seg)
    for k in range(ribs):
        a = k / ribs * math.tau
        pts = [ctr + V(math.sin(a) * r * 1.01 * math.cos(math.radians(e)), r * 0.86 * math.sin(math.radians(e)), math.cos(a) * r * 1.01 * math.cos(math.radians(e))) for e in (-70, -35, 0, 35, 70)]
        T(c, pts, [r * 0.06] * 5, cap, R, seg=5, sub=1, stud=False)
    for sg in (-1, 1):
        cyl(c, ctr + V(0, sg * r * 0.72, 0), ctr + V(0, sg * r * 0.98, 0), r * 0.42, cap, seg=seg[0] - 4, stud=False)
    E(c, ctr, (r * 1.03, r * 0.32, r * 1.03), glow_col, R, seg=(seg[0] - 2, 4), glow=True)   # glowing band through the middle
    tassel(c, ctr + V(0, -r * 0.98, 0), tassel_col or body, cap=cap, size=r * 0.5)


def cloud_scroll(c, ctr, size, col, facing=1, **kw):
    """carved cloud scroll relief: three round curls in a row with a tail, lying on a side face (facing = +1/-1 along x)"""
    for j, (dz, dy, s) in enumerate(((0.0, 0.0, 1.0), (size * 1.1, size * 0.25, 0.8), (size * 2.0, -0.05, 0.65))):
        p = ctr + V(0, dy, dz)
        c.torus(B(p), size * 0.5 * s, size * 0.16 * s, col, R, rot=euler(0, 0, 90), seg=(10, 4), **kw)
        E(c, p, (size * 0.12, size * 0.32 * s, size * 0.32 * s), col, R, seg=(6, 4), **kw)


def crosshatch(col, period=0.6, width=0.18):
    """woven mat: two sets of diagonal stripes on the deck (top view)"""
    def mask(X, Y, Z):
        a = np.mod(X + Z, period) < width
        b = np.mod(X - Z, period) < width
        weave = np.mod(np.floor((X + Z) / period) + np.floor((X - Z) / period), 2) < 1
        return (a & weave) | (b & ~weave)
    return (col, mask)


def bands(col, axis="z", period=1.0, width=0.2, only=None):
    def mask(X, Y, Z):
        U = {"x": X, "y": Y, "z": Z}[axis]
        m = np.mod(U, period) < width
        if only is not None:
            m &= only(X, Y, Z)
        return m
    return (col, mask)


def ring(c, ctr, d, R_, r, col, seg=(16, 5), **kw):
    """torus around the direction d (game Vector) at ctr"""
    from mathutils import Vector
    M = Vector((0, 1, 0)).rotation_difference(d.normalized()).to_matrix()
    c.torus(B(ctr), R_, r, col, R, rot=G @ M @ G, seg=seg, **kw)


def bamboo(c, a, b, r, col, node, every=1.8, seg=8, **kw):
    """bamboo pole with raised node rings"""
    cyl(c, a, b, r, col, seg=seg, **kw)
    d = b - a
    n = max(1, int(d.length / every))
    for i in range(1, n + 1):
        p = a.lerp(b, i / (n + 1))
        ring(c, p, d, r * 1.02, r * 0.16, node, seg=(seg, 3))
    for p in (a, b):
        E(c, p, (r * 1.02, r * 1.02, r * 1.02), node, R, seg=(seg, 4))


def lash(c, p, d, r, col):
    """rope lashing: three wraps around a joint"""
    for k in (-0.5, 0.5):
        ring(c, p + d.normalized() * k * r * 0.4, d, r * 1.12, r * 0.15, col, seg=(8, 3))


def turn_around(c, first, pivot):
    """rotate every shape added since index `first` by 180 degrees around the vertical axis through pivot (game Vector)"""
    M = Matrix.Translation(B(pivot)) @ Matrix.Rotation(math.pi, 4, "Z") @ Matrix.Translation(-B(pivot))
    for sh in c.shapes[first:]:
        bmesh.ops.transform(sh["bm"], matrix=M, verts=sh["bm"].verts)


def roof(c, ctr, hw, hd, h, tiles, trim, tip_col, bell_y=0.7, tile2=C(35, 110, 65)):
    """one pagoda roof tier: a sloped tiled hip roof, a gold ridge trim and 4 upturned gold eave tips with bells"""
    E(c, ctr, (hw, h, hd), tiles, R, seg=(16, 6), paint=bands(tile2, "x", period=0.55, width=0.14))
    rbox(c, ctr + V(0, -h * 0.15, 0), (hw * 1.02, 0.12, hd * 1.02), trim, bevel=0.08, seg=1, stud=False)
    for sx in (-1, 1):
        for sz in (-1, 1):
            base = ctr + V(sx * hw * 0.82, -h * 0.1, sz * hd * 0.82)
            tip = base + V(sx * 0.65, 0.75, sz * 0.4)
            S(c, base, tip, 0.22, tip_col, R, bend=V(0, -0.2, 0), seg=5, n=4, stud=False)
            T(c, [tip + V(0, -0.1, 0), tip + V(0, -bell_y, 0)], [0.03, 0.03], C(90, 60, 40), R, seg=4, sub=1, stud=False)
            bell(c, B(tip + V(0, -bell_y - 0.18, 0)), 0.17, R)
