"""Reusable body plans + animations for the creatures (game coords via P: y up, z back, front -z)."""
import math
from sculpt import *

sin, cos, tau = math.sin, math.cos, math.tau


# ============================================================== QUADRUPED
def quad(c, col, belly=None, L=1.0, H=1.0, W=1.0, leg=1.0, paw=None, chest_y=None, tail=3, neck=True, paint=None, chunk=1.0):
    """standard 4-legged body. L/H/W scale length/height/width. chunk > 1 = thicker legs + fuller body
    (owner asked for chunkier creatures from batch 7 on). Returns key points dict."""
    sh_y = 4.3 * H                     # shoulder height
    hip_z, chest_z = 1.8 * L, -1.9 * L
    x = 1.05 * W * (1 + 0.22 * (chunk - 1))
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    c.bone("Hips", P(0, sh_y, hip_z), P(0, sh_y + 0.1, 0), "Root")
    c.bone("Chest", P(0, sh_y + 0.1, 0), P(0, sh_y + 0.5 * H, chest_z), "Hips")
    nb = P(0, sh_y + 0.7 * H, chest_z)
    hb = P(0, sh_y + 1.7 * H, chest_z - 1.0 * L)
    c.bone("Neck", nb, hb, "Chest")
    c.bone("Head", hb, hb + P(0, 0.3, -1.6 * L), "Neck")
    for s, S in ((-1, "L"), (1, "R")):
        c.bone("Arm" + S, P(s * x, sh_y, chest_z + 0.1), P(s * x, sh_y * 0.5, chest_z - 0.1), "Chest")
        c.bone("Fore" + S, P(s * x, sh_y * 0.5, chest_z - 0.1), P(s * x, 0.45, chest_z - 0.05), "Arm" + S)
        c.bone("Thigh" + S, P(s * x * 0.95, sh_y - 0.2, hip_z - 0.1), P(s * x, sh_y * 0.55, hip_z - 0.6), "Hips")
        c.bone("Shin" + S, P(s * x, sh_y * 0.55, hip_z - 0.6), P(s * x, 0.45, hip_z + 0.1), "Thigh" + S)
    if tail:
        t0 = P(0, sh_y + 0.2, hip_z + 1.1 * L)
        prev = "Hips"
        for i in range(tail):
            t1 = t0 + P(0, 0.35 * H, 1.15 * L)
            c.bone("Tail%d" % (i + 1), t0, t1, prev)
            prev, t0 = "Tail%d" % (i + 1), t1
    belly = belly or col
    r = 1.45 * min(H, W) ** 0.5 * (1 + 0.3 * (chunk - 1))
    c.tube([P(0, sh_y - 0.05, hip_z + 0.95 * L), P(0, sh_y, hip_z + 0.3 * L), P(0, sh_y + 0.1, 0.9 * L * 0.5), P(0, sh_y + 0.2, -0.5 * L), P(0, sh_y + 0.35 * H, chest_z + 0.4 * L), P(0, sh_y + 0.4 * H, chest_z - 0.35 * L)],
           [0.9 * r / 1.45, r * 0.95, r, r * 1.03, r * 1.1, r * 0.92], col, ["Hips", "Chest"], seg=18, flat=(W ** 0.5 * 0.92, 1.0), sub=5, paint=paint)
    c.ellipsoid(P(0, sh_y - r * 0.6, -0.2 * L), (r * 0.72 * W, r * 0.38, 2.1 * L), belly, ["Hips", "Chest"])
    if neck:
        c.tube([P(0, sh_y + 0.3 * H, chest_z + 0.1), P(0, sh_y + 1.0 * H, chest_z - 0.5 * L), hb + P(0, -0.1, 0.1)], [r * 0.8, r * 0.72, r * 0.66], col, ["Chest", "Neck"], seg=14, paint=paint)
    pawc = paw or belly
    if chunk >= 1.3:
        # chunky legs: one smooth rounded column per leg (no flare, no seams) + round paws
        for s, S in ((-1, "L"), (1, "R")):
            lr = 0.55 * leg * W ** 0.5 * chunk
            c.ellipsoid(P(s * x * 0.97, sh_y * 0.86, chest_z + 0.05), (lr * 1.18, sh_y * 0.28, lr * 1.3), col, "Arm" + S, seg=(20, 12), paint=paint)   # shoulder
            c.tube([P(s * x, sh_y * 0.86, chest_z + 0.05), P(s * x * 1.02, sh_y * 0.7, chest_z - 0.02), P(s * x * 1.03, sh_y * 0.5, chest_z - 0.1)],
                   [lr * 1.05, lr * 1.0, lr * 0.93], col, ["Arm" + S], seg=14, paint=paint)
            c.tube([P(s * x * 1.03, sh_y * 0.56, chest_z - 0.1), P(s * x * 1.04, sh_y * 0.3, chest_z - 0.08), P(s * x * 1.05, 0.55, chest_z - 0.05)],
                   [lr * 0.93, lr * 0.88, lr * 0.9], col, ["Fore" + S], seg=14, paint=paint)
            c.ellipsoid(P(s * x * 1.05, 0.45, chest_z - 0.22), (lr * 1.02, 0.45, lr * 1.15), pawc, "Fore" + S, seg=(18, 10))
            c.ellipsoid(P(s * x * 0.97, sh_y * 0.78, hip_z - 0.15), (lr * 1.25, sh_y * 0.32, lr * 1.45), col, "Thigh" + S, seg=(20, 12), paint=paint)
            c.tube([P(s * x, sh_y * 0.7, hip_z - 0.2), P(s * x * 1.02, sh_y * 0.48, hip_z - 0.25), P(s * x * 1.04, sh_y * 0.28, hip_z - 0.05), P(s * x * 1.05, 0.55, hip_z + 0.1)],
                   [lr * 1.0, lr * 0.93, lr * 0.88, lr * 0.9], col, ["Shin" + S], seg=14, paint=paint)
            c.ellipsoid(P(s * x * 1.05, 0.45, hip_z - 0.12), (lr * 1.0, 0.45, lr * 1.12), pawc, "Shin" + S, seg=(18, 10))
            for t in (-1, 0, 1):   # toe beans
                for zz, bone in ((chest_z - 0.22 - lr * 1.05, "Fore" + S), (hip_z - 0.12 - lr * 1.02, "Shin" + S)):
                    c.ellipsoid(P(s * x * 1.05 + t * lr * 0.42, 0.32, zz + 0.12), (lr * 0.22, 0.18, lr * 0.16), pawc, bone, seg=(8, 6))
        return dict(sh_y=sh_y, hip_z=hip_z, chest_z=chest_z, x=x, head=hb, r=r)
    for s, S in ((-1, "L"), (1, "R")):
        lr = 0.55 * leg * W ** 0.5 * chunk
        tp = 1 + 0.5 * (chunk - 1)          # chunky legs taper less (thick all the way down)
        top = 1.45 if chunk <= 1.0 else 1.18          # mild chunk: thicker legs without the flared tops
        c.tube([P(s * x, sh_y + 0.2, chest_z + 0.15), P(s * x * 1.03, sh_y * 0.75, chest_z - 0.05), P(s * x * 1.03, sh_y * 0.5, chest_z - 0.12)], [lr * top, lr * 1.08, lr * 0.9], col, ["Arm" + S], seg=10, paint=paint)
        c.tube([P(s * x * 1.03, sh_y * 0.53, chest_z - 0.12), P(s * x * 1.05, sh_y * 0.27, chest_z - 0.08), P(s * x * 1.05, 0.5, chest_z - 0.05)], [lr * 0.9, lr * 0.8 * tp, lr * 0.82 * tp], col, ["Fore" + S], seg=10, paint=paint)
        c.ellipsoid(P(s * x * 1.05, 0.33, chest_z - 0.3), (lr * 1.0 * tp, 0.33 * tp, lr * 1.25 * tp), pawc, "Fore" + S)
        c.ellipsoid(P(s * x * 0.95, sh_y * 0.8, hip_z - 0.15), (lr * 1.5, sh_y * 0.3, lr * 1.85), col, "Thigh" + S, seg=(20, 12), paint=paint)
        c.tube([P(s * x, sh_y * 0.78, hip_z - 0.25), P(s * x * 1.02, sh_y * 0.55, hip_z - 0.55), P(s * x * 1.04, sh_y * 0.3, hip_z - 0.1), P(s * x * 1.05, 0.5, hip_z + 0.15)], [lr * 1.1, lr * 0.9 * tp, lr * 0.75 * tp, lr * 0.8 * tp], col, ["Shin" + S], seg=10, paint=paint)
        c.ellipsoid(P(s * x * 1.05, 0.33, hip_z - 0.1), (lr * 0.95 * tp, 0.32 * tp, lr * 1.2 * tp), pawc, "Shin" + S)
    return dict(sh_y=sh_y, hip_z=hip_z, chest_z=chest_z, x=x, head=hb, r=r)


def cute_quad(c, col, belly=None, paw=None, body=(1.45, 1.2, 1.75), leg_h=1.35, leg_r=0.42, head_r=1.3,
              head_up=0.55, neck_len=0.35, tail=1, paint=None, spread=0.55):
    """CUTE PET body plan (Kobe's proportion rules): round barrel body, SHORT stubby legs (leg_h about 1/4 of
    total height), big head (about 40-45% of height) sitting forward and up on the body, no visible neck.
    Same bone names as quad(), so quad_anims works. Returns key points (blender vectors) and sizes."""
    rx, ry, rz = body
    by = leg_h + ry * 0.75                     # body centre height
    sz, hz = -rz * 0.55, rz * 0.55            # shoulder / hip z
    lx = rx * spread                           # leg x
    hc = P(0, by + ry * head_up, -rz - head_r * 0.45)   # head centre
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    c.bone("Hips", P(0, by, hz), P(0, by, 0), "Root")
    c.bone("Chest", P(0, by, 0), P(0, by + 0.2, sz), "Hips")
    nb = P(0, by + ry * 0.35, -rz * 0.75)
    c.bone("Neck", nb, nb + P(0, neck_len, -neck_len), "Chest")
    c.bone("Head", nb + P(0, neck_len, -neck_len), hc + P(0, 0, -head_r), "Neck")
    top_y = by - ry * 0.45
    for s, S in ((-1, "L"), (1, "R")):
        c.bone("Arm" + S, P(s * lx, top_y, sz), P(s * lx, leg_h * 0.5, sz), "Chest")
        c.bone("Fore" + S, P(s * lx, leg_h * 0.5, sz), P(s * lx, 0.2, sz - 0.05), "Arm" + S)
        c.bone("Thigh" + S, P(s * lx, top_y, hz), P(s * lx, leg_h * 0.5, hz), "Hips")
        c.bone("Shin" + S, P(s * lx, leg_h * 0.5, hz), P(s * lx, 0.2, hz + 0.05), "Thigh" + S)
    t0, prev = P(0, by + ry * 0.2, rz * 0.95), "Hips"
    for i in range(tail):
        t1 = t0 + P(0, 0.35, 0.6)
        c.bone("Tail%d" % (i + 1), t0, t1, prev)
        prev, t0 = "Tail%d" % (i + 1), t1
    belly = belly or col
    pawc = paw or belly
    c.ellipsoid(P(0, by, 0), (rx, ry, rz), col, ["Hips", "Chest"], seg=(24, 16), paint=paint)
    c.ellipsoid(P(0, by - ry * 0.45, -rz * 0.05), (rx * 0.72, ry * 0.5, rz * 0.8), belly, ["Hips", "Chest"], seg=(18, 10))
    for s, S in ((-1, "L"), (1, "R")):
        for z, up, lo in ((sz, "Arm" + S, "Fore" + S), (hz, "Thigh" + S, "Shin" + S)):
            # haunch: rounded mass sunk into the body so the leg grows out of it (no seam, no gap)
            c.ellipsoid(P(s * lx, by - ry * 0.5, z), (leg_r * 1.4, ry * 0.55, leg_r * 1.5), col, up, seg=(16, 12), paint=paint)
            # short stub leg + rounded paw
            c.ellipsoid(P(s * lx, leg_h * 0.5 + 0.1, z), (leg_r, leg_h * 0.55, leg_r * 1.05), col, lo, seg=(16, 10), paint=paint)
            c.ellipsoid(P(s * lx, 0.27, z - leg_r * 0.2), (leg_r * 1.1, 0.28, leg_r * 1.3), pawc, lo, seg=(14, 8))
    return dict(by=by, rx=rx, ry=ry, rz=rz, sz=sz, hz=hz, lx=lx, head=hc, head_r=head_r, leg_h=leg_h)


def claws(c, x, z, col, bone, n=3, size=0.25):
    for k in range(n):
        o = (k - (n - 1) / 2) * size * 0.9
        c.spike(P(x + o, 0.22, z - 0.05), P(x + o * 1.1, 0.06, z - size * 1.3), size * 0.3, col, bone, seg=5, n=3)


def quad_anims(c, wings=False, tail=3, stride=24, bob=0.1, head_amp=1.0, extra=None):
    def walk(t):
        p = tau * t
        out = {
            "Root": ((0, 0, 0), (0, bob * abs(sin(2 * p)), 0)),
            "Chest": (1.5 * sin(2 * p), 2 * sin(p), 0),
            "Neck": (-3 * sin(2 * p) * head_amp, -2 * sin(p), 0),
            "Head": (2 * sin(2 * p + 0.5) * head_amp, 0, 0),
            "ArmL": (stride * sin(p), 0, 0), "ArmR": (-stride * sin(p), 0, 0),
            "ThighL": (-stride * sin(p), 0, 0), "ThighR": (stride * sin(p), 0, 0),
            "ForeL": (-28 * max(0, -sin(p - 0.6)), 0, 0), "ForeR": (-28 * max(0, sin(p - 0.6)), 0, 0),
            "ShinL": (24 * max(0, sin(p + 0.4)), 0, 0), "ShinR": (24 * max(0, -sin(p + 0.4)), 0, 0),
        }
        for i in range(tail):
            out["Tail%d" % (i + 1)] = (0, (12 + 2 * i) * sin(p - 0.7 * i), 0)
        if wings:
            out.update({"WingL": (0, 0, 8 + 7 * sin(2 * p)), "WingR": (0, 0, -8 - 7 * sin(2 * p)),
                        "WingTipL": (0, 0, 6 * sin(2 * p - 0.6)), "WingTipR": (0, 0, -6 * sin(2 * p - 0.6))})
        if extra:
            out.update(extra(t, True))
        return out

    def idle(t):
        p = tau * t
        out = {
            "Root": ((0, 0, 0), (0, 0.06 * sin(2 * p), 0)),
            "Chest": (1.5 * sin(2 * p), 0, 0),
            "Neck": (2 * sin(p), 14 * sin(p) * head_amp, 0),
            "Head": (4 * sin(2 * p + 1), 0, 4 * sin(p)),
        }
        for i in range(tail):
            out["Tail%d" % (i + 1)] = (0, (9 + 2 * i) * sin(p - 0.8 * i), 0)
        if wings:
            out.update({"WingL": (0, 0, 4 + 10 * sin(p)), "WingR": (0, 0, -4 - 10 * sin(p)),
                        "WingTipL": (0, 0, 8 * sin(p - 0.8)), "WingTipR": (0, 0, -8 * sin(p - 0.8))})
        if extra:
            out.update(extra(t, False))
        return out
    c.animate({"Walk": (24, 1.0, walk), "Idle": (40, 4.0, idle)})


# ============================================================== WINGS
def wing_bones(c, root, mid, tip, parent="Chest"):
    for s, S in ((-1, "L"), (1, "R")):
        r, m, t = (P(s * root[0], root[1], root[2]), P(s * mid[0], mid[1], mid[2]), P(s * tip[0], tip[1], tip[2]))
        c.bone("Wing" + S, r, m, parent)
        c.bone("WingTip" + S, m, t, "Wing" + S)


def feather_wings(c, root, mid, tip, col, tipcol, cover=None, n=12, length=(2.4, 2.0), width=1.25, arm_col=None):
    for s, S in ((-1, "L"), (1, "R")):
        r, m, t = (P(s * root[0], root[1], root[2]), P(s * mid[0], mid[1], mid[2]), P(s * tip[0], tip[1], tip[2]))
        c.tube([r, m], [0.38, 0.3], arm_col or col, ["Wing" + S], seg=8)
        c.tube([m, t], [0.3, 0.16], arm_col or col, ["WingTip" + S], seg=8)
        for i in range(n):
            k = (i + 0.5) / n
            base = r.lerp(m, k * 2) if k < 0.5 else m.lerp(t, (k - 0.5) * 2)
            bone = "Wing" + S if k < 0.5 else "WingTip" + S
            ln = length[0] + length[1] * k
            down = P(s * 0.15, -1.0, 0.75 - 0.3 * k).normalized()
            arm_dir = (m - r) if k < 0.5 else (t - m)
            c.leaf(base, down, arm_dir, ln, width, col, bone, thick=0.16 + 0.02 * (i % 2), shape="feather", curl=0.05)
            c.leaf(base + down * (ln * 0.72) + P(0, 0, 0.02), down, arm_dir, ln * 0.32, width * 0.76, tipcol if i % 2 else tipcol, bone, thick=0.18, shape="feather")
        for i in range(5):
            k = (i + 0.5) / 5
            c.leaf(r.lerp(m, k) + P(0, 0.1, -0.12), P(s * 0.1, -1, 0.4), m - r, 1.4, 1.2, cover or col, "Wing" + S, thick=0.2, shape="feather")


def bat_wings(c, root, mid, tip, bone_col, skin_col, edge_col=None, fingers=4, glow_edge=False):
    """membrane wings: arm + finger bones with skin panels between them"""
    for s, S in ((-1, "L"), (1, "R")):
        r, m, t = (P(s * root[0], root[1], root[2]), P(s * mid[0], mid[1], mid[2]), P(s * tip[0], tip[1], tip[2]))
        c.tube([r, m], [0.34, 0.26], bone_col, ["Wing" + S], seg=8)
        c.tube([m, t], [0.26, 0.12], bone_col, ["WingTip" + S], seg=8)
        c.spike(m, m + P(s * 0.2, 0.7, -0.3), 0.18, edge_col or bone_col, "WingTip" + S, seg=5, n=3)   # thumb claw
        ends = []
        for f in range(fingers):
            k = f / max(1, fingers - 1)
            end = m + (P(s * (1.2 + 2.6 * (1 - k)), -1.0 - 3.2 * k, 0.6 + 2.4 * k))
            c.tube([m, m.lerp(end, 0.5), end], [0.16, 0.12, 0.06], bone_col, ["WingTip" + S], seg=6)
            ends.append(end)
        # membrane: one panel per gap between bones, scalloped trailing edge
        body = r + P(0, -1.8, 1.8)
        chain = [t] + ends + [body]
        for i in range(len(chain) - 1):
            a1, b1 = chain[i], chain[i + 1]
            mid_edge = (a1 + b1) / 2 + (m - (a1 + b1) / 2) * 0.22     # scallop pulls in toward the wrist
            if i == len(chain) - 2:
                panel = [m, a1, mid_edge, b1, r]
                bones = "Wing" + S
            else:
                panel = [m, a1, mid_edge, b1]
                bones = "WingTip" + S
            c.sheet(panel, skin_col, bones, thick=0.1)
        if edge_col and glow_edge:
            for e in ends:
                c.ellipsoid(e, (0.16, 0.16, 0.16), edge_col, "WingTip" + S, glow=True)


# ============================================================== BIPED
def biped(c, col, H=1.0, W=1.0, arm_len=1.0, leg_len=1.0, torso=None):
    """2-legged body (golems, warlocks, owls). Returns key points."""
    hip_y = 2.8 * leg_len * H
    sh_y = hip_y + 3.0 * H
    x_leg, x_arm = 0.75 * W, 1.9 * W
    c.bone("Root", P(0, 0, 0), P(0, 1, 0))
    c.bone("Hips", P(0, hip_y, 0), P(0, hip_y + 1.2 * H, 0), "Root")
    c.bone("Chest", P(0, hip_y + 1.2 * H, 0), P(0, sh_y, 0), "Hips")
    c.bone("Neck", P(0, sh_y, 0), P(0, sh_y + 0.6 * H, 0), "Chest")
    c.bone("Head", P(0, sh_y + 0.6 * H, 0), P(0, sh_y + 2.2 * H, 0), "Neck")
    for s, S in ((-1, "L"), (1, "R")):
        c.bone("Thigh" + S, P(s * x_leg, hip_y, 0), P(s * x_leg, hip_y * 0.5, -0.1), "Hips")
        c.bone("Shin" + S, P(s * x_leg, hip_y * 0.5, -0.1), P(s * x_leg, 0.3, 0), "Thigh" + S)
        c.bone("Arm" + S, P(s * x_arm, sh_y - 0.2, 0), P(s * x_arm * 1.05, sh_y - 1.8 * arm_len * H, 0), "Chest")
        c.bone("Fore" + S, P(s * x_arm * 1.05, sh_y - 1.8 * arm_len * H, 0), P(s * x_arm * 1.08, sh_y - 3.4 * arm_len * H, -0.3), "Arm" + S)
    return dict(hip_y=hip_y, sh_y=sh_y, x_leg=x_leg, x_arm=x_arm)


def biped_anims(c, stride=22, arm=20, bob=0.12, extra=None, sway=3):
    def walk(t):
        p = tau * t
        out = {
            "Root": ((0, 0, sway * sin(p)), (0, bob * abs(sin(p * 2)), 0)),
            "Chest": (3, 5 * sin(p), 0), "Head": (-2, -4 * sin(p), 0),
            "ThighL": (-stride * sin(p), 0, 0), "ThighR": (stride * sin(p), 0, 0),
            "ShinL": (25 * max(0, sin(p + 0.5)), 0, 0), "ShinR": (25 * max(0, -sin(p + 0.5)), 0, 0),
            "ArmL": (arm * sin(p), 0, 4), "ArmR": (-arm * sin(p), 0, -4),
            "ForeL": (-10 - 8 * sin(p), 0, 0), "ForeR": (-10 + 8 * sin(p), 0, 0),
        }
        if extra:
            out.update(extra(t, True))
        return out

    def idle(t):
        p = tau * t
        out = {
            "Root": ((0, 0, 0), (0, 0.05 * sin(2 * p), 0)),
            "Chest": (2 * sin(2 * p), 4 * sin(p), 0), "Head": (3 * sin(2 * p + 1), 16 * sin(p), 0),
            "ArmL": (4 * sin(2 * p), 0, 5 + 3 * sin(2 * p)), "ArmR": (4 * sin(2 * p + 1), 0, -5 - 3 * sin(2 * p)),
            "ForeL": (-12, 0, 0), "ForeR": (-12, 0, 0),
        }
        if extra:
            out.update(extra(t, False))
        return out
    c.animate({"Walk": (24, 1.0, walk), "Idle": (40, 4.0, idle)})


# ============================================================== SWIMMER / SERPENT / FLOATER
def spine(c, pts, names=None, parent="Root"):
    """chain of bones through pts; returns names"""
    names = names or ["Spine%d" % (i + 1) for i in range(len(pts) - 1)]
    prev = parent
    for i in range(len(pts) - 1):
        c.bone(names[i], pts[i], pts[i + 1], prev)
        prev = names[i]
    return names


def swim_anims(c, chain, fins=(), amp=10, axis="yaw", rate=1, extra=None, hover=0.4):
    """undulating body: each chain bone rotates with a travelling wave. axis yaw (snake/fish) or pitch (whale)"""
    def mk(speed, a_mul):
        def fn(t):
            p = tau * t * rate
            out = {"Root": ((0, 0, 0), (0, hover * sin(p if speed < 1 else 2 * p), 0))}
            for i, n in enumerate(chain):
                ang = amp * a_mul * sin(p * speed - i * 0.9) * (0.4 + 0.6 * i / max(1, len(chain) - 1))
                out[n] = (ang, 0, 0) if axis == "pitch" else (0, ang, 0)
            for i, (n, side) in enumerate(fins):
                out[n] = (0, 0, side * (14 * a_mul) * sin(p * speed * 1.3 + i))
            if extra:
                out.update(extra(t, speed > 1))
            return out
        return fn
    c.animate({"Walk": (24, 1.0, mk(2, 1.3)), "Idle": (40, 4.0, mk(1, 0.8))})


def aura(c, style, color, color2=None, rarity=None):
    c.extra.update({"aura": {"style": style, "color": list(color), "color2": list(color2 or color)}})
    if rarity:
        c.extra["rarity"] = rarity


def stripes(col, axis="z", period=0.7, width=0.3, wobble=0.25, only=None):
    """painted stripes (per pixel). axis z = bands around the body. only = fn(x,y,z)->bool array"""
    def mask(X, Y, Z):
        U = {"z": Z, "y": Y, "x": X}[axis] + wobble * np.sin(X * 2.2 + Y * 1.3) + 0.12 * np.sin(Y * 5.1)
        m = np.mod(U, period) < width * (0.75 + 0.25 * np.cos(X * 1.7))
        if only is not None:
            m &= only(X, Y, Z)
        return m
    return (col, mask)


def spots(col, size=0.5, density=0.3, seed=1, only=None):
    def mask(X, Y, Z):
        cx, cy, cz = np.floor(X / size), np.floor(Y / size), np.floor(Z / size)
        h = np.sin(cx * 12.9898 + cy * 78.233 + cz * 37.719 + seed) * 43758.5453
        h = h - np.floor(h)
        fx, fy, fz = X / size - cx - 0.5, Y / size - cy - 0.5, Z / size - cz - 0.5
        m = (h < density) & (fx * fx + fy * fy + fz * fz < 0.16)
        if only is not None:
            m &= only(X, Y, Z)
        return m
    return (col, mask)


def band(col, lo, hi, axis="y"):
    """solid painted region between two heights (e.g. a darker back / lighter belly)"""
    def mask(X, Y, Z):
        U = {"z": Z, "y": Y, "x": X}[axis]
        return (U >= lo) & (U <= hi)
    return (col, mask)

