"""BAI ZE (Celestial, Kunlun Immortal Peaks): the wise white beast of the mountains. A round white lion-goat on
short stubby legs with blue and gold cloud swirl paint, a big head with two curled gold horns, a flowing white
goat beard and mane tufts, blue flame tufts at its elbows and tail, and glowing gold eyes. Royal: glowing eyes."""
from cn import *
from detail import V as GV, E, fur, fur_line, eyes_pair, ram_horn

WHITE, WHITE2, BLUE, GOLDH, MUZ, FLAME, EYE = (C(248, 248, 252), C(215, 222, 240), C(70, 120, 210), C(255, 205, 70),
                                              C(235, 235, 245), C(110, 180, 255), C(255, 215, 60))


def build():
    c = Creature("BaiZe", height=6.5)
    swirl = cloud_filigree(BLUE, scale=1.4, width=0.07)
    k = cute_quad(c, WHITE, belly=WHITE2, paw=GOLDH, body=(1.5, 1.22, 1.8), leg_h=1.15, leg_r=0.46, head_r=1.25, head_up=0.6, tail=2, paint=swirl)
    h, r = k["head"], k["head_r"]
    hg = GV(-h.x, h.z, h.y)
    E(c, hg, (r * 1.02, r * 0.95, r), WHITE, "Head", seg=(18, 14))
    E(c, hg + GV(0, -0.3, -r * 0.8), (0.62, 0.45, 0.55), MUZ, "Head", seg=(12, 8))
    for s in (-1, 1):
        E(c, hg + GV(s * 0.2, -0.22, -r * 1.3), (0.08, 0.06, 0.05), C(60, 70, 110), "Head", stud=False)
        ram_horn(c, hg + GV(s * 0.62, r * 0.82, -0.1), s, 0.6, GOLDH, "Head", turns=0.85, out=0.3, yaw=20)
        E(c, hg + GV(s * 1.0, 0.25, 0.05), (0.38, 0.16, 0.24), WHITE2, "Head", rot=(0, 0, s * -35), seg=(8, 6))
    eyes_pair(c, hg + GV(0, 0.2, -r * 0.85), 0.48, 0.25, "Head", glow=EYE, core=C(255, 250, 220), brow=WHITE2, slant=16, turn=0.5)
    fur_line(c, [hg + GV(-0.3, -0.72, -0.85), hg + GV(0.3, -0.72, -0.85)], WHITE, "Head", length=0.85, width=0.38, out=GV(0, -1, 0.15), n_per=5, seed=101)
    fur(c, hg + GV(0, 0.15, 0.3), (r * 0.95, r * 0.9, r * 0.6), WHITE2, "Head", n=40, length=0.55, width=0.45, flow=GV(0, -0.3, 1), where=lambda u, p: u.z > 0.1 and u.y > -0.3, seed=102, lift=0.25)
    # blue flame tufts at the elbows
    for s, S in ((-1, "L"), (1, "R")):
        base = P(s * k["lx"] * 1.35, k["by"] - 0.5, k["sz"] + 0.2)
        for j in range(3):
            c.leaf(base, P(s * 0.5, 0.2 + 0.3 * j, 0.8), P(0, 1, 0), 0.6, 0.3, FLAME, "Arm" + S, thick=0.08, shape="flame", glow=True)
    t = P(0, k["by"] + 0.25, k["rz"] * 0.95)
    c.tube([t, t + P(0, 0.3, 0.4), t + P(0, 0.65, 0.55)], [0.16, 0.14, 0.1], WHITE, ["Tail1", "Tail2"], seg=8)
    for j in range(3):
        c.leaf(t + P(0, 0.6, 0.55), P((j - 1) * 0.4, 0.8, 0.5), P(1, 0, 0), 0.75, 0.4, FLAME, "Tail2", thick=0.08, shape="flame", glow=True)
    aura(c, "orbit", (110, 180, 255), (255, 215, 60), "Celestial")
    c.extra["speed"] = 1.2
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Head": (5 * sin(2 * p), 0, 6 * sin(p)), "Tail1": (0, 0, 14 * sin(2 * p))}
    quad_anims(c, tail=2, stride=26, bob=0.12, extra=extra)


VARIANTS = {"Dusk": {WHITE: C(70, 60, 110), WHITE2: C(50, 42, 85), MUZ: C(110, 100, 150), BLUE: C(255, 160, 80), FLAME: C(255, 140, 60)}}
