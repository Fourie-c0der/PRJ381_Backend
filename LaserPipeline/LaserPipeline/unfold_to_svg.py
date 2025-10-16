import bpy, os, sys
from mathutils import Vector

# ------------------------------------------------------------
# ARGUMENTS: blender --background --python cube_unfold_wood.py -- <output_dir> [size_mm]
# ------------------------------------------------------------
def parse_args(argv):
    """Robust CLI arg parser for Blender."""
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []

    args = {
        "output_dir": r"C:\LaserPipeline\output",
        "size_mm": 70.0
    }

    if len(argv) == 1:
        # single arg – could be folder or numeric
        try:
            args["size_mm"] = float(argv[0])
        except ValueError:
            args["output_dir"] = os.path.normpath(argv[0])
    elif len(argv) >= 2:
        # first = folder, second = size
        args["output_dir"] = os.path.normpath(argv[0])
        try:
            args["size_mm"] = float(argv[1])
        except ValueError:
            print(f"⚠️ Warning: could not parse '{argv[1]}' as number, using default {args['size_mm']}")

    os.makedirs(args["output_dir"], exist_ok=True)
    return args


# ------------------------------------------------------------
# Parse the arguments now
# ------------------------------------------------------------
args = parse_args(sys.argv)
output_dir = args["output_dir"]
size_mm = args["size_mm"]
print(f"📏 Size set to {size_mm} mm, output = {output_dir}")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
tab_len = 10       # mm
tab_depth = 3      # mm
hole_r = 1.5       # alignment pin hole radius
stroke_cut   = "#FF0000"   # cut
stroke_score = "#0000FF"   # fold/guide
stroke_text  = "#00AA00"   # labels
stroke_w_mm  = 0.1

# ------------------------------------------------------------
# CREATE SVG FOR LASER
# ------------------------------------------------------------
s = size_mm
svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{s*4}mm" height="{s*2}mm"
     viewBox="0 0 {s*4} {s*2}">
  <style>
    .cut {{fill:none;stroke:{stroke_cut};stroke-width:{stroke_w_mm}mm;}}
    .score {{fill:none;stroke:{stroke_score};stroke-width:{stroke_w_mm/2}mm;stroke-dasharray:2,2;}}
    .etch {{fill:none;stroke:{stroke_text};stroke-width:{stroke_w_mm/3}mm;}}
  </style>
'''

# ------------------------------------------------------------
# FUNCTION: draw cube net (T-shape layout)
# ------------------------------------------------------------
def rect(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="cut"/>\n'

def add_tabs(x, y, w, h, side):
    """Add simple rectangular tabs along a side ('top','bottom','left','right')."""
    tabs = ""
    n = int(w//tab_len) if side in ('top','bottom') else int(h//tab_len)
    for i in range(n):
        if side == "top":
            tx = x + i*tab_len + tab_len/2
            tabs += f'<rect x="{tx-tab_len/2}" y="{y-tab_depth}" width="{tab_len}" height="{tab_depth}" class="cut"/>\n'
            tabs += f'<line class="score" x1="{tx-tab_len/2}" y1="{y}" x2="{tx+tab_len/2}" y2="{y}"/>\n'
        if side == "bottom":
            tx = x + i*tab_len + tab_len/2
            tabs += f'<rect x="{tx-tab_len/2}" y="{y+h}" width="{tab_len}" height="{tab_depth}" class="cut"/>\n'
            tabs += f'<line class="score" x1="{tx-tab_len/2}" y1="{y+h}" x2="{tx+tab_len/2}" y2="{y+h}"/>\n'
        if side == "left":
            ty = y + i*tab_len + tab_len/2
            tabs += f'<rect x="{x-tab_depth}" y="{ty-tab_len/2}" width="{tab_depth}" height="{tab_len}" class="cut"/>\n'
            tabs += f'<line class="score" x1="{x}" y1="{ty-tab_len/2}" x2="{x}" y2="{ty+tab_len/2}"/>\n'
        if side == "right":
            ty = y + i*tab_len + tab_len/2
            tabs += f'<rect x="{x+w}" y="{ty-tab_len/2}" width="{tab_depth}" height="{tab_len}" class="cut"/>\n'
            tabs += f'<line class="score" x1="{x+w}" y1="{ty-tab_len/2}" x2="{x+w}" y2="{ty+tab_len/2}"/>\n'
    return tabs

# layout positions (T-net)
faces = [
    (s,0),        # Front
    (s, s),       # Bottom
    (0, s),       # Left
    (2*s, s),     # Right
    (3*s, s),     # Back
    (s, 2*s)      # Top
]

for i,(x,y) in enumerate(faces):
    svg += rect(x,y,s,s)
    svg += add_tabs(x,y,s,s,"top")
    svg += add_tabs(x,y,s,s,"bottom")
    svg += add_tabs(x,y,s,s,"left")
    svg += add_tabs(x,y,s,s,"right")
    svg += f'<text x="{x+s/2}" y="{y+s/2}" font-size="4" fill="{stroke_text}" text-anchor="middle" dominant-baseline="middle">{i}</text>\n'
    # alignment holes (optional)
    svg += f'<circle cx="{x+5}" cy="{y+5}" r="{hole_r}" class="cut"/>\n'
    svg += f'<circle cx="{x+s-5}" cy="{y+s-5}" r="{hole_r}" class="cut"/>\n'

svg += "</svg>"

# ------------------------------------------------------------
# WRITE FILE
# ------------------------------------------------------------
out_path = os.path.join(output_dir, f"cube_{int(s)}mm_tabs.svg")
with open(out_path,"w",encoding="utf-8") as f:
    f.write(svg)

print(f"✅ Laser file ready: {out_path}")
