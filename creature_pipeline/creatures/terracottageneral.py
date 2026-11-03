"""TERRACOTTA GENERAL (Zone 7 guardian, Divine): a giant terracotta warrior statue come to life, standing on two
legs. Clay-orange body with fine cracks and traces of old paint, a long layered lamellar armour coat of clay plates
with bronze rivets, shoulder guards, a wide belt, armoured boots, a stern sculpted face with a carved moustache and
a tied topknot under a ribbon cap, a bronze sword at the hip, and glowing amber angry eyes. Fierce."""
from cn import *
from detail import *

CLAY, CLAY2, CLAY3, CRACK, PLATE, RIVET, BRONZEC, RIBBON, EYE = (
    C(196, 120, 80), C(158, 92, 60), C(220, 160, 120), C(110, 64, 42), C(150, 110, 85), C(190, 140, 70),
    C(160, 120, 60), C(150, 45, 40), C(255, 175, 40))


def build():
    c = detailed("TerracottaGeneral", height=18)
    crk = cracks(CRACK, scale=1.6, width=0.025)
    k = biped(c, CLAY, H=1.15, W=1.25, arm_len=1.0, leg_len=1.4)
    hip, sh, xl, xa = k["hip_y"], k["sh_y"], k["x_leg"], k["x_arm"]
    lam = stripes(CLAY2, "y", period=0.42, width=0.08, wobble=0.0)
    # torso + lamellar armour coat flaring over the hips
    T(c, [V(0, hip - 0.3, 0), V(0, hip + 1.0, 0), V(0, sh - 0.4, 0), V(0, sh + 0.2, 0)], [1.45, 1.55, 1.75, 1.3], CLAY, ["Hips", "Chest"], seg=10, flat=(1.0, 0.75), paint=crk)
    T(c, [V(0, sh - 0.3, 0), V(0, hip + 0.4, 0), V(0, hip - 0.7, 0)], [1.85, 1.75, 1.92], PLATE, ["Chest", "Hips"], seg=12, flat=(1.0, 0.78), paint=lam)
    for i in range(6):
        y = hip - 0.55 + i * 0.68
        for j in range(10):
            a = math.radians(-150 + j * 33)
            rr = 1.85 + 0.08 * (i % 2)
            E(c, V(math.sin(a) * rr, y, -math.cos(a) * rr * 0.78), (0.07, 0.07, 0.07), RIVET, "Chest" if y > hip + 0.6 else "Hips", seg=(6, 4), stud=False)
    # wide belt + shoulder guards
    cuff(c, V(0, hip + 0.15, 0), V(0, hip + 0.55, 0), 1.75, CLAY2, "Hips", thick=0.18, seg=12, flare=0.04)
    BOX(c, V(0, hip + 0.35, -1.45), (0.35, 0.3, 0.12), BRONZEC, "Hips", stud=False)
    for s, X in ((-1, "L"), (1, "R")):
        shell(c, V(s * xa * 0.95, sh - 0.45, 0), (0.88, 0.85, 0.88), PLATE, "Arm" + X, th=(20, 160) if s > 0 else (-160, -20), ph=(-25, 80), trim=CLAY2)
    # legs: thick clay columns + armoured boots
    for s, X in ((-1, "L"), (1, "R")):
        T(c, [V(s * xl, hip, 0), V(s * xl, hip * 0.5, -0.1)], [0.95, 0.82], CLAY, "Thigh" + X, seg=9, paint=crk)
        T(c, [V(s * xl, hip * 0.5, -0.1), V(s * xl, 0.6, 0)], [0.8, 0.72], CLAY, "Shin" + X, seg=9, paint=crk)
        cuff(c, V(s * xl, 0.5, 0), V(s * xl, 1.6, 0), 0.72, PLATE, "Shin" + X, thick=0.14, seg=9, flare=0.06)
        E(c, V(s * xl, 0.32, -0.35), (0.85, 0.38, 1.15), CLAY2, "Shin" + X, seg=(9, 6))
    # arms: thick, fists
    for s, X in ((-1, "L"), (1, "R")):
        a0, e0, f0 = V(s * xa, sh - 0.2, 0), V(s * xa * 1.05, sh - 1.8 * 1.15, 0), V(s * xa * 1.08, sh - 3.4 * 1.15, -0.3)
        T(c, [a0, e0], [0.72, 0.62], CLAY, "Arm" + X, seg=8, paint=crk)
        T(c, [e0, f0], [0.62, 0.55], CLAY, "Fore" + X, seg=8, paint=crk)
        cuff(c, e0.lerp(f0, 0.3), e0.lerp(f0, 0.8), 0.6, PLATE, "Fore" + X, thick=0.12, seg=8)
        E(c, f0 + V(0, -0.2, 0), (0.55, 0.55, 0.55), CLAY3, "Fore" + X, seg=(8, 6))
    # bronze sword in its scabbard at the left hip
    T(c, [V(-1.95, hip + 0.4, -0.5), V(-2.1, hip - 1.8, 0.6)], [0.16, 0.14], BRONZEC, "Hips", seg=6, sub=1)
    BOX(c, V(-1.92, hip + 0.55, -0.55), (0.35, 0.08, 0.12), BRONZEC, "Hips", stud=False)
    # head: stern sculpted face, carved moustache, topknot under a ribbon cap
    hc = V(0, sh + 1.5, -0.1)
    T(c, [V(0, sh, 0), V(0, sh + 0.7, -0.05)], [0.7, 0.62], CLAY, "Neck", seg=8)
    E(c, hc, (1.05, 1.15, 1.05), CLAY3, "Head", seg=(12, 10), paint=crk)
    E(c, hc + V(0, -0.1, -0.95), (0.18, 0.28, 0.2), CLAY2, "Head", seg=(6, 5))    # nose
    for s in (-1, 1):
        T(c, [hc + V(s * 0.05, -0.42, -1.02), hc + V(s * 0.38, -0.5, -0.92), hc + V(s * 0.55, -0.42, -0.7)], [0.09, 0.08, 0.04], CLAY2, "Head", seg=6, sub=1)
        E(c, hc + V(s * 1.0, 0.0, 0.0), (0.18, 0.3, 0.22), CLAY3, "Head", seg=(6, 5))   # ears
    E(c, hc + V(0, -0.7, -0.75), (0.45, 0.18, 0.3), CLAY2, "Head", seg=(8, 5))       # chin tuft
    eyes_pair(c, hc + V(0, 0.18, -0.92), 0.38, 0.2, "Head", glow=EYE, core=C(255, 245, 200), brow=CLAY2, slant=16, turn=0.4)
    E(c, hc + V(0, 0.75, 0.15), (1.05, 0.45, 1.05), CLAY2, "Head", seg=(10, 6))     # hair
    E(c, hc + V(0.35, 1.25, 0.1), (0.42, 0.42, 0.42), CLAY2, "Head", seg=(8, 6))    # topknot
    BOX(c, hc + V(0.35, 1.25, 0.1), (0.5, 0.12, 0.47), RIBBON, "Head", stud=False)
    S(c, hc + V(0.35, 1.25, 0.55), hc + V(0.6, 0.6, 1.2), 0.18, RIBBON, "Head", seg=4, n=3, stud=False)
    aura(c, "sparkle", (255, 175, 40), (196, 120, 80), "Divine")
    c.extra["speed"] = 0.9
    return c


def anims(c):
    biped_anims(c, stride=20, arm=16, bob=0.14, sway=4)


# painted-armour variant: the face keeps its natural clay colours, only the armour and clothing are repainted
VARIANTS = {"Painted": {CLAY: C(70, 82, 105), PLATE: C(40, 46, 62), RIVET: C(255, 200, 60), RIBBON: C(214, 32, 40), CRACK: C(35, 38, 50)}}
