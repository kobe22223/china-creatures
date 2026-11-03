"""AZURE DRAGON (Zone 11 guardian, Godly): Qinglong, guardian of the east. A colossal long serpentine dragon in
azure-blue scales with jade and gold edges, a pearl belly, a white flowing mane, spiny gold back fins, branched gold
antlers, long whiskers, roaring jaws and glowing jade angry eyes, with glowing white cloud trails curling around its
legs and body. Hovers. Fierce."""
from cn import *
from detail import V, B, E

AZURE, AZURE2, BELLY, MANE, GOLDA, WHISK, CLOUDC, CLAWC = (C(40, 120, 220), C(25, 80, 165), C(235, 245, 250), C(245, 250, 255),
                                                          C(255, 200, 60), C(255, 245, 220), C(230, 245, 255), C(250, 245, 230))


def build():
    c = Creature("AzureDragon", height=18)
    c.stud = c.height / 44 * 0.55
    c.stud_k = 0.65
    k = serpent_dragon(c, AZURE, BELLY, MANE, CLAWC, GOLDA, WHISK, C(90, 255, 180), L=17.0, n=8, y0=6.0, wave=1.5, rise=1.0,
                       paint=scale_paint(C(80, 210, 170), size=0.75, width=0.06), horns="antler", fins=GOLDA, seed=171, brow=AZURE2,
                       core=C(220, 255, 240))
    pts, radii, names, R = k["pts"], k["radii"], k["names"], k["R"]
    # glowing cloud trails: soft puffs swirling around the legs and along the body
    for bone in ("ArmL", "ArmR", "ThighL", "ThighR"):
        hd = c.bone_pos(bone, "tail")
        puffs(c, hd + P(0, 0.2, 0.3), (0.7, 0.4, 0.9), CLOUDC, bone, n=10, size=0.32, seed=sum(map(ord, bone)), sink=0.1)
    for i in (2, 4, 6):
        p = pts[i]
        for j in range(5):
            a = j / 5 * math.tau
            q = p + V(math.sin(a) * radii[i] * 1.5, math.cos(a) * radii[i] * 1.3 - radii[i] * 0.4, j * 0.25)
            E(c, q, (R * 0.42, R * 0.32, R * 0.5), CLOUDC, names[i], seg=(10, 6), glow=(j % 2 == 0))
    aura(c, "orbit", (90, 255, 180), (40, 120, 220), "Godly")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.2
    return c


def anims(c):
    serpent_anims(c, ["Spine%d" % (i + 1) for i in range(8)], amp=10, hover=0.8)


VARIANTS = {"Jade": {AZURE: C(40, 170, 110), AZURE2: C(25, 120, 75), GOLDA: C(255, 255, 255), MANE: C(255, 220, 120)}}
