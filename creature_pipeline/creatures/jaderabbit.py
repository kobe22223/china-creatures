"""JADE RABBIT (Secret, Lantern Night Market): the moon rabbit. A round white rabbit with jade-green ears, paws
and a jade cloud swirl on its back, a glowing crescent moon on the forehead, a little jade mortar and pestle held
against its chest and a puffy tail. Cute: flat black eyes."""
from cn import *

WHITE, WHITE2, JADEC, JADEC2, PINK, MOON, MORTAR = (C(250, 252, 250), C(220, 240, 230), C(90, 200, 150), C(50, 150, 105),
                                                   C(255, 175, 190), C(255, 235, 140), C(120, 210, 170))


def build():
    c = Creature("JadeRabbit", height=6)
    swirl = cloud_filigree(JADEC, scale=1.4, width=0.08, only=lambda X, Y, Z: Y > 2.3)
    k = cute_quad(c, WHITE, belly=WHITE2, paw=JADEC, body=(1.4, 1.2, 1.65), leg_h=1.0, leg_r=0.44, head_r=1.3, head_up=0.6, tail=1, paint=swirl)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r * 1.05, r * 0.95, r * 0.98), WHITE, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.35, -r * 0.75), (0.5, 0.35, 0.35), WHITE2, "Head", seg=(14, 8))
    c.ellipsoid(h + P(0, -0.2, -r * 1.04), (0.14, 0.1, 0.08), PINK, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.eye(h + P(s * 0.5, 0.2, -r * 0.84), 0.23, P(s * 0.45, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.85, -0.25, -r * 0.6), (0.2, 0.12, 0.08), PINK, "Head", stud=False)
        # jade ears, leaning back so the silhouette stays round
        e0 = h + P(s * 0.45, r * 0.8, 0.15)
        c.tube([e0, e0 + P(s * 0.2, 1.0, 0.45), e0 + P(s * 0.3, 1.6, 0.9)], [0.32, 0.34, 0.16], JADEC, ["Head"], seg=10, flat=(1.0, 0.5))
        c.tube([e0 + P(0, 0.15, -0.12), e0 + P(s * 0.2, 1.0, 0.3), e0 + P(s * 0.28, 1.45, 0.72)], [0.16, 0.18, 0.08], WHITE2, ["Head"], seg=8, flat=(1.0, 0.4))
    # glowing crescent moon on the forehead
    pts = [h + P(math.sin(math.radians(a)) * 0.38, 0.72 + math.cos(math.radians(a)) * 0.3, -r * 0.9 - 0.1 * math.cos(math.radians(a))) for a in range(-100, 101, 25)]
    c.tube(pts, [0.04, 0.07, 0.1, 0.11, 0.11, 0.11, 0.1, 0.07, 0.04], MOON, ["Head"], seg=6, glow=True)
    # little jade mortar + pestle held against the chest
    mp = P(0, k["by"] - 0.35, -k["rz"] * 1.0)
    c.tube([mp + P(0, -0.3, 0), mp + P(0, 0.25, 0)], [0.3, 0.42], MORTAR, ["Chest"], seg=14, sub=1)
    c.torus(mp + P(0, 0.25, 0), 0.4, 0.06, GOLD, "Chest", seg=(16, 4), stud=False)
    c.tube([mp + P(0, 0.0, 0), mp + P(0.25, 0.85, -0.1)], [0.08, 0.1], WHITE2, ["Chest"], seg=8, sub=1)
    c.ellipsoid(P(0, k["by"] + 0.25, k["rz"] * 0.98), (0.42, 0.4, 0.35), WHITE, "Tail1", seg=(12, 8))
    aura(c, "orbit", (120, 230, 170), (255, 235, 140), "Secret")
    c.extra["speed"] = 1.2
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        if walking:   # bunny hop
            return {"Root": ((0, 0, 0), (0, 0.45 * abs(sin(p)), 0)), "ArmL": (30 * sin(p), 0, 0), "ArmR": (30 * sin(p), 0, 0),
                    "ThighL": (-30 * sin(p), 0, 0), "ThighR": (-30 * sin(p), 0, 0), "Chest": (-6 * sin(p), 0, 0)}
        return {"Head": (5 * sin(2 * p), 0, 10 * sin(p))}
    quad_anims(c, tail=1, stride=0, bob=0.0, extra=extra)


VARIANTS = {"Moonlit": {WHITE: C(200, 205, 240), WHITE2: C(170, 175, 225), JADEC: C(240, 220, 120), JADEC2: C(200, 170, 70), MORTAR: C(255, 220, 120)}}
