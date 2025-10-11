import bpy
import sys
import os

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Get arguments
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if len(argv) != 2:
    print("Usage: blender --background --python blender_convert.py input.fbx output.obj")
    sys.exit(1)

input_file = argv[0]
output_file = argv[1]

# Import FBX
bpy.ops.import_scene.fbx(filepath=input_file)

# Assume first object is the mesh
if bpy.context.selected_objects:
    obj = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)

# Export to OBJ
bpy.ops.wm.obj_export(filepath=output_file, export_selected_objects=True)

print(f"Converted {input_file} to {output_file}")