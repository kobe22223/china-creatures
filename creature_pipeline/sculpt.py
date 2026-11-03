"""Sculpting toolkit for studded creature meshes (bpy).

Write creatures in "game" coordinates: P(x, y, z) with y = up and z = backwards (the creature's
front points to -z), like Roblox. Internally Blender is Z-up with the front at -Y.

Every shape belongs to one or more bones (rigid or blended weights), has a colour, and flags:
  stud=False  -> no stud pattern (eyes, mouth, gems)
  glow=True   -> exported as a separate "Glow_*" mesh that Roblox renders as Neon
The final mesh is UV-unwrapped and gets a baked texture: flat colours + shading + studs.
"""
import math, json, os, random
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix, Euler, Quaternion
from PIL import Image, ImageDraw, ImageFilter


# game (x right, y up, z back) -> blender: a proper rotation, matching the FBX export axes
# (blender -Y forward / Z up -> FBX -Z forward / Y up), so game x = -blender x.
G = Matrix(((-1, 0, 0), (0, 0, 1), (0, 1, 0)))


def P(x, y, z):
    return Vector((-x, z, y))


def C(r, g, b):
    return (r / 255, g / 255, b / 255)


def euler(rx=0, ry=0, rz=0):
    """rotation given in game axes (degrees), returned as a blender-space matrix"""
    return G @ Euler((math.radians(rx), math.radians(ry), math.radians(rz)), "XYZ").to_matrix() @ G


STUD_SCALE = 0.55


class Creature:
    def __init__(self, name, height=9.0, stud=None):
        self.name = name
        self.height = height
        self.stud = (stud or height / 30) * STUD_SCALE   # owner asked for denser studs
        self.bones = []          # (name, head, tail, parent)
        self.shapes = []         # dicts: bm, color, bones, glow, stud
        self.palette = []
        self.anim_spec = {}
        self.extra = {}

    # ---------------------------------------------------------------- skeleton
    def bn(self, n):
        """exported bone name: unique per creature (Roblox's importer merges same-named bones across a batch)"""
        return self.name + "__" + n

    def bone(self, name, head, tail, parent=None):
        self.bones.append((name, Vector(head), Vector(tail), parent))
        return name

    def bone_pos(self, name, end="head"):
        for n, h, t, p in self.bones:
            if n == name:
                return h if end == "head" else t
        raise KeyError(name)

    # ---------------------------------------------------------------- shapes
    def _add(self, bm, color, bones, glow=False, stud=True, smooth=False, paint=None):
        """paint = fn(x, y, z game coords of a face centre) -> colour or None (painted patterns: stripes, spots)"""
        self.shapes.append(dict(bm=bm, color=tuple(color), bones=bones if isinstance(bones, (list, tuple)) else [bones],
                                glow=glow, stud=stud and not glow, smooth=smooth, paint=paint))
        return bm

    def ellipsoid(self, center, radii, color, bones, rot=None, seg=(14, 9), **kw):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=seg[0], v_segments=seg[1], radius=1.0)
        m = Matrix.Diagonal((radii[0], radii[2], radii[1], 1.0))  # game (x,y,z) radii -> blender (x,z,y)
        if rot is not None:
            m = rot.to_4x4() @ m
        m = Matrix.Translation(center) @ m
        bmesh.ops.transform(bm, matrix=m, verts=bm.verts)
        return self._add(bm, color, bones, **kw)

    def tube(self, points, radii, color, bones, seg=10, cap=True, flat=None, sub=3, **kw):
        """tapered tube through points (Vectors) with per-point radius. flat = (sx, sy) squash of the
        cross-section (sx along the 'side' axis, sy along the 'up-ish' axis). sub = smooth subdivision."""
        if sub > 1 and len(points) >= 3:
            pts2, rad2 = [], []
            n0 = len(points)
            for i in range(n0 - 1):
                p0, p1, p2, p3 = points[max(i - 1, 0)], points[i], points[i + 1], points[min(i + 2, n0 - 1)]
                for k in range(sub):
                    t = k / sub
                    t2, t3 = t * t, t * t * t
                    pts2.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
                    rad2.append(radii[i] + (radii[i + 1] - radii[i]) * t)
            pts2.append(points[-1]); rad2.append(radii[-1])
            points, radii = pts2, rad2
        bm = bmesh.new()
        rings = []
        n = len(points)
        up_hint = Vector((0, 0, 1))
        for i, p in enumerate(points):
            d = (points[min(i + 1, n - 1)] - points[max(i - 1, 0)]).normalized()
            side = d.cross(up_hint)
            if side.length < 1e-3:
                side = d.cross(Vector((1, 0, 0)))
            side.normalize()
            up = side.cross(d).normalized()
            r = radii[i]
            sx, sy = flat or (1, 1)
            ring = []
            for k in range(seg):
                a = k / seg * math.tau
                ring.append(bm.verts.new(p + side * math.cos(a) * r * sx + up * math.sin(a) * r * sy))
            rings.append(ring)
        for i in range(n - 1):
            for k in range(seg):
                a, b = rings[i][k], rings[i][(k + 1) % seg]
                c, d2 = rings[i + 1][(k + 1) % seg], rings[i + 1][k]
                bm.faces.new((a, b, c, d2))
        if cap:
            for ring, pt, sign in ((rings[0], points[0], -1), (rings[-1], points[-1], 1)):
                dirv = (points[1] - points[0]) if sign < 0 else (points[-1] - points[-2])
                tip = bm.verts.new(pt + dirv.normalized() * radii[0 if sign < 0 else -1] * 0.35 * sign)
                for k in range(seg):
                    v1, v2 = ring[k], ring[(k + 1) % seg]
                    if sign < 0:
                        bm.faces.new((v2, v1, tip))
                    else:
                        bm.faces.new((v1, v2, tip))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        return self._add(bm, color, bones, **kw)

    def curve_points(self, a, b, bend=Vector((0, 0, 0)), n=6):
        """quadratic curve from a to b, bulging by `bend` at the middle"""
        pts = []
        for i in range(n):
            t = i / (n - 1)
            pts.append(a.lerp(b, t) + bend * (4 * t * (1 - t)))
        return pts

    def spike(self, base, tip, r, color, bones, bend=None, seg=7, n=5, **kw):
        pts = self.curve_points(base, tip, bend or Vector((0, 0, 0)), n)
        radii = [r * (1 - i / (n - 1)) ** 1.1 + 0.02 for i in range(n)]
        return self.tube(pts, radii, color, bones, seg=seg, **kw)

    def leaf(self, origin, along, width_dir, length, width, color, bones, thick=0.12, n=7, shape="feather", curl=0.0, **kw):
        """flat shape (feather, fin, ear, flame, membrane) with thickness"""
        along = along.normalized()
        width_dir = (width_dir - along * width_dir.dot(along)).normalized()
        normal = along.cross(width_dir).normalized()
        top, bot = [], []
        prof = []
        for i in range(n):
            t = i / (n - 1)
            if shape == "feather":
                w = math.sin(math.pi * min(1, t * 1.15)) ** 0.7 * (1 - 0.35 * t)
            elif shape == "flame":
                w = math.sin(math.pi * t) ** 0.6 * (1 - t) ** 0.5 * 1.4
            elif shape == "fin":
                w = (1 - t) ** 0.8
            else:  # ear / blade
                w = math.sin(math.pi * (0.5 + 0.5 * t)) if t > 0 else 1
            prof.append(max(w, 0.02))
        bm = bmesh.new()
        for i, w in enumerate(prof):
            t = i / (n - 1)
            c = origin + along * (t * length) + normal * (curl * t * t * length)
            for s in (-1, 1):
                for h in (-1, 1):
                    pass
            top.append((bm.verts.new(c - width_dir * w * width / 2 + normal * thick / 2), bm.verts.new(c + width_dir * w * width / 2 + normal * thick / 2)))
            bot.append((bm.verts.new(c - width_dir * w * width / 2 - normal * thick / 2), bm.verts.new(c + width_dir * w * width / 2 - normal * thick / 2)))
        for i in range(n - 1):
            bm.faces.new((top[i][0], top[i][1], top[i + 1][1], top[i + 1][0]))
            bm.faces.new((bot[i][0], bot[i + 1][0], bot[i + 1][1], bot[i][1]))
            bm.faces.new((top[i][0], top[i + 1][0], bot[i + 1][0], bot[i][0]))
            bm.faces.new((top[i][1], bot[i][1], bot[i + 1][1], top[i + 1][1]))
        bm.faces.new((top[0][0], bot[0][0], bot[0][1], top[0][1]))
        bm.faces.new((top[-1][0], top[-1][1], bot[-1][1], bot[-1][0]))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        return self._add(bm, color, bones, **kw)

    def sheet(self, pts, color, bones, thick=0.12, **kw):
        """thin solid panel through a loop of 3D points (fan from their average): wing membranes, fins"""
        bm = bmesh.new()
        ctr = sum(pts, Vector()) / len(pts)
        n = Vector()
        for i in range(len(pts)):
            n += (pts[i] - ctr).cross(pts[(i + 1) % len(pts)] - ctr)
        n = n.normalized() * thick / 2
        top = [bm.verts.new(p + n) for p in pts]; bot = [bm.verts.new(p - n) for p in pts]
        ct, cb = bm.verts.new(ctr + n), bm.verts.new(ctr - n)
        m = len(pts)
        for i in range(m):
            j = (i + 1) % m
            bm.faces.new((ct, top[i], top[j]))
            bm.faces.new((cb, bot[j], bot[i]))
            bm.faces.new((top[i], bot[i], bot[j], top[j]))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        return self._add(bm, color, bones, **kw)

    def torus(self, center, R, r, color, bones, rot=None, seg=(24, 8), **kw):
        bm = bmesh.new()
        rings = []
        for i in range(seg[0]):
            a = i / seg[0] * math.tau
            ring = []
            for k in range(seg[1]):
                b = k / seg[1] * math.tau
                x = (R + r * math.cos(b)) * math.cos(a)
                z = (R + r * math.cos(b)) * math.sin(a)
                y = r * math.sin(b)
                ring.append(bm.verts.new(P(x, y, z)))
            rings.append(ring)
        for i in range(seg[0]):
            for k in range(seg[1]):
                a, b = rings[i][k], rings[i][(k + 1) % seg[1]]
                c, d = rings[(i + 1) % seg[0]][(k + 1) % seg[1]], rings[(i + 1) % seg[0]][k]
                bm.faces.new((a, d, c, b))
        m = Matrix.Translation(center) @ ((rot.to_4x4()) if rot else Matrix.Identity(4))
        bmesh.ops.transform(bm, matrix=m, verts=bm.verts)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        return self._add(bm, color, bones, **kw)

    def box(self, center, half, color, bones, rot=None, **kw):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=2.0)
        m = Matrix.Diagonal((half[0], half[2], half[1], 1.0))
        if rot is not None:
            m = rot.to_4x4() @ m
        bmesh.ops.transform(bm, matrix=Matrix.Translation(center) @ m, verts=bm.verts)
        return self._add(bm, color, bones, **kw)

    # cartoon eye: white, coloured iris, black pupil, two highlights. `facing` = outward direction
    def snap(self, point, direction, max_dist=4.0):
        """move a point onto the outer surface of the shapes built so far, looking back along -direction"""
        from mathutils.bvhtree import BVHTree
        d = direction.normalized()
        start = point + d * max_dist
        best = None
        for sh in self.shapes:
            if sh["glow"]:
                continue
            tree = BVHTree.FromBMesh(sh["bm"])
            hit = tree.ray_cast(start, -d, max_dist * 2)
            if hit[0] is not None:
                dist = (hit[0] - start).length
                if best is None or dist < best[1]:
                    best = (hit[0], dist, hit[1])
        return (best[0], best[2]) if best else (point, d)

    def eye(self, center, size, facing, bones, iris=C(60, 140, 230), lid=None, angry=0.0, style="black", snap=True):
        if snap:
            center, nrm = self.snap(center, facing)
            facing = (facing.normalized() * 0.5 + nrm.normalized() * 0.5)
        f = facing.normalized()
        up = Vector((0, 0, 1))
        side = f.cross(up).normalized()
        upv = side.cross(f).normalized()
        rot = Matrix((side, f, upv)).transposed()  # columns: x=side, y=facing, z=up (blender)
        def ell(off, rad, col):
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=1.0)
            m = Matrix.Translation(center + side * off[0] + f * off[1] + upv * off[2]) @ rot.to_4x4() @ Matrix.Diagonal((rad[0], rad[1], rad[2], 1))
            bmesh.ops.transform(bm, matrix=m, verts=bm.verts)
            self._add(bm, col, bones, stud=False, smooth=True)
        s = size
        if style == "black":
            # flat black eye: a thin oval pushed into the surface so only a flush, flat face shows
            ell((0, -s * 0.12, 0), (s * 0.62, s * 0.2, s * 0.85), C(12, 12, 16))
        else:
            ell((0, 0, 0), (s * 0.85, s * 0.45, s), C(255, 255, 255))
            ell((0, s * 0.18, -s * 0.08), (s * 0.6, s * 0.35, s * 0.68), iris)
            ell((0, s * 0.3, -s * 0.1), (s * 0.36, s * 0.28, s * 0.42), C(15, 15, 25))
            ell((-s * 0.22, s * 0.48, s * 0.25), (s * 0.17, s * 0.1, s * 0.17), C(255, 255, 255))
            ell((s * 0.2, s * 0.44, -s * 0.32), (s * 0.08, s * 0.06, s * 0.08), C(255, 255, 255))
        if lid:
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=1.0)
            m = Matrix.Translation(center + upv * s * 0.55 + f * s * 0.05) @ rot.to_4x4() @ Matrix.Rotation(angry, 4, "Y") @ Matrix.Diagonal((s * 1.0, s * 0.5, s * 0.35, 1))
            bmesh.ops.transform(bm, matrix=m, verts=bm.verts)
            self._add(bm, lid, bones)

    # ---------------------------------------------------------------- build
    def _weights(self, verts, bones):
        """weights for a shape: single bone -> 1.0; several -> blend by distance to bone segments"""
        if len(bones) == 1:
            return [{bones[0]: 1.0} for _ in verts]
        segs = []
        for b in bones:
            for n, h, t, p in self.bones:
                if n == b:
                    segs.append((b, h, t))
        out = []
        for v in verts:
            ds = []
            for b, h, t in segs:
                ab = t - h
                tt = max(0, min(1, (v - h).dot(ab) / ab.length_squared))
                ds.append((b, (v - (h + ab * tt)).length + 1e-4))
            ws = [(b, 1 / d ** 4) for b, d in ds]
            tot = sum(w for _, w in ws)
            ws = sorted(((b, w / tot) for b, w in ws), key=lambda x: -x[1])[:2]
            tot = sum(w for _, w in ws)
            out.append({b: w / tot for b, w in ws})
        return out

    def build(self, outdir):
        os.makedirs(outdir, exist_ok=True)
        bpy.ops.wm.read_factory_settings(use_empty=True)
        scn = bpy.context.scene
        # armature
        arm_data = bpy.data.armatures.new(self.name + "_Rig")
        arm = bpy.data.objects.new(self.name, arm_data)
        scn.collection.objects.link(arm)
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode="EDIT")
        for n, h, t, p in self.bones:
            eb = arm_data.edit_bones.new(self.bn(n))
            eb.head, eb.tail = h, t
            eb.roll = 0
        for n, h, t, p in self.bones:
            if p:
                eb = arm_data.edit_bones[self.bn(n)]
                eb.parent = arm_data.edit_bones[self.bn(p)]
                eb.use_connect = False
        bpy.ops.object.mode_set(mode="OBJECT")
        self.arm = arm
        # palette
        cols = []
        for s in self.shapes:
            if s["color"] not in cols:
                cols.append(s["color"])
        self.palette = cols
        self.paints = []
        # meshes: one "Body" mesh (studded, textured) + one mesh per glow colour
        groups = {"Body": [s for s in self.shapes if not s["glow"]]}
        for s in self.shapes:
            if s["glow"]:
                key = "Glow_%02x%02x%02x" % tuple(int(c * 255) for c in s["color"])
                groups.setdefault(key, []).append(s)
        self.mesh_objs = {}
        for gname, shapes in groups.items():
            bm = bmesh.new()
            col_layer = bm.faces.layers.int.new("col")
            flag_layer = bm.faces.layers.int.new("flag")
            paint_layer = bm.faces.layers.int.new("paint")
            deform = bm.verts.layers.deform.verify()
            bone_index = {n: i for i, (n, *_r) in enumerate(self.bones)}
            for s in shapes:
                src = s["bm"]
                vmap = {}
                ws = self._weights([v.co for v in src.verts], s["bones"])
                for v, w in zip(src.verts, ws):
                    nv = bm.verts.new(v.co)
                    for b, wt in w.items():
                        nv[deform][bone_index[b]] = wt
                    vmap[v] = nv
                ci = cols.index(s["color"])
                pidx = 0
                if s.get("paint"):
                    self.paints.append(s["paint"])
                    pidx = len(self.paints)
                for f in src.faces:
                    try:
                        nf = bm.faces.new([vmap[v] for v in f.verts])
                    except ValueError:
                        continue
                    nf[col_layer] = ci
                    nf[paint_layer] = pidx
                    nf[flag_layer] = (1 if s["stud"] else 0) | (2 if s["smooth"] else 0)
                    nf.smooth = s["smooth"]
            uname = self.name + "_" + gname          # unique per creature (batch FBX files hold several)
            me = bpy.data.meshes.new(uname)
            bm.to_mesh(me)
            bm.free()
            ob = bpy.data.objects.new(uname, me)
            scn.collection.objects.link(ob)
            for n, *_r in self.bones:
                ob.vertex_groups.new(name=self.bn(n))
            ob.parent = arm
            mod = ob.modifiers.new("Armature", "ARMATURE")
            mod.object = arm
            self.mesh_objs[gname] = ob
        self._texture(outdir)
        return self

    # ---------------------------------------------------------------- texture
    def _texture(self, outdir, size=2048):
        body = self.mesh_objs["Body"]
        bpy.ops.object.select_all(action="DESELECT")
        body.select_set(True)
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        # lightmap pack: every face tiled tightly (smart project used only ~10% of the texture on faceted fur)
        bpy.ops.uv.lightmap_pack(PREF_CONTEXT="ALL_FACES", PREF_PACK_IN_ONE=True, PREF_BOX_DIV=48, PREF_MARGIN_DIV=0.15)
        bpy.ops.object.mode_set(mode="OBJECT")
        self.tex_path = os.path.join(outdir, self.name + "_Tex.png")
        self._paint(self.palette, self.paints, size).save(self.tex_path)
        # material
        mat = bpy.data.materials.new(self.name + "_Mat")
        mat.use_nodes = True
        nt = mat.node_tree
        bsdf = nt.nodes["Principled BSDF"]
        bsdf.inputs["Roughness"].default_value = 0.6
        tn = nt.nodes.new("ShaderNodeTexImage")
        tn.image = bpy.data.images.load(self.tex_path)
        nt.links.new(tn.outputs["Color"], bsdf.inputs["Base Color"])
        body.data.materials.append(mat)
        for gname, ob in self.mesh_objs.items():
            if gname.startswith("Glow_"):
                gm = bpy.data.materials.new(gname + "_Mat")
                gm.use_nodes = True
                b = gm.node_tree.nodes["Principled BSDF"]
                hexs = gname[5:]
                rgbv = tuple(int(hexs[i:i + 2], 16) / 255 for i in (0, 2, 4))
                b.inputs["Base Color"].default_value = rgbv + (1,)
                b.inputs["Emission Color"].default_value = rgbv + (1,)
                b.inputs["Emission Strength"].default_value = 1.4
                ob.data.materials.append(gm)

    def _paint(self, palette, paints, size=2048):
        """bake the texture for the Body mesh (already UV-unwrapped) with the given palette / paints"""
        body = self.mesh_objs["Body"]
        me = body.data
        uv = me.uv_layers.active.data
        cols = me.attributes["col"].data
        flags = me.attributes["flag"].data
        img = Image.new("RGB", (size, size), (0, 0, 0))
        mask = Image.new("L", (size, size), 0)       # 255 = has stud pattern
        filled = Image.new("L", (size, size), 0)
        dr, dm, df = ImageDraw.Draw(img), ImageDraw.Draw(mask), ImageDraw.Draw(filled)
        rng = random.Random(7)
        world_area, uv_area = 0.0, 0.0
        for poly in me.polygons:
            pts = [uv[li].uv for li in poly.loop_indices]
            a = 0.0
            for i in range(len(pts)):
                x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]
                a += x1 * y2 - x2 * y1
            uv_area += abs(a) / 2
            world_area += poly.area
            base = palette[cols[poly.index].value]
            nz = poly.normal.z
            shade = 1.0 + 0.10 * nz - (0.10 if nz < -0.3 else 0) + rng.uniform(-0.025, 0.025)
            if flags[poly.index].value & 2:
                shade = 1.0
            c = tuple(int(max(0, min(255, ch * 255 * shade))) for ch in base)
            xy = [(p[0] * size, (1 - p[1]) * size) for p in pts]
            dr.polygon(xy, fill=c, outline=c)
            df.polygon(xy, fill=255, outline=255)
            if flags[poly.index].value & 1:
                dm.polygon(xy, fill=255, outline=255)
        # bleed colours into empty pixels so UV seams don't show black lines
        arr = np.array(img).astype(np.int32)
        fm = np.array(filled) > 0
        for _ in range(24):
            grown = arr.copy(); gm = fm.copy()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                sh = np.roll(np.roll(arr, dx, 1), dy, 0)
                shm = np.roll(np.roll(fm, dx, 1), dy, 0)
                take = shm & ~gm
                grown[take] = sh[take]; gm |= take
            arr, fm = grown, gm
        # per-pixel painted patterns (stripes, spots...): every texel finds its 3D spot on the body
        if paints:
            pa = me.attributes["paint"].data
            co = np.array([(-v.co.x, v.co.z, v.co.y) for v in me.vertices])   # game coords
            for poly in me.polygons:
                pi = pa[poly.index].value
                if pi == 0:
                    continue
                col, maskfn = paints[pi - 1]
                lis = list(poly.loop_indices)
                for tri in range(1, len(lis) - 1):
                    ids = (lis[0], lis[tri], lis[tri + 1])
                    uvp = np.array([(uv[i].uv[0] * size, (1 - uv[i].uv[1]) * size) for i in ids])
                    p3 = co[[me.loops[i].vertex_index for i in ids]]
                    x0, y0 = np.floor(uvp.min(0)).astype(int) - 1
                    x1, y1 = np.ceil(uvp.max(0)).astype(int) + 1
                    x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, size - 1), min(y1, size - 1)
                    if x1 <= x0 or y1 <= y0:
                        continue
                    gy, gx = np.mgrid[y0:y1 + 1, x0:x1 + 1]
                    (ax, ay), (bx, by), (cx, cy) = uvp
                    den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
                    if abs(den) < 1e-9:
                        continue
                    l1 = ((by - cy) * (gx + 0.5 - cx) + (cx - bx) * (gy + 0.5 - cy)) / den
                    l2 = ((cy - ay) * (gx + 0.5 - cx) + (ax - cx) * (gy + 0.5 - cy)) / den
                    l3 = 1 - l1 - l2
                    inside = (l1 >= -0.02) & (l2 >= -0.02) & (l3 >= -0.02)
                    if not inside.any():
                        continue
                    X = l1 * p3[0, 0] + l2 * p3[1, 0] + l3 * p3[2, 0]
                    Y = l1 * p3[0, 1] + l2 * p3[1, 1] + l3 * p3[2, 1]
                    Z = l1 * p3[0, 2] + l2 * p3[1, 2] + l3 * p3[2, 2]
                    m2 = inside & maskfn(X, Y, Z)
                    if m2.any():
                        shade = arr[gy[m2], gx[m2]].astype(np.float32) / (np.array(palette[cols[poly.index].value]) * 255 + 1e-3)
                        shade = np.clip(shade.mean(-1, keepdims=True), 0.7, 1.3)
                        arr[gy[m2], gx[m2]] = np.clip(np.array(col) * 255 * shade, 0, 255).astype(np.int32)
        # stud pattern evaluated in 3D (world units) per texel, so every stud is the same size whatever the UV
        # layout does. Each face projects onto the two axes most parallel to it.
        ppu = math.sqrt(uv_area * size * size / max(world_area, 1e-6))
        print("STUDTILE", round(self.stud * ppu, 1), "px", "cover", round(uv_area, 3))
        studs = np.ones((size, size), np.float32)
        co = np.array([(-v.co.x, v.co.z, v.co.y) for v in me.vertices])   # game coords
        m = 0.16
        k_ = getattr(self, "stud_k", 1.0)

        def pattern(Ua, Va):
            u = Ua - np.floor(Ua); v = Va - np.floor(Va)
            inner = (u > m) & (u < 1 - m) & (v > m) & (v < 1 - m)
            cu, cv = (u - 0.5) / (0.5 - m), (v - 0.5) / (0.5 - m)
            mx = np.maximum(np.abs(cu), np.abs(cv))
            edge = inner & (mx > 0.72)
            out = np.ones_like(u)
            out[inner] = 1.03
            out[edge & (((cu < 0) & (np.abs(cu) >= np.abs(cv))) | ((cv > 0) & (np.abs(cv) >= np.abs(cu))))] = 1.14
            out[edge & (((cu > 0) & (np.abs(cu) >= np.abs(cv))) | ((cv < 0) & (np.abs(cv) >= np.abs(cu))))] = 0.8
            out[(u < 0.05) | (v < 0.05)] = 0.94
            return 1 + (out - 1) * k_
        for poly in me.polygons:
            if not (flags[poly.index].value & 1):
                continue
            nb = poly.normal
            ng = (abs(nb.x), abs(nb.z), abs(nb.y))          # game |x|,|y|,|z|
            ax = (2, 1) if ng[0] >= max(ng[1], ng[2]) else ((0, 2) if ng[1] >= ng[2] else (0, 1))
            lis = list(poly.loop_indices)
            for tri in range(1, len(lis) - 1):
                ids = (lis[0], lis[tri], lis[tri + 1])
                uvp = np.array([(uv[i].uv[0] * size, (1 - uv[i].uv[1]) * size) for i in ids])
                p3 = co[[me.loops[i].vertex_index for i in ids]]
                x0, y0 = np.floor(uvp.min(0)).astype(int) - 1
                x1, y1 = np.ceil(uvp.max(0)).astype(int) + 1
                x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, size - 1), min(y1, size - 1)
                if x1 <= x0 or y1 <= y0:
                    continue
                gy, gx = np.mgrid[y0:y1 + 1, x0:x1 + 1]
                (ax_, ay_), (bx_, by_), (cx_, cy_) = uvp
                den = (by_ - cy_) * (ax_ - cx_) + (cx_ - bx_) * (ay_ - cy_)
                if abs(den) < 1e-9:
                    continue
                l1 = ((by_ - cy_) * (gx + 0.5 - cx_) + (cx_ - bx_) * (gy + 0.5 - cy_)) / den
                l2 = ((cy_ - ay_) * (gx + 0.5 - cx_) + (ax_ - cx_) * (gy + 0.5 - cy_)) / den
                l3 = 1 - l1 - l2
                inside = (l1 >= -0.08) & (l2 >= -0.08) & (l3 >= -0.08)
                if not inside.any():
                    continue
                A = l1 * p3[0, ax[0]] + l2 * p3[1, ax[0]] + l3 * p3[2, ax[0]]
                Bv = l1 * p3[0, ax[1]] + l2 * p3[1, ax[1]] + l3 * p3[2, ax[1]]
                pat = pattern(A[inside] / self.stud, Bv[inside] / self.stud)
                studs[gy[inside], gx[inside]] = pat
        f = studs[..., None]
        return Image.fromarray(np.clip(arr * f, 0, 255).astype(np.uint8))

    def variant_texture(self, outdir, vname, vmap):
        """palette-swapped copy of the texture on the SAME mesh + UVs: <Name>_Tex_<vname>.png.
        vmap = {old colour: new colour}; colours not in the map stay as they are."""
        pal = [tuple(vmap.get(c, c)) for c in self.palette]
        pts = [(tuple(vmap.get(tuple(c), c)), m) for c, m in self.paints]
        path = os.path.join(outdir, "%s_Tex_%s.png" % (self.name, vname))
        self._paint(pal, pts).save(path)
        return path

    # ---------------------------------------------------------------- animation
    def animate(self, clips):
        """clips = {"Idle": (frames, seconds, fn), ...} where fn(t01) returns
        {bone: (rx, ry, rz) degrees in game axes (local, applied around the bone head) or (rot, (dx,dy,dz))}"""
        arm = self.arm
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode="POSE")
        self.anim_data = {}
        rest = {b.name: b.matrix_local.copy() for b in arm.data.bones}
        rest = {n: rest[self.bn(n)] for n, *_r in self.bones}
        for clip, (frames, seconds, fn) in clips.items():
            data = []
            for fi in range(frames):
                t = fi / frames
                pose = fn(t)
                # reset
                for pb in arm.pose.bones:
                    pb.matrix_basis = Matrix.Identity(4)
                bpy.context.view_layer.update()
                # apply top-down: rotation around the bone head in WORLD(armature) axes, given in game axes
                order = [n for n, *_r in self.bones]
                for name in order:
                    if name not in pose:
                        continue
                    val = pose[name]
                    rot, off = (val, (0, 0, 0)) if len(val) == 3 and not isinstance(val[0], tuple) else val
                    pb = arm.pose.bones[self.bn(name)]
                    R = euler(*rot).to_4x4()   # game-axis rotation -> blender
                    cur = pb.matrix.copy()                          # armature-space current matrix
                    head = cur.to_translation()
                    M = Matrix.Translation(head + P(*off)) @ R @ Matrix.Translation(-head) @ cur
                    pb.matrix = M
                    bpy.context.view_layer.update()
                frame = {}
                for name in order:
                    pb = arm.pose.bones[self.bn(name)]
                    delta = pb.matrix @ rest[name].inverted()       # armature-space delta (rest -> posed)
                    # convert to game axes: Dg = G^-1 * delta * G
                    Dg = G.to_4x4() @ delta @ G.to_4x4()
                    q = Dg.to_quaternion()
                    tr = Dg.to_translation()
                    frame[name] = [round(q.w, 4), round(q.x, 4), round(q.y, 4), round(q.z, 4), round(tr.x, 3), round(tr.y, 3), round(tr.z, 3)]
                data.append(frame)
            self.anim_data[clip] = {"fps": round(frames / seconds, 3), "frames": data}
        for pb in arm.pose.bones:
            pb.matrix_basis = Matrix.Identity(4)
        bpy.ops.object.mode_set(mode="OBJECT")

    def pose_at(self, clip, fi):
        """apply a recorded frame to the blender rig (for preview renders)"""
        arm = self.arm
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode="POSE")
        rest = {b.name: b.matrix_local.copy() for b in arm.data.bones}
        rest = {n: rest[self.bn(n)] for n, *_r in self.bones}
        for name, *_r in self.bones:
            w, x, y, z, tx, ty, tz = self.anim_data[clip]["frames"][fi][name]
            Dg = Matrix.Translation((tx, ty, tz)) @ Quaternion((w, x, y, z)).to_matrix().to_4x4()
            delta = G.to_4x4() @ Dg @ G.to_4x4()
            arm.pose.bones[self.bn(name)].matrix = delta @ rest[name]
            bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode="OBJECT")

    # ---------------------------------------------------------------- output
    def render(self, path, angle=30, elev=15, res=800, samples=20, dist=1.35):
        scn = bpy.context.scene
        scn.render.engine = "CYCLES"; scn.cycles.device = "CPU"; scn.cycles.samples = samples
        scn.cycles.use_denoising = True
        scn.render.resolution_x = scn.render.resolution_y = res
        if not scn.world:
            scn.world = bpy.data.worlds.new("W")
        scn.world.use_nodes = True
        bg = scn.world.node_tree.nodes["Background"]
        bg.inputs["Color"].default_value = (0.6, 0.78, 0.95, 1); bg.inputs["Strength"].default_value = 0.9
        mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3)
        dg = bpy.context.evaluated_depsgraph_get()
        for ob in self.mesh_objs.values():
            ev = ob.evaluated_get(dg)
            for v in ev.to_mesh().vertices:
                w = ob.matrix_world @ v.co
                mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
            ev.to_mesh_clear()
        ctr = (mn + mx) / 2; size = (mx - mn).length
        if "Sun" not in bpy.data.objects:
            sun = bpy.data.lights.new("Sun", "SUN"); sun.energy = 2.6; sun.angle = math.radians(10)
            so = bpy.data.objects.new("Sun", sun); scn.collection.objects.link(so)
            so.rotation_euler = (math.radians(45), math.radians(15), math.radians(-30))
            bpy.ops.mesh.primitive_plane_add(size=300, location=(ctr.x, ctr.y, 0))
            g = bpy.context.active_object; g.name = "Ground"
            gmat = bpy.data.materials.new("Gr"); gmat.use_nodes = True
            gmat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.3, 0.65, 0.22, 1)
            g.data.materials.append(gmat)
        cam = bpy.data.objects.get("Cam")
        if not cam:
            cd = bpy.data.cameras.new("Cam"); cd.lens = 50
            cam = bpy.data.objects.new("Cam", cd); scn.collection.objects.link(cam)
        scn.camera = cam
        a, e = math.radians(angle), math.radians(elev)
        d = size * dist
        cam.location = ctr + Vector((math.sin(a) * math.cos(e) * d, -math.cos(a) * math.cos(e) * d, math.sin(e) * d))
        cam.rotation_euler = (ctr - cam.location).to_track_quat("-Z", "Y").to_euler()
        scn.render.filepath = path
        bpy.ops.render.render(write_still=True)

    def export(self, outdir, scale_info=True):
        fbx = os.path.join(outdir, self.name + ".fbx")
        bpy.ops.object.select_all(action="DESELECT")
        self.arm.select_set(True)
        for ob in self.mesh_objs.values():
            ob.select_set(True)
        bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={"ARMATURE", "MESH"},
                                 path_mode="COPY", embed_textures=True, axis_forward="-Z", axis_up="Y",
                                 add_leaf_bones=False, bake_anim=False, use_armature_deform_only=False,
                                 mesh_smooth_type="FACE", apply_scale_options="FBX_SCALE_ALL")
        info = {"name": self.name, "height": self.height,
                "bones": [{"name": n, "parent": p, "head": [round(c, 3) for c in (-h.x, h.z, h.y)]} for n, h, t, p in self.bones],
                "glow": {self.name + "_" + g: g[5:] for g in self.mesh_objs if g.startswith("Glow_")},
                "body": self.name + "_Body",
                "anims": getattr(self, "anim_data", {}), "extra": self.extra}
        with open(os.path.join(outdir, self.name + "_data.json"), "w") as f:
            json.dump(info, f, separators=(",", ":"))
        return fbx

