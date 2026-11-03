"""LION DANCE CUB (Eternal, Lantern Night Market): a little festival lion-dance cub in costume style. A round red
and gold body with a painted scale cape and white fur fringe along the back, an oversized round costume head with a
gold forehead mirror, a small horn nub, white fluffy brows and beard, pom-pom ears and a fluffy tail. Cute: flat black eyes."""
from cn import *

REDC, REDC2, GOLDC, GOLDC2, WHITEF, GREEN, MIRROR, LIPC = (C(215, 35, 40), C(165, 20, 30), C(255, 200, 60), C(220, 150, 30),
                                                         C(252, 250, 245), C(60, 170, 100), C(220, 235, 255), C(255, 220, 90))


def build():
    c = Creature("LionDanceCub", height=6)
    scales_ = stripes(GOLDC2, "z", period=0.5, width=0.1, wobble=0.25)
    k = cute_quad(c, REDC, belly=GOLDC, paw=GOLDC, body=(1.45, 1.2, 1.75), leg_h=1.05, leg_r=0.45, head_r=1.45, head_up=0.55, tail=2, paint=scales_)
    h, r = k["head"], k["head_r"]
    by, rz = k["by"], k["rz"]
    # oversized costume head: red dome, gold cheeks, big gold lips
    c.ellipsoid(h, (r * 1.08, r * 0.95, r * 0.98), REDC, "Head", seg=(24, 16))
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.75, -0.25, -r * 0.55), (0.6, 0.55, 0.5), GOLDC, "Head", seg=(14, 10))
    c.ellipsoid(h + P(0, -0.62, -r * 0.72), (0.95, 0.32, 0.55), LIPC, "Head", seg=(16, 8))
    c.ellipsoid(h + P(0, -0.85, -r * 0.62), (0.75, 0.22, 0.45), REDC2, "Head", seg=(14, 6))
    # gold forehead mirror + horn nub
    c.tube([h + P(0, 0.62, -r * 0.82), h + P(0, 0.66, -r * 0.95)], [0.32, 0.32], GOLDC, ["Head"], seg=16, sub=1)
    c.ellipsoid(h + P(0, 0.66, -r * 0.97), (0.22, 0.22, 0.04), MIRROR, "Head", seg=(14, 6), stud=False, smooth=True)
    c.tube([h + P(0, r * 0.88, -0.3), h + P(0, r * 1.12, -0.45)], [0.2, 0.06], GOLDC, ["Head"], seg=10, sub=1)
    for s in (-1, 1):
        c.eye(h + P(s * 0.55, 0.15, -r * 0.84), 0.27, P(s * 0.45, 0.05, -1), "Head")
        # white fluffy brows over the eyes
        puffs(c, h + P(s * 0.55, 0.52, -r * 0.8), (0.42, 0.16, 0.22), WHITEF, "Head", n=7, size=0.16, seed=50 + s, sink=0.1)
        # pom-pom ears
        c.ellipsoid(h + P(s * 1.15, r * 0.55, 0.1), (0.3, 0.3, 0.3), GREEN, "Head", seg=(12, 8))
    # white beard fringe under the lips
    puffs(c, h + P(0, -1.05, -r * 0.55), (0.75, 0.2, 0.35), WHITEF, "Head", n=12, size=0.2, seed=53, sink=0.1)
    # white fur fringe along the spine + gold trim
    for j in range(7):
        z = -rz * 0.6 + j * rz * 0.25
        c.ellipsoid(P(0, by + k["ry"] * 0.98 - 0.05 * abs(j - 3), z), (0.32, 0.3, 0.3), WHITEF, ["Chest"] if z < 0 else ["Hips"], seg=(10, 8))
    # fluffy tail
    t = P(0, by + 0.35, rz * 0.95)
    puffs(c, t + P(0, 0.3, 0.3), (0.5, 0.5, 0.5), WHITEF, "Tail2", n=14, size=0.28, seed=55, col2=GOLDC, mix=0.3, sink=0.2)
    aura(c, "sparkle", (255, 60, 50), (255, 210, 60), "Eternal")
    c.extra["speed"] = 1.15
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        # lion-dance head toss: big side-to-side head shakes and a blink-nod
        if walking:
            return {"Head": (5 * sin(2 * p), 0, 10 * sin(p)), "Tail1": (0, 0, 14 * sin(2 * p))}
        shake = max(0, sin(math.pi * (t - 0.4) / 0.3)) if 0.4 <= t <= 0.7 else 0.0
        return {"Head": (6 * sin(2 * p) - 10 * shake, 0, 18 * shake * sin(6 * tau * t)), "Tail1": (0, 0, 20 * sin(2 * p))}
    quad_anims(c, tail=2, stride=26, bob=0.14, extra=extra)


VARIANTS = {"Jade": {REDC: C(60, 170, 110), REDC2: C(35, 120, 75), GREEN: C(214, 32, 40)}}
