"""Build the China voxel eggs, render contact sheets, and (with --export) write out/eggs/EggsChina.fbx + layout.json.

python3 make_eggs.py [zones...] [--export]      e.g.  python3 make_eggs.py 1 2      or      python3 make_eggs.py --export
Per zone it renders one sheet (out/eggs/sheets/zone_Zxx.png): the 3 eggs side by side at 30 degrees, from the top,
and as a flat single-colour preview (what a Golden / Diamond / Rainbow mutation recolour will look like).
"""
import sys, os, json, math, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
from PIL import Image, ImageDraw, ImageFont
from voxel import VOX
import mesher, china

OUT = os.path.join(HERE, "..", "out", "eggs")
SHEETS = os.path.join(OUT, "sheets")
os.makedirs(SHEETS, exist_ok=True)
BUDGET = {"Egg": 3000, "BigEgg": 5000, "GiantEgg": 8000}
MAXRUN = {"Egg": 3, "BigEgg": 3, "GiantEgg": 3}
ATLAS_PNG = os.path.join(OUT, "EggsChina_Atlas.png")
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)


def gp(p):
    """game (x, y, z) studs -> blender"""
    return (-p[0], p[2], p[1])


def make_objects(egg, atlas_img, maxrun):
    (verts, quads, uvs), glow, tris = mesher.build(egg, ATLAS, maxrun)
    objs = []
    me = bpy.data.meshes.new(egg.name + "_Body")
    me.from_pydata([gp(v) for v in verts], [], quads)
    uvl = me.uv_layers.new(name="UV")
    li = 0
    for poly, quv in zip(me.polygons, uvs):
        for k, loop in enumerate(poly.loop_indices):
            uvl.data[loop].uv = quv[k]
    me.validate()
    ob = bpy.data.objects.new(egg.name + "_Body", me)
    ob.data.materials.append(body_mat(atlas_img))
    bpy.context.scene.collection.objects.link(ob)
    objs.append(ob)
    for col, (gv, gq) in glow.items():
        nm = egg.name + "_Glow_%02x%02x%02x" % col
        gme = bpy.data.meshes.new(nm)
        gme.from_pydata([gp(v) for v in gv], [], gq)
        gme.validate()
        g = bpy.data.objects.new(nm, gme)
        g.data.materials.append(glow_mat(col))
        bpy.context.scene.collection.objects.link(g)
        objs.append(g)
    return objs, tris


_mats = {}


def body_mat(img):
    if "body" not in _mats:
        m = bpy.data.materials.new("EggsChina_Atlas")
        m.use_nodes = True
        nt = m.node_tree
        b = nt.nodes["Principled BSDF"]
        b.inputs["Roughness"].default_value = 0.55
        tn = nt.nodes.new("ShaderNodeTexImage")
        tn.image = img
        tn.interpolation = "Closest"
        nt.links.new(tn.outputs["Color"], b.inputs["Base Color"])
        _mats["body"] = m
    return _mats["body"]


def glow_mat(col):
    key = ("glow", col)
    if key not in _mats:
        m = bpy.data.materials.new("Glow_%02x%02x%02x" % col)
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        rgb = tuple(c / 255 for c in col) + (1,)
        b.inputs["Base Color"].default_value = rgb
        b.inputs["Emission Color"].default_value = rgb
        b.inputs["Emission Strength"].default_value = 1.2
        _mats[key] = m
    return _mats[key]


def flat_mat():
    if "flat" not in _mats:
        m = bpy.data.materials.new("Flat")
        m.use_nodes = True
        m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.85, 0.68, 0.25, 1)
        _mats["flat"] = m
    return _mats["flat"]


def setup_scene():
    scn = bpy.context.scene
    scn.render.engine = "CYCLES"
    scn.cycles.device = "CPU"
    scn.cycles.samples = 24
    scn.cycles.use_denoising = True
    scn.render.resolution_x, scn.render.resolution_y = 1200, 560
    scn.world = bpy.data.worlds.new("W")
    scn.world.use_nodes = True
    bg = scn.world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.05, 0.06, 0.09, 1)
    bg.inputs["Strength"].default_value = 1.0
    sun = bpy.data.lights.new("Sun", "SUN"); sun.energy = 3.2; sun.angle = math.radians(12)
    so = bpy.data.objects.new("Sun", sun); scn.collection.objects.link(so)
    so.rotation_euler = (math.radians(40), math.radians(10), math.radians(-35))
    fill = bpy.data.lights.new("Fill", "SUN"); fill.energy = 1.0
    fo = bpy.data.objects.new("Fill", fill); scn.collection.objects.link(fo)
    fo.rotation_euler = (math.radians(60), 0, math.radians(150))
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0))
    g = bpy.context.active_object
    gm = bpy.data.materials.new("Ground"); gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.09, 0.1, 0.14, 1)
    g.data.materials.append(gm)
    cd = bpy.data.cameras.new("Cam"); cd.lens = 50
    cam = bpy.data.objects.new("Cam", cd); scn.collection.objects.link(cam); scn.camera = cam
    return scn, cam


def shoot(scn, cam, centre, dist, angle, elev, path, ortho=None):
    a, e = math.radians(angle), math.radians(elev)
    c = Vector(centre)
    if ortho:
        cam.data.type = "ORTHO"; cam.data.ortho_scale = ortho
    else:
        cam.data.type = "PERSP"
    cam.location = c + Vector((math.sin(a) * math.cos(e) * dist, -math.cos(a) * math.cos(e) * dist, math.sin(e) * dist))
    cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    scn.render.filepath = path
    bpy.ops.render.render(write_still=True)


def label(img, text, xy, col=(235, 235, 240)):
    ImageDraw.Draw(img).text(xy, text, fill=col, font=FONT)


# ------------------------------------------------------------------ main
args = [a for a in sys.argv[1:] if not a.startswith("--")]
zones = [int(a) for a in args] or sorted(china.ZONES)
export = "--export" in sys.argv

# 1) voxels for every requested zone (and every zone when exporting, so the shared atlas is complete)
eggs = {}
for z in (sorted(china.ZONES) if export else zones):
    eggs[z] = china.ZONES[z]()
    print("VOXELS zone", z, [(e.kind, len(e.body), len(e.glow)) for e in eggs[z]], flush=True)

# 2) shared atlas over every colour used by every zone in china.ZONES (built once, cached by colour list)
ATLAS = mesher.Atlas()
for z in sorted(eggs):
    for e in eggs[z]:
        for col in e.body.values():
            ATLAS.add(col)
if not export:      # previews get their own atlas file so parallel runs don't overwrite each other
    ATLAS_PNG = os.path.join(SHEETS, "_atlas_%s.png" % "_".join(map(str, zones)))
ATLAS.image(ATLAS_PNG)
print("ATLAS colours", len(ATLAS.cols), flush=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scn, cam = setup_scene()
img = bpy.data.images.load(ATLAS_PNG)
report = {}
layout = {}
giants = []
x_export = 0
for z in sorted(eggs):
    row = []
    for e in eggs[z]:
        objs, tris = make_objects(e, img, MAXRUN[e.kind])
        ok = tris <= BUDGET[e.kind]
        report[e.name] = {"tris": tris, "budget": BUDGET[e.kind], "ok": ok, "glow": [o.name for o in objs[1:]]}
        print("MESH", e.name, tris, "tris", "OK" if ok else "OVER BUDGET", [o.name for o in objs], flush=True)
        row.append((e, objs, tris))
    if z in zones:
        # contact sheet: the three eggs side by side (Egg, BigEgg, GiantEgg), 30 deg + top + flat colour
        xs = [-5.8, -0.9, 5.4]                      # blender x: Egg left, GiantEgg right
        for (e, objs, _), x in zip(row, xs):
            for o in objs:
                o.location = (x, 0, 0)
        tmp = os.path.join(SHEETS, "_tmp_%02d_" % z)
        bpy.context.view_layer.update()
        zs = [(o.matrix_world @ v.co).z for e, objs, _ in row for o in objs for v in o.data.vertices]
        xsz = [(o.matrix_world @ v.co).x for e, objs, _ in row for o in objs for v in o.data.vertices]
        top, xl, xr = max(zs), min(xsz), max(xsz)
        cz = top * 0.5
        dist = max(top * 3.3, (xr - xl) * 1.45) + 3
        cxm = (xl + xr) / 2
        shoot(scn, cam, (cxm, 0, cz), dist, 25, 12, tmp + "a.png")
        shoot(scn, cam, (cxm, 0, 2.0), 30, 0, 89, tmp + "b.png", ortho=(xr - xl) + 3)
        saved = {}
        for e, objs, _ in row:
            saved[objs[0].name] = objs[0].data.materials[0]
            objs[0].data.materials[0] = flat_mat()
            for g in objs[1:]:
                saved[g.name] = g.data.materials[0]
                g.data.materials[0] = flat_mat()
        shoot(scn, cam, (cxm, 0, cz), dist, 25, 12, tmp + "c.png")
        for e, objs, _ in row:
            for o in objs:
                o.data.materials[0] = saved[o.name]
        # close-up of the GiantEgg
        gx = xs[2]
        gz = [(o.matrix_world @ v.co).z for o in row[2][1] for v in o.data.vertices]
        shoot(scn, cam, (gx, 0, max(gz) * 0.5), max(gz) * 3.4 + 2, 25, 10, tmp + "d.png")
        S = Image.new("RGB", (1200, 560 * 4 + 60), (14, 15, 20))
        for i, s in enumerate("abcd"):
            S.paste(Image.open(tmp + s + ".png"), (0, 60 + i * 560))
            os.remove(tmp + s + ".png")
        txt = "Zone %02d    " % z + "    ".join("%s %d/%d tris" % (e.kind, t, BUDGET[e.kind]) for e, _, t in row)
        label(S, txt, (16, 16), (255, 120, 120) if any(t > BUDGET[e.kind] for e, _, t in row) else (235, 235, 240))
        label(S, "30 deg", (16, 70)); label(S, "top", (16, 630)); label(S, "flat colour (mutation recolour)", (16, 1190)); label(S, "GiantEgg close-up", (16, 1750))
        S.save(os.path.join(SHEETS, "zone_Z%02d.png" % z))
        print("SHEET", z, flush=True)
    # move this zone out of the way (or into its export slot)
    for e, objs, _ in row:
        for o in objs:
            o.location = (-x_export * VOX * 0 - x_export, 0, 0) if export else (1000, 0, 0)
        if export:
            layout[e.name] = {"x": x_export, "height": e.H}
            x_export += 10
        giants.append((z, e, objs)) if e.kind == "GiantEgg" else None

json.dump(report, open(os.path.join(OUT, "report.json"), "w"), indent=1)

if export:
    for o in [o for o in bpy.data.objects if o.type != "MESH" or not o.name.startswith("China_")]:
        o.select_set(False)
    bpy.ops.object.select_all(action="DESELECT")
    for o in bpy.data.objects:
        if o.type == "MESH" and o.name.startswith("China_"):
            o.select_set(True)
    img.pack()
    path = os.path.join(OUT, "EggsChina.fbx")
    bpy.ops.export_scene.fbx(filepath=path, use_selection=True, object_types={"MESH"}, path_mode="COPY", embed_textures=True,
                             axis_forward="-Z", axis_up="Y", mesh_smooth_type="FACE", apply_scale_options="FBX_SCALE_ALL")
    json.dump(layout, open(os.path.join(OUT, "layout.json"), "w"), indent=1)
    print("FBX", path, os.path.getsize(path))
