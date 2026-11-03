"""FENGHUANG (Infinity, Heavenly Court): the Chinese phoenix. A round elegant phoenix on short tucked legs, gold
head with a fan crest of jade and red plumes, a red breast, jade and cobalt folded wings with gold edges, glowing
amber eyes, a short gold beak and long drooping tail streamers ending in glowing eye-spot feathers. Royal: glowing eyes."""
from cn import *
from detail import V as GV, eyes_pair

GOLDF, RED_, JADEF, COBALT_, BEAK, LEGC, SPOT, SPOT2, EYE = (C(255, 200, 60), C(220, 45, 45), C(60, 180, 130), C(50, 90, 200),
                                                           C(255, 215, 120), C(200, 160, 80), C(80, 220, 255), C(255, 240, 120), C(255, 190, 60))


def build():
    c = Creature("Fenghuang", height=7)
    swirl = cloud_filigree(GOLDF, scale=1.8, width=0.07)
    k = cute_bird(c, RED_, belly=GOLDF, leg_col=LEGC, body=(1.2, 1.18, 1.45), leg_h=0.8, head_r=0.98, head_up=1.15, head_fwd=0.55,
                  wing_col=JADEF, tail=3, foot="toes")
    h, r = k["head"], k["head_r"]
    c.ellipsoid(h, (r, r, r * 0.95), GOLDF, "Head", seg=(24, 16))
    c.ellipsoid(h + P(0, -0.35, -0.1), (r * 0.85, r * 0.55, r * 0.75), RED_, "Head", seg=(18, 10))
    c.tube([h + P(0, -0.05, -r * 0.82), h + P(0, -0.18, -r * 1.25)], [0.2, 0.04], BEAK, ["Head"], seg=10, sub=1)
    hg = GV(-h.x, h.z, h.y)
    eyes_pair(c, hg + GV(0, 0.15, -r * 0.82), 0.4, 0.2, "Head", glow=EYE, core=C(255, 250, 220), brow=RED_, slant=16, turn=0.5)
    for j in range(5):    # fan crest
        a = (j - 2) * 0.35
        c.tube([h + P(a * 0.2, r * 0.75, 0.05), h + P(a * 0.6, r * 1.3, 0.25), h + P(a, r * 1.6, 0.45)], [0.05, 0.04, 0.03], GOLDF, ["Head"], seg=5)
        c.ellipsoid(h + P(a, r * 1.65, 0.48), (0.14, 0.14, 0.1), JADEF if j % 2 else RED_, "Head", seg=(8, 6))
    # cobalt edges on the folded wings
    for s, S in ((-1, "L"), (1, "R")):
        w = P(s * k["rx"] * 0.84, k["by"] + k["ry"] * 0.12, k["rz"] * 0.15)
        c.ellipsoid(w + P(s * 0.03, -0.05, 0.1), (k["rx"] * 0.27, k["ry"] * 0.5, k["rz"] * 0.64), JADEF, "Wing" + S, rot=euler(-14, s * -6, s * 4),
                    seg=(16, 10), paint=band(COBALT_, 0.45, 9, axis="z"))
    c.ellipsoid(P(0, k["by"] + 0.25, k["rz"] * 0.3), (0.8, 0.45, 0.8), RED_, ["Hips", "Chest"], seg=(14, 8), paint=swirl)
    # long drooping tail streamers with glowing eye-spot tips
    t0 = P(0, k["by"] + 0.2, k["rz"] * 0.85)
    for j in range(5):
        a = (j - 2) * 0.3
        pts = [t0, t0 + P(a * 0.5, 0.45, 0.8), t0 + P(a, 0.2, 1.8), t0 + P(a * 1.3, -0.55, 2.5), t0 + P(a * 1.4, -1.2, 2.7)]
        c.tube(pts, [0.16, 0.16, 0.13, 0.1, 0.05], [GOLDF, COBALT_, JADEF, RED_, GOLDF][j], ["Tail1", "Tail2", "Tail3"], seg=8, flat=(1.0, 0.5))
        c.ellipsoid(pts[-1] + P(0, 0.1, -0.05), (0.26, 0.3, 0.1), SPOT2, "Tail3", seg=(10, 6), glow=True)
        c.ellipsoid(pts[-1] + P(0, 0.1, -0.1), (0.13, 0.16, 0.08), SPOT, "Tail3", seg=(8, 5), glow=True)
    aura(c, "orbit", (255, 200, 60), (60, 180, 130), "Infinity")
    c.extra["speed"] = 1.3
    return c


def anims(c):
    bird_anims(c, tail=3, stride=26, waddle=4, bob=0.1, flap=16)


VARIANTS = {"Moonlight": {GOLDF: C(235, 240, 255), RED_: C(150, 160, 230), JADEF: C(200, 220, 255), COBALT_: C(90, 100, 200)}}
