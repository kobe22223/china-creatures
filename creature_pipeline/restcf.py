"""rest CFrame of every bone in game space (relative to creature origin), matching Roblox import"""
import sys, os, importlib, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "creatures"))
import bpy
from mathutils import Matrix
from sculpt import G
def rest(cid):
    mod = importlib.import_module(cid); c = mod.build()
    # build only the armature (fast)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    ad = bpy.data.armatures.new("A"); arm = bpy.data.objects.new("A", ad); bpy.context.scene.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode="EDIT")
    for n, h, t, p in c.bones:
        eb = ad.edit_bones.new(n); eb.head, eb.tail = h, t; eb.roll = 0
    bpy.ops.object.mode_set(mode="OBJECT")
    out = []
    for n, h, t, p in c.bones:
        M = ad.bones[n].matrix_local
        R = G @ M.to_3x3()          # bone axes expressed in game coords
        pos = G @ M.to_translation()
        out.append((n, p, [round(v, 3) for v in pos], [[round(R[i][j], 4) for j in range(3)] for i in range(3)]))
    return c.name, out
if __name__ == "__main__":
    name, out = rest(sys.argv[1])
    for n, p, pos, R in out:
        # roblox XYZ euler from rotation matrix (R = Rx Ry Rz)
        ry = math.asin(max(-1, min(1, R[0][2])))
        rx = math.atan2(-R[1][2], R[2][2]); rz = math.atan2(-R[0][1], R[0][0])
        print(n, pos, [round(math.degrees(a)) for a in (rx, ry, rz)])

