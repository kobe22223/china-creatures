"""creature _data.json -> compact Luau ModuleScript source (one per creature)."""
import json, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "lua")
os.makedirs(OUT, exist_ok=True)


def qmul_vec(q, v):
    w, x, y, z = q
    # rotate v by quaternion
    ux, uy, uz = x, y, z
    vx, vy, vz = v
    cx = uy * vz - uz * vy; cy = uz * vx - ux * vz; cz = ux * vy - uy * vx
    cx2 = uy * cz - uz * cy; cy2 = uz * cx - ux * cz; cz2 = ux * cy - uy * cx
    return (vx + 2 * (w * cx + cx2), vy + 2 * (w * cy + cy2), vz + 2 * (w * cz + cz2))


def num(x, d=3):
    s = ("%." + str(d) + "f") % x
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return "0" if s in ("-0", "") else s


def convert(path):
    d = json.load(open(path))
    bones = d["bones"]
    names = [b["name"] for b in bones]
    lines = ["-- generated from Blender (" + d["name"] + "). Rotations per bone per frame (w,x,y,z, game axes)",
             "-- + root offset per frame. Positions are rebuilt in game from the real bone positions.",
             "return {", '\tName = "%s", Height = %s, Body = "%s",' % (d["name"], num(d["height"]), d.get("body", d["name"] + "_Body"))]
    lines.append("\tBones = {" + ", ".join('{"%s", %s, Vector3.new(%s)}' % (b["name"], ('"%s"' % b["parent"]) if b["parent"] else "nil", ", ".join(num(v) for v in b["head"])) for b in bones) + "},")
    glow = d.get("glow", {})
    if isinstance(glow, dict):
        lines.append("\tGlow = {" + ", ".join('["%s"] = "%s"' % (k, v) for k, v in glow.items()) + "},")
    ex = d.get("extra", {})
    au = ex.get("aura")
    if au:
        lines.append('\tAura = {Style = "%s", Color = Color3.fromRGB(%s), Color2 = Color3.fromRGB(%s)},' % (au["style"], ", ".join(map(str, au["color"])), ", ".join(map(str, au["color2"]))))
    lines.append("\tHover = %s, Speed = %s," % (num(ex.get("hover", 0)), num(ex.get("speed", 1))))
    lines.append("\tClips = {")
    root_head = bones[0]["head"]
    for clip, cd in d["anims"].items():
        q, off = [], []
        for fr in cd["frames"]:
            for n in names:
                w, x, y, z, tx, ty, tz = fr[n]
                q.extend([w, x, y, z])
            w, x, y, z, tx, ty, tz = fr[names[0]]
            rh = qmul_vec((w, x, y, z), root_head)
            off.extend([tx - (root_head[0] - rh[0]), ty - (root_head[1] - rh[1]), tz - (root_head[2] - rh[2])])
        lines.append('\t\t%s = {Fps = %s, Frames = %d,' % (clip, num(cd["fps"]), len(cd["frames"])))
        lines.append("\t\t\tQ = {" + ",".join(num(v, 3) for v in q) + "},")
        lines.append("\t\t\tOff = {" + ",".join(num(v, 3) for v in off) + "}},")
    lines.append("\t},")
    lines.append("}")
    src = "\n".join(lines)
    out = os.path.join(OUT, d["name"] + ".lua")
    open(out, "w").write(src)
    return d["name"], len(src)


if __name__ == "__main__":
    tot = 0
    for cid in open(os.path.join(HERE, "list.txt")).read().split():
        dd = os.path.join(HERE, "out", cid)
        js = [f for f in os.listdir(dd) if f.endswith("_data.json")][0]
        n, sz = convert(os.path.join(dd, js))
        tot += sz
        print(n, sz)
    print("TOTAL", tot)

