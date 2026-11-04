"""Merge the 10 tier FBXs into out/treadmills/TreadmillsChina.fbx (tier N at x = 30 * (N - 1) studs, meshes only)
and write out/treadmills/layout.json."""
import bpy, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "treadmills")
bpy.ops.wm.read_factory_settings(use_empty=True)
layout = {}
for n in range(1, 11):
    fbx = os.path.join(OUT, "china%d" % n, "China%d.fbx" % n)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=fbx, use_image_search=True)
    for o in [o for o in bpy.data.objects if o not in before]:
        if o.parent is None:
            o.location.x += -(n - 1) * 30.0          # blender -X = game +X
    layout["China%d" % n] = {"x": (n - 1) * 30}
bad = [o.name for o in bpy.data.objects if o.type != "MESH"]
assert not bad, bad
bpy.ops.file.pack_all()
path = os.path.join(OUT, "TreadmillsChina.fbx")
bpy.ops.export_scene.fbx(filepath=path, use_selection=False, object_types={"MESH"}, path_mode="COPY", embed_textures=True,
                         axis_forward="-Z", axis_up="Y", mesh_smooth_type="FACE", apply_scale_options="FBX_SCALE_ALL")
json.dump(layout, open(os.path.join(OUT, "layout.json"), "w"), indent=1)
print("MERGED", path, os.path.getsize(path), sorted(o.name for o in bpy.data.objects))
