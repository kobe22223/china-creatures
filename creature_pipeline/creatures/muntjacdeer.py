"""MUNTJAC DEER (Legendary, Tea Terraces): round little reddish-brown muntjac on short stubby legs, big head with a
cream muzzle, dark brow stripes, tiny two-point antlers on short pedicels, big soft ears angled out, a garland of
jade tea leaves around the neck and a white-tipped tail. Cute: flat black eyes."""
from cn import *

FUR, FUR2, CREAM, NOSE, ANTLER, TEA, TEA2, HOOFC = (C(200, 120, 70), C(140, 80, 45), C(250, 230, 200), C(40, 30, 30),
                                                    C(230, 210, 170), C(80, 170, 90), C(50, 130, 70), C(70, 50, 40))


def build():
    c = Creature("MuntjacDeer", height=6)
    k = cute_quad(c, FUR, belly=CREAM, paw=HOOFC, body=(1.4, 1.15, 1.75), leg_h=1.15, leg_r=0.4, head_r=1.25, head_up=0.6, tail=1)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r * 0.95, r * 1.0), FUR, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.35, -r * 0.72), (0.58, 0.45, 0.52), CREAM, "Head", seg=(16, 10))
    c.ellipsoid(h + P(0, -0.25, -r * 1.12), (0.18, 0.13, 0.1), NOSE, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.eye(h + P(s * 0.48, 0.22, -r * 0.84), 0.23, P(s * 0.45, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.25, 0.65, -r * 0.8), (0.08, 0.32, 0.06), FUR2, "Head", rot=euler(0, 0, s * 20), stud=False)   # brow stripe
        # big soft ears angled out and back, with cream insides
        e0 = h + P(s * 0.75, r * 0.55, 0.15)
        c.leaf(e0, P(s * 0.55, 0.85, 0.45), P(0, 0, 1), 0.72, 0.52, FUR, "Head", thick=0.18, shape="blade")
        c.leaf(e0 + P(0, 0.02, -0.08), P(s * 0.55, 0.85, 0.45), P(0, 0, 1), 0.55, 0.32, CREAM, "Head", thick=0.1, shape="blade")
        # tiny antlers: short furry pedicel + two small points
        a0 = h + P(s * 0.35, r * 0.85, 0.05)
        c.tube([a0, a0 + P(s * 0.05, 0.3, 0.05)], [0.12, 0.1], FUR, ["Head"], seg=8, sub=1)
        tip = a0 + P(s * 0.05, 0.3, 0.05)
        c.tube([tip, tip + P(s * 0.05, 0.38, 0.2)], [0.08, 0.03], ANTLER, ["Head"], seg=6, sub=1)
        c.tube([tip + P(0, 0.08, 0), tip + P(0, 0.22, -0.2)], [0.06, 0.02], ANTLER, ["Head"], seg=6, sub=1)
    # jade tea-leaf garland around the base of the neck
    nk = P(0, k["by"] + 0.15, -k["rz"] * 0.92)
    for j in range(7):
        a = math.radians(-75 + j * 25)
        p = nk + P(math.sin(a) * 1.0, -0.35 * math.cos(a), -math.cos(a) * 0.3)
        c.leaf(p, P(math.sin(a) * 0.4, -0.6, -1), P(math.cos(a), 0, 0), 0.55, 0.32, TEA if j % 2 else TEA2, "Chest", thick=0.1, shape="feather")
    # little tail, white underside
    t = P(0, k["by"] + 0.35, k["rz"] * 0.97)
    c.ellipsoid(t, (0.25, 0.4, 0.2), FUR, "Tail1", rot=euler(-30, 0, 0), seg=(10, 8))
    c.ellipsoid(t + P(0, -0.08, 0.12), (0.18, 0.3, 0.12), CREAM, "Tail1", rot=euler(-30, 0, 0), seg=(10, 8))
    aura(c, "sparkle", (110, 210, 130), (255, 220, 140), "Legendary")
    c.extra["speed"] = 1.15
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (20 * sin(4 * p), 0, 0), "Head": (3 * sin(2 * p), 0, 6 * sin(p))}
    quad_anims(c, tail=1, stride=28, bob=0.14, extra=extra)


VARIANTS = {"Silver": {FUR: C(170, 170, 180), FUR2: C(100, 100, 115), CREAM: C(240, 240, 248), TEA: C(255, 200, 60), TEA2: C(214, 32, 40)}}
