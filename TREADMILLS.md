# Steal an Egg in China: treadmill handoff

10 sculpted Chinese treadmills, one per upgrade tier, to replace the part-built `ServerStorage.TreadmillSkins.China1..10`.

## Files
- `creature_pipeline/out/treadmills/TreadmillsChina.fbx`: all 10 tiers in one file, tier N at x = 30 x (N - 1) studs, meshes only (no rig), textures embedded (1024 px each).
- `creature_pipeline/out/treadmills/layout.json`: the x offset of each tier.
- `creature_pipeline/out/treadmills/sheets/`: `TreadmillsChina_contact.png` (all 10, front and back) and a front / back / top sheet per tier.
- `creature_pipeline/treadmills/china1.py ... china10.py`: the tier sources; `tm.py` holds the shared parts; `make_tm.py` builds and checks one tier; `merge_tm.py` builds the combined FBX.

## Checked on every tier (make_tm.py, and again on the merged FBX)
- Units are studs; origin is the centre of the belt on the ground; the console end is at -z.
- Belt deck: flat top, 20 long x 5.4 wide, top at y = 1.2, visible mesh (part of `China<N>_Body`).
- Nothing above y = 3 over the belt from z = -6 to z = +10. Roofs, arches, the moon gate and the halo only sit over the console end.
- Footprint at most 10 wide x 25 long x 17 tall; nothing below the ground.
- At most 10k triangles, 1 Body mesh + at most 4 Glow meshes, every mesh named `China<N>_...`.

| Tier | Name | Size W x L x H (studs) | Triangles | Glow meshes |
|---|---|---|---|---|
| China1 | Bamboo Mat | 9.8 x 23.5 x 7.7 | 9482 | none |
| China2 | Red Lacquer | 7.8 x 21.8 x 9.0 | 6468 | none |
| China3 | Jade | 8.4 x 22.4 x 9.8 | 6668 | `Glow_8cffbe` |
| China4 | Lantern | 9.9 x 21.6 x 11.0 | 8212 | `Glow_ffa03c` |
| China5 | Porcelain | 8.9 x 23.4 x 8.8 | 4136 | `Glow_aad7ff` |
| China6 | Golden Pagoda | 8.8 x 22.6 x 13.6 | 7836 | `Glow_ffd778`, `Glow_ff5032` |
| China7 | Dragon Scale | 8.2 x 24.7 x 9.9 | 7218 | `Glow_dcfff5`, `Glow_ffd232`, `Glow_fffadc` |
| China8 | Phoenix Fire | 9.3 x 24.1 x 11.1 | 7448 | `Glow_ff781e`, `Glow_fff5c8`, `Glow_ffe65a` |
| China9 | Moon Palace | 9.7 x 23.4 x 10.8 | 9876 | `Glow_fff5cd` |
| China10 | Heavenly Cloud | 9.7 x 24.8 x 11.9 | 9584 | `Glow_96d2ff`, `Glow_ffd75a`, `Glow_ffeb96` |

## Import (Kobe)
1. Download `creature_pipeline/out/treadmills/TreadmillsChina.fbx` from the branch `claude/pensive-noether-4m1inf` (or the zip of the branch).
2. In Studio: **File > Import 3D**, pick `TreadmillsChina.fbx`, import it into **Workspace**, keep the file name `TreadmillsChina`, leave Rig Type as it is.
3. Then ask the Studio chat to: split it into `ServerStorage.TreadmillSkins.China1..10` (use `layout.json` to re-centre each tier at x = 0), set `FrontSign = -1`, turn every `China<N>_Glow_<rrggbb>` mesh Neon with that colour, and add particles (fire on the Phoenix Fire tier, sparkles on the Heavenly Cloud tier).
