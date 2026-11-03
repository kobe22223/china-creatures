"""XIEZHI (Divine, Forbidden City): the one-horned beast of justice. A round midnight-blue beast on short stubby
legs with gold cloud swirl paint, a big lion-goat head with a single swept-forward gold horn, a white shard mane
and beard, gold hooves and a tufted tail. Royal: glowing eyes."""
from cn import *
from detail import V as GV, E, fur, fur_line, eyes_pair, swept_horn

NAVY, NAVY2, WHITEM, GOLDH, MUZ, EYE = C(40, 55, 110), C(28, 38, 80), C(240, 240, 250), C(255, 200, 60), C(70, 90, 150), C(120, 220, 255)


def build():
    c = Creature("Xiezhi", height=6.5)
    swirl = cloud_filigree(GOLDH, scale=1.4, width=0.07)
    k = cute_quad(c, NAVY, belly=NAVY2, paw=GOLDH, body=(1.5, 1.22, 1.8), leg_h=1.15, leg_r=0.46, head_r=1.25, head_up=0.6, tail=2, paint=swirl)
    h, r = k["head"], k["head_r"]
    hg = GV(-h.x, h.z, h.y)                               # head centre in game space
    E(c, hg, (r * 1.02, r * 0.95, r), NAVY, "Head", seg=(18, 14))
    E(c, hg + GV(0, -0.3, -r * 0.8), (0.62, 0.45, 0.55), MUZ, "Head", seg=(12, 8))
    for s in (-1, 1):
        E(c, hg + GV(s * 0.2, -0.22, -r * 1.3), (0.08, 0.06, 0.05), C(15, 15, 30), "Head", stud=False)
        E(c, hg + GV(s * 0.95, 0.35, 0.1), (0.4, 0.18, 0.25), NAVY2, "Head", rot=(0, 0, s * -30), seg=(8, 6))   # ears
    eyes_pair(c, hg + GV(0, 0.2, -r * 0.85), 0.48, 0.25, "Head", glow=EYE, core=C(230, 250, 255), brow=NAVY2, slant=18, turn=0.5)
    # single gold horn sweeping forward from the forehead
    swept_horn(c, [hg + GV(0, r * 0.75, -0.35), hg + GV(0, r * 1.3, -0.45), hg + GV(0, r * 1.65, -0.95)], 0.28, GOLDH, "Head", seg=7, ribs=True)
    # white mane around the head + beard
    fur(c, hg + GV(0, 0.05, 0.1), (r * 1.02, r * 0.98, r * 0.8), WHITEM, "Head", n=60, length=0.55, width=0.5, flow=GV(0, -0.4, 1),
        where=lambda u, p: u.z > 0.05 and u.y > -0.5, seed=91, lift=0.25)
    fur_line(c, [hg + GV(-0.25, -0.75, -0.8), hg + GV(0.25, -0.75, -0.8)], WHITEM, "Head", length=0.6, width=0.35, out=GV(0, -1, 0.1), n_per=4, seed=92)
    t = P(0, k["by"] + 0.25, k["rz"] * 0.95)
    c.tube([t, t + P(0, 0.2, 0.45), t + P(0, 0.55, 0.65)], [0.15, 0.13, 0.1], NAVY, ["Tail1", "Tail2"], seg=8)
    fur(c, GV(-t.x, t.z, t.y) + GV(0, 0.6, 0.7), (0.32, 0.32, 0.32), WHITEM, "Tail2", n=18, length=0.5, width=0.35, flow=lambda p, n: n, seed=93, lift=0.6)
    aura(c, "sparkle", (120, 220, 255), (255, 200, 60), "Divine")
    c.extra["speed"] = 1.15
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Head": (5 * sin(2 * p), 0, 6 * sin(p)), "Tail1": (0, 0, 14 * sin(2 * p))}
    quad_anims(c, tail=2, stride=26, bob=0.12, extra=extra)


VARIANTS = {"Ivory": {NAVY: C(240, 236, 225), NAVY2: C(205, 195, 175), MUZ: C(250, 245, 235), WHITEM: C(214, 32, 40)}}
