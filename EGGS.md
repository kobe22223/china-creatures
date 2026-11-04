# Steal an Egg in China: voxel egg handoff

33 blocky voxel eggs (11 zones x Egg / BigEgg / GiantEgg) to replace the part-built eggs in `Models.Egg`.

## Files
- `creature_pipeline/out/eggs/EggsChina.fbx`: all 33 eggs, meshes only, one shared 1024 px atlas embedded.
- `creature_pipeline/out/eggs/layout.json`: x position (studs) and nominal height of every egg.
- `creature_pipeline/out/eggs/sheets/`: one contact sheet per zone (`zone_Z01.png` ... `zone_Z11.png`) and `ALL_GiantEggs.png`.
- `creature_pipeline/eggs/`: `voxel.py` (the voxel egg tool), `mesher.py` (face culling, capped greedy merge, atlas), `china.py` (the 33 designs), `make_eggs.py` (build, sheets, export).

## Layout and naming
- Order: Z01 Egg, Z01 BigEgg, Z01 GiantEgg, Z02 Egg ... Z11 GiantEgg, 10 studs apart along +x starting at x = 0.
- Origin = bottom centre of each egg. Game coords: x right, y up, front (main design) = -z.
- Mesh names: `China_Z<zone>_<Kind>_Body` and `China_Z<zone>_<Kind>_Glow_<rrggbb>` (Studio makes Glow meshes Neon with that colour).
- Egg bodies are 3.2 / 4.4 / 6.0 studs tall. Features on top (hats, roofs, flags, stalks, crests) make some BigEggs and GiantEggs taller overall: up to 5.0 (BigEgg) and 9.0 (GiantEgg, the bamboo stalks).
- Triangles: Eggs 888 to 1,166 (budget 3k), BigEggs 2,010 to 2,794 (5k), GiantEggs 3,958 to 5,464 (8k).

## Import (Kobe)
1. Open the **Steal an Egg in China** place in Studio.
2. **File > Import 3D**, pick `EggsChina.fbx`, import into **Workspace**, keep the file name, leave Rig Type as it is.
3. Ask the Studio chat to split it into `ReplicatedStorage.EggAssets` (re-centre each egg at its own origin using `layout.json`), turn the Glow meshes Neon, and map the eggs per zone in Config (Egg / BigEgg / GiantEgg). Mutations (Golden, Diamond, Rainbow) can clear the TextureID and recolour the mesh as before.
