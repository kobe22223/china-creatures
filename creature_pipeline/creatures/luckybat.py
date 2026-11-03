"""LUCKY BAT (Cosmic, Lantern Night Market): a round red fortune bat that hovers, big head-body ball with gold
cloud swirl paint, large rounded ears, small scalloped membrane wings with gold edges, tiny feet and a gold coin
pendant. Cute: flat black eyes."""
from cn import *

RED_, RED3, GOLDC, MEM, MEM2, PINK, FANG = C(210, 40, 45), C(160, 25, 35), C(255, 200, 60), C(240, 90, 80), C(180, 40, 50), C(255, 170, 170), C(255, 255, 250)


def build():
    c = Creature("LuckyBat", height=5)
    y0 = 2.6
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    c.bone("Hips", P(0, y0 - 0.6, 0.2), P(0, y0, 0), "Root")
    c.bone("Chest", P(0, y0, 0), P(0, y0 + 0.5, -0.2), "Hips")
    c.bone("Neck", P(0, y0 + 0.5, -0.2), P(0, y0 + 0.8, -0.3), "Chest")
    c.bone("Head", P(0, y0 + 0.8, -0.3), P(0, y0 + 0.9, -1.4), "Neck")
    wing_bones(c, (1.0, y0 + 0.2, 0.1), (2.0, y0 + 0.6, 0.3), (3.0, y0 + 0.2, 0.5))
    for s, X in ((-1, "L"), (1, "R")):
        c.bone("Thigh" + X, P(s * 0.4, y0 - 0.8, 0.2), P(s * 0.4, y0 - 1.2, 0.3), "Hips")
    swirl = cloud_filigree(GOLDC, scale=1.6, width=0.07)
    # one round body-head ball (cute), lighter face
    c.ellipsoid(P(0, y0, 0), (1.35, 1.3, 1.25), RED_, ["Hips", "Chest"], seg=(24, 16), paint=swirl)
    c.ellipsoid(P(0, y0 + 0.75, -0.35), (1.15, 1.0, 1.05), RED_, "Head", seg=(24, 16))
    c.ellipsoid(P(0, y0 + 0.55, -1.15), (0.62, 0.42, 0.3), PINK, "Head", seg=(14, 8))
    c.ellipsoid(P(0, y0 + 0.62, -1.42), (0.12, 0.08, 0.06), RED3, "Head", stud=False)
    for s in (-1, 1):
        c.eye(P(s * 0.45, y0 + 0.95, -1.2), 0.22, P(s * 0.45, 0.05, -1), "Head")
        c.spike(P(s * 0.15, y0 + 0.35, -1.3), P(s * 0.15, y0 + 0.15, -1.32), 0.06, FANG, "Head", seg=5, n=3, stud=False)
        # big rounded ears
        e0 = P(s * 0.6, y0 + 1.55, -0.25)
        c.leaf(e0, P(s * 0.5, 1, 0.1), P(0, 0, 1), 0.85, 0.72, RED_, "Head", thick=0.2, shape="blade")
        c.leaf(e0 + P(0, 0.05, -0.1), P(s * 0.5, 1, 0.1), P(0, 0, 1), 0.62, 0.45, PINK, "Head", thick=0.1, shape="blade")
    # small scalloped membrane wings with gold edges
    for s, S in ((-1, "L"), (1, "R")):
        r_, m_, t_ = P(s * 1.0, y0 + 0.2, 0.1), P(s * 2.0, y0 + 0.6, 0.3), P(s * 3.0, y0 + 0.2, 0.5)
        c.tube([r_, m_], [0.16, 0.12], RED3, ["Wing" + S], seg=8)
        c.tube([m_, t_], [0.12, 0.06], RED3, ["WingTip" + S], seg=8)
        ends = [t_, m_ + P(s * 0.7, -1.1, 0.25), m_ + P(s * 0.0, -1.3, 0.2)]
        for e in ends[1:]:
            c.tube([m_, e], [0.08, 0.04], RED3, ["WingTip" + S], seg=6)
        body = r_ + P(0, -0.9, 0.0)
        chain = ends + [body]
        for i in range(len(chain) - 1):
            a1, b1 = chain[i], chain[i + 1]
            mid = (a1 + b1) / 2 + (m_ - (a1 + b1) / 2) * 0.25
            c.sheet([m_, a1, mid, b1] + ([r_] if i == len(chain) - 2 else []), MEM if i % 2 == 0 else MEM2,
                    "WingTip" + S if i < len(chain) - 2 else "Wing" + S, thick=0.1)
            c.ellipsoid(a1, (0.1, 0.1, 0.1), GOLDC, "WingTip" + S, stud=False)
    # tiny feet + coin pendant
    for s, X in ((-1, "L"), (1, "R")):
        c.ellipsoid(P(s * 0.4, y0 - 1.2, 0.25), (0.18, 0.15, 0.22), RED3, "Thigh" + X, seg=(10, 6))
    coin(c, P(0, y0 - 0.25, -1.25), 0.32, "Chest", facing=(0, 0.1, -1))
    aura(c, "orbit", (255, 200, 60), (210, 40, 45), "Cosmic")
    c.extra["hover"] = 1
    c.extra["speed"] = 1.25
    return c


def anims(c):
    def mk(rate, flap):
        def fn(t):
            p = tau * t * rate
            return {
                "Root": ((4 * sin(p - 1.2), 0, 0), (0, 0.35 * sin(p - 1.2), 0)),
                "Chest": (3 * sin(p), 0, 0), "Head": (4 * sin(p + 1.2), 0, 5 * sin(t * tau)),
                "WingL": (0, 0, flap * sin(p)), "WingR": (0, 0, -flap * sin(p)),
                "WingTipL": (0, 0, flap * 0.6 * sin(p - 0.7)), "WingTipR": (0, 0, -flap * 0.6 * sin(p - 0.7)),
                "ThighL": (10 * sin(p), 0, 0), "ThighR": (10 * sin(p + 1), 0, 0),
            }
        return fn
    c.animate({"Walk": (24, 1.0, mk(3, 34)), "Idle": (40, 4.0, mk(4, 26))})


VARIANTS = {"Jade": {RED_: C(70, 180, 120), RED3: C(40, 120, 80), MEM: C(120, 220, 160), MEM2: C(60, 150, 100), PINK: C(210, 250, 220)}}
