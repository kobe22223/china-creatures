"""Generate seamless stud tiles that match the box icons (square inset studs).
Output is black/white on transparent, so it overlays any coloured panel in Roblox."""
import sys
from PIL import Image, ImageDraw, ImageFilter

OUT = sys.argv[1]
S = 4  # supersample factor


def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)


def square_stud(tile=128, stud=86, radius=10, edge=9):
    T, st, r, e = tile * S, stud * S, radius * S, edge * S
    o = (T - st) // 2
    img = Image.new("RGBA", (T, T), (0, 0, 0, 0))

    # soft dark inset body (slightly darker than the panel)
    body = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    rounded(ImageDraw.Draw(body), (o, o, o + st, o + st), r, (0, 0, 0, 34))
    img.alpha_composite(body)

    # dark shading on the top + left inner edges (light comes from bottom-right, like the icons)
    shade = Image.new("L", (T, T), 0)
    d = ImageDraw.Draw(shade)
    rounded(d, (o, o, o + st, o + st), r, 255)
    rounded(d, (o + e, o + e, o + st + e, o + st + e), r, 0)
    dark = Image.new("RGBA", (T, T), (0, 0, 0, 120))
    dark.putalpha(shade.point(lambda v: v * 120 // 255))
    img.alpha_composite(dark)

    # light rim on the bottom + right inner edges
    rim = Image.new("L", (T, T), 0)
    d = ImageDraw.Draw(rim)
    rounded(d, (o, o, o + st, o + st), r, 255)
    rounded(d, (o - e // 2, o - e // 2, o + st - e // 2, o + st - e // 2), r, 0)
    light = Image.new("RGBA", (T, T), (255, 255, 255, 0))
    light.putalpha(rim.point(lambda v: v * 95 // 255))
    img.alpha_composite(light)

    img = img.filter(ImageFilter.GaussianBlur(S * 0.6))
    return img.resize((tile, tile), Image.LANCZOS)


def round_stud(tile=128, stud=78, edge=9):
    T, st, e = tile * S, stud * S, edge * S
    o = (T - st) // 2
    img = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    # drop shadow down-right
    sh = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((o + e, o + e, o + st + e, o + st + e), fill=(0, 0, 0, 90))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(S * 2)))
    # stud top
    ImageDraw.Draw(img).ellipse((o, o, o + st, o + st), fill=(255, 255, 255, 40))
    # highlight crescent top-left
    hl = Image.new("L", (T, T), 0)
    d = ImageDraw.Draw(hl)
    d.ellipse((o, o, o + st, o + st), fill=255)
    d.ellipse((o + e, o + e, o + st + e, o + st + e), fill=0)
    white = Image.new("RGBA", (T, T), (255, 255, 255, 0))
    white.putalpha(hl.point(lambda v: v * 150 // 255))
    img.alpha_composite(white)
    return img.filter(ImageFilter.GaussianBlur(S * 0.6)).resize((tile, tile), Image.LANCZOS)


def preview(tiles, path):
    colours = [(235, 40, 60), (230, 40, 160), (70, 60, 230), (60, 200, 70), (255, 190, 30)]
    W = 260
    out = Image.new("RGBA", (W * len(colours), W * len(tiles)), (40, 40, 40, 255))
    for row, t in enumerate(tiles):
        small = t.resize((40, 40), Image.LANCZOS)
        for col, c in enumerate(colours):
            panel = Image.new("RGBA", (W - 10, W - 10), c + (255,))
            for y in range(0, W, 40):
                for x in range(0, W, 40):
                    panel.alpha_composite(small, (x, y)) if x + 40 <= W - 10 and y + 40 <= W - 10 else None
            out.alpha_composite(panel, (col * W + 5, row * W + 5))
    out.save(path)


sq = square_stud()
rd = round_stud()
sq.save(f"{OUT}/Stud_Square_Tile.png")
rd.save(f"{OUT}/Stud_Round_Tile.png")
preview([sq, rd], f"{OUT}/stud_preview.png")
print("ok")

