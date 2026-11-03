"""PADDY DUCKLING (Uncommon, Rice Paddy Village): round sunny-yellow duckling on short orange legs, big head,
flat orange bill, a little rice-sprout tuft on its head and a gold lucky coin on a red charm. Cute: flat black eyes."""
from cn import *

YEL, YEL2, CREAM, BILL, BILL2, SPROUT, SPROUT2, _ = (C(255, 205, 35), C(245, 165, 25), C(255, 236, 140), C(255, 140, 30),
                                                        C(230, 110, 20), C(110, 190, 70), C(70, 150, 50), C(240, 205, 110))


def build():
    c = Creature("PaddyDuckling", height=5)
    k = cute_bird(c, YEL, belly=CREAM, leg_col=BILL, body=(1.25, 1.12, 1.35), leg_h=0.8, head_r=1.05,
                  head_up=1.05, head_fwd=0.5, wing_col=YEL2, tail=1)
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r * 0.95, r * 0.95), YEL, "Head", seg=(24, 16))
    # flat duck bill: wide rounded upper + slimmer lower
    c.ellipsoid(h + P(0, -0.22, -r * 0.98), (0.55, 0.13, 0.42), BILL, "Head", seg=(16, 8))
    c.ellipsoid(h + P(0, -0.38, -r * 0.9), (0.45, 0.1, 0.33), BILL2, "Head", seg=(14, 6))
    for s in (-1, 1):
        c.eye(h + P(s * 0.45, 0.18, -r * 0.82), 0.2, P(s * 0.5, 0.05, -1), "Head")
        c.ellipsoid(h + P(s * 0.74, -0.18, -r * 0.6), (0.18, 0.11, 0.08), C(255, 150, 120), "Head", stud=False)
    # rice-sprout tuft: three small blades low on the crown, a little accent
    top = h + P(0, r * 0.86, 0.1)
    for j, (dx, dz) in enumerate(((-0.4, 0.15), (0.0, -0.15), (0.4, 0.15))):
        c.leaf(top + P(dx * 0.3, -0.12, dz * 0.3), P(dx, 1, dz + 0.3), P(1, 0, 0), 0.62 - 0.12 * abs(dx), 0.26,
               SPROUT if j != 1 else SPROUT2, "Head", thick=0.12, shape="blade", curl=0.18)
    # round fluffy tail tuft, tipped up
    t = P(0, k["by"] + 0.3, k["rz"] * 0.92)
    c.ellipsoid(t, (0.42, 0.32, 0.45), YEL2, "Tail1", rot=euler(-30, 0, 0), seg=(12, 8))
    # gold lucky coin on a short red cord, on the chest under the chin
    cp = P(0, k["by"] + 0.15, -k["rz"] * 1.0)
    coin(c, cp, 0.33, "Chest", facing=(0, 0.2, -1), backing=RED)
    aura(c, "sparkle", (255, 214, 70), (140, 220, 110), "Uncommon")
    c.extra["speed"] = 1.0
    return c


def anims(c):
    bird_anims(c, tail=1, stride=32, waddle=8, bob=0.1, flap=12)


# Porcelain duckling: white and porcelain blue
VARIANTS = {"Porcelain": {YEL: C(245, 246, 252), YEL2: C(70, 110, 200), CREAM: C(215, 228, 250), BILL: C(255, 170, 60), BILL2: C(235, 135, 40)}}
