# Steal-an-Egg Game Template: Full Context for Building a New Game

Written 2026-11-03 from the live build of **"+1 Superpower for an Egg"** (Kobe's game, placeId 136671677085775).
Kobe wants to make many games in this genre from this template, each with a new twist. The goal is to ship each
one fast, keep what is proven, and push every metric to the 90th percentile.

**Read this whole file before touching Studio.** Then:
1. Load the `roblox-game-dev` skill (Studio MCP tooling, Luau patterns, backdoor scanning, mobile UI bugs).
2. Read `claude/superpower-egg-launch-checklist.md` and `claude/superpower-egg-store-page.md` in this project.
3. Ask Kobe for the new game's name, theme and twist if he hasn't said them, then follow section 7.

Companion file in this project: `claude/creature-and-icon-pipeline-bundle.txt`. It holds the Python source that
makes the sculpted creature meshes and the cartoon UI icons (section 9).

---

## 1. The genre and the core loop

Steal-an-Egg / Steal-a-Brainrot style simulator:

1. **Treadmill** on your plot: step on it and your **Speed** stat climbs every 0.3 s. Speed sets your walk speed.
2. **Zones** run in a straight corridor past the safe line. Each zone has a theme, a **Recommended** speed and
   pedestals of **eggs**, each guarded by a giant **guardian**.
3. **Steal**: hold E on an egg (0.5 s). The guardian wakes up and chases you. Get back past the safe line to keep it.
   If it catches you, the egg goes back to its nest.
4. **Place** the egg on your plot. It incubates, then **hatches** into a pet with a rarity, a mutation and a weight.
5. **Pets** sit in your pen and make **cash per second**. Cash buys superpowers, treadmill tiers, trails and pet slots.
6. Faster you = further zones = better eggs = more cash. The loop scales with huge numbers (K, M, B, T, Qd, Qn...).
7. **PvP**: a bat and bear traps make other players drop the egg they are carrying.

The twist for each new game goes on top of this loop (section 8). Do not rebuild the loop.

---

## 2. Map layout (world coordinates in the template)

- **Base** (safe area), centred around x 0, z -200..200. Ground: `Workspace.Map.Base.BaseGround` (top at y 0).
  - 6 **plots**, 3 per side: x = ±155, z = -155 / -35 / 85. Floor 80 x 100 (rotated ±90). Each plot has a
    `Treadmill` model (x ±97), `PetSlots` (16 parts, the pet pen), `EggSlots`, `ClaimPad`, `OwnerSign`, `Fence`.
  - **Shop row** at z -183, facing +Z: `PowerStand` x -70, `SellStand` x -23, `TrailStand` x 23, `FreeGift` x 70.
    Stands are scaled 1.89x, shopkeeper NPCs 2.35x (`ShopKeepers` script).
  - **RoyalStand** (exclusive pet display) in the middle at (0, 0, -30).
  - **Leaderboards** at x ±158, z 186.
- **Safe line** `SAFE_Z = 200` (red line). Guardians never cross it. `DayNight` can raise a wall there.
- **Zones** go along +Z. `Workspace.Map.Zones.ZoneN` (Model) with attributes `ZoneIndex`, `StartZ`, `EndZ`.
  Each is about 600 studs long and 240 wide (inner walls at x ±120). Zone 1 eggs sit around z 620; zone 11
  runs z 6200..6800 with an `EndWall` at z 6804. Children: `Ground`, `Pedestals`, `GuardSpawn`, `Sign`
  (recommended speed board), `AssetDecor` (props, CanCollide false), `Backdrop` (big scenery like a volcano).
- `Workspace.WorldEggs` holds every egg sitting in the world. `Workspace.BearTraps` holds placed traps.
- **StreamingEnabled is on.** Anything a player must see from far away needs
  `ModelStreamingMode = Persistent` (rare eggs already do this).

---

## 3. Script inventory and architecture

Server-authoritative. The client only draws things and asks the server to act.

### ServerScriptService.Server (ModuleScripts, started by `GameServer`)
| Module | Job |
|---|---|
| `Net` | Remotes in `ReplicatedStorage.Remotes`: `Request` (RemoteFunction), `Action` (fire and forget), `State` (snapshots), `Notify`, `Effect` (kind, payload). `Net.On(action, fn)` registers a handler that returns `ok, msg`. Token-bucket spam limit (20/s, burst 45, kicks after 400 dropped calls) + per-action 0.12 s limit. |
| `Data` | DataStore load/save (`Config.DataStoreName`), defaults, `Data.Profiles[player]` (saved) and `Data.Sessions[player]` (temporary). `Data.Push` batches a snapshot to the client. Offline earnings, Friend Boost (`RefreshFriendBoost`), Premium flag, Slow Mode walk speed, `ApplyWalkSpeed`. |
| `Plots` | Claim plot, eggs on plot (`AddEgg`, timers, hatch / hatch all), pets (`GivePet`, `RenderPets`, `SetActive`, `EquipBest`, `PickUp`, `PutBack`, `Sell`, `BuySlot`), 1 s income loop, `SendHome`. |
| `Steal` | World eggs on pedestals (rarity, mutation, weight rolled on spawn), steal prompt + reach check, carrying model on the head, guardians (spawn, chase, catch, return), drop / return eggs, decoys, shields, freeze. |
| `Economy` | Treadmill (auto-run when you step on the belt, step loop, upgrades), trails, Robux: `ProcessReceipt` (receipt de-dupe), product handlers, gamepass checks, `PromptProduct` guards, upgrade board. |
| `Rewards` | Daily (7-day streak), time rewards, Lucky Wheel, codes, group / community gift, index discovery rewards + Claim All, offline claim, settings saves, favourite prompt flag. `grant()` helper. |
| `Leaderboards` | OrderedDataStores `LB_Speed_v1` / `LB_Cash_v1` and the boards in the base. |
| `Powers` | Superpowers: buy levels, use actives (server cooldowns, escape lockout), free starter power pick. |

### ServerScriptService (Scripts)
`GameServer` (init order + Studio-only `DevGive` / `DevGivePet` test remotes), `AdminServer` (admin panel actions,
admins checked by **UserId only**), `AntiCheat` (section 6), `PvPServer` (bat, bear traps, server ragdoll,
Backpack tools for bat / trap / powers), `TutorialServer`, `DayNight`, `ShopKeepers`, `RoyalStand`, `DevGrants`
(one-off dev speed gift, remove for a new game).

### ReplicatedStorage.Shared (ModuleScripts used by both sides)
| Module | Job |
|---|---|
| `Config` | **Every tunable number, name, ID and list.** Re-theme a game here first (section 5). |
| `Logic` | Game maths: `PetIncome`, `TotalIncome`, `IncomeMult` (friend / VIP / Premium / 2X timer), `StepGain`, `ScaledCash` + `RewardMult` (free rewards scale with progress), `BestZone`, `BackpackSize`, `RollEggRarity` / `RollEggMut` / `RollPet` (luck), `EggTier` (rare / super rare), `ZoneTopRarity`, `WheelSpeed`, `PowerStat`, `ActiveCount` (exclusive pets don't count), `IndexReward`, `EggName`, `ZoneAt`. |
| `Format` | `Short` (1.2K, 3.4Qd), `Clock`, `Time`. |
| `Models` | Builds pets (mesh creatures, rigged creatures, asset pets, part-built fallbacks), eggs, guardians, mutation looks (Golden / Diamond / Rainbow), the "Royal" exclusive look. Tags pets `RarityPet` with a `Rarity` attribute. |
| `Prices` | Reads live Robux prices (managed pricing) into Config on server start. |
| `CreatureAnimator` | Plays the Blender walk / idle clips on mesh creatures (bones), from `CreatureData` modules. |
| `Creatures` | Older rigged showcase creatures. |

Other ReplicatedStorage: `CreatureMeshes` (built mesh creature templates), `EggAssets` (vetted voxel egg models,
`Config.EggAssets[zone][type]`), `PvPAssets` (`BatTool`, `TrapTool`, `BearTrapOpen`, `BearTrapClosed`),
`GenAssets` (generated zone decor). ServerStorage: `DevNotes` (change log, read it), `CreatureRigBuilder`
(builds `CreatureMeshes`), `Archive` (old Trade + Tackle scripts), `_*Backup` folders, `_AssetQuarantine`.

### StarterPlayerScripts
- `ClientMain`: makes ScreenGuis `HUD` (order 1), `Panels` (5), `Overlay` (10), each with a UIScale fitted to a
  1920x1080 design (`min(vp.X/1920, vp.Y/1080)`, clamped 0.35..1.4). Builds HUD and panels, refreshes on
  `State.Changed`, daily popup, treadmill animation, notification sounds.
- `Client` folder (ModuleScripts): `UIKit` (all UI building blocks: `new`, `label`, `button`, `panel`, `card`,
  `icon`, `corner`, `stroke`, `gradient`, `pattern`, `rays`, `shine`, `bounce`, `hover`, `setButton`, `viewport`,
  `fontPass`, `autoTheme`, `toggle/open/close`), `State` (client copy of data + `State.request`), `HUD`, `PanelsA`
  (Index, Shop, group Rewards, Daily, Codes), `PanelsB` (Wheel, Time rewards, Eggs, Pets, Settings), `PowersUI`,
  `ChaseUI`, `PetIdle` (pets wander the pen + animate), `Sfx` (sound library), `Offers` (contextual buy cards,
  rate-limited), `Icons3D`, `Hotbar` / `PvPKit` (partner's custom hotbar).
- LocalScripts: `PvPClient`, `GuardFX`, `RarityAuras`, `EggRarityTitles`, `EggBeacons`, `EggPlacer`,
  `SellStandUI`, `TrailStandUI`, `Tutorial`, `AdminPanel`, `DayNightClock`, `ZoneAtmosphere`, `SpeedFeel`,
  `SnappyMovement`, `TreadmillWhoosh`, `Engagement`, `VIPChat`, `OwnedStands`, `GroupReward`,
  `StarterPowerPicker`.
- Gotcha: a separate LocalScript can `require(script.Parent.Client.State)` and gets the SAME module as
  ClientMain (same client VM). `execute_luau` in the Client datamodel does NOT (it gets a fresh copy).

---

## 4. Systems in detail (what exists, so you reuse instead of rebuild)

**Speed and movement**
- Walk speed: `Config.WalkSpeedFor(speed) = min(400, 16 + 26*log10(1 + speed/60))`. About 27 at 100,
  92 at 50K, 125 at 1M, 274 at 640B.
- `SpeedFeel` widens the FOV from 70 to 90 as you go faster.
- `SnappyMovement` gives near-instant acceleration and braking above 30 WalkSpeed. It follows `WalkToPoint` for
  tap-to-move players.
- Slow Mode HUD toggle: normal speed (16) inside the base.

**Treadmill**
- Steps every `Config.StepInterval` (0.3 s) while you're on the belt. Gain is `Logic.StepGain`, including trail
  multiplier, 2X Speed pass and VIP x1.25.
- 10 tiers in `Config.Treadmill` (Cost, PerStep, Skin). Can be upgraded with cash or Robux.
- `Config.Trails` multiply every step.

**Zones and eggs**
- `Config.Zones[i]` = {Name, Emoji, Color, Recommended, Mult}. `Config.ZoneSlots[zone]` = rarity odds.
- `Config.EggTypes` / `SpecialEggs`. Egg weight (Kg) affects pet income.
- Rarities (15, low to high): Common, Uncommon, Rare, Epic, Legendary, Mythic, Cosmic, Secret, Eternal, Divine,
  Celestial, Titanic, Omega, Infinity, Godly. Base income 5 up to 1,000,000, times the zone `Mult`.
- Mutations: Normal 88%, Golden x2 9%, Diamond x4 2.5%, Rainbow x10 0.5%.
- Luck (Lucky Grab power, 2X Luck pass) bumps the rarity up a step inside the zone.

**Guardians** (`Config.Guardians[zone]` = Name, Creature/model, Size/Scale, SpeedMult, CatchRange)
- Server physics assembly moved by AlignPosition / AlignOrientation, so it looks smooth on clients.
- States `Sleep` / `Awake` / `Chase` / `Return`, shown with the `State` attribute (GuardFX animates).
- Chase speed `max(14, WalkSpeedFor(zone Recommended) * SpeedMult)`, so it scales with the speed curve.
- `Config.GuardReactTime` (0.75 s) before chasing, plus the Sneaky power. `CatchAfter` grace after a steal.
- **Fair catches**:
  - The distance is measured from the body centre (`CenterOff`), not the root.
  - The player is only caught if both the server position AND the lag-predicted position
    (pos + velocity x (ping + 0.05)) are inside `CatchRange - Speed*0.03`.
  - Without this, fast players got caught from 25+ studs away.
- Walks home at `Config.GuardReturnMult` (1.6x) once nobody is carrying its egg. A caught player gets knocked back.
- Never crosses `SAFE_Z`; clamped inside the zone walls.

**Pets**
- Record: {Id, Mut, Kg, Active, Zone (exclusive only), Locked}.
- `MaxActive` 16 slots, bought with cash.
- Index (`d.Index`, `d.IndexClaimed`) with discovery rewards and a Claim All button.
- Sell at the SELL stand: pick up, carry, sell.

**Superpowers** (`Config.Powers`, 5 levels each, cost `BaseCost * CostMult^(lvl-1)`)
- Actives: Dash, Invisibility, Decoy, Freeze Blast, Shield, Fly. They are Roblox Backpack tools with the
  `PowerId` attribute.
- Passives: Quick Hands, Sneaky, Double Jump, Magnet Hands, Fast Incubator, Iron Grip, Butterfingers Guard,
  Lucky Grab, Slippery.
- Free starter power picker on first join.

**PvP** (`Config.Bat`, `Config.BearTrap`)
- Bat: 1 s cooldown. A hit knocks the egg out and RAGDOLLS the victim for 2.5 s.
  - The ragdoll is done on the server: joints become BallSocketConstraints, and the client goes into the Physics
    state.
  - Current avatars use **AnimationConstraint** joints, not Motor6D. The code handles both.
- Bear traps: up to 4 out at once. They snap egg carriers and freeze them.
- Only players carrying an egg can be hit, never in the base. Shield blocks; Iron Grip may keep the egg.
- Running into things never ragdolls you (FallingDown / Ragdoll humanoid states are disabled).

**Rewards and retention**
- Daily: 7-day streak.
- Time rewards: 12 per session (1, 3, 5, 8, 12, 16, 20, 25, 30, 40, 50, 60 min), with a countdown under the
  Rewards tile.
- Lucky Wheel (free every 8 min, odds shown on each slice): JACKPOT 1% (Rainbow egg of the zone's best rarity
  plus big cash, announced to the server), $1K 26%, +1 Spin 12%, $10K 18%, Speed 14%, 2X Money 5 min 10%,
  $100K 10%, Giant Egg 9%. Licensed tick / start / win sounds.
- Codes, group reward (`GroupReward` popup with in-game join prompt), FREE gift stand.
- Offline earnings up to 8 h.
- NEXT ZONE goal bar.
- Friend Boost (+10% per friend in the server, max +40%) with an Invite button.
- Roblox Premium +10% cash.
- Favourite prompt after 8 min (once per 3 days).
- All free cash rewards AND paid cash packs scale with progress (`Logic.ScaledCash`), so they never go worthless.

**Rare egg visibility** (`EggBeacons`)
- `Logic.EggTier`: Super = the zone's best rarity or a Rainbow egg; Rare = 2nd best or Diamond.
- Super eggs get a 260-stud light beam. Both tiers get an always-on-top outline (nearest 18 only; Roblox draws
  at most 31 Highlights).

**Monetisation** (template IDs belong to the template game; a new game needs its own, section 7)
- Gamepasses: VIP 399 (x1.25 money, x1.25 treadmill, gold [VIP] chat tag), +1 Egg Carry Slot 249, 2X Luck 199,
  Fast Recharge 179, 2X Money 149, 2X Speed 99.
- Products:
  - Cash packs (all scaled): Mega Cash 999, Huge Cash 499, Big Cash 199, Small Cash 25.
  - Exclusive pet "Royal Rex" 299: Robux only. It earns 3x the best pet in your zone, grows as you progress,
    never uses a slot, can't be sold, and has its own display stand that hides once owned.
  - Boosts: Skip to Next Zone 99, Treadmill Upgrade 125, Hatch All Now 39, 2X Money 15 min 29 (stacks), Starter
    Pack 28 (once), Instant Recharge 19.
  - Spins: 2 / 5 / 10 for 29 / 59 / 99.
- Shop tabs: Featured, Passes, Boosts, Cash, Spins.
- `Offers` pops contextual cards, e.g. "+1 Egg Slot" when you try to carry a 2nd egg.
- In Studio the place owner owns every pass, so they all show OWNED there. That is normal.

**Other**
- Tutorial (steps with arrows).
- Admin panel (UserId list): set / add speed and cash, max powers, give pet, grow eggs, teleport to zone, reset.
- Day / night clock pill.
- Zone atmosphere per zone.
- Low graphics setting; music playlist (licensed); settings sliders.

---

## 5. Config cheat sheet (what to change for a new game)

All in `ReplicatedStorage.Shared.Config`:

| Key | Change it to |
|---|---|
| `GameName` | New name. |
| `DataStoreName` | A new `<Name>_v1`. A new experience already gets a fresh DataStore, but rename anyway. |
| `GroupId`, `GroupName` | Kobe's group: currently 15308075 "low's group :)". |
| `Gamepasses`, `Products` | Set every `Id = 0` until Kobe creates them in the new experience. Id 0 = hidden / not set up. |
| `Zones`, `ZoneSlots`, `EggTypes`, `SpecialEggs`, `EggAssets` | New theme. |
| `Pets` (+ `REMAKE` mesh map), `Guardians` | New creatures. |
| `Rarities`, `RarityOrder`, `Mutations` | Usually keep. Rename only if the theme needs it. |
| `Powers`, `Bat`, `BearTrap` | Keep or re-skin to fit the twist. |
| `Treadmill`, `Trails`, `StepInterval`, `WalkSpeedFor`, `MaxWalkSpeed` | Keep (tuned). |
| `Daily`, `TimeRewards`, `Wheel`, `WheelFreeEvery`, `Codes`, `GroupReward`, `CommunityGift`, `StarterPack` | Fresh launch codes. |
| `FriendBoost`, `PremiumIncomeMult`, `VIP`, `MoneyBoost`, `OfflineMaxHours`, `FavoritePromptAfter` | Keep. |
| `GuardReactTime`, `GuardReturnMult`, `StealReach`, `BackpackSize` | Keep. |
| `UIAssets` | Kobe's uploaded icon image IDs; reusable across his games. |
| `Music`, `MainFontFace` | Licensed tracks; LuckiestGuy. |
| `ExclusivePetId` + the exclusive pet entry | One Robux-only showpiece per game. |

Also outside Config:
- `AdminServer` ADMINS: Kobe 4057805004, co-worker incogfal 2326255766.
- `Server.Leaderboards` store names.
- `DevGrants`: delete it.
- Sfx IDs in `Client.Sfx`.
- Map signs and stands.

---

## 6. Anticheat and security (keep these rules)

**AntiCheat**
- `ServerScriptService.AntiCheat` checks every player every 0.2 s:
  - Horizontal speed against `WalkSpeedFor(d.Speed)` x 1.3 + 8 (never against the client's WalkSpeed).
  - Rising faster than jumps allow.
  - Hovering without the Fly power for 7 s.
- A bad move is rubber-banded back. 8 strikes in a burst kicks. Strikes fade 1 per 15 s.
- Allowed windows are player attributes holding a server time (`workspace:GetServerTimeNow() + secs`):
  `ACGrace` (server teleports), `ACKnock` (knockbacks), `ACDash`, `ACFly`.
- **Any new code that teleports or flings a player must set one of these first**, or the anticheat will undo it.

**Security rules**
- Server validates everything: reach checks on steals, cooldowns on the server, receipt de-dupe, prompts refused
  when invalid (e.g. Skip Zone at the last zone, a second exclusive pet).
- Admin by UserId only. Never by username (names can be changed or re-registered).
- Studio-only test remotes are wrapped in `RunService:IsStudio()`.

**Free models**
- Always scan every inserted model for Scripts / LocalScripts / ModuleScripts before using it.
- The first bat model found had backdoor scripts named `Runtime` and `ScreenBuilder` (35 KB).
- Strip all scripts, keep the parts, record the asset ID and creator in DevNotes.

---

## 7. Playbook: making the next game from this template

**Step 0. Copy, never edit the original**
- In Studio, open "+1 Superpower for an Egg", then File > Save to Roblox As > **new experience** (or Save to File
  then publish as new).
- Work only in the copy. Check `list_roblox_studios` and use the copy's studio_id (ids change on every reconnect).

**Step 1. Clean the copy**
1. Rename `Config.GameName` and `DataStoreName`, and the leaderboard store names.
2. Set all gamepass / product IDs to 0. Delete `DevGrants`.
3. Delete `Workspace.AssetShowcase` / `CreatureShowcase` if present. Delete old backups in ServerStorage if you
   want a smaller file.
4. Start a new `ServerStorage.DevNotes` section for this game.

**Step 2. Theme**
1. Zones: names, colours, emojis, `AssetDecor`, `Backdrop`, `ZoneAtmosphere` entries, signs. Keep the corridor
   geometry, zone spacing and `SAFE_Z` unless the twist needs a different layout.
2. Eggs: new `EggAssets` or recoloured ones.
3. Creatures: new pets and guardians (section 9). A game needs roughly 8-17 pets per zone across the rarities
   that zone drops, plus 1 guardian per zone.
4. Base: plots, shop stands, signs, fonts (LuckiestGuy), studded classic look.
5. Exclusive Robux pet + its display stand (copy `RoyalStand`).

**Step 3. Twist** (section 8). Add it as a NEW module or script with its own Config block. Hook it into existing
systems through their public functions (`Net.On`, `Data.Push`, `Plots.GivePet`, `Steal.*`, `Rewards.Grant`,
`Logic.IncomeMult`) instead of rewriting them.

**Step 4. Monetise**
- Kobe creates the passes and products in the new experience (same list as section 4, plus any twist items) and
  sends the IDs. Wire them into `Config`, the `Economy` product handlers and the Shop tabs.
- Check each pass is On Sale.

**Step 5. Store page**
- ChatGPT prompts for the icon (1024 to 512) and 5 thumbnails (16:9), plus a description under 1000 characters.
- Use `claude/superpower-egg-store-page.md` as the model. Attach an in-game screenshot to each prompt.

**Step 6. Test in Studio**
- New-player run (tutorial, starter power, daily popup).
- Steal / chase / catch, hatch, sell, wheel spin, shop prompts.
- Mobile emulator.
- 2-player test (Test > Clients and Servers) for bat, traps and Friend Boost.
- Console must be clean.

**Step 7. Launch**
- Make a launch checklist doc for the new game in this project (copy `claude/superpower-egg-launch-checklist.md`).
- Creator Dashboard: questionnaire, icon, thumbnails, description, genre, devices, Public.
- Fresh codes. Experience notifications.

---

## 8. Twist ideas and where they plug in

Pick ONE strong twist that fits in a title like "+1 X every second" or "Steal a Y". Twists that change what you
steal, how you escape or what you get are best, because the loop stays the same.

| Twist | Integration |
|---|---|
| **Trend character** (e.g. "Steal a Jean Phil", Kobe's planned idea) | Re-skin pets + eggs + guardians; title rides the trend. Mostly `Config.Pets`, `Models`, art. |
| **"+1 X every second"** (+1 Speed / Jump / Size / Power every second) | A timer in `Data` adds to a new stat; `Logic.WalkSpeedFor`-style curve turns it into an ability. |
| **Growing egg / pet size** | Kg already exists. Make it visible: scale models by Kg, show weight on HUD, income from Kg. |
| **Day / night raids** | `DayNight` already raises a wall and sends players home; make guardians stronger at night with better eggs. |
| **Boss zone** | Last zone with a boss guardian that needs a team (Freeze Blast + Decoy) and drops a guaranteed top-rarity egg. |
| **Steal from players** | Let players steal pets / eggs from other plots (needs base locks or shields as products; very strong in this genre). |
| **Vehicles / mounts** | Rideable pets that add speed; fits the speed curve and the AntiCheat (raise the allowance via an attribute). |
| **Fusion / evolve** | 3 same pets become a higher mutation; use the `Mut` system and Rainbow look. |

Whatever the twist, keep these:
- Scaled rewards.
- The fair-catch rules.
- AntiCheat attributes.
- Server authority.
- Licensed audio.
- Owned stands hiding.
- The retention set (wheel, time rewards, daily, friend boost, offline earnings).

---

## 9. Art pipeline (creatures, icons, sounds)

### Creatures (sculpted, studded, rigged + animated meshes)
Source: `claude/creature-and-icon-pipeline-bundle.txt` (unpack instructions are at its top). It runs headless in
the cloud container with `pip install bpy` (Blender 5.x as a Python module), numpy, pillow and cairosvg.

**Library files**
- `sculpt.py`: base toolkit. Shapes bound to bones, studded baked texture, `Glow_*` meshes that Roblox shows as
  Neon. Game coords: x right, y up, front = -z.
- `kit.py`: body plans and animations for cute chunky creatures (quadrupeds, birds etc.).
- `detail.py`: faceted, fierce, armoured / royal / elemental detail (shard fur, plates, jaws with teeth,
  glowing eyes).
- `dino.py`: theropod skeleton and dino animations.

**Examples** (`creatures/*.py`): `moonbunny`, `nebulafox` (cute, `kit`); `lionemperor`, `sentinelraptor`
(detailed); `tyrantrex`, `stormptero` (dino / flyer). Each defines `build()` (and `anims()`), with
`c.extra["speed"]`, `hover` and an `aura(...)` for the rarity look.

**Steps**
1. Write `creatures/<id>.py`.
2. `python3 make.py <id> --render --export`, then look at the PNG renders and fix them before going on.
   `sheet.py` makes a contact sheet.
3. Add the ids to a batch in `batch_fbx.py`, run it with `bpy` to merge the FBXs (one per batch, 30 studs apart).
4. Run `gen_rbxmx.py` to make `out/CreatureData.rbxmx` (one ModuleScript per creature: animation clips, bone rest
   CFrames, batch layout).
5. Kobe imports the batch FBX with the Studio 3D Importer and inserts `CreatureData.rbxmx` (the MCP can't upload
   files from the container).
6. Run `ServerStorage.CreatureRigBuilder.Build()` to (re)build `ReplicatedStorage.CreatureMeshes`. Read its source
   for the exact expected import location before asking Kobe to import.
7. Set `Mesh = "<Name>"` on the pet / guardian in `Config`. `Models.Pet` and `Shared.CreatureAnimator` do the rest.

**Look Kobe wants**
- Sculpted meshes with a studded classic-Roblox surface, not voxel or part builds.
- Cute ones: plain flat black eyes.
- Fierce / royal ones: glowing angry eyes.
- Chunky proportions.
- Rarity aura particles.

**Alternatives** for quick decor: Studio `generate_mesh` (async; outputs are tagged
"AssistantAIGeneratedAsset"; prompt "tall steep cone" style shapes), or vetted Creator Store models (strip
scripts).

### UI icons
- `ui_icons/make_icons.py` (cairosvg) draws the cartoon icon style: thick dark outline, bevelled edge, glossy
  gradient, shine streaks. 512 px PNGs.
- Kobe uploads PNGs through the Asset Manager. Find their IDs with `search_asset` (scope user, assetType Image)
  and put them in `Config.UIAssets`. `upload_image` only takes http(s) URLs.
- Template image IDs: Index 135786636342008, Eggs 120857862351580, Pets 82587575444945, Speed 128296731928168,
  Cash 137126801654495, Codes 121635812339918, Powers 88802117561776 (reusable in Kobe's other games).
- `make_studs.py` makes the stud overlay tiles.

### Sounds (licensed only, high quality)
- Find them in Studio with `AssetService:SearchAudio(AudioSearchParams)`: `AudioSubType = SoundEffect`,
  `Artist = "Pro Sound Effects"` (or creator APMOfficial). Check each with `IsLoaded` / `TimeLength` before use.
- Add to the `Client.Sfx` LIB (`Name = {id, volume}`). Fanfares de-dupe within 0.8 s.
- IDs in use:
  - Wheel: WheelStart 9120657420, WheelTick 9120917861, WheelWin 1840076509.
  - Bat: BatSwing 9120972444, BatHit 9125380872.
  - Traps: TrapPlace 9116541944, TrapSnap 9113764330.
  - Treadmill wind loop: 9120697823.

---

## 10. Studio MCP working rules and gotchas (learned the hard way)

**Modes and datamodels**
- `execute_luau` has three datamodels:
  - **Edit**: change scripts and the map. Only works when NOT playing ("Edit datamodel is not available in Play
    mode" means stop play first).
  - **Server / Client**: test only.
- `insert_asset` and `multi_edit` are Edit-only.
- Kobe often tests in Studio himself. If Studio is in Play mode when you start, stop it and tell him.
- **studio_id changes on every reconnect.** Call `list_roblox_studios` when a call fails. A studio with
  name null / "Place is not open" means the place isn't open: ask Kobe to open it.

**Module copies**
- **Never require `ServerScriptService.Server` modules from `execute_luau` while playing.** You get a second copy;
  the second `Net` overwrites `Remotes.Request.OnServerInvoke` and breaks every request. Test through the
  remotes instead (Client: `ReplicatedStorage.Remotes.Request:InvokeServer("Spin")`), or fire
  `Remotes.Effect:FireClient(...)` from the Server datamodel.
- Client `execute_luau` also gets fresh module copies (`State.Data` is nil there). Read the PlayerGui / workspace
  instead.
- Edit-mode `require` caches modules: after editing a Shared module, test a fresh copy
  (`ReplicatedStorage.Shared:Clone()` into ServerStorage, require it, destroy it).

**Editing scripts**
- Edit big scripts by reading `.Source`, finding an exact chunk with `string.find(s, a, 1, true)`, splicing, and
  writing back. Assert the chunk was found.
- If the new code contains `]]` (e.g. `t[k[1]]`), wrap it in `[==[ ... ]==]`.
- `script_read` paths are `game.ServerScriptService.Server.Steal` etc.
- `script_grep` uses Lua patterns: no `|` alternation, escape `.` and `(`.

**Screenshots and input**
- `screen_capture` doesn't show CoreGui (Roblox hotbar, player list, purchase prompts).
- To frame a shot, run a RenderStepped loop that sets a Scriptable camera, stored in `_G.__camConn`.
  Disconnect it and set the camera back to Custom afterwards.
- Edit-mode captures can take `camera_position` / `look_at_position`.
- `user_mouse_input` with `instance_path` clicks HUD buttons reliably. Some panel buttons don't register: then
  test the server path by invoking the remote.

**Roblox behaviours to remember**
- Studio and the live game share the DataStore. Admin-boosted test stats leak into live unless `DataStoreName`
  changes before launch.
- `TextScaled` caps at 100 px; big world signs need SurfaceGui `SizingMode` PixelsPerStud.
- Some emoji don't render in LuckiestGuy (🪤, 👟): use text or images.
- `ScaleTo` on rotated models: compute the real bottom from part corners before placing.
- MeshPart `TextureID` is writable at runtime (used for the gold exclusive pet).
- Highlights: max 31 drawn at once.
- Models inside UI ViewportFrames still fire CollectionService tag signals. Filter on
  `IsDescendantOf(workspace)`, or their effects appear at world (0,0,0), the middle of the base.
- `Humanoid:MoveTo` leaves `MoveDirection` at zero.
- Avatars use AnimationConstraint joints.
- Partner: Kobe works with a co-worker whose own Claude edits the same place (e.g. `GroupReward`, the custom
  `Hotbar`). Read DevNotes and the current source before changing a script; don't overwrite their work.
- Log every change in `ServerStorage.DevNotes` (date, owner request, scripts touched, how it was tested).
- Restore any test changes made to Kobe's own data.

---

## 11. Benchmarks to beat (90th percentile, from a reference screenshot)

| Metric | 90th pct | What in the template targets it |
|---|---|---|
| Avg playtime | 19.5 min | Time rewards every 1-5 min early on, wheel every 8 min, goal bar, beacons, PvP. |
| D1 retention | 18.11% | Daily streak, offline earnings 8 h, favourite prompt, notifications (dashboard). |
| D7 retention | 4.78% | Long zone ladder, exclusive pets, index completion. |
| Payer conversion | 1.83% | Starter pack 28, contextual Offers, cheap boosts, egg slot pass. |
| ARPPU | 504 R$ | VIP 399, Mega Cash 999, Huge Cash 499, exclusive pet 299, all scaled. |
| Play-through | 5.80% | Icon + thumbnails + title (store-page doc). Trend names help. |

---

## 12. Kobe's preferences (apply by default)

**Style**
- Font: LuckiestGuy everywhere (`UIKit.fontPass`). Rarity titles may keep their own fonts.
- HUD like the reference simulator:
  - Left tiles: Shop, Index, Rewards with timers, plus the Slow Mode switch.
  - Right tiles: Spin, Eggs, Pets.
  - Codes pill and settings gear top-right.
  - Shiny cash / speed stats bottom-left with green + buttons.
  - Roblox Backpack hotbar for bat, trap and powers.
  - Goal bar, Friend Boost and Premium pills top-centre.
- Image icons, not spinning 3D icons. Classic studded look for base, zones and UI.

**Quality**
- High-quality licensed sounds only. No floating junk effects. Clean middle of the base.
- Stands for things a player already owns disappear for that player.
- Nothing annoying: no tripping / ragdoll from running into things (only from bat hits), no forced popups
  stacking.

**Communication**
- Ask for anything only Kobe can do (Robux IDs, uploads, imports, dashboard) in one clear list at the end of a
  reply.
- His style rule for writing he'll read: no em dashes, use commas.

**Project docs**
- Keep a launch checklist and a store-page doc per game in this project, updated as work lands.
