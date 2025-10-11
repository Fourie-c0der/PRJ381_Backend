
import numpy as np
import svgwrite
import trimesh

# Slice a 3D model into 2D slices
def slice_model(input_file, layer_height=5.0, output_prefix="slice"):
    # Load mesh (supports .stl, .obj, .ply, etc. For .fbx, convert to .obj using the blender_convert.py script first)
    mesh = trimesh.load(input_file)

    # Get mesh bounds
    min_z, max_z = mesh.bounds[:, 2]
    print(f"Mesh bounds: min_z={min_z}, max_z={max_z}")
    z_levels = np.arange(min_z, max_z, layer_height)
    print(f"Number of slices: {len(z_levels)}")

    for i, z in enumerate(z_levels):
        # Create a plane at this Z
        slice_section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])

        if slice_section is None:
            print(f"No section at Z={z}")
            continue

        # Convert to 2D polygon
        slice_2D, _ = slice_section.to_2D()
        print(f"Slice {i} at Z={z}: {len(slice_2D.polygons_full)} polygons")

        if not slice_2D.polygons_full:
            continue

        # Export to SVG for laser cutter
        scale = 1000  # scale to make visible
        dwg = svgwrite.Drawing(f"{output_prefix}_{i}.svg", profile='tiny')
        for path in slice_2D.polygons_full:
            points = [(float(x)*scale, float(y)*scale) for x, y in path.exterior.coords]
            dwg.add(dwg.polygon(points, stroke='black', fill='none'))
        dwg.save()

        print(f"Saved slice {i} at Z={z}")

# Example usage
slice_model("Sword14.obj", layer_height=0.02)