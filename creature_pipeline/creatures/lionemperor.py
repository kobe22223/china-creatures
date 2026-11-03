"""LION EMPEROR (Divine, royal): golden lion with a huge layered shard mane, gold crown with sapphires,
gold pauldrons and chest plate, a red royal cape with gold trim, glowing golden eyes and a roaring mouth."""
from detail import *

FUR, FUR2, CREAM, MANE, MANE2, MANE3, GOLD, GOLD2, GEM, CAPE, NOSE, CLAW = (
    C(240, 186, 102), C(214, 152, 74), C(252, 228, 180), C(206, 104, 34), C(150, 62, 26), C(244, 150, 46),
    C(255, 206, 60), C(214, 150, 30), C(70, 160, 255), C(186, 28, 48), C(70, 40, 35), C(250, 245, 230))


def build():
    c = detailed("LionEmperor", height=10)
    k = beast(c, sh=3.85, hip=3.6, L=1.9, W=1.15, neck=(0.9, 0.9), head=1.6, tail=4, tail_len=0.95, tail_lift=0.2)
    sh, hip, cz, hz, hb, mid = k["sh"], k["hip"], k["cz"], k["hz"], k["hb"], k["mid"]
    TB = ["Hips", "Chest"]
    T(c, [V(0, hip, hz + 0.8), V(0, hip, hz), V(0, mid.y, 0), V(0, sh, cz), V(0, sh + 0.2, cz - 0.5)], [0.8, 1.12, 1.15, 1.25, 1.05], FUR, TB, seg=9)
    E(c, V(0, mid.y - 0.6, -0.3), (0.95, 0.5, 2.0), CREAM, TB)
    # ---- royal cape over the back, gold chest plate, pauldrons
    shell(c, V(0, mid.y + 0.05, 0.45), (1.32, 1.25, 1.9), CAPE, TB, th=(-180, 180), ph=(32, 90), seg=(12, 3), trim=GOLD, thick=0.12, inset=0.08)
    for s in (-1, 1):
        shell(c, V(0, mid.y + 0.05, 0.45), (1.32, 1.25, 1.9), CAPE, TB, th=(40, 140) if s > 0 else (-140, -40), ph=(-25, 34), seg=(6, 3), thick=0.1)
        shell(c, V(0, mid.y + 0.05, 0.45), (1.36, 1.29, 1.94), GOLD, TB, th=(40, 140) if s > 0 else (-140, -40), ph=(-30, -22), seg=(6, 1), thick=0.1)
    E(c, V(0, mid.y + 1.36, 0.45), (0.28, 0.12, 0.28), GEM, TB, seg=(8, 4), glow=True)
    shell(c, V(0, sh - 0.25, cz - 0.3), (1.15, 1.18, 0.98), GOLD, "Chest", th=(-58, 58), ph=(-55, 30), trim=GOLD2)
    BOX(c, V(0, sh - 0.25, cz - 1.42), (0.22, 0.22, 0.08), GEM, "Chest", rot=(0, 0, 45), glow=True)
    # ---- legs with big paws, white claws, elbow tufts
    for s, X in ((-1, "L"), (1, "R")):
        for front in (True, False):
            b = leg(c, k, X, FUR, r=(0.68, 0.52, 0.44) if front else (0.74, 0.52, 0.42), paw_col=FUR, paw=(0.66, 0.38, 0.85), front=front)
            lo = "Fore" + X if front else "Shin" + X
            ft = k["paw" + X] if front else k["foot" + X]
            claws3(c, ft + V(0, 0, -0.15), CLAW, lo, size=0.26)
            cuff(c, b.lerp(ft, 0.55), b.lerp(ft, 0.75), 0.45, GOLD, lo, thick=0.09, seg=8, flare=0.02)
            fur_line(c, [b + V(0, 0.1, 0.2), b + V(0, -0.2, 0.35)], FUR2, lo, length=0.55, width=0.38, out=V(0, -0.4, 1), n_per=3, seed=41 + s + front)
        sho = k["sho" + X]
        shell(c, sho + V(s * 0.15, 0.35, 0), (0.85, 0.75, 0.95), GOLD, "Arm" + X, th=(20, 160) if s > 0 else (-160, -20), ph=(-10, 85), trim=GOLD2)
        E(c, sho + V(s * 0.95, 0.55, 0), (0.1, 0.18, 0.18), GEM, "Arm" + X, seg=(6, 4), glow=True)
        S(c, sho + V(s * 0.6, 1.0, 0), sho + V(s * 0.85, 1.55, 0.1), 0.18, GOLD2, "Arm" + X, stud=False)
    # ---- head: skull, cream muzzle, roaring jaw, glowing eyes
    T(c, [V(0, sh, cz), k["nb"], hb + V(0, -0.1, 0.2)], [1.05, 0.9, 0.75], FUR, ["Chest", "Neck"], seg=8)
    E(c, hb + V(0, 0.0, -0.45), (0.86, 0.8, 0.86), FUR, "Head")
    E(c, hb + V(0, -0.3, -1.15), (0.62, 0.42, 0.55), CREAM, "Head")
    E(c, hb + V(0, 0.32, -0.95), (0.7, 0.2, 0.32), FUR2, "Head")
    E(c, hb + V(0, -0.1, -1.62), (0.24, 0.16, 0.14), NOSE, "Head", stud=False)
    for s in (-1, 1):
        E(c, hb + V(s * 0.6, 0.62, -0.15), (0.24, 0.26, 0.15), FUR2, "Head")
    E(c, hb + V(0, -0.98, -1.0), (0.5, 0.2, 0.6), CREAM, "Jaw", rot=(-12, 0, 0))
    maw(c, hb + V(0, -0.62, -1.5), 0.42, 0.7, 0.55, "Head", "Jaw", n=8, tooth=0.17, fangs=2.2)
    eyes_pair(c, hb + V(0, 0.15, -1.08), 0.38, 0.23, "Head", glow=C(255, 215, 50), core=C(255, 250, 200), brow=FUR2, slant=22, turn=0.4)
    # ---- mane: two shard layers radiating out and back around the face
    mc = hb + V(0, -0.1, -0.05)
    rad_flow = lambda p, n: (p - mc).normalized() * 0.5 + V(0, -0.1, 1)
    fur(c, mc, (1.45, 1.45, 1.05), MANE2, ["Neck", "Head"], n=170, length=1.35, width=0.72, flow=rad_flow, where=lambda u, p: u.z > -0.5, col2=MANE, mix=0.3, seed=43, lift=0.65)
    fur(c, mc + V(0, 0, -0.25), (1.2, 1.2, 0.85), MANE3, ["Neck", "Head"], n=110, length=0.9, width=0.55, flow=rad_flow, where=lambda u, p: -0.62 < u.z < 0.2, col2=MANE, mix=0.4, seed=44, lift=0.8)
    fur(c, k["nb"] + V(0, -0.2, 0.1), (1.15, 1.1, 1.0), MANE2, ["Chest", "Neck"], n=60, length=1.1, width=0.6, flow=V(0, -0.6, 0.6), where=lambda u, p: u.y < 0.2, col2=MANE, seed=45)
    crown(c, hb + V(0, 0.98, -0.3), 0.55, 0.36, GOLD, "Head", n=5, gem=GEM, tall=1.7, tilt=(-8, 0, 0))
    # ---- tail with a mane tuft and gold ring
    tp = k["tail"]
    T(c, tp, [0.3, 0.26, 0.22, 0.18, 0.14], FUR, ["Tail%d" % (i + 1) for i in range(4)], seg=7)
    fur(c, tp[-1], (0.45, 0.45, 0.55), MANE2, "Tail4", n=36, length=0.75, width=0.45, flow=(tp[-1] - tp[-2]).normalized(), col2=MANE, seed=47, lift=0.6)
    cuff(c, tp[-2].lerp(tp[-1], 0.3), tp[-2].lerp(tp[-1], 0.6), 0.2, GOLD, "Tail4", thick=0.08, seg=8)
    aura(c, "sparkle", (255, 215, 60), (255, 255, 220), "Divine")
    c.extra["speed"] = 1.0
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        if walking:
            return {"Jaw": (-4 - 4 * max(0, sin(2 * p)), 0, 0)}
        roar = max(0, sin(math.pi * (t - 0.5) / 0.32)) if 0.5 <= t <= 0.82 else 0.0
        return {"Jaw": (-3 - 26 * roar, 0, 0), "Head": (14 * roar + 3 * sin(2 * p), 0, 4 * sin(p) * (1 - roar)), "Neck": (2 * sin(p) + 6 * roar, 14 * sin(p) * (1 - roar), 0)}
    quad_anims(c, tail=4, stride=24, bob=0.12, head_amp=0.8, extra=extra)

