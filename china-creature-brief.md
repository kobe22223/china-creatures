# Steal an Egg in China: creature sculpting brief (for a Claude Code cloud session)

Goal: sculpt, rig and animate every pet and guardian for **Steal an Egg in China** with the existing pipeline, then hand Kobe batch FBX files plus `CreatureData.rbxmx` to import into Studio. Studio work (map, Config, systems) happens in a separate chat with Studio connected; this session only makes art.

## Setup (tested 2026-11-03, works headless)
1. From the Roblox Games project, read `steal-egg-template-context.md` section 9, `creature-and-icon-pipeline-bundle.txt` and `claude/china-pipeline-additions.txt` (or ask Kobe to paste them into the repo).
2. Unpack the bundle (instructions at its top), then apply `china-pipeline-additions.txt`: it adds `cute_quad` to `kit.py` and the approved `luckypiglet.py`.
3. `pip install --break-system-packages bpy numpy pillow cairosvg` (bpy 5.2.3 LTS installs fine from PyPI).
4. `cd creature_pipeline && python3 make.py <id> --render --two --walk --export`. About 25 s per cute creature. Make a 3-view sheet (front 30, back 150, walk frame) and look at it before moving on. `sheet.py` makes a contact sheet per batch.
5. Replace the `BATCHES` dict in `batch_fbx.py` with the China batches below, run it, then run `gen_rbxmx.py`.
6. Commit `out/batches/*.fbx`, `out/CreatureData.rbxmx`, the creature `.py` files and the contact sheets to the repo so Kobe can download them.

## Style rules (Kobe's, non-negotiable)
- Sculpted meshes with the studded classic-Roblox surface. Never voxel or part builds.
- Cute pets: plain flat black eyes (`c.eye`, style black). Fierce, royal and guardian creatures: glowing angry eyes (`detail.eyes_pair`).
- Chinese theme through colour and details: red, gold, jade green, porcelain blue and white, lantern and coin motifs, cloud swirl `filigree` paint on royal ones. Keep it respectful: creatures, statues and festival motifs only, no caricatured people.
- Every creature gets an `aura(...)` matching its rarity tier, and `c.extra["speed"]` (and `hover` for floaters).
- Bone names must be unique per creature (already handled by `c.bn`).

## Proportion rules (Kobe rejected the first piglet for long, stilt-like legs)
**Cute pets (most of zones 1 to 6):** use `kit.cute_quad`, not `kit.quad`. `luckypiglet.py` is the approved reference.
- Legs are short stubs: about **20 to 25%** of total height. Haunches sink into the body so legs grow out of it, no visible gap or seam.
- Body is a round barrel, wider than it is tall from the front. Legs sit **under** the body (spread about 0.55), not splayed out to the sides.
- Head is big: about **40 to 45%** of total height, sits forward and slightly up on the body with no visible neck.
- Eyes sit on the front half of the face, a little below the head's middle. Ears, horns and tails are small accents that don't change the silhouette much.
- Never use `quad(chunk >= 1.3)` for small pets: the legs come out as long cylinders.

**Fierce creatures and guardians:** use `detail.beast` / `dino.theropod`. Legs are thick and muscular (the `leg()` helper's muscle mass), roughly 35 to 45% of height, and stance is wide. Heads are about 25 to 30% of height. They should feel heavy and powerful, not lanky.

**Birds:** round body, head about 35% of height, short legs tucked under (about 15%), wings folded against the body unless it flies.

**Serpentine dragons:** body thickness about 1/8 of length, a head about twice the body width, short clawed legs, whiskers, and a `fur_line` mane. Use `kit.spine` + `swim_anims` (yaw) and `c.extra["hover"] = 1`.

**Check every creature** before batching. Reject and fix it if:
- legs look longer than the body is deep (cute pets)
- there are gaps between parts or dark holes at joints
- the walk frame shows limbs detaching
- ears, horns or tails stick straight out like paddles

## Roster (58 unique sculpts)
Each zone has 4 unique pets (zone 11 has 5) and 1 guardian. Recoloured variants fill each zone to about 9 pets: for each pet, also export 1 palette-swapped texture `<Name>_Tex_<Variant>.png` (same mesh, same UVs) so Kobe can upload it and the game swaps `TextureID`.

| Zone | Pets (low to high) | Guardian (fierce, height 14 to 18) |
|---|---|---|
| 1 Rice Paddy Village | Lucky Piglet (done), Paddy Duckling, Rice Rooster, Buffalo Calf | Giant Water Buffalo |
| 2 Bamboo Grove | Bamboo Rat, Golden Pheasant, Red Panda, Baby Panda | Giant Panda (angry, bamboo stalk in mouth) |
| 3 Tea Terraces | Mandarin Duck, Silkie Chicken, Muntjac Deer, Pangolin | South China Tiger |
| 4 Great Wall | Golden Eagle, Steppe Wolf, Bactrian Camel, Ferghana Horse | Stone Guardian Lion (grey stone, ball under paw) |
| 5 Jade River | Fishing Cormorant, Softshell Turtle, Koi Carp, River Dolphin | Giant Salamander |
| 6 Lantern Night Market | Money Toad (coin in mouth), Lucky Bat, Jade Rabbit, Lion Dance Cub | Lion Dance Lion (costume style, big eyes and fur fringe) |
| 7 Terracotta Tomb | Terracotta Hound, Jade Cicada, Bronze Ox, Terracotta Horse | Terracotta General (biped statue, armour plates, cracked clay paint) |
| 8 Forbidden City | Pekingese, Chiwen (roof dragon-fish), Xiezhi (one horn), Bixi (dragon turtle) | Pixiu (gold, winged) |
| 9 Kunlun Immortal Peaks | Immortal Crane, White Deer, Bai Ze, Nine-Tailed Fox | Qilin (scaled, flame mane, hooves) |
| 10 Dragon King's Palace | Shrimp Soldier, Crab General, Kun Fish, Pearl Dragon | Dragon King (serpentine sea dragon, crown, hovers) |
| 11 Heavenly Court | Black Tortoise, White Tiger, Vermilion Bird, Fenghuang, Peng | Azure Dragon (serpentine, cloud trails, hovers) |
| Special | Nian (night raider for the Nian Night Raids twist, red and gold, horn, fierce) | |
| Exclusive (Robux) | Golden Emperor Dragon (gold scales, jade gems, crown, glowing eyes) | |

## Batches (4 per FBX, zone order)
- `China01_Z1`: piglet, duckling, rooster, buffalo calf.
- `China02_Z1G2`: water buffalo, bamboo rat, golden pheasant, red panda.
- Then continue in roster order, 4 per batch, with guardians in the batch with their zone.

Name ids in lowercase without spaces (e.g. `luckypiglet`, `giantwaterbuffalo`). Creature `Name` is PascalCase; Config uses it as `Mesh = "<Name>"`.

## Done means
- Every creature rendered and checked against the proportion rules, with a 3-view sheet per creature and a contact sheet per batch committed.
- All batch FBX + `CreatureData.rbxmx` + variant texture PNGs committed.
- A short list for Kobe: which FBX to import, and the exact import location `ServerStorage.CreatureRigBuilder` expects (the Studio chat will confirm it from the source before import).
