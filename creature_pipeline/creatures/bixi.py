"""BIXI (Celestial, Forbidden City): the dragon turtle that carries stone tablets. A round jade-green tortoise on
short stubby legs, a high domed shell with gold hexagon lines and a gold rim, a small carved stone stele on its
back, and a dragon head with swept horns, whiskers and glowing eyes. Royal: glowing eyes."""
from cn import *
from detail import V as GV, cracks

SKIN, SKIN2, SHELL, SHELL2, STONE, STONE2, WHISK, EYE = (C(80, 160, 120), C(55, 120, 90), C(40, 110, 85), C(255, 200, 60),
                                                        C(190, 190, 185), C(140, 140, 138), C(255, 215, 120), C(255, 200, 60))


def build():
    c = Creature("Bixi", height=7)
    k = cute_quad(c, SKIN, belly=C(230, 220, 170), paw=SKIN2, body=(1.55, 1.1, 1.8), leg_h=1.0, leg_r=0.5, head_r=0.9, head_up=0.25, tail=1)
    by, rx, ry, rz = k["by"], k["rx"], k["ry"], k["rz"]
    # high domed shell with gold hexagon lines and a gold rim
    c.ellipsoid(P(0, by + ry * 0.45, 0.1), (rx * 1.25, ry * 1.05, rz * 1.12), SHELL, ["Hips", "Chest"], seg=(28, 16),
                paint=cracks(SHELL2, scale=1.3, width=0.03))
    c.torus(P(0, by + ry * 0.1, 0.1), rx * 1.2, 0.17, SHELL2, ["Hips", "Chest"], rot=Matrix.Diagonal((1, rz * 1.12 / (rx * 1.25), 1)), seg=(32, 6), stud=False)
    # small carved stone stele standing on the shell
    st = P(0, by + ry * 1.45 + 0.35, 0.15)
    c.box(st, (0.62, 0.48, 0.16), STONE, ["Hips", "Chest"])
    c.ellipsoid(st + P(0, 0.48, 0), (0.66, 0.2, 0.2), STONE2, ["Hips", "Chest"], seg=(12, 6))
    for j in range(3):
        c.box(st + P(0, 0.22 - j * 0.22, -0.17), (0.38, 0.04, 0.02), STONE2, ["Hips", "Chest"], stud=False)   # carved lines
    # dragon head on a short neck, poking out from under the shell
    h = k["head"]
    hb = GV(-h.x, h.z, h.y) + GV(0, 0.0, 0.7)
    dragon_head(c, hb, 0.72, SKIN, C(230, 220, 170), SHELL2, WHISK, None, EYE, bone="Head", horns="swept", seed=95, brow=SKIN2)
    c.tube([P(0, by - 0.1, rz * 1.0), P(0, by - 0.3, rz * 1.4)], [0.2, 0.06], SKIN, ["Tail1"], seg=8, sub=1)
    aura(c, "orbit", (255, 200, 60), (80, 200, 140), "Celestial")
    c.extra["speed"] = 0.85
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Head": (4 * sin(2 * p), 0, 7 * sin(p))}
    quad_anims(c, tail=1, stride=20, bob=0.06, extra=extra)


VARIANTS = {"Obsidian": {SKIN: C(50, 50, 60), SKIN2: C(30, 30, 38), SHELL: C(25, 25, 32), STONE: C(240, 235, 220), STONE2: C(200, 190, 170)}}
