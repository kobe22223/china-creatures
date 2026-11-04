"""TIER 7, DRAGON SCALE TREADMILL: the treadmill is a dragon. Its big head (antlers, whiskers, open jaw, glowing
eyes) forms the console; its scaled body runs back along the left rail, crosses behind the belt, runs forward along
the right rail and coils down under the frame, and its tail curls up high behind the belt. Gold belly plates line
the deck edges and one front claw holds a glowing pearl."""
from tm import *

TEAL, TEAL2, JADET, GOLDD, BELLYD, WHISK, EYE, PEARL, CLAWD, BELT = (
    C(30, 130, 135), C(20, 90, 100), C(80, 190, 140), C(255, 200, 60), C(240, 220, 150), C(255, 240, 200),
    C(255, 210, 50), C(220, 255, 245), C(250, 245, 230), C(35, 55, 60))


def build():
    c = tread("China7")
    scl = scale_paint(JADET, size=0.55, width=0.07)
    deck(c, BELT, TEAL2, roller=TEAL2, rims=False, belt_paint=bands(C(45, 70, 75), "z", period=0.9, width=0.12))
    # gold belly plates along both deck edges
    for s in (-1, 1):
        for i in range(11):
            z = -9.5 + i * 1.9
            rbox(c, V(s * 3.0, 0.75, z), (0.32, 0.5, 0.82), GOLDD, bevel=0.2, seg=1, stud=False)
        rbox(c, V(s * 3.0, 0.3, 0), (0.4, 0.3, 10.6), TEAL2, bevel=0.15)
    # the body: left rail back, across behind the belt, right rail forward, then coiling down under the frame
    y = 3.6
    path = [V(-2.2, 6.0, -8.8), V(-3.5, 4.6, -6.5), V(-3.5, y, -2.0), V(-3.5, y, 3.0), V(-3.45, 2.9, 8.8), V(-2.2, 2.1, 11.0),
            V(2.2, 2.1, 11.0), V(3.45, 2.9, 8.8), V(3.5, y, 3.0), V(3.5, y, -2.0), V(3.5, 3.0, -5.6), V(3.4, 1.1, -6.6)]
    radii = [0.62, 0.6, 0.58, 0.56, 0.54, 0.52, 0.5, 0.5, 0.5, 0.48, 0.46, 0.44]
    T(c, path, radii, TEAL, R, seg=12, sub=3, paint=scl)
    fur_line(c, [p + V(0, r * 0.85, 0) for p, r in zip(path[1:-2], radii[1:-2])], GOLDD, R, length=0.65, width=0.4, out=V(0, 1, 0.4), n_per=2, seed=7)
    # tail rising from under the back and curling up high behind the belt (z > 10, so the air over the belt stays clear)
    tail = [V(0, 0.8, 10.6), V(0, 2.5, 11.5), V(0, 5.0, 11.7), V(0, 7.2, 11.2), V(0, 8.2, 10.8), V(0, 7.7, 10.5)]
    T(c, tail, [0.5, 0.48, 0.42, 0.34, 0.24, 0.12], TEAL, R, seg=10, sub=3, paint=scl)
    fur_line(c, tail[2:], GOLDD, R, length=0.8, width=0.45, out=V(0, 0.4, 1), n_per=3, seed=8)
    # legs: front claws reach down to the floor at the console, one holding the pearl
    for s in (-1, 1):
        sh = V(s * 2.6, 5.0, -8.6)
        paw = V(s * 3.3, 0.35, -10.0)
        T(c, [sh, sh.lerp(paw, 0.5) + V(s * 0.5, 0.3, -0.3), paw], [0.42, 0.36, 0.32], TEAL, R, seg=10, sub=2, paint=scl)
        claws3(c, paw, CLAWD, R, size=0.3, spread=0.28, z=-0.6)
    E(c, V(3.3, 1.0, -10.9), (0.5, 0.5, 0.5), PEARL, R, seg=(14, 10), glow=True)
    # the head is the console: dragon head facing +z towards the runner, raised above the console end
    hb = V(0, 7.4, -10.6)
    n0 = len(c.shapes)
    dragon_head(c, hb, 1.2, TEAL, BELLYD, GOLDD, WHISK, GOLDD, EYE, bone=R, horns="antler", seed=9, brow=TEAL2)
    turn_around(c, n0, hb)          # the head is built facing -z; turn it to face the runner (+z)
    T(c, [path[0], hb + V(0, -0.3, 0.2)], [0.62, 0.75], TEAL, R, seg=12, sub=1, paint=scl)   # neck joins the head to the body
    # console plate with a dark jade screen, tucked under the dragon's chin
    sc, hc, n = console(c, TEAL, C(20, 40, 45), glow=None, posts=False, head_half=(2.6, 0.7, 0.65), y=5.6, z=-9.6, screen_half=(1.8, 0.45),
                        body_paint=scl)
    return c
