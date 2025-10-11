#!/usr/bin/env python3
"""
Minimal FBX → PNG converter aligned to the existing Blender script style.

USAGE (exactly two args after --):
blender --background --python blender_render_png.py -- input.fbx output.png

Notes
- Orthographic TOP view, transparent background, 2048×2048
- Auto-frames the mesh's bounding box with a small margin
- Single-color fill (black) for crisp silhouettes suitable for laser prep pipelines that accept rasters
- Keep this simple on purpose to mirror your blender_convert.py pattern
"""

import bpy
import sys
import os
import math
import mathutils

# -----------------------------
# Helpers
# -----------------------------

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # Purge orphan data blocks
    for datablock in (bpy.data.meshes, bpy.data.materials, bpy.data.images, bpy.data.cameras, bpy.data.lights, bpy.data.collections):
        for b in list(datablock):
            try:
                datablock.remove(b, do_unlink=True)
            except Exception:
                pass


def world_bbox(objs):
    
    inf = float('inf')
    mins = mathutils.Vector((inf, inf, inf))
    maxs = mathutils.Vector((-inf, -inf, -inf))
    found = False
    for o in objs:
        if o.type != 'MESH':
            continue
        found = True
        for corner in o.bound_box:
            w = o.matrix_world @ mathutils.Vector(corner)
            mins.x = min(mins.x, w.x)
            mins.y = min(mins.y, w.y)
            mins.z = min(mins.z, w.z)
            maxs.x = max(maxs.x, w.x)
            maxs.y = max(maxs.y, w.y)
            maxs.z = max(maxs.z, w.z)
    if not found:
        raise RuntimeError("No mesh geometry found after import")
    center = (mins + maxs) * 0.5
    size = maxs - mins
    return mins, maxs, center, size


# -----------------------------
# Main (match your CLI pattern)
# -----------------------------

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if len(argv) != 2:
    print("Usage: blender --background --python blender_render_png.py -- input.fbx output.png")
    sys.exit(1)

input_file = os.path.abspath(argv[0])
output_file = os.path.abspath(argv[1])

# Basic config mirroring a clean, deterministic render
WIDTH = 2048
HEIGHT = 2048
MARGIN = 0.05  # 5% around bbox
FILL_RGB = (0.0, 0.0, 0.0, 1.0)  # black

# 1) Fresh scene
clear_scene()

# 2) Import FBX
if not os.path.exists(input_file):
    print(f"Input file not found: {input_file}")
    sys.exit(1)

bpy.ops.import_scene.fbx(filepath=input_file, use_anim=False, automatic_bone_orientation=True)

# 3) Collect mesh objects
mesh_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
if not mesh_objs:
    print("No mesh objects imported from FBX.")
    sys.exit(1)

# Make sure they're visible
for o in mesh_objs:
    o.hide_render = False
    o.hide_viewport = False

# 4) Compute bbox and center
mins, maxs, center, size = world_bbox(mesh_objs)

# 5) Setup camera (ORTHO, TOP view)
cam_data = bpy.data.cameras.new("OrthoCam")
cam_data.type = 'ORTHO'
cam_obj = bpy.data.objects.new("OrthoCam", cam_data)
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Position above center, looking down Z-
diag = max(size.x, size.y, size.z) if max(size.x, size.y, size.z) > 0 else 1.0
cam_obj.location = (center.x, center.y, center.z + diag)
cam_obj.rotation_euler = (math.radians(90.0), 0.0, 0.0)  # top/plan view

# Ortho scale to fit XY bbox with margin
width_xy = maxs.x - mins.x
height_xy = maxs.y - mins.y
cam_data.ortho_scale = max(width_xy, height_xy) * (1.0 + MARGIN)

# 6) Render settings (transparent PNG, flat color)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = True
scene.render.resolution_x = WIDTH
scene.render.resolution_y = HEIGHT
scene.render.resolution_percentage = 100

# Workbench flat shading, single color
scene.display.shading.light = 'STUDIO'
scene.display.shading.color_type = 'SINGLE'
scene.display.shading.single_color = FILL_RGB

# 7) Output
out_dir = os.path.dirname(output_file)
if out_dir and not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)
scene.render.filepath = output_file

# 8) Render still
bpy.ops.render.render(write_still=True)
print(f"Rendered {output_file} from {input_file}")
