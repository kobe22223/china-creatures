"""Voxel -> quads: exterior faces only, greedy-merged per colour (with a max run so blocks still read), UVs onto a
shared palette atlas. Pure python (no bpy) so it is easy to test.

Atlas: 1024 px, 32 px cells. Each colour gets 4 cells: TOP (lit), SIDE_A / SIDE_B (top-light gradient, two slightly
different brightnesses so neighbouring blocks don't merge visually) and BOTTOM (dark). Every cell has a darker 2 px
border, which draws the block edge lines.
"""
import math
from PIL import Image, ImageDraw
from voxel import VOX, DIRS, shade

CELL, ATLAS = 32, 1024
PER_ROW = ATLAS // CELL
KINDS = ("top", "sa", "sb", "bot")


class Atlas:
    def __init__(self):
        self.cols = []
        self.index = {}

    def add(self, col):
        if col not in self.index:
            self.index[col] = len(self.cols)
            self.cols.append(col)

    def cell(self, col, kind):
        i = self.index[col] * 4 + KINDS.index(kind)
        assert i < PER_ROW * PER_ROW, "atlas full"
        return i % PER_ROW, i // PER_ROW

    def uv_box(self, col, kind):
        cx, cy = self.cell(col, kind)
        u0, u1 = (cx * CELL + 0.5) / ATLAS, ((cx + 1) * CELL - 0.5) / ATLAS
        vt, vb = 1 - (cy * CELL + 0.5) / ATLAS, 1 - ((cy + 1) * CELL - 0.5) / ATLAS
        return u0, u1, vb, vt

    def image(self, path):
        img = Image.new("RGB", (ATLAS, ATLAS), (0, 0, 0))
        px = img.load()
        for col in self.cols:
            for kind in KINDS:
                cx, cy = self.cell(col, kind)
                for j in range(CELL):
                    g = 1 - j / (CELL - 1)                       # 1 at the top row of the cell
                    if kind == "top":
                        k = 1.12 + 0.04 * g
                    elif kind == "bot":
                        k = 0.68
                    else:
                        k = (0.9 if kind == "sa" else 0.87) + 0.14 * g
                    for i in range(CELL):
                        edge = i < 2 or i >= CELL - 2 or j < 2 or j >= CELL - 2
                        c = shade(col, k * (0.62 if edge else 1.0))
                        px[cx * CELL + i, cy * CELL + j] = c
        img.save(path)
        return path


def faces(egg):
    """{(axis, sign, slice): {(a, b): colour}} for body faces and {colour: [same]} for glow faces"""
    occ = egg.body.keys() | egg.glow.keys()
    body, glow = {}, {}
    for src, out in ((egg.body, body), (egg.glow, None)):
        for p, col in src.items():
            for d in DIRS:
                q = (p[0] + d[0], p[1] + d[1], p[2] + d[2])
                if q in occ:
                    continue
                axis = 0 if d[0] else (1 if d[1] else 2)
                sign = d[axis]
                if axis == 1:
                    a, b = p[0], p[2]
                else:
                    a, b = (p[2] if axis == 0 else p[0]), p[1]      # b = y on side faces
                key = (axis, sign, p[axis])
                if out is not None:
                    out.setdefault(key, {})[(a, b)] = col
                else:
                    glow.setdefault(col, {}).setdefault(key, {})[(a, b)] = col
    return body, glow


def greedy(cells, maxrun):
    """merge a {(a, b): key} grid into rectangles (a0, b0, w, h, key)"""
    done = set()
    rects = []
    for (a, b) in sorted(cells, key=lambda k: (k[1], k[0])):
        if (a, b) in done:
            continue
        key = cells[(a, b)]
        w = 1
        while w < maxrun and (a + w, b) not in done and cells.get((a + w, b)) == key:
            w += 1
        h = 1
        while h < maxrun and all(cells.get((a + i, b + h)) == key and (a + i, b + h) not in done for i in range(w)):
            h += 1
        for i in range(w):
            for j in range(h):
                done.add((a + i, b + j))
        rects.append((a, b, w, h, key))
    return rects


def quad_corners(axis, sign, sl, a0, b0, w, h):
    """4 corners (voxel units) of a face rectangle, wound counter-clockwise seen from outside, plus (a, b) per corner"""
    plane = sl + (1 if sign > 0 else 0)
    ab = [(a0, b0), (a0 + w, b0), (a0 + w, b0 + h), (a0, b0 + h)]

    def P(a, b):
        if axis == 1:
            return (a, plane, b)
        if axis == 0:
            return (plane, b, a)
        return (a, b, plane)
    pts = [P(a, b) for a, b in ab]
    # fix winding: normal of (p1 - p0) x (p3 - p0) must point along +sign on axis
    e1 = [pts[1][i] - pts[0][i] for i in range(3)]
    e2 = [pts[3][i] - pts[0][i] for i in range(3)]
    n = (e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0])
    if n[axis] * sign < 0:
        pts = [pts[0], pts[3], pts[2], pts[1]]
        ab = [ab[0], ab[3], ab[2], ab[1]]
    return pts, ab


def build(egg, atlas, maxrun=3):
    """returns body = (verts, quads, uvs) in game studs, glow = {colour: (verts, quads)}, and triangle count"""
    bf, gf = faces(egg)
    verts, quads, uvs = [], [], []
    vmap = {}

    def vid(p, vm, vl):
        if p not in vm:
            vm[p] = len(vl)
            vl.append(p)
        return vm[p]
    for (axis, sign, sl), cells in bf.items():
        for a0, b0, w, h, col in greedy(cells, maxrun):
            pts, ab = quad_corners(axis, sign, sl, a0, b0, w, h)
            if axis == 1:
                kind = "top" if sign > 0 else "bot"
            else:
                kind = "sa" if (a0 + b0 + sl) % 2 == 0 else "sb"
            u0, u1, vb, vt = atlas.uv_box(col, kind)
            quad = []
            quv = []
            for (px_, py_, pz_), (a, b) in zip(pts, ab):
                quad.append(vid((px_ * VOX, py_ * VOX, pz_ * VOX), vmap, verts))
                quv.append((u0 if a == a0 else u1, vb if b == b0 else vt))
            quads.append(quad)
            uvs.append(quv)
    glow = {}
    for col, groups in gf.items():
        gv, gq, gm = [], [], {}
        for (axis, sign, sl), cells in groups.items():
            for a0, b0, w, h, _ in greedy(cells, 64):
                pts, _ab = quad_corners(axis, sign, sl, a0, b0, w, h)
                gq.append([vid((x * VOX, y * VOX, z * VOX), gm, gv) for x, y, z in pts])
        glow[col] = (gv, gq)
    tris = 2 * len(quads) + sum(2 * len(q) for _, q in glow.values())
    return (verts, quads, uvs), glow, tris
