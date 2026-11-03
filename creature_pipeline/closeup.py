import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "creatures"))
mod = importlib.import_module(sys.argv[1]); c = mod.build(); out = os.path.join(HERE, "out", sys.argv[1]); c.build(out)
c.render(os.path.join(out, c.name + "_30.png"), angle=30)
c.render(os.path.join(out, c.name + "_close.png"), angle=20, elev=10, dist=0.55)

