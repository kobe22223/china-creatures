"""Voxel egg tool: chunky block eggs (0.2 stud voxels) with surface patterns, features that stick out and glow.

Units inside an Egg are VOXELS (1 = 0.2 studs). Game axes: x right, y up, front = -z. The grid is centred on x/z = 0
and starts at y = 0, so the exported origin is the bottom centre of the egg.

    e = Egg("China_Z01_Egg", 3.2, base=WHITE)
    e.paint(band(0.4, 0.55, COBALT, wave=1.0))        # recolour egg surface voxels
    e.shell_offset(lambda x, y, z, a, t: t > 0.8, 0, 1, GOLD)   # add a 1-voxel cap layer outside the surface
    e.sphere((0, e.h + 1, 0), 1.5, RED)                 # free primitive
    e.crack(0, 0.5, 18, GLOWC)                          # glowing jagged crack on the front
Angles: 0 = front (-z), 90 = right (+x). t = height fraction (0 bottom, 1 top).
"""
import math, random

VOX = 0.2
DIRS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def hsh(*a):
    """deterministic hash of ints -> [0, 1)"""
    h = 2166136261
    for v in a:
        h = ((h ^ (int(v) & 0xffffffff)) * 16777619) & 0xffffffff
    h ^= h >> 13
    h = (h * 1274126177) & 0xffffffff
    return (h & 0xffffff) / float(0x1000000)


def mix(c1, c2, k):
    return tuple(int(round(a + (b - a) * k)) for a, b in zip(c1, c2))


def shade(c, k):
    return tuple(max(0, min(255, int(round(v * k)))) for v in c)


class Egg:
    def __init__(self, name, height, base=(240, 240, 240), width_ratio=0.75, kind="Egg"):
        self.name, self.H, self.kind = name, height, kind
        self.h = int(round(height / VOX))
        self.w = self.h * width_ratio
        self.body, self.glow = {}, {}
        # radius profile R(y): the classic egg curve (wider low down) with a small flat base so it stands
        ys = [i * 0.25 for i in range(int(self.h * 4) + 1)]
        rs = []
        for y in ys:
            t = -0.94 + 1.94 * y / self.h
            rs.append(math.sqrt(max(0.0, 1 - t * t)) * (1 + 0.12 * (1 - t)))
        m = max(rs)
        self._py = ys
        self._pr = [self.w / 2 * r / m for r in rs]
        n = int(self.w / 2) + 2
        self.n = n
        for iy in range(self.h):
            r = self.R(iy + 0.5)
            for ix in range(-n, n):
                for iz in range(-n, n):
                    if (ix + 0.5) ** 2 + (iz + 0.5) ** 2 <= r * r:
                        self.body[(ix, iy, iz)] = base
        self.smooth()
        self.shell = set(self.body)          # the egg itself (patterns only touch these)
        self.base = base

    def smooth(self, passes=2):
        """clean the raw voxel egg: drop lone voxels sticking out (<= 2 solid neighbours), fill 1-voxel pits (>= 5)"""
        for _ in range(passes):
            occ = set(self.body)
            cand = set()
            for p in occ:
                for d in DIRS:
                    cand.add((p[0] + d[0], p[1] + d[1], p[2] + d[2]))
            for p in occ:
                if p[1] == 0:
                    continue
                if sum((p[0] + d[0], p[1] + d[1], p[2] + d[2]) in occ for d in DIRS) <= 2:
                    del self.body[p]
            for p in cand - occ:
                if 0 <= p[1] < self.h and sum((p[0] + d[0], p[1] + d[1], p[2] + d[2]) in occ for d in DIRS) >= 5:
                    self.body[p] = self.base

    # ------------------------------------------------------------------ geometry queries
    def R(self, y):
        if y <= 0:
            return self._pr[0]
        if y >= self.h:
            return 0.0
        f = y * 4
        i = int(f)
        k = f - i
        return self._pr[i] * (1 - k) + self._pr[min(i + 1, len(self._pr) - 1)] * k

    def sdf(self, x, y, z):
        """approximate signed distance (voxels) to the egg surface: negative inside"""
        rr = math.hypot(x, z)
        best = 1e9
        py, pr = self._py, self._pr
        step = 2
        for i in range(0, len(py) - step, step):
            ax, ay, bx, by = pr[i], py[i], pr[i + step], py[i + step]
            dx, dy = bx - ax, by - ay
            L = dx * dx + dy * dy
            k = 0.0 if L == 0 else max(0.0, min(1.0, ((rr - ax) * dx + (y - ay) * dy) / L))
            d = math.hypot(rr - (ax + dx * k), y - (ay + dy * k))
            best = min(best, d)
        best = min(best, math.hypot(max(0.0, rr - pr[0]), y)) if y < 0.5 else best
        inside = 0 <= y <= self.h and rr <= self.R(y)
        return -best if inside else best

    def surf(self, ang, t, out=0.0):
        """point on the egg surface at angle (deg, 0 = front) and height fraction t, pushed `out` voxels outward"""
        a = math.radians(ang)
        y = t * self.h
        r = self.R(y) + out
        return (r * math.sin(a), y, -r * math.cos(a))

    def normal(self, ang, t):
        a = math.radians(ang)
        y = t * self.h
        dr = (self.R(y + 0.5) - self.R(y - 0.5))
        n = (math.sin(a), -dr, -math.cos(a))
        L = math.sqrt(sum(v * v for v in n))
        return tuple(v / L for v in n)

    @staticmethod
    def polar(x, y, z, h):
        return math.degrees(math.atan2(x, -z)) % 360, y / h

    def surface_voxels(self):
        occ = self.body.keys() | self.glow.keys()
        out = []
        for p in self.shell:
            if p in self.body:
                for d in DIRS:
                    if (p[0] + d[0], p[1] + d[1], p[2] + d[2]) not in occ:
                        out.append(p)
                        break
        return out

    # ------------------------------------------------------------------ painting the egg surface
    def paint(self, fn, depth=2):
        """fn(x, y, z, ang, t) -> colour or None, applied to egg voxels within `depth` of the surface"""
        for p in list(self.shell):
            if p not in self.body:
                continue
            x, y, z = p[0] + 0.5, p[1] + 0.5, p[2] + 0.5
            if math.hypot(x, z) < self.R(y) - depth - 0.5 and depth < 50:
                continue
            ang, t = self.polar(x, y, z, self.h)
            c = fn(x, y, z, ang, t)
            if c is not None:
                self.body[p] = c

    # ------------------------------------------------------------------ adding voxels
    def put(self, p, col, glow=False):
        if glow:
            self.body.pop(p, None)
            self.glow[p] = col
        else:
            if p in self.glow:
                return
            self.body[p] = col

    def fill(self, inside, bbox, col, glow=False):
        """add every voxel whose centre passes inside(x, y, z) (voxel units) within bbox ((x0,x1),(y0,y1),(z0,z1)).
        col may be a colour or fn(x, y, z) -> colour."""
        (x0, x1), (y0, y1), (z0, z1) = bbox
        for ix in range(int(math.floor(x0)) - 1, int(math.ceil(x1)) + 1):
            for iy in range(int(math.floor(y0)) - 1, int(math.ceil(y1)) + 1):
                for iz in range(int(math.floor(z0)) - 1, int(math.ceil(z1)) + 1):
                    x, y, z = ix + 0.5, iy + 0.5, iz + 0.5
                    if inside(x, y, z):
                        c = col(x, y, z) if callable(col) else col
                        if c is not None:
                            self.put((ix, iy, iz), c, glow)

    def box(self, c, half, col, glow=False):
        cx, cy, cz = c
        hx, hy, hz = half
        self.fill(lambda x, y, z: abs(x - cx) <= hx and abs(y - cy) <= hy and abs(z - cz) <= hz,
                  ((cx - hx, cx + hx), (cy - hy, cy + hy), (cz - hz, cz + hz)), col, glow)

    def sphere(self, c, r, col, scale=(1, 1, 1), glow=False):
        cx, cy, cz = c
        sx, sy, sz = scale
        self.fill(lambda x, y, z: ((x - cx) / sx) ** 2 + ((y - cy) / sy) ** 2 + ((z - cz) / sz) ** 2 <= r * r,
                  ((cx - r * sx, cx + r * sx), (cy - r * sy, cy + r * sy), (cz - r * sz, cz + r * sz)), col, glow)

    def capsule(self, p0, p1, r0, r1, col, glow=False):
        """tapered capsule from p0 (radius r0) to p1 (radius r1)"""
        ax, ay, az = p0
        dx, dy, dz = p1[0] - ax, p1[1] - ay, p1[2] - az
        L2 = dx * dx + dy * dy + dz * dz or 1e-6
        R = max(r0, r1)

        def inside(x, y, z):
            k = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy + (z - az) * dz) / L2))
            r = r0 + (r1 - r0) * k
            return (x - ax - dx * k) ** 2 + (y - ay - dy * k) ** 2 + (z - az - dz * k) ** 2 <= r * r
        self.fill(inside, ((min(ax, p1[0]) - R, max(ax, p1[0]) + R), (min(ay, p1[1]) - R, max(ay, p1[1]) + R),
                           (min(az, p1[2]) - R, max(az, p1[2]) + R)), col, glow)

    def chain(self, pts, radii, col, glow=False):
        for i in range(len(pts) - 1):
            self.capsule(pts[i], pts[i + 1], radii[i], radii[i + 1], col, glow)

    def shell_offset(self, region, d0, d1, col, glow=False, pad=None):
        """add voxels whose signed distance to the egg surface is in (d0, d1] and region(x, y, z, ang, t) is true.
        d0 = 0, d1 = 1 adds a 1-voxel layer on the outside (caps, raised swirls, moss, plates)."""
        pad = pad if pad is not None else d1 + 1
        n = self.n + int(pad) + 1
        for ix in range(-n, n):
            for iz in range(-n, n):
                for iy in range(-1, self.h + int(pad) + 1):
                    x, y, z = ix + 0.5, iy + 0.5, iz + 0.5
                    rr = math.hypot(x, z)
                    if 0 < y < self.h and (rr > self.R(y) + d1 + 1.5 or rr < self.R(y) + d0 - 1.5):
                        continue
                    ang, t = self.polar(x, y, z, self.h)
                    if not region(x, y, z, ang, t):
                        continue
                    d = self.sdf(x, y, z)
                    if d0 < d <= d1:
                        c = col(x, y, z, ang, t) if callable(col) else col
                        if c is not None:
                            self.put((ix, iy, iz), c, glow)

    def carve(self, region, col, depth=2, glow=True):
        """turn egg voxels within `depth` of the surface into `col` where region(x, y, z, ang, t) (cracks, windows)"""
        for p in list(self.body):
            x, y, z = p[0] + 0.5, p[1] + 0.5, p[2] + 0.5
            if p not in self.shell:
                continue
            if math.hypot(x, z) < self.R(y) - depth - 0.5:
                continue
            ang, t = self.polar(x, y, z, self.h)
            if region(x, y, z, ang, t):
                self.put(p, col, glow)

    def crack(self, ang, t, length, col, seed=1, width=0.35, depth=2, branches=2, spread=1.0):
        """jagged glowing crack starting at (ang, t), wandering across the surface"""
        rng = random.Random(seed)
        paths = []

        def walk(a, tt, n, heading):
            pts = [(a, tt)]
            for _ in range(n):
                heading += rng.uniform(-0.9, 0.9) * spread
                r = max(self.R(tt * self.h), 1.0)
                a += math.degrees(math.cos(heading) * 1.0 / r)
                tt += math.sin(heading) * 1.0 / self.h
                pts.append((a, tt))
            return pts
        main = walk(ang, t, length, rng.uniform(0, math.tau))
        paths.append(main)
        for b in range(branches):
            a0, t0 = main[rng.randrange(len(main) // 3, len(main))]
            paths.append(walk(a0, t0, length // 2, rng.uniform(0, math.tau)))
        pts3 = [self.surf(a, tt) for p in paths for a, tt in p if 0.02 < tt < 0.98]

        def region(x, y, z, a, tt):
            return any((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2 <= (width + 0.5) ** 2 for px, py, pz in pts3)
        self.carve(region, col, depth=depth, glow=True)

    def plate(self, c, u, v, a, b, thick, col, glow=False):
        """flat elliptic plate (leaves, fins, feathers, bows): centre c, in-plane unit axes u, v, half sizes a, b"""
        nx, ny, nz = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        R = max(a, b) + thick

        def inside(x, y, z):
            dx, dy, dz = x - c[0], y - c[1], z - c[2]
            pu = dx * u[0] + dy * u[1] + dz * u[2]
            pv = dx * v[0] + dy * v[1] + dz * v[2]
            pn = dx * nx + dy * ny + dz * nz
            return (pu / a) ** 2 + (pv / b) ** 2 <= 1 and abs(pn) <= thick / 2
        self.fill(inside, ((c[0] - R, c[0] + R), (c[1] - R, c[1] + R), (c[2] - R, c[2] + R)), col, glow)


# ====================================================================== surface patterns (for Egg.paint)
def band(t0, t1, col, wave=0.0, freq=4, phase=0.0):
    def f(x, y, z, a, t):
        w = wave * math.sin(math.radians(a * freq) + phase) / 100.0 * 4
        return col if t0 + w <= t <= t1 + w else None
    return f


def stripes(cols, period, t0=0.0, t1=1.0, wave=0.0, freq=4):
    def f(x, y, z, a, t):
        if not (t0 <= t <= t1):
            return None
        w = wave * math.sin(math.radians(a * freq)) / 100.0 * 4
        k = int(math.floor((t - t0 + w) / period))
        return cols[k % len(cols)]
    return f


def swirl(col, arms=3, turns=1.0, width=0.18, t0=0.0, t1=1.0):
    def f(x, y, z, a, t):
        if not (t0 <= t <= t1):
            return None
        ph = (a / 360.0 * arms + t * turns * arms) % 1.0
        return col if ph < width else None
    return f


def bricks(col, mortar, row=2, length=4, t0=0.0, t1=1.0, egg=None, jitter=None, seed=3):
    """brick rows of `row` voxels with `length`-voxel bricks, staggered; jitter = (colour, chance) for odd bricks"""
    def f(x, y, z, a, t):
        if not (t0 <= t <= t1):
            return None
        iy = int(math.floor(y))
        ri = iy // row
        r = math.hypot(x, z)
        s = math.radians(a) * r + (ri % 2) * length / 2.0
        k = int(math.floor(s))
        if iy % row == 0 or k % length == 0:
            return mortar
        if jitter and hsh(ri, k // length, seed) < jitter[1]:
            return jitter[0]
        return col
    return f


def scales(col, edge, row=3, length=4, t0=0.0, t1=1.0):
    def f(x, y, z, a, t):
        if not (t0 <= t <= t1):
            return None
        ri = int(math.floor(y / row))
        dy = y / row - ri
        r = math.hypot(x, z)
        s = math.radians(a) * r / length + (ri % 2) * 0.5
        dx = (s - math.floor(s)) - 0.5
        e = (dx * 2) ** 2 + (1 - dy) ** 2
        return edge if 0.75 < e < 1.25 or dy < 1.0 / row else col
    return f


def dots(col, chance=0.08, seed=1, t0=0.0, t1=1.0):
    def f(x, y, z, a, t):
        if not (t0 <= t <= t1):
            return None
        return col if hsh(int(x * 2), int(y * 2), int(z * 2), seed) < chance else None
    return f


def mottle(cols, cell=2, chance=0.5, seed=2, t0=0.0, t1=1.0):
    """blotchy blocks: cells of `cell` voxels get a random colour from cols"""
    def f(x, y, z, a, t):
        if not (t0 <= t <= t1):
            return None
        k = hsh(math.floor(x / cell), math.floor(y / cell), math.floor(z / cell), seed)
        if k >= chance:
            return None
        return cols[int(k / chance * len(cols)) % len(cols)]
    return f


def crackle(col, cell=4.0, width=0.18, seed=5, t0=0.0, t1=1.0):
    """celadon crackle: Voronoi cell edges on the surface"""
    def f(x, y, z, a, t):
        if not (t0 <= t <= t1):
            return None
        r = math.hypot(x, z)
        s = math.radians(a) * r / cell
        v = y / cell
        ds = []
        for i in range(int(math.floor(s)) - 1, int(math.floor(s)) + 2):
            for j in range(int(math.floor(v)) - 1, int(math.floor(v)) + 2):
                px, py = i + hsh(i, j, seed), j + hsh(j, i, seed + 7)
                ds.append(math.hypot(s - px, v - py))
        ds.sort()
        return col if ds[1] - ds[0] < width else None
    return f


def layers(*fns):
    """combine patterns: the last one that returns a colour wins"""
    def f(x, y, z, a, t):
        out = None
        for fn in fns:
            c = fn(x, y, z, a, t)
            if c is not None:
                out = c
        return out
    return f
