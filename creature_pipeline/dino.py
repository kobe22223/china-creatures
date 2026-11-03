"""Prehistoric zone helpers: theropod (2-legged dino) skeleton + body, dino animations.
Game space: V(x, y, z), y up, front = -z. Built on detail.py (faceted, detailed look)."""
from detail import *


def theropod(c, hip=4.2, L=1.8, W=1.0, neck=(1.0, 1.3), head=2.0, tail=5, tail_len=1.25, tail_drop=0.12,
             arm=1.0, upright=0.35):
    """2-legged dinosaur skeleton. Hips at z=+0.4, chest forward at z=-L. Legs: Thigh (down-forward),
    Shin (down-back), Foot (forward toes). Small arms (Arm/Fore). Returns key points (game vectors)."""
    hz, cz = 0.4, -L
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    mid = V(0, hip + 0.15 + upright * 0.3, hz - L * 0.5)
    c.bone("Hips", B(V(0, hip, hz)), B(mid), "Root")
    chest = V(0, hip + 0.35 + upright * L * 0.5, cz)
    c.bone("Chest", B(mid), B(chest), "Hips")
    nb = chest + V(0, 0.25, -0.15)
    hb = nb + V(0, neck[1], -neck[0])
    c.bone("Neck", B(nb), B(hb), "Chest")
    c.bone("Head", B(hb), B(hb + V(0, 0.05, -head)), "Neck")
    c.bone("Jaw", B(hb + V(0, -0.4, -0.25)), B(hb + V(0, -0.75, -head)), "Head")
    k = dict(hip=hip, hz=hz, cz=cz, W=W, nb=nb, hb=hb, mid=mid, chest=chest)
    for s, X in ((-1, "L"), (1, "R")):
        hp_ = V(s * W, hip - 0.15, hz)
        kn = V(s * W * 1.08, hip * 0.55, hz - 0.75)
        an = V(s * W * 1.1, hip * 0.2, hz + 0.25)
        toe = V(s * W * 1.12, 0.25, hz - 0.85)
        c.bone("Thigh" + X, B(hp_), B(kn), "Hips")
        c.bone("Shin" + X, B(kn), B(an), "Thigh" + X)
        c.bone("Foot" + X, B(an), B(toe), "Shin" + X)
        sho = chest + V(s * W * 0.72, -0.55, 0.15)
        el = sho + V(s * 0.25, -0.75 * arm, -0.1)
        hd = el + V(0, -0.1, -0.75 * arm)
        c.bone("Arm" + X, B(sho), B(el), "Chest")
        c.bone("Fore" + X, B(el), B(hd), "Arm" + X)
        k.update({"hip" + X: hp_, "knee" + X: kn, "ankle" + X: an, "toe" + X: toe, "sho" + X: sho, "elb" + X: el, "hand" + X: hd})
    t0, prev, tp = V(0, hip + 0.05, hz + 0.7), "Hips", []
    tp.append(t0)
    for i in range(tail):
        t1 = t0 + V(0, -tail_drop * (1 - i / max(1, tail)) + 0.05 * i / tail, tail_len)
        c.bone("Tail%d" % (i + 1), B(t0), B(t1), prev)
        prev, t0 = "Tail%d" % (i + 1), t1
        tp.append(t1)
    k["tail"] = tp
    return k


def theropod_legs(c, k, col, claw_col, r=(0.85, 0.55, 0.32), paint=None, toe_col=None, seg=7):
    """powerful drumstick thighs, slim shins, 3-toed clawed feet"""
    for s, X in ((-1, "L"), (1, "R")):
        hp_, kn, an, toe = k["hip" + X], k["knee" + X], k["ankle" + X], k["toe" + X]
        L = (hp_ - kn).length
        E(c, hp_.lerp(kn, 0.35) + V(s * 0.08, 0, 0.05), (r[0] * 1.3, L * 0.55, r[0] * 1.55), col, "Thigh" + X, seg=(10, 7), paint=paint)
        T(c, [hp_.lerp(kn, 0.3), kn], [r[0] * 1.05, r[1]], col, "Thigh" + X, seg=seg, paint=paint)
        E(c, kn, (r[1] * 1.05, r[1] * 1.05, r[1] * 1.1), col, "Shin" + X, seg=(8, 5), paint=paint)
        T(c, [kn, kn.lerp(an, 0.5), an], [r[1], r[1] * 0.8, r[2]], col, "Shin" + X, seg=seg, paint=paint)
        E(c, an, (r[2] * 1.15, r[2] * 1.15, r[2] * 1.2), col, "Foot" + X, seg=(7, 5))
        fc = toe_col or col
        for j in (-1, 0, 1):
            base = an + V(0, -0.05, -0.1)
            tip = V(an.x + j * r[2] * 1.5, 0.22, toe.z - (0.15 if j == 0 else 0))
            T(c, [base, base.lerp(tip, 0.5) + V(0, 0.05, 0), tip], [r[2] * 0.75, r[2] * 0.6, r[2] * 0.48], fc, "Foot" + X, seg=6)
            S(c, tip + V(0, 0.1, 0.1), tip + V(j * 0.08, -0.15, -r[2] * 2.0), r[2] * 0.42, claw_col, "Foot" + X, bend=V(0, 0.15, 0), seg=4, n=4, stud=False)
        S(c, an + V(0, 0.1, 0.15), an + V(0, -0.05, 0.75), r[2] * 0.4, claw_col, "Foot" + X, seg=4, n=3, stud=False)   # dew claw


def tiny_arms(c, k, col, claw_col, r=0.26, fingers=2):
    for s, X in ((-1, "L"), (1, "R")):
        sh, el, hd = k["sho" + X], k["elb" + X], k["hand" + X]
        T(c, [sh, el], [r * 1.25, r], col, "Arm" + X, seg=6)
        T(c, [el, hd], [r, r * 0.8], col, "Fore" + X, seg=6)
        for j in range(fingers):
            o = (j - (fingers - 1) / 2) * r * 0.9
            S(c, hd + V(o, 0, 0), hd + V(o, -0.35, -0.35), r * 0.45, claw_col, "Fore" + X, bend=V(0, 0.1, 0), seg=4, n=3, stud=False)


def dino_tail(c, k, col, r0, col2=None, paint=None, seg=8, flat=(0.85, 1.0)):
    tp = k["tail"]
    n = len(tp) - 1
    radii = [r0 * (1 - 0.88 * i / n) + 0.06 for i in range(n + 1)]
    T(c, tp, radii, col, ["Tail%d" % (i + 1) for i in range(n)], seg=seg, paint=paint, flat=flat)
    return radii


def theropod_anims(c, tail=5, stride=30, bob=0.18, extra=None, lean=6, head_amp=1.0):
    def walk(t):
        p = tau * t
        out = {
            "Root": ((0, 0, 3 * sin(p)), (0, bob * abs(sin(p)) - bob * 0.5, 0)),
            "Hips": (0, 5 * sin(p), 0),
            "Chest": (2 * sin(2 * p), -4 * sin(p), 0),
            "Neck": (-4 * sin(2 * p + 0.6) * head_amp, 3 * sin(p), 0),
            "Head": (3 * sin(2 * p + 1.2) * head_amp, 0, 0),
            "ThighL": (-stride * sin(p), 0, 0), "ThighR": (stride * sin(p), 0, 0),
            "ShinL": (30 * max(0, sin(p + 0.6)), 0, 0), "ShinR": (30 * max(0, -sin(p + 0.6)), 0, 0),
            "FootL": (-25 * max(0, sin(p + 1.0)), 0, 0), "FootR": (-25 * max(0, -sin(p + 1.0)), 0, 0),
            "ArmL": (10 * sin(p), 0, 0), "ArmR": (-10 * sin(p), 0, 0),
        }
        for i in range(tail):
            out["Tail%d" % (i + 1)] = (2 * sin(2 * p - i), (8 + 2 * i) * sin(p - 0.7 * i - 0.5), 0)
        if extra:
            out.update(extra(t, True))
        return out

    def idle(t):
        p = tau * t
        roar = max(0, sin(math.pi * (t - 0.55) / 0.3)) if 0.55 <= t <= 0.85 else 0.0
        out = {
            "Root": ((0, 0, 0), (0, 0.06 * sin(2 * p), 0)),
            "Chest": (1.5 * sin(2 * p) - 3 * roar, 0, 0),
            "Neck": (2 * sin(p) - 8 * roar, 16 * sin(p) * head_amp * (1 - roar), 0),
            "Head": (3 * sin(2 * p + 1) + 14 * roar, 0, 5 * sin(p) * (1 - roar)),
            "Jaw": (-3 - 26 * roar, 0, 0),
            "ArmL": (6 * sin(2 * p), 0, 0), "ArmR": (6 * sin(2 * p + 1), 0, 0),
        }
        for i in range(tail):
            out["Tail%d" % (i + 1)] = (1.5 * sin(p - i), (7 + 2 * i) * sin(p - 0.8 * i), 0)
        if extra:
            out.update(extra(t, False))
        return out
    c.animate({"Walk": (24, 1.0, walk), "Idle": (40, 4.0, idle)})


def scale_row(c, pts, col, bones_fn, size=0.35, shrink=0.0, lean=0.4, side=False, **kw):
    """row of back spikes/plates along a list of points. bones_fn(i) -> bone name"""
    n = len(pts)
    for i, p in enumerate(pts):
        sz = size * (1 - shrink * abs(i - n / 2) / (n / 2))
        S(c, p, p + V(0, sz * 1.6, sz * lean), sz * 0.45, col, bones_fn(i), seg=4, n=3, **kw)

