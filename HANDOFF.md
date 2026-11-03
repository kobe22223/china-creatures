# Steal an Egg in China: creature handoff

All 58 creatures from the brief are sculpted, rigged, animated (Walk + Idle) and checked against Kobe's proportion rules.
Branch: `claude/pensive-noether-4m1inf`.

## What's in the repo
- `creature_pipeline/out/batches/*.fbx`: 15 batch FBX files (4 creatures each, the last one has 2). Creatures sit 30 studs apart along X, each with its own rig, textures embedded, bone names unique per creature (checked by re-importing every FBX: 58 rigs, no duplicate bones).
- `creature_pipeline/out/CreatureData.rbxmx`: one ModuleScript per creature (58), with the animation clips, bone rest CFrames, aura, rarity, speed, hover and batch layout.
- `creature_pipeline/out/textures/<Name>_Tex_<Variant>.png`: 58 palette-swapped textures, same mesh and UVs as the base, so the game can swap `TextureID`.
- `creature_pipeline/out/sheets/`: a front / back / walk sheet per creature (`<id>_views.png`), a base + variant contact sheet per batch (`<Batch>_contact.png`) and `ALL_China_roster.png` with every creature.
- `creature_pipeline/creatures/*.py`: the 58 creature sources. `creature_pipeline/cn.py` holds the China helpers (bird, swimmer, flyer, guardian quad, serpent dragon, dragon head, coin, knot, bell, lantern, panda / scale paint).

## Import order for Kobe
1. In Studio, open the 3D Importer and import the batch FBX files one at a time:
1. `creature_pipeline/out/batches/China01_Z1.fbx`: LuckyPiglet, PaddyDuckling, RiceRooster, BuffaloCalf
2. `creature_pipeline/out/batches/China02_Z1G2.fbx`: GiantWaterBuffalo, BambooRat, GoldenPheasant, RedPanda
3. `creature_pipeline/out/batches/China03_Z2G3.fbx`: BabyPanda, GiantPanda, MandarinDuck, SilkieChicken
4. `creature_pipeline/out/batches/China04_Z3G4.fbx`: MuntjacDeer, Pangolin, SouthChinaTiger, GoldenEagle
5. `creature_pipeline/out/batches/China05_Z4.fbx`: SteppeWolf, BactrianCamel, FerghanaHorse, StoneGuardianLion
6. `creature_pipeline/out/batches/China06_Z5.fbx`: FishingCormorant, SoftshellTurtle, KoiCarp, RiverDolphin
7. `creature_pipeline/out/batches/China07_Z5G6.fbx`: GiantSalamander, MoneyToad, LuckyBat, JadeRabbit
8. `creature_pipeline/out/batches/China08_Z6G7.fbx`: LionDanceCub, LionDanceLion, TerracottaHound, JadeCicada
9. `creature_pipeline/out/batches/China09_Z7G8.fbx`: BronzeOx, TerracottaHorse, TerracottaGeneral, Pekingese
10. `creature_pipeline/out/batches/China10_Z8.fbx`: Chiwen, Xiezhi, Bixi, Pixiu
11. `creature_pipeline/out/batches/China11_Z9.fbx`: ImmortalCrane, WhiteDeer, BaiZe, NineTailedFox
12. `creature_pipeline/out/batches/China12_Z9G10.fbx`: Qilin, ShrimpSoldier, CrabGeneral, KunFish
13. `creature_pipeline/out/batches/China13_Z10G11.fbx`: PearlDragon, DragonKing, BlackTortoise, WhiteTiger
14. `creature_pipeline/out/batches/China14_Z11.fbx`: VermilionBird, Fenghuang, Peng, AzureDragon
15. `creature_pipeline/out/batches/China15_Special.fbx`: Nian, GoldenEmperorDragon
2. Insert `creature_pipeline/out/CreatureData.rbxmx` (right-click > Insert from File).
3. Put both where `ServerStorage.CreatureRigBuilder` expects them. **The Studio chat must confirm the exact location from the CreatureRigBuilder source before you import** (the template doc, section 9 step 6, says to read its source first). This session has no Studio access, so it can't read it.
4. Run `ServerStorage.CreatureRigBuilder.Build()` to rebuild `ReplicatedStorage.CreatureMeshes`.
5. Upload the 58 variant PNGs from `creature_pipeline/out/textures/` with the Asset Manager, then give the Studio chat the image IDs so it can set up the variant pets.
6. Set `Mesh = "<Name>"` on each pet / guardian in `Config` (names below).

## Roster
| Zone | Mesh (Config `Mesh =`) | Rarity / aura | Speed | Hover | Batch FBX (slot) | Variant texture |
|---|---|---|---|---|---|---|
| 1 | `LuckyPiglet` | Common (sparkle) | 1.0 | no | China01_Z1 (1) | `LuckyPiglet_Tex_Jade.png` |
| 1 | `PaddyDuckling` | Uncommon (sparkle) | 1.0 | no | China01_Z1 (2) | `PaddyDuckling_Tex_Porcelain.png` |
| 1 | `RiceRooster` | Rare (sparkle) | 1.05 | no | China01_Z1 (3) | `RiceRooster_Tex_Golden.png` |
| 1 | `BuffaloCalf` | Epic (sparkle) | 0.95 | no | China01_Z1 (4) | `BuffaloCalf_Tex_Ink.png` |
| 1 guardian | `GiantWaterBuffalo` | Epic (sparkle) | 0.9 | no | China02_Z1G2 (1) | `GiantWaterBuffalo_Tex_Bronze.png` |
| 2 | `BambooRat` | Uncommon (sparkle) | 1.05 | no | China02_Z1G2 (2) | `BambooRat_Tex_Snow.png` |
| 2 | `GoldenPheasant` | Rare (sparkle) | 1.1 | no | China02_Z1G2 (3) | `GoldenPheasant_Tex_Silver.png` |
| 2 | `RedPanda` | Epic (sparkle) | 1.05 | no | China02_Z1G2 (4) | `RedPanda_Tex_Snowy.png` |
| 2 | `BabyPanda` | Legendary (sparkle) | 1.0 | no | China03_Z2G3 (1) | `BabyPanda_Tex_Golden.png` |
| 2 guardian | `GiantPanda` | Legendary (sparkle) | 0.95 | no | China03_Z2G3 (2) | `GiantPanda_Tex_Qinling.png` |
| 3 | `MandarinDuck` | Rare (sparkle) | 1.05 | no | China03_Z2G3 (3) | `MandarinDuck_Tex_Hen.png` |
| 3 | `SilkieChicken` | Epic (sparkle) | 1.0 | no | China03_Z2G3 (4) | `SilkieChicken_Tex_Ink.png` |
| 3 | `MuntjacDeer` | Legendary (sparkle) | 1.15 | no | China04_Z3G4 (1) | `MuntjacDeer_Tex_Silver.png` |
| 3 | `Pangolin` | Mythic (orbit) | 1.0 | no | China04_Z3G4 (2) | `Pangolin_Tex_Jade.png` |
| 3 guardian | `SouthChinaTiger` | Mythic (orbit) | 1.1 | no | China04_Z3G4 (3) | `SouthChinaTiger_Tex_White.png` |
| 4 | `GoldenEagle` | Epic (sparkle) | 1.2 | no | China04_Z3G4 (4) | `GoldenEagle_Tex_Imperial.png` |
| 4 | `SteppeWolf` | Legendary (sparkle) | 1.2 | no | China05_Z4 (1) | `SteppeWolf_Tex_Midnight.png` |
| 4 | `BactrianCamel` | Mythic (orbit) | 0.95 | no | China05_Z4 (2) | `BactrianCamel_Tex_Snowpeak.png` |
| 4 | `FerghanaHorse` | Cosmic (orbit) | 1.35 | no | China05_Z4 (3) | `FerghanaHorse_Tex_Night.png` |
| 4 guardian | `StoneGuardianLion` | Cosmic (orbit) | 0.85 | no | China05_Z4 (4) | `StoneGuardianLion_Tex_Jade.png` |
| 5 | `FishingCormorant` | Legendary (sparkle) | 1.1 | no | China06_Z5 (1) | `FishingCormorant_Tex_Ivory.png` |
| 5 | `SoftshellTurtle` | Mythic (orbit) | 0.9 | no | China06_Z5 (2) | `SoftshellTurtle_Tex_Golden.png` |
| 5 | `KoiCarp` | Cosmic (orbit) | 1.1 | yes | China06_Z5 (3) | `KoiCarp_Tex_Ogon.png` |
| 5 | `RiverDolphin` | Secret (orbit) | 1.15 | yes | China06_Z5 (4) | `RiverDolphin_Tex_Pink.png` |
| 5 guardian | `GiantSalamander` | Secret (orbit) | 0.85 | no | China07_Z5G6 (1) | `GiantSalamander_Tex_Albino.png` |
| 6 | `MoneyToad` | Mythic (orbit) | 0.9 | no | China07_Z5G6 (2) | `MoneyToad_Tex_Jade.png` |
| 6 | `LuckyBat` | Cosmic (orbit) | 1.25 | yes | China07_Z5G6 (3) | `LuckyBat_Tex_Jade.png` |
| 6 | `JadeRabbit` | Secret (orbit) | 1.2 | no | China07_Z5G6 (4) | `JadeRabbit_Tex_Moonlit.png` |
| 6 | `LionDanceCub` | Eternal (sparkle) | 1.15 | no | China08_Z6G7 (1) | `LionDanceCub_Tex_Jade.png` |
| 6 guardian | `LionDanceLion` | Eternal (sparkle) | 1.05 | no | China08_Z6G7 (2) | `LionDanceLion_Tex_Golden.png` |
| 7 | `TerracottaHound` | Cosmic (orbit) | 1.15 | no | China08_Z6G7 (3) | `TerracottaHound_Tex_Painted.png` |
| 7 | `JadeCicada` | Secret (orbit) | 1.0 | no | China08_Z6G7 (4) | `JadeCicada_Tex_Imperial.png` |
| 7 | `BronzeOx` | Eternal (sparkle) | 0.95 | no | China09_Z7G8 (1) | `BronzeOx_Tex_Polished.png` |
| 7 | `TerracottaHorse` | Divine (sparkle) | 1.3 | no | China09_Z7G8 (2) | `TerracottaHorse_Tex_Painted.png` |
| 7 guardian | `TerracottaGeneral` | Divine (sparkle) | 0.9 | no | China09_Z7G8 (3) | `TerracottaGeneral_Tex_Painted.png` |
| 8 | `Pekingese` | Secret (orbit) | 1.0 | no | China09_Z7G8 (4) | `Pekingese_Tex_Snow.png` |
| 8 | `Chiwen` | Eternal (sparkle) | 1.1 | yes | China10_Z8 (1) | `Chiwen_Tex_Imperial.png` |
| 8 | `Xiezhi` | Divine (sparkle) | 1.15 | no | China10_Z8 (2) | `Xiezhi_Tex_Ivory.png` |
| 8 | `Bixi` | Celestial (orbit) | 0.85 | no | China10_Z8 (3) | `Bixi_Tex_Obsidian.png` |
| 8 guardian | `Pixiu` | Celestial (orbit) | 1.1 | no | China10_Z8 (4) | `Pixiu_Tex_Jade.png` |
| 9 | `ImmortalCrane` | Eternal (sparkle) | 1.2 | no | China11_Z9 (1) | `ImmortalCrane_Tex_Golden.png` |
| 9 | `WhiteDeer` | Divine (sparkle) | 1.25 | no | China11_Z9 (2) | `WhiteDeer_Tex_Spirit.png` |
| 9 | `BaiZe` | Celestial (orbit) | 1.2 | no | China11_Z9 (3) | `BaiZe_Tex_Dusk.png` |
| 9 | `NineTailedFox` | Titanic (orbit) | 1.3 | no | China11_Z9 (4) | `NineTailedFox_Tex_Shadow.png` |
| 9 guardian | `Qilin` | Titanic (orbit) | 1.2 | no | China12_Z9G10 (1) | `Qilin_Tex_Celestial.png` |
| 10 | `ShrimpSoldier` | Divine (sparkle) | 1.1 | yes | China12_Z9G10 (2) | `ShrimpSoldier_Tex_Glass.png` |
| 10 | `CrabGeneral` | Celestial (orbit) | 1.0 | no | China12_Z9G10 (3) | `CrabGeneral_Tex_Azure.png` |
| 10 | `KunFish` | Titanic (orbit) | 1.0 | yes | China12_Z9G10 (4) | `KunFish_Tex_Abyss.png` |
| 10 | `PearlDragon` | Omega (orbit) | 1.25 | yes | China13_Z10G11 (1) | `PearlDragon_Tex_Coral.png` |
| 10 guardian | `DragonKing` | Omega (orbit) | 1.1 | yes | China13_Z10G11 (2) | `DragonKing_Tex_Crimson.png` |
| 11 | `BlackTortoise` | Celestial (orbit) | 0.85 | no | China13_Z10G11 (3) | `BlackTortoise_Tex_Frost.png` |
| 11 | `WhiteTiger` | Titanic (orbit) | 1.3 | no | China13_Z10G11 (4) | `WhiteTiger_Tex_Golden.png` |
| 11 | `VermilionBird` | Omega (orbit) | 1.35 | yes | China14_Z11 (1) | `VermilionBird_Tex_Bluefire.png` |
| 11 | `Fenghuang` | Infinity (orbit) | 1.3 | no | China14_Z11 (2) | `Fenghuang_Tex_Moonlight.png` |
| 11 | `Peng` | Godly (orbit) | 1.45 | yes | China14_Z11 (3) | `Peng_Tex_Dawn.png` |
| 11 guardian | `AzureDragon` | Godly (orbit) | 1.2 | yes | China14_Z11 (4) | `AzureDragon_Tex_Jade.png` |
| Special (Nian Night Raids) | `Nian` | Secret (orbit) | 1.15 | no | China15_Special (1) | `Nian_Tex_Shadow.png` |
| Exclusive (Robux) | `GoldenEmperorDragon` | Godly (orbit) | 1.3 | yes | China15_Special (2) | `GoldenEmperorDragon_Tex_Jade.png` |

Rarity plan: zone N pets cover the 4 tiers starting at tier N (zone 11 has 5 and ends at Godly), guardians take their zone's top tier, Nian is Secret and the Golden Emperor Dragon is Godly (it also carries `royal = true` in its extra data for the exclusive look). If `Config.ZoneSlots` uses a different spread, the Rarity field in CreatureData is only used for the aura and can be changed there.

## Style notes
- Cute pets (zones 1 to 7 and the zone 8 to 11 cuties) use flat black eyes and Kobe's cute proportions (cute_quad legs about 20%, big heads, birds with short tucked legs). Guardians, Nian and the royal mythic creatures (Chiwen, Xiezhi, Bixi, Bai Ze, the dragons, the Four Symbols, Fenghuang, Peng) have glowing angry eyes.
- Fierce guardians stand on thick legs at 35 to 41% of their height, except the Terracotta General (a biped statue in a long armour coat) and the floating serpent dragons.
- Floaters (`Hover = 1`): Koi Carp, River Dolphin, Lucky Bat, Chiwen, Shrimp Soldier, Kun Fish, Pearl Dragon, Dragon King, Vermilion Bird, Peng, Azure Dragon, Golden Emperor Dragon.
- Glow parts export as separate `Glow_*` meshes (Neon in Roblox). The flames, fox fire and pearls look pale in the Blender previews but render bright as Neon.

## Rebuilding
```
pip install --break-system-packages bpy numpy pillow cairosvg
cd creature_pipeline
./run.sh <id> [<id> ...]        # build + render + export, 2 at a time, then the 3-view sheets
./finish.sh <BatchName>          # batch FBX + contact sheet + CreatureData.rbxmx
```
