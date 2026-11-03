"""Merge single-creature FBXs into one FBX per batch (creatures side by side, 30 studs apart)."""
import bpy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BATCHES = {
    "China01_Z1": ["luckypiglet", "paddyduckling", "riceroster", "buffalocalf"],
    "China02_Z1G2": ["giantwaterbuffalo", "bamboorat", "goldenpheasant", "redpanda"],
    "China03_Z2G3": ["babypanda", "giantpanda", "mandarinduck", "silkiechicken"],
    "China04_Z3G4": ["muntjacdeer", "pangolin", "southchinatiger", "goldeneagle"],
    "China05_Z4": ["steppewolf", "bactriancamel", "ferghanahorse", "stoneguardianlion"],
    "China06_Z5": ["fishingcormorant", "softshellturtle", "koicarp", "riverdolphin"],
    "China07_Z5G6": ["giantsalamander", "moneytoad", "luckybat", "jaderabbit"],
    "China08_Z6G7": ["liondancecub", "liondancelion", "terracottahound", "jadecicada"],
    "China09_Z7G8": ["bronzeox", "terracottahorse", "terracottageneral", "pekingese"],
    "China10_Z8": ["chiwen", "xiezhi", "bixi", "pixiu"],
    "China11_Z9": ["immortalcrane", "whitedeer", "baize", "ninetailedfox"],
    "China12_Z9G10": ["qilin", "shrimpsoldier", "crabgeneral", "kunfish"],
    "China13_Z10G11": ["pearldragon", "dragonking", "blacktortoise", "whitetiger"],
    "China14_Z11": ["vermilionbird", "fenghuang", "peng", "azuredragon"],
    "China15_Special": ["nian", "goldenemperordragon"],
}
only = [a for a in sys.argv[1:] if a.startswith(("Batch", "China"))]
if only:
    BATCHES = {k: v for k, v in BATCHES.items() if k in only}
outdir = os.path.join(HERE, "out", "batches")
os.makedirs(outdir, exist_ok=True)
def built(cid):
    d = os.path.join(HERE, "out", cid)
    return os.path.isdir(d) and any(f.endswith(".fbx") for f in os.listdir(d))
for bname, ids in BATCHES.items():
    if not all(built(i) for i in ids):
        print("SKIP", bname, "(not built yet:", [i for i in ids if not built(i)], ")")
        continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for i, cid in enumerate(ids):
        d = os.path.join(HERE, "out", cid)
        fbx = [f for f in os.listdir(d) if f.endswith(".fbx")][0]
        before = set(bpy.data.objects)
        bpy.ops.import_scene.fbx(filepath=os.path.join(d, fbx), use_image_search=True)
        new = [o for o in bpy.data.objects if o not in before]
        for o in new:
            if o.parent is None:
                o.location.x += -i * 30.0   # blender -X = game +X
    bpy.ops.file.pack_all()
    path = os.path.join(outdir, bname + ".fbx")
    bpy.ops.export_scene.fbx(filepath=path, use_selection=False, object_types={"ARMATURE", "MESH"},
                             path_mode="COPY", embed_textures=True, axis_forward="-Z", axis_up="Y",
                             add_leaf_bones=False, bake_anim=False, mesh_smooth_type="FACE", apply_scale_options="FBX_SCALE_ALL")
    print("BATCH", bname, os.path.getsize(path))

