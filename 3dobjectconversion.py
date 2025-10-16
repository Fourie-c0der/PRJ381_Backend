import bpy
import bmesh

# Select the active object (your 3D model)
obj = bpy.context.active_object
mesh = obj.data

# Ensure we're in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Create a new UV map if needed
if not mesh.uv_layers:
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.03)
    bpy.ops.object.mode_set(mode='OBJECT')

# Now get flattened UV coordinates
uv_layer = mesh.uv_layers.active.data
verts = [v.co for v in mesh.vertices]

# Convert UVs (2D layout) into an SVG
svg = '<?xml version="1.0" encoding="UTF-8"?>\n'
svg += '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1">\n'
for poly in mesh.polygons:
    svg += '  <polygon points="'
    for loop_index in poly.loop_indices:
        uv = uv_layer[loop_index].uv
        svg += f"{uv.x},{1 - uv.y} "
    svg += '" fill="none" stroke="black" stroke-width="0.001"/>\n'
svg += '</svg>'

with open(r"C:\exports\sphere_unfold.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("✅ Unfolded 3D model into 2D SVG successfully.")
