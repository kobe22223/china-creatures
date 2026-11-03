"""PEKINGESE (Secret, Forbidden City): a round fluffy golden Pekingese on short stubby legs, a long flowing coat of
soft puffs, a big round head with a flat dark muzzle, long feathered ears, a plumed tail curled over the back and a
gold imperial collar with a jade tassel. Cute: flat black eyes."""
from cn import *

FUR, FUR2, CREAM, MASK, NOSE, JADET = C(235, 180, 100), C(210, 145, 70), C(250, 230, 190), C(70, 50, 40), C(30, 24, 22), C(80, 190, 130)


def build():
    c = Creature("Pekingese", height=5)
    k = cute_quad(c, FUR, belly=CREAM, paw=CREAM, body=(1.5, 1.15, 1.75), leg_h=0.9, leg_r=0.45, head_r=1.35, head_up=0.5, tail=3)
    h, r = k["head"], k["head_r"]
    by, rx, ry, rz = k["by"], k["rx"], k["ry"], k["rz"]
    # long flowing coat: puffs over the body, longer at the sides
    puffs(c, P(0, by, 0), (rx * 1.05, ry * 1.05, rz), FUR, ["Hips", "Chest"], n=70, size=0.4, seed=71, col2=FUR2, mix=0.2, sink=0.75, where=lambda u: u[1] > -0.45)
    c.ellipsoid(h, (r * 1.08, r * 0.95, r * 0.95), FUR, "Head", seg=(24, 16))
    puffs(c, h, (r * 1.05, r * 0.95, r * 0.95), FUR, "Head", n=46, size=0.34, seed=72, col2=FUR2, mix=0.2, sink=0.7, where=lambda u: u[2] > -0.15 or u[1] > 0.55)
    # flat dark muzzle + cream cheeks
    c.ellipsoid(h + P(0, -0.3, -r * 0.82), (0.55, 0.4, 0.3), MASK, "Head", seg=(16, 10))
    c.ellipsoid(h + P(0, -0.18, -r * 1.05), (0.2, 0.14, 0.1), NOSE, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.62, -0.35, -r * 0.62), (0.45, 0.42, 0.4), CREAM, "Head", seg=(14, 8))
        c.eye(h + P(s * 0.52, 0.2, -r * 0.84), 0.26, P(s * 0.45, 0.05, -1), "Head")
        # long feathered ears hanging down
        c.ellipsoid(h + P(s * r * 0.98, -0.25, 0.05), (0.38, 0.85, 0.48), FUR2, "Head", rot=euler(0, 0, s * 12), seg=(14, 10))
    # plumed tail curled over the back
    t = P(0, by + 0.5, rz * 0.8)
    puffs(c, t + P(0, 0.55, -0.1), (0.62, 0.42, 0.75), CREAM, ["Tail2", "Tail3"], n=16, size=0.32, seed=75, col2=FUR, sink=0.2)
    # gold imperial collar with a jade tassel
    bib = P(0, by - 0.1, -rz * 0.98)
    c.ellipsoid(bib, (1.05, 0.32, 0.36), GOLD, "Chest", seg=(16, 8), stud=False)
    c.ellipsoid(bib + P(0, -0.25, -0.35), (0.18, 0.18, 0.18), JADET, "Chest", seg=(10, 6), stud=False)
    c.tube([bib + P(0, -0.38, -0.36), bib + P(0, -0.85, -0.36)], [0.08, 0.17], JADET, ["Chest"], seg=8, sub=1)
    aura(c, "orbit", (255, 210, 120), (80, 190, 130), "Secret")
    c.extra["speed"] = 1.0
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail2": (0, 0, 10 * sin(2 * p)), "Head": (4 * sin(2 * p), 0, 8 * sin(p))}
    quad_anims(c, tail=3, stride=26, bob=0.12, extra=extra)


VARIANTS = {"Snow": {FUR: C(250, 250, 248), FUR2: C(225, 225, 230), CREAM: C(255, 245, 230), MASK: C(70, 60, 70)}}
