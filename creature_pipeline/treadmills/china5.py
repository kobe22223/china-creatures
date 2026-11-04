"""TIER 5, PORCELAIN TREADMILL: the whole body looks like blue-and-white porcelain. White glaze with cobalt wave
bands and round flower motifs painted on, console posts shaped like slim vases with lotus-bud tops, a cobalt blue
belt with white wave lines, a little gold, and a pale blue glowing screen."""
from tm import *

WHITE, COBALT_, COBALT2, GOLDP, SCREEN = C(248, 250, 255), C(35, 70, 175), C(70, 110, 205), C(255, 205, 80), C(170, 215, 255)


def porcelain(col=COBALT_, wave_y=(0.3, 0.55), scale=1.0):
    """cobalt wave band near the bottom + round flower medallions above it (painted)"""
    def mask(X, Y, Z):
        w = np.abs(Y - (wave_y[0] + 0.12 * np.sin(Z * 3.0 * scale) + 0.12 * np.sin(X * 3.0 * scale))) < 0.07
        w |= np.abs(Y - (wave_y[1] + 0.12 * np.sin(Z * 3.0 * scale + 1.6) + 0.12 * np.sin(X * 3.0 * scale + 1.6))) < 0.05
        cz = np.round(Z / 2.4) * 2.4
        cy = 1.15
        d = np.sqrt((Z - cz) ** 2 + (Y - cy) ** 2)
        petals = (np.abs(d - 0.32 - 0.1 * np.cos(6 * np.arctan2(Y - cy, Z - cz))) < 0.06) | (d < 0.1)
        return w | (petals & (Y > 0.75))
    return (col, mask)


def vase_post(c, x, z, top):
    """slim vase-shaped post with a cobalt neck band and a lotus-bud cap"""
    prof = [(0.0, 0.42), (0.15, 0.5), (0.25, 0.36), (0.55, 0.28), (0.8, 0.34), (0.92, 0.42), (1.0, 0.3)]
    pts = [V(x, DECK_TOP - 0.1 + (top - DECK_TOP) * t, z + 0.3 * t) for t, _ in prof]
    T(c, pts, [r for _, r in prof], WHITE, R, seg=12, sub=2, paint=bands(COBALT_, "y", period=1.1, width=0.12))
    E(c, pts[-1] + V(0, 0.25, 0), (0.28, 0.4, 0.28), COBALT2, R, seg=(10, 6))
    E(c, pts[-1] + V(0, 0.68, 0), (0.1, 0.1, 0.1), GOLDP, R, seg=(8, 5), stud=False)


def build():
    c = tread("China5")
    deck(c, COBALT_, WHITE, roller=COBALT2, belt_paint=bands(COBALT2, "z", period=1.4, width=0.12), rims=False)
    for s in (-1, 1):
        rbox(c, V(s * 3.3, 0.8, 0), (0.6, 0.8, 10.7), WHITE, bevel=0.35, paint=porcelain())
        rbox(c, V(s * 3.3, 1.64, 0), (0.62, 0.06, 10.72), GOLDP, bevel=0.05, seg=1, stud=False)
        for z in (-10.3, 10.3):
            E(c, V(s * 3.3, 0.16, z), (0.62, 0.16, 0.62), COBALT_, R, seg=(12, 5))
    rbox(c, V(0, 0.55, 10.95), (3.9, 0.55, 0.35), WHITE, bevel=0.25, paint=porcelain())
    for s in (-1, 1):
        vase_post(c, s * 2.45, -9.6, 6.1)
    sc, hc, n = console(c, WHITE, SCREEN, glow=SCREEN, posts=False, head_half=(3.0, 0.9, 0.75), body_paint=porcelain(wave_y=(6.0, 6.25)))
    # a little porcelain vase standing on the console
    vb = hc + V(0, 0.85, -0.2)
    T(c, [vb, vb + V(0, 0.45, 0), vb + V(0, 1.0, 0), vb + V(0, 1.3, 0)], [0.35, 0.5, 0.22, 0.3], WHITE, R, seg=12, sub=2, paint=bands(COBALT_, "y", period=0.35, width=0.08))
    rails(c, COBALT2, r=0.25)
    # big blue-and-white ginger jars at the back corners
    for sx in (-1, 1):
        jb = V(sx * 3.55, 1.7, 11.6)
        T(c, [jb, jb + V(0, 0.6, 0), jb + V(0, 1.5, 0), jb + V(0, 2.1, 0), jb + V(0, 2.3, 0)], [0.55, 0.95, 0.9, 0.5, 0.42], WHITE, R, seg=14, sub=2,
          paint=porcelain(wave_y=(2.1, 2.4)))
        E(c, jb + V(0, 2.45, 0), (0.5, 0.3, 0.5), COBALT_, R, seg=(12, 6))
        E(c, jb + V(0, 2.8, 0), (0.14, 0.14, 0.14), GOLDP, R, seg=(8, 5), stud=False)
        rbox(c, jb + V(0, -0.9, 0), (0.75, 0.8, 0.75), COBALT2, bevel=0.2)
    for s in (-1, 1):
        E(c, V(s * 3.05, 4.6, -1.5), (0.3, 0.3, 0.3), GOLDP, R, seg=(10, 6), stud=False)
    return c
