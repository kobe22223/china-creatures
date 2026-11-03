"""BLACK TORTOISE (Celestial, Heavenly Court): Xuanwu, guardian of the north. A round dark tortoise on short stubby
legs with a domed black shell lined in gold and a gold rim, a sturdy head with glowing teal eyes, and a jade-green
serpent coiled around the shell, raising its own head over the tortoise's. Royal: glowing eyes."""
from cn import *
from detail import V as GV, eyes_pair, E as GE, T as GT, cracks

SKIN, SKIN2, SHELL, GOLDT, SNAKE, SNAKE2, EYE = (C(60, 70, 85), C(40, 48, 60), C(25, 28, 38), C(255, 200, 60),
                                                C(60, 170, 120), C(230, 240, 200), C(80, 255, 220))


def build():
    c = Creature("BlackTortoise", height=7)
    k = cute_quad(c, SKIN, belly=C(140, 140, 120), paw=SKIN2, body=(1.55, 1.1, 1.8), leg_h=1.0, leg_r=0.5, head_r=1.05, head_up=0.3, tail=1)
    by, rx, ry, rz = k["by"], k["rx"], k["ry"], k["rz"]
    h, r = k["head"], k["head_r"]
    c.ellipsoid(P(0, by + ry * 0.45, 0.1), (rx * 1.25, ry * 1.05, rz * 1.12), SHELL, ["Hips", "Chest"], seg=(28, 16), paint=cracks(GOLDT, scale=1.3, width=0.03))
    c.torus(P(0, by + ry * 0.1, 0.1), rx * 1.2, 0.17, GOLDT, ["Hips", "Chest"], rot=Matrix.Diagonal((1, rz * 1.12 / (rx * 1.25), 1)), seg=(32, 6), stud=False)
    # tortoise head: rounded, with a beak line and glowing eyes
    c.ellipsoid(h, (r * 1.0, r * 0.88, r * 1.05), SKIN, "Head", seg=(22, 14))
    c.ellipsoid(h + P(0, -0.3, -r * 0.82), (0.45, 0.12, 0.25), SKIN2, "Head", seg=(10, 6), stud=False)
    hg = GV(-h.x, h.z, h.y)
    eyes_pair(c, hg + GV(0, 0.18, -r * 0.82), 0.42, 0.22, "Head", glow=EYE, core=C(220, 255, 245), brow=SKIN2, slant=18, turn=0.5)
    # serpent coiled around the shell, rising over the back
    coil = []
    for i in range(14):
        a = i / 14 * math.tau * 1.15 + 0.5
        coil.append(P(math.sin(a) * rx * 1.3, by + ry * 0.25 + i * 0.07, 0.1 + math.cos(a) * rz * 1.18))
    rise = [coil[-1] + P(0, 0.6, -0.3), P(0.2, by + ry * 1.9, -rz * 0.2), P(0.1, by + ry * 2.4, -rz * 0.7)]
    c.bone("Snake1", coil[0], coil[7], "Chest")
    c.bone("Snake2", coil[7], rise[1], "Snake1")
    c.bone("SnakeHead", rise[1], rise[2], "Snake2")
    c.tube(coil + rise, [0.18] + [0.3] * 12 + [0.32] * 3 + [0.34], SNAKE, ["Snake1", "Snake2"], seg=10, paint=band(SNAKE2, -10, by + ry * 0.2))
    sh_ = rise[2]
    c.ellipsoid(sh_ + P(0, 0.05, -0.25), (0.42, 0.3, 0.55), SNAKE, "SnakeHead", seg=(14, 8))
    sg = GV(-sh_.x, sh_.z, sh_.y)
    eyes_pair(c, sg + GV(0, 0.18, -0.45), 0.22, 0.13, "SnakeHead", glow=EYE, core=C(220, 255, 245), brow=None, slant=20, turn=0.6)
    c.tube([sh_ + P(0, -0.08, -0.75), sh_ + P(0, -0.1, -1.1)], [0.04, 0.03], C(220, 40, 60), ["SnakeHead"], seg=5, sub=1)   # tongue
    c.tube([P(0, by - 0.1, rz * 1.0), P(0, by - 0.3, rz * 1.4)], [0.2, 0.06], SKIN, ["Tail1"], seg=8, sub=1)
    aura(c, "orbit", (80, 255, 220), (60, 70, 120), "Celestial")
    c.extra["speed"] = 0.85
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Head": (4 * sin(2 * p), 0, 6 * sin(p)), "Snake2": (6 * sin(p), 12 * sin(p + 1), 0), "SnakeHead": (8 * sin(2 * p), 10 * sin(p + 2), 0)}
    quad_anims(c, tail=1, stride=20, bob=0.06, extra=extra)


VARIANTS = {"Frost": {SHELL: C(200, 225, 245), SKIN: C(150, 175, 200), SKIN2: C(110, 135, 165), GOLDT: C(60, 110, 200), SNAKE: C(240, 245, 255)}}
