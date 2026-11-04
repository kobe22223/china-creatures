# Kobe's 3D model pipeline: cheat sheet for a new Claude Code session

You are making sculpted, rigged and animated 3D models (pets, guardians, props like treadmills) for one of Kobe's Roblox "Steal an Egg" games, headless in a cloud container with Blender as a Python module. Another chat with Studio connected does the Studio side (import, Config, wiring). **You only make art and hand over files.**

This guide comes from building 58 creatures and 10 treadmills for "Steal an Egg in China" (repo `kobe22223/china-creatures`, branch `claude/pensive-noether-4m1inf`). Everything below was tested there.

---

## 1. Setup (about 3 minutes)

1. Get the pipeline code. The easiest route is copying it from the China repo, which already has every helper:
   - Ask Kobe to add `kobe22223/china-creatures` to your session (or he uploads `creature_pipeline/` into the new repo).
   - Copy `creature_pipeline/` without `out/` and without `creatures/*.py` and `treadmills/china*.py` (those are China-specific, but keep a few as examples).
   - If you only get the original bundle (`creature-and-icon-pipeline-bundle.txt`), unpack it with the script at its top, then apply `china-pipeline-additions.txt` (adds `cute_quad` to `kit.py` + `luckypiglet.py`). You then lack `cn.py`, `tm.py`, `views.py`, `run.sh`, `finish.sh`, `stack.py`, `make_tm.py`, `merge_tm.py` and the `variant_texture` patch in `sculpt.py`: copy those from the China repo, they are generic.
2. `pip install --break-system-packages bpy numpy pillow cairosvg` (bpy 5.2.3 from PyPI works headless, about 400 MB).
3. Smoke test: `cd creature_pipeline && python3 make.py luckypiglet --render --two --walk --export` (about 20 s). If it renders, you are ready.
4. Add a `.gitignore` so only deliverables are committed:
   ```
   __pycache__/
   creature_pipeline/out/*
   !creature_pipeline/out/sheets/
   !creature_pipeline/out/batches/
   !creature_pipeline/out/textures/
   !creature_pipeline/out/CreatureData.rbxmx
   !creature_pipeline/out/treadmills/
   creature_pipeline/out/treadmills/china*/
   ```

## 2. File map

| File | What it is |
|---|---|
| `sculpt.py` | Core: `Creature`, shapes (`ellipsoid`, `tube`, `leaf`, `sheet`, `torus`, `box`, `spike`, `eye`), studded texture bake, `animate`, `render`, `export`, `variant_texture` (palette swap on the same UVs), `tex_size` attribute. |
| `kit.py` | Cute body plans: `quad`, `cute_quad` (the approved pet plan), `biped`, `spine`, wings, `quad_anims`, `biped_anims`, `swim_anims`, `aura`, paints `stripes` / `spots` / `band`. |
| `detail.py` | Game-space helpers (`V`, `B`, `E`, `T`, `S`, `BOX`, `SHEET`), shard `fur`, `fur_line`, armour `shell` / `cuff` / `crown`, `fierce_eye` / `eyes_pair` (glowing angry eyes), `maw` (teeth), horns, `beast` + `leg` (fierce quadruped), paints `filigree` / `cracks`. |
| `dino.py` | Theropod skeleton + anims. |
| `cn.py` | Higher-level plans written for China, reusable for any theme: `cute_bird` + `bird_anims`, `flying_bird` + `flyer_anims` (spread wings, hovers, tucked legs), `cute_swimmer` + `swimmer_anims`, `fierce_quad` + `fierce_anims` (guardians), `hoof`, `serpent_dragon` + `serpent_anims`, `dragon_head`, `puffs` (fluff / clouds), `scale_paint`, `panda_paint`, motifs `coin`, `lucky_knot`, `bell`, `lantern`, `cloud_filigree`. |
| `make.py` | Build one creature: `python3 make.py <id> --render --two --walk --export`. Also writes `proportions.json` and variant textures. |
| `views.py` / `stack.py` / `sheet.py` | 3-view sheet per creature, stack several sheets for review, base + variant contact sheet per batch. |
| `run.sh` | `./run.sh id1 id2 ...` builds 2 at a time (4 at once ran out of memory), then makes the 3-view sheets. |
| `batch_fbx.py` / `finish.sh` | `BATCHES` dict (4 per FBX). `./finish.sh <BatchName>` = merged batch FBX + contact sheet + `CreatureData.rbxmx`. Skips batches not built yet. |
| `gen_rbxmx.py` | `out/CreatureData.rbxmx`, one ModuleScript per creature (anims, bone rest CFrames, aura, speed, hover, batch layout). |
| `treadmills/tm.py`, `make_tm.py`, `merge_tm.py` | Static props: rounded boxes, deck, console, rails, roof, lanterns, `turn_around`; per-tier rule checker; merge into one FBX + `layout.json`. |

## 3. Coordinates and conventions (get these right first)

- **Game space:** x right, y up, **front = -z**. `P(x, y, z)` converts to Blender for `sculpt.py` calls. `detail.V(x, y, z)` is a game-space vector and `B(v)` converts it. Never mix the two in one call: `c.ellipsoid(P(...))` vs `E(c, V(...))`.
- `cn.py` helpers that take a centre (`coin`, `bell`, `lantern`, `puffs`) expect a **P() point**. To pass a `V` point, wrap it: `coin(c, B(v), ...)`.
- Bone names are prefixed per creature automatically (`c.bn`). Keep the standard names (`Root, Hips, Chest, Neck, Head, Jaw, ArmL/R, ForeL/R, ThighL/R, ShinL/R, Tail1.., Spine1.., WingL/R, WingTipL/R, FinL/R`) so the stock anims work.
- `Creature(name, height=...)`: `height` is metadata the game uses for scale. Pets were 5 to 7, guardians 14 to 18. The `Name` is PascalCase and becomes `Mesh = "<Name>"` in Config. The file / module id is lowercase with no spaces.
- `c.extra["speed"]` on everything, `c.extra["hover"] = 1` on floaters, `aura(c, style, color, color2, rarity)` on everything. Known aura styles: `sparkle`, `orbit`.
- `glow=True` shapes export as separate `Glow_<rrggbb>` meshes that Studio turns Neon. They render pale in Blender previews; that is normal.
- `bones` argument: a string or a list of strings, **never a list inside a list** (the `coin` bug: passing a list to a helper that wrapped it again crashed `_snap`).

## 4. Kobe's style rules (non-negotiable)

- Sculpted meshes with the studded classic-Roblox surface. Never voxel or part builds.
- **Cute pets:** plain flat black eyes (`c.eye`, default style). **Fierce, royal, guardian:** glowing angry eyes (`eyes_pair`).
- **Cute proportions:** use `cute_quad`, never `quad(chunk >= 1.3)` for small pets. Legs are short stubs at 20 to 25% of height, sunk into a round barrel body (no seam). Big head at 40 to 45% of height, no visible neck. Eyes on the front half of the face, a bit below the middle.
- **Birds:** round body, big head, short legs tucked under (about 15%), wings folded unless it flies. Flyers: `flying_bird` lifts the whole bird and keeps legs short. **Never stretch legs to the ground.**
- **Guardians:** `fierce_quad` (or `detail.beast`, `dino.theropod`, `kit.biped` for statues). Thick muscular legs at 35 to 45% of height, wide stance, head at 25 to 30%, heavy not lanky.
- **Serpent dragons:** `serpent_dragon` does Kobe's rule for you (thickness about 1/8 of length, head about twice body width, short clawed legs, whiskers, `fur_line` mane, yaw swim, hover).
- **Reject and fix** if: legs look longer than the body is deep (cute), gaps or dark holes at joints, limbs detach in the walk frame, ears / horns / tails / fins stick straight out like paddles.
- Theme through colour and details, kept respectful: creatures, statues, architecture, festival props. No caricatured people, no text or characters on meshes.
- Each creature gets one palette-swapped variant: `VARIANTS = {"Jade": {OLD_COLOUR: NEW_COLOUR, ...}}` at the bottom of its file. Colours not in the map stay. Keep faces natural on human-like statues (a red-faced variant read as a clown).

## 5. Workflow that worked

1. Read the brief, ask Kobe anything unclear in **one** round (rarity mapping, what the example is, check-in cadence). Default cadence: build batch 1, stop for his OK, then do everything else without stopping.
2. Per batch of 4: write the 4 creature files, `./run.sh a b c d`, then `python3 stack.py <scratch>/chk.png a b` and **look at every sheet** (front 30, back 150, walk frame). Fix, rebuild only the broken ones, look again. Usually 1 or 2 fix rounds.
3. `./finish.sh <Batch>`, look at the contact sheet (variants too), commit, push.
4. At the end: verify by re-importing every batch FBX (rig count, unique bone names, embedded textures), check the rbxmx module count, write a handoff doc, push.

The 3-view sheet header shows `legs %` (ground to the bottom of the Hips/Chest shapes) and `head %` (Head/Jaw shape span). The approved piglet reads legs 22%, head 62% on this metric, so compare against that, not against the brief's numbers.

## 6. Pitfalls already hit (and the fix)

| Problem | Fix |
|---|---|
| Collar / scarf torus around the neck floats like a hoop or a red fin (head and body are separate spheres) | Use a chest bib ellipsoid under the chin, slightly low and forward (`by - 0.3`, `-rz * 0.97`), with the bell / coin / knot in front of it. |
| Accessories on the chest hidden behind the big head | Place them low under the chin and forward, then check the walk view. |
| Wings / ears / tails / feathers sticking straight out (paddles) | Hug the body (smaller radius, closer x), angle up-and-back or down, or make them a round ellipsoid instead of a flat leaf. |
| `flat=(sx, sy)` on tubes squashes the wrong way | For a sideways-thin feather or tail, use `flat=(0.4, 1.0)`. |
| Puffs look like bubbles / grapes | Use more, smaller puffs with high `sink` (0.7 to 0.75) and little colour mix; use smooth ellipsoids for ears. |
| Diamond shard scales look like scattered chips | Use rows of flattened ellipsoid plates aligned to the surface (pangolin `scales()`), or `scale_paint`. |
| Thin eye-stripes / patches invisible or giant | Check from the front view; move markings forward (more -z) so they sit on the visible face. |
| Black eyes vanish on dark patches (panda) | Lighten the patch a little and make the eye bigger. |
| Head and body read as two balls with a pinched waist (fish, dolphin) | Add a filler ellipsoid at the join. |
| Paint patterns read as giant swirls or contour lines | Raise `scale`, lower `width` (cracks: `scale=2.8, width=0.018`). |
| Head stripes form a messy mask | Restrict paint with `only=lambda X, Y, Z: np.abs(X) > ...`. |
| `dragon_head` and other heads are built facing -z | For a console or anything that must look at +z, build it then call `turn_around(c, n0, pivot)` (in `tm.py`). |
| 4 parallel Blender builds killed (exit 137) | `run.sh` runs 2 at a time. |
| `git push` of big FBX files fails with HTTP 502 | Retry with backoff (2, 4, 8, 16 s). Push in the background while you build the next batch. |
| `batch_fbx.py` ignored the batch name argument | It filtered on names starting with `Batch`; now accepts any prefix you add (check it for new names). |
| Session restart mid-build | Files on disk survive. Check `git status` and `out/`, rerun the interrupted step. |

## 7. Static props (treadmills, stands, decor)

- `tread(name)` in `tm.py`: a Creature with one `Root` bone, studs about half a stud wide, 1024 px texture. Bind everything to `R` (= `"Root"`). `make_tm.py` exports **meshes only** (removes the armature).
- Units are studs. Design to the brief's hard numbers and let `make_tm.py` check them: deck size and height, clear air over the walk area, footprint, at most 10k triangles, at most 4 Glow meshes, mesh names `<Name>_Body` / `<Name>_Glow_<rrggbb>`. Adapt the checks in `make_tm.py` to the new brief's rules first.
- Triangle budget killers: tori and many small rings. Use `seg=(8, 3)` for small rings, `(6, 4)` for small spheres, and `make_tm.py <id> --tris` to list the heaviest shapes.
- A box only has vertices at its corners: a vertex-based "is the deck at y = 1.2" test must look at the edges, not the middle.
- Round caps on tubes poke below the floor: start ground-level tubes a bit above y = 0 and check the lowest point after merging.
- `merge_tm.py` places pieces 30 studs apart along +x (Blender -x) and writes `layout.json`.

## 8. Handoff to Kobe (what "done" looks like)

- Commit: batch FBXs (`out/batches/`), `out/CreatureData.rbxmx`, variant PNGs (`out/textures/`), 3-view + contact sheets (`out/sheets/`), all source `.py` files, plus a handoff `.md` with a table: zone, `Mesh` name, rarity / aura, speed, hover, batch, variant texture.
- Tell Kobe the Studio chat must read `ServerStorage.CreatureRigBuilder` first to confirm where the FBX imports and CreatureData go, then: import each batch FBX with the 3D Importer, insert the rbxmx, run `CreatureRigBuilder.Build()`, bulk-upload the variant PNGs, set `Mesh = "<Name>"` in Config.
- Give him ready-to-paste prompts for the Studio chat and the branch zip download link (`https://github.com/<owner>/<repo>/archive/refs/heads/<branch>.zip`).

## 9. Talking to Kobe

- Writing he reads: no em dashes, use commas. Plain words, short sentences.
- Put everything only he can do (uploads, imports, IDs, approvals) in one clear numbered list at the end of a message.
- Send the contact sheet image with each batch result so he can see it on his phone.
- He expects you to look at every render and fix problems before showing him. Say what you fixed and why in a line each.
