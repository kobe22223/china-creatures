"""CRAB GENERAL (Celestial, Dragon King's Palace): a round red crab commander. A wide round shell body on short
stubby legs, eye stalks with flat black eyes, two big chunky claws that snap, a gold general's helmet with a red
plume and a little gold armour sash across the shell. Cute: flat black eyes."""
from cn import *

RED_, RED3, BELLY, GOLDC, PLUME, TIP = C(225, 60, 45), C(175, 35, 30), C(255, 200, 170), C(255, 200, 60), C(214, 32, 40), C(60, 30, 30)


def build():
    c = Creature("CrabGeneral", height=5.5)
    k = cute_quad(c, RED_, belly=BELLY, paw=RED3, body=(1.9, 1.05, 1.45), leg_h=0.85, leg_r=0.32, head_r=0.75, head_up=0.0, tail=0, spread=0.75)
    by, rx, ry, rz = k["by"], k["rx"], k["ry"], k["rz"]
    c.shapes = [sh for sh in c.shapes if not (set(sh["bones"]) <= {"Head", "Neck"})]   # the head sits inside the shell
    # extra stubby side legs (decor)
    for s in (-1, 1):
        for z in (-0.1, 0.45):
            c.tube([P(s * rx * 0.85, by - 0.35, z), P(s * (rx + 0.45), by - 0.6, z + 0.05), P(s * (rx + 0.55), 0.2, z + 0.1)], [0.22, 0.18, 0.12], RED3, ["Chest"], seg=8)
    # eye stalks on top of the front edge of the shell
    for s in (-1, 1):
        st = P(s * 0.45, by + ry * 0.9 + 0.35, -rz * 0.7)
        c.tube([P(s * 0.4, by + ry * 0.55, -rz * 0.65), st], [0.16, 0.13], RED_, ["Head"], seg=8, sub=1)
        c.ellipsoid(st, (0.3, 0.3, 0.28), RED_, "Head", seg=(12, 8))
        c.eye(st + P(s * 0.05, 0.02, -0.28), 0.22, P(s * 0.3, 0.05, -1), "Head")
    c.ellipsoid(P(0, by - 0.05, -rz * 0.95), (0.35, 0.12, 0.08), RED3, "Chest", stud=False)   # little smile
    # big chunky claws on their own bones
    for s, S in ((-1, "L"), (1, "R")):
        a0 = P(s * rx * 0.75, by, -rz * 0.6)
        e0 = a0 + P(s * 0.55, 0.15, -0.65)
        c.bone("Claw" + S, a0, e0, "Chest")
        c.bone("Pincer" + S, e0, e0 + P(0, 0.3, -0.8), "Claw" + S)
        c.tube([a0, e0], [0.3, 0.35], RED_, ["Claw" + S], seg=10, sub=1)
        c.ellipsoid(e0 + P(0, 0.05, -0.45), (0.62, 0.55, 0.7), RED_, "Claw" + S, seg=(16, 10))
        c.spike(e0 + P(0, 0.2, -0.85), e0 + P(-s * 0.05, 0.3, -1.4), 0.3, TIP, "Claw" + S, seg=6, n=3)
        c.spike(e0 + P(0, -0.1, -0.85), e0 + P(-s * 0.05, -0.35, -1.25), 0.24, TIP, "Pincer" + S, seg=6, n=3)
    # gold general's helmet with a red plume + armour sash
    hp = P(0, by + ry * 0.95, 0.0)
    c.ellipsoid(hp, (0.75, 0.32, 0.65), GOLDC, ["Chest"], seg=(16, 8), stud=False)
    c.tube([hp + P(0, 0.25, 0), hp + P(0, 0.7, 0.05)], [0.08, 0.06], GOLDC, ["Chest"], seg=6, sub=1, stud=False)
    for j in range(3):
        c.leaf(hp + P(0, 0.65, 0.05), P((j - 1) * 0.3, 1, 0.55), P(1, 0, 0), 0.75, 0.32, PLUME, "Chest", thick=0.12, shape="feather", curl=0.15)
    c.ellipsoid(P(0, by + ry * 0.35, 0.1), (rx * 1.02, 0.18, rz * 0.7), GOLDC, ["Chest", "Hips"], rot=euler(0, 0, 18), seg=(20, 6), stud=False)
    aura(c, "orbit", (255, 100, 70), (255, 200, 60), "Celestial")
    c.extra["speed"] = 1.0
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        snap = max(0, sin(math.pi * (t - 0.5) / 0.2)) if (not walking and 0.5 <= t <= 0.7) else 0.0
        return {"ClawL": (8 * sin(2 * p), 0, -6 * sin(p)), "ClawR": (8 * sin(2 * p + 1), 0, 6 * sin(p)),
                "PincerL": (-25 * snap - 6 * max(0, sin(4 * p)), 0, 0), "PincerR": (-25 * snap - 6 * max(0, sin(4 * p + 1)), 0, 0),
                "Root": ((0, 0, 4 * sin(2 * p)) if walking else (0, 0, 0), (0, 0.05 * abs(sin(2 * p)), 0))}
    quad_anims(c, tail=0, stride=18, bob=0.06, extra=extra)


VARIANTS = {"Azure": {RED_: C(60, 120, 220), RED3: C(35, 80, 170), BELLY: C(210, 230, 255), PLUME: C(255, 200, 60)}}
