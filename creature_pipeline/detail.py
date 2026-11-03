"""Detail toolkit for the fierce armoured / royal / elemental creatures (batch 10+).

Everything here is written in GAME space: V(x, y, z) with y up, z back, front = -z. B() converts to
blender. The look is faceted (low segment counts, flat shading) like the owner's reference models:
shard fur clumps, crisp armour plates with trims, glowing angry eyes, open jaws with sharp teeth.
"""
import math, random
from kit import *
import bmesh
import numpy as np
from mathutils import Vector, Matrix, Euler
from mathutils.bvhtree import BVHTree

R = math.radians
GM = G.to_4x4()
TOOTH = C(250, 248, 236)
MOUTH = C(85, 12, 22)
TONGUE = C(215, 70, 95)


def V(x, y=None, z=None):
    if y is None:
        return Vector(x)
    return Vector((x, y, z))


def B(v):
    return P(v[0], v[1], v[2])


def grot(rx=0, ry=0, rz=0):
    return Euler((R(rx), R(ry), R(rz)), "XYZ").to_matrix()


def mirror(v):
    return V(-v.x, v.y, v.z)


def _finish(c, bm, color, bones, **kw):
    bmesh.ops.transform(bm, matrix=GM, verts=bm.verts)     # game -> blender
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return c._add(bm, color, bones, **kw)


# ------------------------------------------------------------------ basic wrappers (game space)
def E(c, ctr, rad, col, bones, rot=None, seg=(10, 7), **kw):
    return c.ellipsoid(B(ctr), rad, col, bones, rot=euler(*rot) if rot else None, seg=seg, **kw)


def T(c, pts, radii, col, bones, seg=8, sub=2, **kw):
    return c.tube([B(p) for p in pts], radii, col, bones, seg=seg, sub=sub, **kw)


def S(c, base, tip, r, col, bones, bend=None, seg=4, n=3, **kw):
    """faceted spike (pyramid by default)"""
    return c.spike(B(base), B(tip), r, col, bones, bend=B(bend) if bend is not None else None, seg=seg, n=n, **kw)


def BOX(c, ctr, half, col, bones, rot=None, **kw):
    return c.box(B(ctr), half, col, bones, rot=euler(*rot) if rot else None, **kw)


def SHEET(c, pts, col, bones, thick=0.15, **kw):
    return c.sheet([B(p) for p in pts], col, bones, thick=thick, **kw)


def crystal(c, base, tip, r, col, bones, **kw):
    d = tip - base
    return T(c, [base - d * 0.08, base + d * 0.7, tip], [r, r, 0.02], col, bones, seg=6, sub=1, **kw)


# ------------------------------------------------------------------ shard fur
def shard(c, base, tip, width, col, bones, n=None, thick=0.38, mid=0.42, bulge=1.12, lift=0.1, **kw):
    """one faceted fur clump / scale / feather: flat diamond blade lying on the surface (normal n)"""
    d = tip - base
    L = d.length
    dn = d / L
    n = V(0, 1, 0) if n is None else n.copy()
    n = n - dn * n.dot(dn)
    if n.length < 1e-4:
        n = dn.orthogonal()
    n.normalize()
    w = dn.cross(n).normalized()
    bm = bmesh.new()

    def ring(p, s):
        hw, ht = width * 0.5 * s, width * thick * 0.5 * s
        return [bm.verts.new(p + w * hw), bm.verts.new(p + n * ht), bm.verts.new(p - w * hw), bm.verts.new(p - n * ht)]
    r0 = ring(base, 0.8)
    r1 = ring(base + d * mid + n * L * lift * 0.5, bulge)
    tp = bm.verts.new(tip + n * L * lift)
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((r0[i], r0[j], r1[j], r1[i]))
        bm.faces.new((r1[i], r1[j], tp))
    bm.faces.new(list(reversed(r0)))
    return _finish(c, bm, col, bones, **kw)


def fibo(n):
    ga = math.pi * (3 - math.sqrt(5))
    out = []
    for i in range(n):
        y = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(max(0, 1 - y * y))
        out.append(V(math.cos(ga * i) * r, y, math.sin(ga * i) * r))
    return out


def fur(c, ctr, rad, col, bones, n=80, length=0.9, width=0.55, flow=V(0, -1, 0.3), where=None, col2=None, mix=0.35,
        seed=1, rot=None, lift=0.45, jitter=0.3, thick=0.38, sink=0.3, glow2=False, wjit=0.2):
    """cover part of an ellipsoid in shard clumps. where(u, p) filters by unit-sphere dir u / point p.
    flow = Vector or fn(p, normal) -> Vector (direction the fur lies)."""
    rng = random.Random(seed)
    M = grot(*rot) if rot else Matrix.Identity(3)
    count = 0
    for u in fibo(n):
        p = ctr + M @ V(u.x * rad[0], u.y * rad[1], u.z * rad[2])
        if where and not where(u, p):
            continue
        nrm = (M @ V(u.x / rad[0], u.y / rad[1], u.z / rad[2])).normalized()
        f = flow(p, nrm) if callable(flow) else flow.copy()
        f = f - nrm * f.dot(nrm)
        if f.length < 1e-3:
            f = nrm.orthogonal()
        f.normalize()
        dirv = (f + nrm * lift).normalized()
        ln = length * (1 + rng.uniform(-jitter, jitter))
        wd = width * (1 + rng.uniform(-wjit, wjit))
        base = p - dirv * ln * 0.18 - nrm * wd * thick * sink
        cc = col2 if (col2 is not None and rng.random() < mix) else col
        shard(c, base, base + dirv * ln, wd, cc, bones, n=nrm, thick=thick, glow=bool(glow2 and cc == col2))
        count += 1
    return count


def fur_line(c, pts, col, bones, length=0.9, width=0.5, out=None, n_per=3, col2=None, seed=2, lift=0.6, thick=0.4, jitter=0.25):
    """row of shards along a polyline (manes, ridges, cheek tufts). out = fn(p) -> direction"""
    rng = random.Random(seed)
    for i in range(len(pts) - 1):
        for k in range(n_per):
            t = (k + rng.uniform(0.1, 0.9)) / n_per
            p = pts[i].lerp(pts[i + 1], t)
            d = out(p) if callable(out) else out
            d = d.normalized()
            ln = length * (1 + rng.uniform(-jitter, jitter))
            seg_dir = (pts[i + 1] - pts[i]).normalized()
            nrm = d.cross(seg_dir).cross(d) if abs(d.dot(seg_dir)) < 0.99 else d.orthogonal()
            cc = col2 if (col2 is not None and rng.random() < 0.4) else col
            shard(c, p - d * ln * 0.15, p + d * ln, width * (1 + rng.uniform(-0.2, 0.2)), cc, bones, n=nrm, thick=thick, lift=0.05)


# ------------------------------------------------------------------ armour
def shell(c, ctr, rad, col, bones, th=(-60, 60), ph=(-30, 60), off=0.06, thick=0.16, seg=(6, 4), rot=None,
          trim=None, inset=0.16, **kw):
    """curved armour plate over part of an ellipsoid. th = azimuth range in degrees (0 = front -z, 90 = +x,
    180 = back), ph = elevation range. trim=colour -> plate in trim colour + raised inset panel in col."""
    M = grot(*rot) if rot else Matrix.Identity(3)
    kw.setdefault("stud", False)          # armour plates are clean hard surfaces

    def surf(t, p, o):
        t, p = R(t), R(p)
        u = V(math.sin(t) * math.cos(p), math.sin(p), -math.cos(t) * math.cos(p))
        pt = V(u.x * rad[0], u.y * rad[1], u.z * rad[2])
        nr = V(u.x / rad[0], u.y / rad[1], u.z / rad[2]).normalized()
        return ctr + M @ (pt + nr * o)

    def slab(t0, t1, p0, p1, o0, o1, color, **k2):
        bm = bmesh.new()
        nu, nv = seg
        A = [[bm.verts.new(surf(t0 + (t1 - t0) * i / nu, p0 + (p1 - p0) * j / nv, o1)) for j in range(nv + 1)] for i in range(nu + 1)]
        Bq = [[bm.verts.new(surf(t0 + (t1 - t0) * i / nu, p0 + (p1 - p0) * j / nv, o0)) for j in range(nv + 1)] for i in range(nu + 1)]
        for i in range(nu):
            for j in range(nv):
                bm.faces.new((A[i][j], A[i + 1][j], A[i + 1][j + 1], A[i][j + 1]))
                bm.faces.new((Bq[i][j], Bq[i][j + 1], Bq[i + 1][j + 1], Bq[i + 1][j]))
        edge = [(i, 0) for i in range(nu)] + [(nu, j) for j in range(nv)] + [(i, nv) for i in range(nu, 0, -1)] + [(0, j) for j in range(nv, 0, -1)]
        for k in range(len(edge)):
            (i1, j1), (i2, j2) = edge[k], edge[(k + 1) % len(edge)]
            bm.faces.new((A[i1][j1], Bq[i1][j1], Bq[i2][j2], A[i2][j2]))
        return _finish(c, bm, color, bones, **k2)

    if trim is None:
        return slab(th[0], th[1], ph[0], ph[1], off, off + thick, col, **kw)
    slab(th[0], th[1], ph[0], ph[1], off, off + thick, trim, **kw)
    dt, dp = (th[1] - th[0]) * inset, (ph[1] - ph[0]) * inset
    return slab(th[0] + dt, th[1] - dt, ph[0] + dp, ph[1] - dp, off + thick * 0.5, off + thick * 1.5, col, **kw)


def cuff(c, a, b, r, col, bones, thick=0.14, seg=8, flare=0.15, spikes=0, spike_col=None, spike_len=0.5, **kw):
    """armour ring / gauntlet / greave around a limb from a to b (game). r = inner radius at the middle"""
    kw.setdefault("stud", False)
    d = b - a
    dn = d.normalized()
    s1 = dn.cross(V(0, 1, 0)) if abs(dn.y) < 0.95 else dn.cross(V(1, 0, 0))
    s1.normalize()
    s2 = dn.cross(s1).normalized()
    bm = bmesh.new()
    prof = [(0.0, r + flare), (0.5, r), (1.0, r + flare)]
    outer, inner = [], []
    for t, rr in prof:
        ctr = a + d * t
        dirs = [s1 * math.cos(k / seg * math.tau) + s2 * math.sin(k / seg * math.tau) for k in range(seg)]
        outer.append([bm.verts.new(ctr + q * (rr + thick)) for q in dirs])
        inner.append([bm.verts.new(ctr + q * rr) for q in dirs])
    for i in range(len(prof) - 1):
        for k in range(seg):
            k2 = (k + 1) % seg
            bm.faces.new((outer[i][k], outer[i][k2], outer[i + 1][k2], outer[i + 1][k]))
            bm.faces.new((inner[i][k], inner[i + 1][k], inner[i + 1][k2], inner[i][k2]))
    for ro, ri in ((outer[0], inner[0]), (outer[-1], inner[-1])):
        for k in range(seg):
            k2 = (k + 1) % seg
            bm.faces.new((ro[k], ri[k], ri[k2], ro[k2]))
    _finish(c, bm, col, bones, **kw)
    if spikes:
        mid = a + d * 0.5
        for k in range(spikes):
            q = s1 * math.cos(k / spikes * math.tau + 0.3) + s2 * math.sin(k / spikes * math.tau + 0.3)
            S(c, mid + q * (r + thick * 0.6), mid + q * (r + thick + spike_len) + dn * spike_len * 0.3, thick * 1.6, spike_col or col, bones, stud=False)


def crown(c, ctr, rad, h, col, bones, n=5, gem=None, tilt=(0, 0, 0), thick=0.18, tall=1.5, emblem=True, points="spike", stud=False):
    """royal crown: ring band + n tall points + front emblem with a glowing gem"""
    M = grot(*tilt)
    cuff(c, ctr, ctr + M @ V(0, h, 0), rad, col, bones, thick=thick, seg=max(10, n * 2), flare=0.06, stud=stud)
    for i in range(n):
        a = i / n * math.tau
        dirv = V(math.sin(a), 0, -math.cos(a))
        tang = V(math.cos(a), 0, math.sin(a))
        ph = h * tall * (1.25 if i == 0 else 1.0)
        base = ctr + M @ (dirv * (rad + thick * 0.5) + V(0, h * 0.85, 0))
        w = rad * math.tau / n * 0.36
        tip = base + M @ (V(0, ph, 0) + dirv * 0.08 * ph)
        SHEET(c, [base - M @ tang * w, base + M @ tang * w, tip], col, bones, thick=thick * 1.2, stud=stud)
        if gem:
            E(c, tip - M @ V(0, ph * 0.15, 0) + M @ dirv * thick * 0.6, (0.09 * rad * 1.5,) * 3, gem, bones, seg=(6, 4), glow=True)
    if emblem:
        f = ctr + M @ V(0, h * 0.55, -(rad + thick))
        BOX(c, f, (h * 0.42, h * 0.42, thick * 0.6), col, bones, rot=(tilt[0], tilt[1], 45 + tilt[2]), stud=stud)
        if gem:
            BOX(c, f + M @ V(0, 0, -thick * 0.45), (h * 0.24, h * 0.24, thick * 0.4), gem, bones, rot=(tilt[0], tilt[1], 45 + tilt[2]), glow=True)


# ------------------------------------------------------------------ face
def _snap(c, point, direction, bones, max_dist=3.0):
    d = direction.normalized()
    start = point + d * max_dist
    best = None
    bset = set(bones if isinstance(bones, (list, tuple)) else [bones])
    for sh in c.shapes:
        if sh["glow"] or not (set(sh["bones"]) & bset):
            continue
        hit = BVHTree.FromBMesh(sh["bm"]).ray_cast(start, -d, max_dist * 2)
        if hit[0] is not None:
            dist = (hit[0] - start).length
            if best is None or dist < best[1]:
                best = (hit[0], dist, hit[1])
    return (best[0], best[2]) if best else (point, d)


def fierce_eye(c, center, size, bones, facing=None, glow=C(255, 45, 45), core=C(255, 150, 120), brow=None,
               slant=20, socket=C(25, 10, 12), brow_len=1.2, brow_lift=0.62, snap=True):
    """glowing angry eye: dark socket, slanted glowing almond (inner corner down), hot core, angry brow"""
    cb, fb = B(center), B(facing if facing is not None else V(0, 0, -1)).normalized()
    if snap:
        cb, nrm = _snap(c, cb, fb, bones)
        fb = (fb * 0.5 + nrm.normalized() * 0.5).normalized()
    f = fb
    inner = Vector((-math.copysign(1, cb.x) if abs(cb.x) > 1e-4 else 1, 0, 0))
    sv = f.cross(Vector((0, 0, 1)))
    if sv.length < 1e-3:
        sv = Vector((1, 0, 0))
    sv.normalize()
    if sv.dot(inner) < 0:
        sv = -sv
    up = Vector((0, 0, 1)) - f * f.z
    up = (up - sv * up.dot(sv)).normalized()

    def axes(deg):
        a = R(deg)
        return sv * math.cos(a) - up * math.sin(a), up * math.cos(a) + sv * math.sin(a)

    def ell(off, rad, col, X, Y, gl):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=7, radius=1.0)
        Mx = Matrix((X, f, Y)).transposed().to_4x4()
        m = Matrix.Translation(cb + X * off[0] + f * off[1] + Y * off[2]) @ Mx @ Matrix.Diagonal((rad[0], rad[1], rad[2], 1))
        bmesh.ops.transform(bm, matrix=m, verts=bm.verts)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        c._add(bm, col, bones, glow=gl, stud=False)
    s = size
    ax, bx = axes(slant)
    ell((0, -s * 0.1, 0), (s * 0.95, s * 0.2, s * 0.6), socket, ax, bx, False)
    ell((0, 0.0, 0), (s * 0.74, s * 0.14, s * 0.38), glow, ax, bx, True)
    ell((-s * 0.08, s * 0.04, s * 0.02), (s * 0.2, s * 0.12, s * 0.14), core, ax, bx, True)
    if brow:
        ax2, bx2 = axes(slant * 1.6)
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=2.0)
        Mx = Matrix((ax2, f, bx2)).transposed().to_4x4()
        m = Matrix.Translation(cb + bx * s * brow_lift + f * s * 0.08 + ax * s * 0.12) @ Mx @ Matrix.Diagonal((s * 0.78 * brow_len, s * 0.3, s * 0.22, 1))
        bmesh.ops.transform(bm, matrix=m, verts=bm.verts)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        c._add(bm, brow, bones)


def eyes_pair(c, ctr, dx, size, bones, **kw):
    """both eyes; ctr = midpoint between the eyes (game), dx = half distance"""
    turn = kw.pop("turn", 0.45)
    for s in (-1, 1):
        fierce_eye(c, ctr + V(s * dx, 0, 0), size, bones, facing=V(s * turn, 0.05, -1), **kw)


def maw(c, F, w, d, gap, upper, jaw, n=8, tooth=0.24, fangs=1.8, teeth_col=TOOTH, mouth_col=MOUTH, tongue_col=TONGUE,
        lower_teeth=True, tongue=True, inner=True):
    """open mouth with rows of sharp teeth. F = front centre of the mouth opening (game), w = half width,
    d = depth back to the corners, gap = opening height. Upper teeth on `upper` bone, lower on `jaw`."""
    if inner:
        E(c, F + V(0, 0, d * 0.78), (w * 0.95, gap * 0.6, d * 0.85), mouth_col, [upper], stud=False, seg=(10, 7))
    if tongue:
        E(c, F + V(0, -gap * 0.3, d * 0.5), (w * 0.6, gap * 0.17, d * 0.62), tongue_col, [jaw], stud=False, seg=(8, 6))
    rows = [(gap * 0.5, -1, upper, 1.0)] + ([(-gap * 0.5, 1, jaw, 0.8)] if lower_teeth else [])
    for yy, sgn, bone, scale in rows:
        for i in range(n):
            t = -1 + 2 * i / (n - 1)
            x = t * w * 0.9
            z = F.z + d * t * t * 0.95 + 0.04
            canine = abs(abs(t) - 0.62) < 0.15
            ln = tooth * (fangs if canine else 1.0) * scale
            base = V(x, F.y + yy - sgn * 0.04, z)
            tip = base + V(-x * 0.04, sgn * ln, 0)
            S(c, base, tip, tooth * 0.38 * (1.2 if canine else 1), teeth_col, bone, stud=False)


def ram_horn(c, base, s, size, col, bones, turns=0.85, out=0.5, yaw=25, ribs=True, seg=7, r0=None, **kw):
    """curled ram horn starting at `base` (game) on side s: goes up, back, down and forward, drifting outward"""
    M = grot(0, s * yaw, 0)
    pts, radii = [], []
    n = 16
    r0 = r0 or size * 0.42
    for i in range(n + 1):
        k = i / n
        a = k * turns * math.tau
        rr = size * (1 - 0.45 * k)
        off = V(s * out * size * k * 1.6, rr * math.cos(a) - size, rr * math.sin(a))
        pts.append(base + M @ off)
        r = r0 * (1 - 0.82 * k) + 0.04
        radii.append(r * (1.12 if ribs and i % 2 else 1.0))
    return T(c, pts, radii, col, bones, seg=seg, sub=1, **kw)


def swept_horn(c, pts, r, col, bones, seg=6, ribs=False, **kw):
    n = len(pts)
    radii = [r * (1 - 0.88 * i / (n - 1)) + 0.03 for i in range(n)]
    if ribs:
        radii = [rr * (1.1 if i % 2 else 1) for i, rr in enumerate(radii)]
    return T(c, pts, radii, col, bones, seg=seg, sub=2 if not ribs else 1, **kw)


# ------------------------------------------------------------------ painted patterns
def filigree(col, scale=1.0, width=0.09, only=None):
    """swirling gold trim lines"""
    def mask(X, Y, Z):
        u = np.sin(X * 1.7 * scale + np.sin(Z * 1.3 * scale) * 1.8) + 0.8 * np.sin(Z * 1.1 * scale + np.sin(Y * 1.9 * scale) * 1.5) + np.sin(Y * 1.4 * scale)
        m = np.abs(u) < width * 3
        if only is not None:
            m &= only(X, Y, Z)
        return m
    return (col, mask)


def cracks(col, scale=1.0, width=0.06, only=None):
    """glowing-lava / lightning style crack network (painted)"""
    def mask(X, Y, Z):
        a = np.abs(np.sin(X * 2.1 * scale + np.sin(Y * 1.7 * scale) * 2.2 + Z * 0.7 * scale))
        b = np.abs(np.sin(Z * 2.3 * scale + np.sin(X * 1.3 * scale) * 2.0 - Y * 0.9 * scale))
        m = (a < width * 2.5) | (b < width * 2.0)
        if only is not None:
            m &= only(X, Y, Z)
        return m
    return (col, mask)


def detailed(name, height):
    """Creature preset for the detailed batch: smaller, subtler studs"""
    c = Creature(name, height=height, stud=height / 44)
    c.stud_k = 0.65
    return c


# ------------------------------------------------------------------ quadruped skeleton
def beast(c, sh=4.2, hip=None, L=2.0, W=1.1, neck=(1.0, 1.0), head=1.5, tail=4, tail_len=1.0, tail_lift=0.25):
    """quadruped skeleton compatible with kit.quad_anims (+ a Jaw bone). Chest at z=-L, hips at z=+L.
    Returns key points (game Vectors)."""
    hip = hip or sh
    cz, hz = -L, L
    mid = V(0, (hip + sh) / 2, 0)
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    c.bone("Hips", B(V(0, hip, hz)), B(mid), "Root")
    c.bone("Chest", B(mid), B(V(0, sh, cz)), "Hips")
    nb = V(0, sh + 0.3, cz - 0.2)
    hb = nb + V(0, neck[1], -neck[0])
    c.bone("Neck", B(nb), B(hb), "Chest")
    c.bone("Head", B(hb), B(hb + V(0, 0.1, -head)), "Neck")
    c.bone("Jaw", B(hb + V(0, -0.35, -0.3)), B(hb + V(0, -0.7, -head)), "Head")
    k = dict(sh=sh, hip=hip, cz=cz, hz=hz, W=W, nb=nb, hb=hb, mid=mid)
    for s, X in ((-1, "L"), (1, "R")):
        sho, elb, paw = V(s * W, sh - 0.2, cz), V(s * W * 1.05, sh * 0.5, cz - 0.15), V(s * W * 1.05, 0.35, cz - 0.1)
        hp_, kn, ft = V(s * W * 0.95, hip - 0.2, hz), V(s * W * 1.02, hip * 0.52, hz - 0.45), V(s * W * 1.05, 0.35, hz + 0.15)
        c.bone("Arm" + X, B(sho), B(elb), "Chest")
        c.bone("Fore" + X, B(elb), B(paw), "Arm" + X)
        c.bone("Thigh" + X, B(hp_), B(kn), "Hips")
        c.bone("Shin" + X, B(kn), B(ft), "Thigh" + X)
        k.update({"sho" + X: sho, "elb" + X: elb, "paw" + X: paw, "hip" + X: hp_, "knee" + X: kn, "foot" + X: ft})
    t0, prev, tp = V(0, hip + 0.1, hz + 0.5), "Hips", []
    tp.append(t0)
    for i in range(tail):
        t1 = t0 + V(0, tail_lift * (1 - i / max(1, tail)), tail_len)
        c.bone("Tail%d" % (i + 1), B(t0), B(t1), prev)
        prev, t0 = "Tail%d" % (i + 1), t1
        tp.append(t1)
    k["tail"] = tp
    return k


def leg(c, k, X, col, r=(0.62, 0.5, 0.42), paw_col=None, paw=(0.62, 0.36, 0.8), seg=7, front=True, paint=None, muscle=True):
    """faceted leg along the skeleton: muscle mass at the top, upper + lower tube and a paw.
    r = (top, joint, ankle) radius"""
    r = tuple(v * 1.16 for v in r)            # owner wants sturdy, not skinny, legs
    if front:
        a, b, f, ub, lb = k["sho" + X], k["elb" + X], k["paw" + X], "Arm" + X, "Fore" + X
    else:
        a, b, f, ub, lb = k["hip" + X], k["knee" + X], k["foot" + X], "Thigh" + X, "Shin" + X
    s = 1 if a.x > 0 else -1
    if muscle:
        L = (a - b).length
        E(c, a.lerp(b, 0.32) + V(s * 0.05, 0, 0.1 if not front else 0), (r[0] * 1.22, L * 0.42, r[0] * (1.45 if not front else 1.3)), col, ub, seg=(9, 6), paint=paint)
    T(c, [a + V(0, 0.2, 0), a.lerp(b, 0.5), b], [r[0] * 1.15, r[0], r[1]], col, ub, seg=seg, paint=paint)
    E(c, b, (r[1] * 1.08, r[1] * 1.1, r[1] * 1.12), col, lb, seg=(8, 5), paint=paint)
    T(c, [b, b.lerp(f, 0.5), f + V(0, 0.15, 0)], [r[1], r[2] * 1.05, r[2]], col, lb, seg=seg, paint=paint)
    E(c, f + V(0, -0.05, -paw[2] * 0.35), paw, paw_col or col, lb, seg=(8, 5))
    return b


def claws3(c, f, col, bone, n=3, size=0.32, spread=0.32, z=-0.75):
    for i in range(n):
        o = (i - (n - 1) / 2) * spread
        S(c, f + V(o, 0.15, z * 0.8), f + V(o * 1.15, -0.25, z - size * 1.4), size * 0.42, col, bone, bend=V(0, 0.18, 0), seg=4, n=4, stud=False)

