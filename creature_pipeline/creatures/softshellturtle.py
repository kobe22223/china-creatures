"""SOFTSHELL TURTLE (Mythic, Jade River): round olive softshell turtle with a big soft spotted shell, a big head
with a little snorkel nose, short webbed stubby legs and a pink lotus flower growing on its back. Cute: flat black eyes."""
from cn import *

SKIN, SKIN2, SHELL, SPOT, BELLY, PINK, PINK2, LOTUSC, LEAFC = (C(150, 170, 100), C(115, 135, 75), C(120, 140, 80), C(85, 100, 55),
                                                               C(240, 225, 170), C(255, 160, 190), C(240, 110, 150), C(255, 215, 80), C(70, 160, 90))


def build():
    c = Creature("SoftshellTurtle", height=5.5)
    k = cute_quad(c, SKIN, belly=BELLY, paw=SKIN2, body=(1.45, 1.0, 1.65), leg_h=0.9, leg_r=0.42, head_r=1.15, head_up=0.25, tail=1)
    h, r = k["head"], k["head_r"]
    by, rx, ry, rz = k["by"], k["rx"], k["ry"], k["rz"]
    # big soft shell disc with a spotted top and a flared rim
    c.ellipsoid(P(0, by + ry * 0.35, 0.1), (rx * 1.3, ry * 0.75, rz * 1.15), SHELL, ["Hips", "Chest"], seg=(28, 14),
                paint=spots(SPOT, size=0.42, density=0.32, seed=7))
    c.torus(P(0, by + ry * 0.2, 0.1), rx * 1.18, 0.16, SKIN, ["Hips", "Chest"], rot=Matrix.Diagonal((1, rz * 1.15 / (rx * 1.3), 1)), seg=(32, 6))
    c.ellipsoid(h, (r, r * 0.92, r), SKIN, "Head", seg=(24, 16))
    c.tube([h + P(0, -0.05, -r * 0.85), h + P(0, -0.02, -r * 1.3)], [0.22, 0.14], SKIN2, ["Head"], seg=10, sub=1)   # snorkel nose
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.06, 0.0, -r * 1.33), (0.04, 0.05, 0.03), C(30, 30, 30), "Head", stud=False)
        c.eye(h + P(s * 0.48, 0.2, -r * 0.82), 0.22, P(s * 0.45, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.75, -0.3, -r * 0.55), (0.18, 0.1, 0.08), PINK, "Head", stud=False)
    # lotus on the back: leaf pad + petals + gold centre
    lt = P(0, by + ry * 1.05, 0.25)
    c.ellipsoid(lt + P(0, -0.05, 0), (0.8, 0.08, 0.8), LEAFC, ["Hips", "Chest"], seg=(18, 6))
    for j in range(8):
        a = j / 8 * math.tau
        c.leaf(lt + P(math.sin(a) * 0.15, 0.05, math.cos(a) * 0.15), P(math.sin(a), 1.1, math.cos(a)), P(math.cos(a), 0, -math.sin(a)),
               0.62, 0.36, PINK if j % 2 else PINK2, ["Hips", "Chest"], thick=0.1, shape="feather")
    c.ellipsoid(lt + P(0, 0.2, 0), (0.18, 0.12, 0.18), LOTUSC, ["Hips", "Chest"], seg=(10, 6), stud=False)
    c.tube([P(0, by - 0.1, rz * 1.0), P(0, by - 0.3, rz * 1.35)], [0.16, 0.05], SKIN, ["Tail1"], seg=8, sub=1)
    aura(c, "orbit", (255, 160, 190), (110, 210, 140), "Mythic")
    c.extra["speed"] = 0.9
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Head": (4 * sin(2 * p), 0, 8 * sin(p)), "Neck": (0, 10 * sin(p) if not walking else 0, 0)}
    quad_anims(c, tail=1, stride=20, bob=0.06, extra=extra)


VARIANTS = {"Golden": {SKIN: C(235, 195, 90), SKIN2: C(200, 150, 50), SHELL: C(214, 32, 40), SPOT: C(255, 200, 60)}}
