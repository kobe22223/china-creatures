"""JADE CICADA (Secret, Terracotta Tomb): a round carved-jade cicada. A plump pale-green jade body with darker
carved bands, a big wide head with two round bulging eye-domes, folded translucent jade wings with carved veins
on its back, short stubby legs and a glowing jade gem between the eyes. Cute: flat black eyes."""
from cn import *

JADEP, JADED, JADEL, WING, WING2, GEM = (C(150, 210, 170), C(90, 160, 120), C(200, 240, 210), C(185, 235, 205), C(110, 180, 140), C(120, 255, 190))


def build():
    c = Creature("JadeCicada", height=5)
    carve = stripes(JADED, "z", period=0.45, width=0.08, wobble=0.0)
    k = cute_quad(c, JADEP, belly=JADEL, paw=JADED, body=(1.35, 1.1, 1.9), leg_h=0.85, leg_r=0.36, head_r=1.25, head_up=0.25, tail=1, paint=carve)
    h, r = k["head"], k["head_r"]
    by, ry, rz = k["by"], k["ry"], k["rz"]
    c.ellipsoid(h, (r * 1.2, r * 0.85, r * 0.9), JADEP, "Head", seg=(24, 16))
    for s in (-1, 1):
        # bulging eye-domes at the sides, flat black eye on each
        c.ellipsoid(h + P(s * 1.05, 0.35, -0.35), (0.42, 0.42, 0.42), JADEL, "Head", seg=(14, 10))
        c.eye(h + P(s * 1.15, 0.38, -0.65), 0.24, P(s * 0.5, 0.05, -1), "Head")
        # middle pair of legs (decorative stubs) on the chest
        c.ellipsoid(P(s * k["lx"] * 1.1, 0.55, 0.0), (0.3, 0.45, 0.3), JADED, "Chest", seg=(12, 8))
    c.ellipsoid(h + P(0, 0.62, -r * 0.65), (0.17, 0.17, 0.12), GEM, "Head", seg=(10, 6), glow=True)
    c.ellipsoid(h + P(0, -0.4, -r * 0.72), (0.5, 0.3, 0.3), JADED, "Head", seg=(12, 8))   # carved mouth plate
    # folded wings on the back: two long leaf panels with carved vein stripes
    for s in (-1, 1):
        c.leaf(P(s * 0.4, by + ry * 1.02, -rz * 0.45), P(s * 0.22, -0.22, 1), P(1, 0, 0), rz * 1.5, 1.15, WING, ["Chest", "Hips"],
               thick=0.14, shape="feather", paint=stripes(WING2, "z", period=0.55, width=0.06, wobble=0.1))
    aura(c, "orbit", (120, 255, 190), (220, 255, 230), "Secret")
    c.extra["speed"] = 1.0
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        buzz = max(0, sin(math.pi * (t - 0.2) / 0.15)) if (not walking and 0.2 <= t <= 0.35) else 0.0
        return {"Chest": (2 * sin(16 * p) * buzz, 0, 0), "Head": (3 * sin(2 * p), 0, 6 * sin(p))}
    quad_anims(c, tail=1, stride=22, bob=0.08, extra=extra)


VARIANTS = {"Imperial": {JADEP: C(245, 240, 225), JADED: C(214, 150, 30), JADEL: C(255, 250, 240), WING: C(255, 230, 150), WING2: C(214, 150, 30), GEM: C(255, 80, 70)}}
