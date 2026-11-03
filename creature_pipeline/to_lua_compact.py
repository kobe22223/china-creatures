"""compact creature data: quaternions packed as 12-bit x,y,z (w >= 0 rebuilt), 2 base64 chars each."""
import json, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "lua_compact"); os.makedirs(OUT, exist_ok=True)
from to_lua import qmul_vec
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
def enc(v):
    q = max(0, min(4095, int(round((v + 1) * 2047.5))))
    return A[q >> 6] + A[q & 63]
def num(x, d=2):
    s = ("%." + str(d) + "f") % x
    s = s.rstrip("0").rstrip(".") if "." in s else s
    return "0" if s in ("-0", "") else s
def convert(path):
    d = json.load(open(path)); bones = d["bones"]; names = [b["name"] for b in bones]
    L = ['return {Name = "%s", Height = %s, Body = "%s",' % (d["name"], num(d["height"]), d.get("body", d["name"] + "_Body"))]
    L.append("Bones = {" + ", ".join('{"%s", %s, Vector3.new(%s)}' % (b["name"], ('"%s"' % b["parent"]) if b["parent"] else "nil", ", ".join(num(v, 3) for v in b["head"])) for b in bones) + "},")
    L.append("Glow = {" + ", ".join('["%s"] = "%s"' % (k, v) for k, v in d.get("glow", {}).items()) + "},")
    ex = d.get("extra", {}); au = ex.get("aura")
    if au:
        L.append('Aura = {Style = "%s", Color = Color3.fromRGB(%s), Color2 = Color3.fromRGB(%s)}, Rarity = "%s",' % (au["style"], ", ".join(map(str, au["color"])), ", ".join(map(str, au["color2"])), ex.get("rarity", "")))
    L.append("Hover = %s, Speed = %s," % (num(ex.get("hover", 0)), num(ex.get("speed", 1))))
    L.append("Clips = {")
    root_head = bones[0]["head"]
    for clip, cd in d["anims"].items():
        qs, off = [], []
        for fr in cd["frames"]:
            for n in names:
                w, x, y, z = fr[n][:4]
                if w < 0: w, x, y, z = -w, -x, -y, -z
                qs.append(enc(x) + enc(y) + enc(z))
            w, x, y, z, tx, ty, tz = fr[names[0]]          # root offset (as in to_lua.py)
            rh = qmul_vec((w, x, y, z), root_head)
            off += [num(tx - (root_head[0] - rh[0])), num(ty - (root_head[1] - rh[1])), num(tz - (root_head[2] - rh[2]))]
        L.append('%s = {Fps = %s, Frames = %d, Qs = "%s", Off = {%s}},' % (clip, num(cd["fps"], 3), len(cd["frames"]), "".join(qs), ",".join(off)))
    L.append("}}")
    src = "\n".join(L)
    open(os.path.join(OUT, d["name"] + ".lua"), "w").write(src)
    return d["name"], len(src)
if __name__ == "__main__":
  ids = sys.argv[1:] or open(os.path.join(HERE, "list.txt")).read().split()
  for i in ids:
      dj = [f for f in os.listdir(os.path.join(HERE, "out", i)) if f.endswith("_data.json")][0]
      print(*convert(os.path.join(HERE, "out", i, dj)))

