"""Cartoon UI icons in the style of Kobe's icon set (thick dark outline, bevelled 3D edge, glossy gradient,
diagonal shine streaks). Outputs 512px PNGs."""
import cairosvg, os
OUT = os.path.dirname(os.path.abspath(__file__))
INK = "#160c07"
_id = [0]


def uid(p):
    _id[0] += 1
    return f"{p}{_id[0]}"


def grad(c1, c2, x1=0, y1=0, x2=0, y2=1):
    g = uid("g")
    return g, f'<linearGradient id="{g}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'


def piece(d, top, bottom, side, depth=12, outline=13, shine=True, transform=""):
    """a bevelled flat shape: dark side extruded down by `depth`, glossy top face, outline around both"""
    defs, body = [], []
    g, gd = grad(top, bottom)
    defs.append(gd)
    clip = uid("c")
    defs.append(f'<clipPath id="{clip}"><path d="{d}"/></clipPath>')
    t = f' transform="{transform}"' if transform else ""
    body.append(f'<g{t}>')
    # outline around top + side
    body.append(f'<path d="{d}" transform="translate(0,{depth})" fill="{INK}" stroke="{INK}" stroke-width="{outline * 2}" stroke-linejoin="round"/>')
    body.append(f'<path d="{d}" fill="{INK}" stroke="{INK}" stroke-width="{outline * 2}" stroke-linejoin="round"/>')
    body.append(f'<path d="{d}" transform="translate(0,{depth})" fill="{side}"/>')
    body.append(f'<path d="{d}" fill="url(#{g})"/>')
    if shine:
        body.append(f'<g clip-path="url(#{clip})" opacity="0.38">'
                    f'<path d="M-40 150 L150 -40 L185 -40 L-5 150 Z" fill="#fff"/>'
                    f'<path d="M20 230 L240 10 L262 10 L42 230 Z" fill="#fff"/>'
                    f'<path d="M120 300 L330 90 L345 90 L135 300 Z" fill="#fff"/></g>')
        # light rim on the top-left edge of the face
        body.append(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-opacity="0.45" stroke-width="5" clip-path="url(#{clip})" transform="translate(3,4)"/>')
    body.append('</g>')
    return defs, body


def svg(parts, name):
    defs, body = [], []
    for d, b in parts:
        defs += d; body += b
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="512" height="512"><defs>{"".join(defs)}</defs>{"".join(body)}</svg>'
    open(os.path.join(OUT, name + ".svg"), "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(OUT, name + ".png"), output_width=512, output_height=512)


def ell(cx, cy, rx, ry):
    return f"M{cx - rx} {cy} a{rx} {ry} 0 1 0 {2 * rx} 0 a{rx} {ry} 0 1 0 {-2 * rx} 0 Z"


def rrect(x, y, w, h, r):
    return f"M{x + r} {y} H{x + w - r} Q{x + w} {y} {x + w} {y + r} V{y + h - r} Q{x + w} {y + h} {x + w - r} {y + h} H{x + r} Q{x} {y + h} {x} {y + h - r} V{y + r} Q{x} {y} {x + r} {y} Z"


# ---------- INDEX: blue book with white pages, red bookmark and a gold star
book = [
    piece(rrect(52, 58, 150, 150, 14), "#ffffff", "#c9d8ee", "#8ea3c4", depth=14, shine=False, transform="rotate(-8 128 128) translate(10,6)"),
    piece(rrect(40, 40, 150, 150, 16), "#5ab8ff", "#1c64d8", "#123f8f", depth=10, transform="rotate(-8 128 128)"),
    piece(rrect(40, 40, 30, 150, 10), "#2f7fe6", "#123f8f", "#0c2c66", depth=10, shine=False, transform="rotate(-8 128 128)"),
    piece("M150 30 L176 30 L176 92 L163 80 L150 92 Z", "#ff5a5a", "#c41020", "#7d0710", depth=4, outline=8, shine=False, transform="rotate(-8 128 128)"),
    piece("M125 82 L136 106 L162 108 L142 124 L149 150 L125 136 L101 150 L108 124 L88 108 L114 106 Z", "#fff27a", "#ffb400", "#b06a00", depth=5, outline=8, transform="rotate(-8 128 128)"),
]
svg(book, "Icon_Index")

# ---------- EGGS: cream egg with blue / green / orange spots
eggd = "M128 30 C178 30 208 112 208 154 C208 202 172 230 128 230 C84 230 48 202 48 154 C48 112 78 30 128 30 Z"
spots = []
for (cx, cy, rx, ry, c1, c2) in [(96, 118, 20, 24, "#6fd2ff", "#2a8de8"), (150, 92, 16, 18, "#8bf06a", "#34b52a"), (160, 160, 22, 20, "#ffb35a", "#f06a12"),
                                  (104, 186, 16, 14, "#8bf06a", "#34b52a"), (130, 140, 10, 10, "#ff7aa8", "#e0306a")]:
    spots.append(piece(ell(cx, cy, rx, ry), c1, c2, c2, depth=0, outline=5, shine=False))
svg([piece(eggd, "#fffdf2", "#e9d8b0", "#b39a6a", depth=10)] + spots, "Icon_Eggs")

# ---------- PETS: big orange paw print
paw = [piece(ell(128, 160, 58, 48), "#ffbd6b", "#e66f12", "#9a420a", depth=10)]
for (cx, cy, rx, ry) in [(62, 100, 22, 28), (102, 66, 24, 30), (154, 66, 24, 30), (194, 100, 22, 28)]:
    paw.append(piece(ell(cx, cy, rx, ry), "#ffbd6b", "#e66f12", "#9a420a", depth=8))
svg(paw, "Icon_Pets")

# ---------- SPEED: red sneaker with white sole and laces
sole = "M26 176 L222 176 Q236 176 234 190 Q232 204 216 204 L36 204 Q20 204 20 190 Q20 176 26 176 Z"
upper = "M30 176 L44 96 Q48 82 62 86 L104 98 Q118 102 128 116 L150 134 L206 148 Q230 156 228 176 Z"
laces = "".join("")
shoe = [piece(upper, "#ff6a5a", "#d2141e", "#86080e", depth=6),
        piece(sole, "#ffffff", "#cfd6e2", "#8a93a6", depth=8, shine=False)]
for i, (x, y) in enumerate([(96, 112), (112, 122), (128, 134)]):
    shoe.append(piece(rrect(x - 4, y - 14, 30, 9, 4), "#ffffff", "#dfe5ef", "#9aa3b5", depth=2, outline=5, shine=False, transform=f"rotate(28 {x} {y})"))
shoe.append(piece("M40 150 L86 150 L80 164 L36 164 Z", "#ffffff", "#e5e9f2", "#9aa3b5", depth=2, outline=5, shine=False))
svg(shoe, "Icon_Speed")

# ---------- CASH: stack of green bills
cash = []
for i, (dx, dy, rot) in enumerate([(10, 40, -12), (0, 20, -6), (-6, 0, 2)]):
    t = f"translate({dx},{dy}) rotate({rot} 128 120)"
    cash.append(piece(rrect(34, 78, 188, 96, 12), "#8ef06a", "#2fb33a", "#16701f", depth=8, transform=t))
    cash.append(piece(ell(128, 126, 26, 26), "#e8ffd2", "#9ee082", "#4f9a3c", depth=0, outline=6, shine=False, transform=t))
    cash.append((["" ], [f'<g transform="{t}"><path d="M139 113 Q128 105 119 112 Q111 121 128 126 Q145 131 138 141 Q128 149 116 141" fill="none" stroke="#14531a" stroke-width="7" stroke-linecap="round"/><path d="M128 102 V150" stroke="#14531a" stroke-width="6" stroke-linecap="round"/></g>']))
svg(cash, "Icon_Cash")

# ---------- CODES: blue rounded badge with a white tick
check = [piece(ell(128, 120, 92, 92), "#5fc4ff", "#1360d8", "#0b3a8a", depth=12),
         piece("M80 122 L106 96 L122 112 L164 66 L190 92 L122 162 Z", "#ffffff", "#dde8f6", "#8fa4c4", depth=6, outline=8, shine=False)]
svg(check, "Icon_Codes")

# ---------- POWERS: yellow lightning bolt
bolt = [piece("M150 20 L58 140 L118 140 L92 236 L198 100 L136 100 L170 20 Z", "#fff27a", "#ffae00", "#a85f00", depth=12)]
svg(bolt, "Icon_Powers")
print("done")

# ---------- BAT: wooden baseball bat, diagonal, dark grip
import math
def batpath():
    # along the x axis from handle (x=30) to barrel end (x=226), then rotated -45 deg about the centre
    return "M30 120 L120 116 Q170 102 214 104 Q232 106 232 128 Q232 150 214 152 Q170 154 120 140 L30 136 Q22 128 30 120 Z"
bat = [piece(batpath(), "#ffd38a", "#c47a2c", "#7a4414", depth=10, transform="rotate(-42 128 128)"),
       piece("M26 116 L76 116 L76 140 L26 140 Q18 128 26 116 Z", "#5a4a6a", "#2c2236", "#18121e", depth=10, shine=False, transform="rotate(-42 128 128)"),
       piece(ell(22, 128, 9, 16), "#7a6a8a", "#3a2e46", "#18121e", depth=6, outline=8, shine=False, transform="rotate(-42 128 128)")]
svg(bat, "Icon_Bat")

# ---------- TRAP: steel bear trap, open jaws with teeth
teeth = []
n = 14
ring_out = []
for i in range(n * 2):
    a = math.pi * 2 * i / (n * 2)
    r = 104 if i % 2 == 0 else 80
    ring_out.append((128 + r * math.cos(a), 136 + r * 0.78 * math.sin(a)))
outer = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in ring_out) + " Z"
trap = [piece(outer, "#e6ecf5", "#8a96aa", "#4a5466", depth=12),
        piece(ell(128, 136, 62, 48), "#4a5466", "#2a3140", "#1a1f2a", depth=0, outline=8, shine=False),
        piece(ell(128, 136, 26, 20), "#ffd34a", "#e08a00", "#8a5200", depth=6, outline=8),
        piece("M60 136 L196 136 L196 146 L60 146 Z", "#c9d2e0", "#7c879a", "#4a5466", depth=4, outline=6, shine=False)]
svg(trap, "Icon_Trap")

