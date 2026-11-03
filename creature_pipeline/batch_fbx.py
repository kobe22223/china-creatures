"""Merge single-creature FBXs into one FBX per batch (creatures side by side, 30 studs apart)."""
import bpy, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BATCHES = {
    "Batch1_Divine": ["seraphlion", "sugarwing", "abysswhale", "tidetiger"],
    "Batch2_Cosmic": ["nebulastag", "starowl", "cometwolf", "lunarmoth"],
    "Batch3_Secret": ["pumpkinwarlock", "voidkraken", "glitchgolem", "shadowdrake"],
    "Batch4_NewDivine": ["sunfirephoenix", "gumdrophydra", "coralleviathan", "halogriffin"],
    "Batch5_NewCosmic": ["nebulafox", "crystalunicorn", "galaxymanta", "prismdragon"],
    "Batch6_NewSecret": ["bonewyvern", "abyssangler", "hollowsteed", "thornbehemoth"],
    "Batch7_Cute1": ["aurorakirin", "marshbear", "pearlturtle", "moonbunny"],
    "Batch8_Cute2": ["saturnpig", "starhamster", "hextoad", "grimrhino"],
    "Batch9_Cute3": ["scorpionking", "phantomgorilla", "chocomammoth", "bubbleseal"],
    "Batch10_Royal": ["apeking", "lionemperor", "dragonoverlord", "crocpharaoh"],
    "Batch11_Armoured": ["sentinelraptor", "ironwarwolf", "siegerhino", "mechscorpion"],
    "Batch12_Elemental": ["frostyeti", "voidqilin", "infernohound", "stormbull"],
    "Batch13_Dino1": ["tyrantrex", "razorraptor", "spinosaurus", "parasaur"],
    "Batch14_Dino2": ["triceratops", "stegosaurus", "ankylosaurus", "brachiosaurus", "stormptero"],
}
only = [a for a in sys.argv[1:] if a.startswith("Batch")]
if only:
    BATCHES = {k: v for k, v in BATCHES.items() if k in only}
outdir = os.path.join(HERE, "out", "batches")
os.makedirs(outdir, exist_ok=True)
for bname, ids in BATCHES.items():
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

