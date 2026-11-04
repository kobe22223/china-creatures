"""python3 make_tm.py china<N> [--render]
Builds one treadmill tier from treadmills/china<N>.py, checks the brief's hard rules, renders a 3-view sheet and
exports the meshes only (no armature) to out/treadmills/china<N>/China<N>.fbx."""
import sys, os, importlib, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "treadmills"))
import bpy
from PIL import Image, ImageDraw, ImageFont

tid = sys.argv[1]
mod = importlib.import_module(tid)
out = os.path.join(HERE, "out", "treadmills", tid)
c = mod.build()
c.build(out)

# ---------------------------------------------------------------- checks (game coords: x = -bx, y = bz, z = by)
problems = []
allv = [(-v.co.x, v.co.z, v.co.y) for sh in c.shapes for v in sh["bm"].verts]
xs, ys, zs = zip(*allv)
size = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
if size[0] > 10.01: problems.append("too wide %.2f" % size[0])
if size[2] > 25.01: problems.append("too long %.2f" % size[2])
if max(ys) > 17.01: problems.append("too tall %.2f" % max(ys))
air = [v for v in allv if abs(v[0]) < 2.7 and -6 < v[2] < 10 and v[1] > 3.0]
if air: problems.append("%d verts above y=3 over the deck (max y %.2f)" % (len(air), max(v[1] for v in air)))
deck_top = [v for v in allv if abs(v[0]) < 2.5 and -8.5 < v[2] < 9.5 and 1.0 < v[1] < 3.0]   # running area
if deck_top and max(v[1] for v in deck_top) > 1.2001:
    problems.append("something sticks up out of the belt (max y %.3f)" % max(v[1] for v in deck_top))
tris = sum(len(p.vertices) - 2 for ob in c.mesh_objs.values() for p in ob.data.polygons)
if "--tris" in sys.argv:
    import collections
    cnt = collections.Counter()
    for sh in c.shapes:
        cnt[len(sh["bm"].verts)] += sum(len(f.verts) - 2 for f in sh["bm"].faces)
    print("SHAPES", len(c.shapes), "heaviest vert-counts", cnt.most_common(8))
glows = [g for g in c.mesh_objs if g.startswith("Glow_")]
if tris > 10000: problems.append("tris %d > 10000" % tris)
if len(glows) > 4: problems.append("%d glow meshes > 4" % len(glows))
names = [ob.name for ob in c.mesh_objs.values()]
if any(not n.startswith(c.name + "_") for n in names): problems.append("bad mesh names %s" % names)
report = dict(name=c.name, size=[round(s, 2) for s in size], top=round(max(ys), 2), tris=tris, meshes=names, problems=problems)
json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1)
print("REPORT", json.dumps(report))

# ---------------------------------------------------------------- renders + 3-view sheet
if "--render" in sys.argv:
    views = [(30, 18, "front"), (150, 18, "back"), (0, 80, "top")]
    for ang, el, nm in views:
        c.render(os.path.join(out, "%s_%s.png" % (c.name, nm)), angle=ang, elev=el, res=700, dist=1.15)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except OSError:
        font = ImageFont.load_default()
    S = Image.new("RGB", (2100, 760), "white")
    for i, (_, _, nm) in enumerate(views):
        S.paste(Image.open(os.path.join(out, "%s_%s.png" % (c.name, nm))), (i * 700, 60))
    txt = "%s   %.1f x %.1f x %.1f studs   %d tris   %d glow   %s" % (c.name, size[0], size[2], max(ys), tris, len(glows), "OK" if not problems else "; ".join(problems))
    ImageDraw.Draw(S).text((14, 16), txt + "      front / back / top", fill=(0, 0, 0) if not problems else (200, 0, 0), font=font)
    os.makedirs(os.path.join(HERE, "out", "treadmills", "sheets"), exist_ok=True)
    S.save(os.path.join(HERE, "out", "treadmills", "sheets", tid + "_views.png"))

# ---------------------------------------------------------------- export meshes only (no armature)
for ob in c.mesh_objs.values():
    ob.modifiers.clear()
    ob.parent = None
    ob.vertex_groups.clear()
bpy.data.objects.remove(c.arm, do_unlink=True)
bpy.ops.object.select_all(action="DESELECT")
for ob in c.mesh_objs.values():
    ob.select_set(True)
fbx = os.path.join(out, c.name + ".fbx")
bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={"MESH"}, path_mode="COPY", embed_textures=True,
                         axis_forward="-Z", axis_up="Y", mesh_smooth_type="FACE", apply_scale_options="FBX_SCALE_ALL")
print("FBX", fbx)
