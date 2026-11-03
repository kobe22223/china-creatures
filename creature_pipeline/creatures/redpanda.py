"""RED PANDA (Epic, Bamboo Grove): round rusty-red red panda on short dark stubby legs, big head with a cream
face mask and tear marks, white-rimmed triangle ears, a fluffy ringed tail curled around its side, holding
nothing, wearing a small gold bell. Cute: flat black eyes."""
from cn import *

RUST, RUST2, DARK, CREAM, WHITE, NOSE = C(205, 92, 40), C(150, 58, 30), C(70, 40, 34), C(250, 236, 214), C(255, 255, 255), C(40, 28, 26)


def build():
    c = Creature("RedPanda", height=5.5)
    k = cute_quad(c, RUST, belly=DARK, paw=DARK, body=(1.45, 1.2, 1.75), leg_h=1.1, leg_r=0.44, head_r=1.3, head_up=0.5, tail=3)
    h, r = k["head"], k["head_r"]
    # legs darker: paint the lower body dark
    c.ellipsoid(h, (r * 1.08, r * 0.95, r * 0.95), RUST, "Head", seg=(24, 16))
    # cream face mask: muzzle + eyebrow spots + cheeks
    c.ellipsoid(h + P(0, -0.32, -r * 0.72), (0.62, 0.45, 0.45), CREAM, "Head", seg=(16, 10))
    c.ellipsoid(h + P(0, -0.18, -r * 1.08), (0.17, 0.12, 0.1), NOSE, "Head", stud=False, smooth=True)
    for s in (-1, 1):
        c.ellipsoid(h + P(s * 0.8, -0.2, -r * 0.55), (0.48, 0.42, 0.38), CREAM, "Head", seg=(14, 8))
        c.ellipsoid(h + P(s * 0.42, 0.62, -r * 0.78), (0.2, 0.13, 0.08), CREAM, "Head", seg=(10, 6), stud=False)
        c.eye(h + P(s * 0.48, 0.25, -r * 0.84), 0.23, P(s * 0.45, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.48, -0.08, -r * 0.84), (0.09, 0.22, 0.05), RUST2, "Head", stud=False)   # tear mark
        # triangle ears with white rims, short and upright
        e0 = h + P(s * 0.78, r * 0.68, 0.0)
        c.leaf(e0, P(s * 0.45, 1, 0.05), P(0, 0, 1), 0.72, 0.62, WHITE, "Head", thick=0.2, shape="blade")
        c.leaf(e0 + P(0, 0.05, -0.08), P(s * 0.45, 1, 0.05), P(0, 0, 1), 0.55, 0.42, RUST2, "Head", thick=0.12, shape="blade")
    # fluffy ringed tail curling up behind
    rings = stripes(RUST2, "y", period=0.55, width=0.22, wobble=0.0)
    t = P(0, k["by"] + 0.1, k["rz"] * 0.9)
    c.tube([t, t + P(0.2, 0.2, 0.6), t + P(0.5, 0.8, 0.9), t + P(0.6, 1.5, 0.75)], [0.45, 0.55, 0.5, 0.25], RUST,
           ["Tail1", "Tail2", "Tail3"], seg=14, paint=rings)
    bell(c, P(0, k["by"] - 0.15, -k["rz"] * 1.0), 0.3, "Chest", col=GOLD2, rim=GOLD)
    aura(c, "sparkle", (255, 120, 50), (255, 230, 170), "Epic")
    c.extra["speed"] = 1.05
    return c


def anims(c):
    def extra(t, walking):
        p = tau * t
        return {"Tail1": (0, 0, 10 * sin(2 * p)), "Tail2": (6 * sin(2 * p + 0.5), 0, 8 * sin(2 * p + 0.5))}
    quad_anims(c, tail=3, stride=26, bob=0.1, extra=extra)


VARIANTS = {"Snowy": {RUST: C(240, 236, 230), RUST2: C(190, 170, 150), DARK: C(90, 90, 100)}}
