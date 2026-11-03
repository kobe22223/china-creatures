"""CreatureData.rbxmx: one ModuleScript per creature (compact anims + bone rest CFrames + batch layout)."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Matrix
import restcf
import to_lua_compact as tlc
RY180 = Matrix(((-1, 0, 0), (0, 1, 0), (0, 0, -1)))
src = open(os.path.join(HERE, "batch_fbx.py")).read()
BATCHES = eval(src[src.index("BATCHES = {") + 10: src.index("}\nonly") + 1])
items = []
def built(cid):
    d = f"{HERE}/out/{cid}"
    return os.path.isdir(d) and any(f.endswith("_data.json") for f in os.listdir(d))
for bname, ids in BATCHES.items():
    if not all(built(i) for i in ids):
        print("SKIP", bname)
        continue
    for i, cid in enumerate(ids):
        name, rest = restcf.rest(cid)
        dj = [f for f in os.listdir(f"{HERE}/out/{cid}") if f.endswith("_data.json")][0]
        nm, _ = tlc.convert(f"{HERE}/out/{cid}/{dj}")
        lua = open(f"{HERE}/out/lua_compact/{nm}.lua").read().rstrip()
        assert lua.endswith("}}")
        rs = []
        for n, p, pos, R in rest:
            M = Matrix(R) @ RY180
            q = M.to_quaternion()
            if q.w < 0: q = -q
            rs.append("CFrame.new(%s)" % ", ".join("%g" % round(v, 4) for v in (pos[0], pos[1], pos[2], q.x, q.y, q.z, q.w)))
        extra = 'Rest = {%s},\nBatch = "%s", BatchIndex = %d,\n' % (", ".join(rs), bname, i)
        lua = lua[:-1] + ",\n" + extra + "}"
        items.append((nm, lua))
        print(nm, len(lua), flush=True)
xml = ['<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">',
       '<Item class="Folder" referent="RBX0"><Properties><string name="Name">CreatureData</string></Properties>']
for k, (nm, lua) in enumerate(items):
    assert "]]>" not in lua
    xml.append('<Item class="ModuleScript" referent="RBX%d"><Properties><string name="Name">%s</string><ProtectedString name="Source"><![CDATA[%s]]></ProtectedString></Properties></Item>' % (k + 1, nm, lua))
xml.append("</Item></roblox>")
open(os.path.join(HERE, "out", "CreatureData.rbxmx"), "w").write("\n".join(xml))
print("TOTAL", sum(len(l) for _, l in items))

