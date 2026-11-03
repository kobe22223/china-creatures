"""SOUTH CHINA TIGER (Zone 3 guardian, Mythic): huge muscular orange tiger with bold black stripes, white belly,
cheeks and muzzle, the traditional "king" stripe mark on its forehead, a white shard-fur cheek ruff, a roaring jaw
full of teeth, glowing amber angry eyes, big clawed paws and a long striped tail. Fierce."""
from cn import *
from detail import *

ORANGE, BLACK, WHITE, NOSE, CLAWC = C(240, 130, 40), C(30, 24, 22), C(250, 244, 232), C(200, 90, 90), C(245, 240, 225)


def build():
    c = detailed("SouthChinaTiger", height=16)
    tig = stripes(BLACK, "z", period=0.9, width=0.22, wobble=0.45)
    k = fierce_quad(c, ORANGE, belly=WHITE, sh=4.2, hip=4.0, L=2.2, W=1.3, neck=(1.0, 0.75), head=1.6, tail=5, tail_len=0.95,
                    body_r=1.45, leg_r=(0.86, 0.66, 0.56), paw=(0.8, 0.42, 0.95), paw_col=ORANGE, paint=tig, hump=0.2)
    hb = k["hb"]
    for s, X in ((-1, "L"), (1, "R")):
        claws3(c, k["paw" + X] + V(0, 0, -0.35), CLAWC, "Fore" + X, size=0.3)
        claws3(c, k["foot" + X] + V(0, 0, -0.35), CLAWC, "Shin" + X, size=0.26)
    # head
    hst = stripes(BLACK, "x", period=0.55, width=0.12, wobble=0.15, only=lambda X, Y, Z: np.abs(X) > 0.45)
    E(c, hb + V(0, 0.1, -0.5), (1.15, 1.0, 1.1), ORANGE, "Head", seg=(12, 9), paint=hst)
    E(c, hb + V(0, -0.35, -1.35), (0.75, 0.5, 0.6), WHITE, "Head", seg=(10, 7))
    E(c, hb + V(0, 0.0, -1.9), (0.26, 0.18, 0.14), NOSE, "Head", stud=False)
    E(c, hb + V(0, -0.98, -1.2), (0.6, 0.24, 0.65), WHITE, "Jaw", seg=(8, 5))
    maw(c, hb + V(0, -0.62, -1.72), 0.5, 0.7, 0.5, "Head", "Jaw", n=8, tooth=0.18, fangs=2.3)
    # forehead "king" mark: three bars and a centre stroke, painted on in black boxes
    fh = hb + V(0, 0.82, -1.15)
    for j, w in enumerate((0.42, 0.32, 0.42)):
        BOX(c, fh + V(0, 0.22 - j * 0.2, j * 0.05), (w, 0.05, 0.06), BLACK, "Head", rot=(-30, 0, 0), stud=False)
    BOX(c, fh + V(0, 0.02, 0.04), (0.05, 0.25, 0.06), BLACK, "Head", rot=(-30, 0, 0), stud=False)
    for s in (-1, 1):
        S(c, hb + V(s * 0.75, 0.85, -0.15), hb + V(s * 0.95, 1.5, 0.05), 0.32, ORANGE, "Head", seg=4, n=3)   # ear
        E(c, hb + V(s * 0.85, 1.05, -0.2), (0.2, 0.22, 0.08), WHITE, "Head", seg=(6, 4), stud=False)
    fur(c, hb + V(0, -0.3, -0.6), (1.3, 0.85, 0.9), WHITE, "Head", n=70, length=0.75, width=0.55, flow=V(0, -0.5, 0.7), where=lambda u, p: abs(u.x) > 0.6, seed=17)
    eyes_pair(c, hb + V(0, 0.35, -1.38), 0.52, 0.26, "Head", glow=C(255, 190, 40), core=C(255, 250, 200), brow=BLACK, slant=24, turn=0.55)
    tp = k["tail"]
    T(c, tp, [0.42, 0.36, 0.3, 0.25, 0.2, 0.14], ORANGE, ["Tail%d" % (i + 1) for i in range(5)], seg=8, paint=stripes(BLACK, "z", period=0.6, width=0.18, wobble=0))
    E(c, tp[-1], (0.22, 0.22, 0.3), BLACK, "Tail5", seg=(8, 5))
    aura(c, "orbit", (255, 150, 40), (255, 240, 200), "Mythic")
    c.extra["speed"] = 1.1
    return c


def anims(c):
    fierce_anims(c, tail=5, stride=26, bob=0.14, head_amp=0.8)


VARIANTS = {"White": {ORANGE: C(240, 240, 245), WHITE: C(255, 255, 255), BLACK: C(40, 40, 60)}}
