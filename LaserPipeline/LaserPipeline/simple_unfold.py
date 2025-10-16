import bpy
import bmesh
import os
import sys

# === CONFIG ===
input_file = sys.argv[-2] if len(sys.argv) > 2 else r"C:\LaserPipeline\models\sphere.obj"
output_folder = sys.argv[-1] if len(sys.argv) > 1 else r"C:\LaserPipeline\output"
os.makedirs(output_folder, exist_ok=True)

print("🔹 Starting 3D → 2D unfolding conversion")
print(f"   Input file: {input_file}")
print(f"   Output folder: {output_folder}")

# === CLEAN SCENE ===
bpy.ops.wm.read_factory_settings(use_empty=True)

# === IMPORT MODEL ===
ext = os.path.splitext(input_file)[1].lower()
if ext == ".obj":
    bpy.ops.import_scene.obj(filepath=input_file)
elif ext == ".fbx":
    bpy.ops.import_scene.fbx(filepath=input_file)
else:
    bpy.ops.wm.open_mainfile(filepath=input_file)

obj = bpy.context.selected_objects[0]
bpy.context.view_layer.objects.active = obj
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
bpy.ops.object.mode_set(mode='EDIT')

# === UV UNWRAP (Flatten 3D) ===
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.03)
bpy.ops.object.mode_set(mode='OBJECT')

mesh = obj.data
uv_layer = mesh.uv_layers.active.data

# === CREATE SVG ===
svg = '<?xml version="1.0" encoding="UTF-8"?>\n'
svg += '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">\n'

for poly in mesh.polygons:
    svg += '  <polygon points="'
    for loop_index in poly.loop_indices:
        uv = uv_layer[loop_index].uv
        svg += f"{uv.x:.5f},{1 - uv.y:.5f} "
    svg += '" fill="none" stroke="black" stroke-width="0.001"/>\n'

svg += '</svg>'

output_path = os.path.join(output_folder, os.path.basename(input_file).replace(ext, "_unfold.svg"))
with open(output_path, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"✅ Export complete: {output_path}")
