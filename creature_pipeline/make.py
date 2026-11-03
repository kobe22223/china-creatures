"""python3 make.py <creature_module> [--render] [--export] [--walk]"""
import sys, os, importlib, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "creatures"))
mod = importlib.import_module(sys.argv[1])
out = os.path.join(HERE, "out", sys.argv[1])
c = mod.build()
c.build(out)
if hasattr(mod, "anims"):
    mod.anims(c)
tris = sum(len(p.vertices) - 2 for ob in c.mesh_objs.values() for p in ob.data.polygons)
def _prop(c):
    """rest-pose proportions: total height, legs (ground to bottom of the Hips/Chest body shapes), head span"""
    def ys(sel):
        v = [vv.co.z for sh in c.shapes if not sh["glow"] and sel(sh["bones"]) for vv in sh["bm"].verts]
        return (min(v), max(v)) if v else (0, 0)
    top = ys(lambda b: True)[1]
    body = ys(lambda b: set(b) <= {"Hips", "Chest"})
    head = ys(lambda b: set(b) <= {"Head", "Jaw"})
    return dict(height=top, legs=body[0] / top, head=(head[1] - head[0]) / top)
prop = _prop(c)
json.dump(prop, open(os.path.join(out, "proportions.json"), "w"))
print("PROP height %.2f legs %.0f%% head %.0f%%" % (prop["height"], prop["legs"] * 100, prop["head"] * 100))
if hasattr(mod, "VARIANTS"):
    for vname, vmap in mod.VARIANTS.items():
        vp = c.variant_texture(out, vname, vmap)
        os.makedirs(os.path.join(HERE, "out", "textures"), exist_ok=True)
        import shutil; shutil.copy(vp, os.path.join(HERE, "out", "textures", os.path.basename(vp)))
        print("VARIANT", vp)
print("TRIS", tris, {k: len(o.data.polygons) for k, o in c.mesh_objs.items()})
if "--render" in sys.argv:
    angs = [30, 150] if "--two" in sys.argv else [30]
    for a in angs:
        c.render(os.path.join(out, f"{c.name}_{a}.png"), angle=a)
if "--walk" in sys.argv:
    c.pose_at("Walk", 6)
    c.render(os.path.join(out, f"{c.name}_walk.png"), angle=70)
if "--render" in sys.argv and hasattr(mod, "VARIANTS"):
    # preview each palette swap on the same mesh (swap the image in the body material, render, swap back)
    import bpy
    mat = c.mesh_objs["Body"].data.materials[0]
    tn = [n for n in mat.node_tree.nodes if n.type == "TEX_IMAGE"][0]
    orig = tn.image
    for pb in c.arm.pose.bones:          # back to the rest pose after the walk frame
        pb.matrix_basis.identity()
    bpy.context.view_layer.update()
    for vname in mod.VARIANTS:
        tn.image = bpy.data.images.load(os.path.join(out, "%s_Tex_%s.png" % (c.name, vname)))
        c.render(os.path.join(out, "%s_var_%s.png" % (c.name, vname)), angle=30, res=600)
    tn.image = orig
if "--export" in sys.argv:
    print("FBX", c.export(out))

