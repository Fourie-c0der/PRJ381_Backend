# 🧩 Blender Conversion & Laser Cutting Pipeline

This project provides a set of **Blender automation scripts** for converting 3D files between formats and generating 2D slices for laser cutting or visualization.  
It uses Blender’s Python API (`bpy`) to automate file conversion and rendering in **background mode**, making it suitable for integration into automated pipelines or user-friendly GUIs.

---

## 📁 Project Overview

| Script | Description |
|---------|-------------|
| `blender_converter.py` | Converts **FBX → OBJ** using Blender’s import/export functionality. |
| `blender_render_png.py` | Renders **FBX → PNG** for visual previews. |
| `cutter.py` | Processes **OBJ → SVG slices** as part of a laser-cutting preparation workflow. |

---

## ⚙️ Requirements

- **Blender 3.0+**
- **Python 3.9+**
- Blender’s `bpy` module (included with Blender)
- (Optional) Virtual environment for running external scripts like `cutter.py`

---

## 🚀 Usage

All scripts are designed to run **headlessly** (without Blender’s graphical interface).

### 1. Convert FBX → OBJ
bash
blender --background --python Tools/laser_pipeline/blender_converter.py -- INPUT.fbx OUTPUT.obj
blender --background --python Tools/laser_pipeline/blender_render_png.py -- INPUT.fbx OUTPUT.png
source venv/bin/activate

python Tools/laser_pipeline/cutter.py

Tools/
├── laser_pipeline/
│   ├── blender_converter.py
│   ├── blender_render_png.py
│   ├── cutter.py

🖥️ Future Development: Drag-and-Drop UI

A planned enhancement for this project is a graphical user interface (GUI) that allows users to:

Drag and drop .fbx or .obj files.

Select conversion types:

FBX → OBJ

FBX → PNG

OBJ → SVG

Track conversion progress.

Preview rendered outputs.

🧩 Proposed Tech Stack

Python UI frameworks: PyQt6 or Tkinter

Backend: The existing Blender + Python conversion scripts

Optional: Electron frontend communicating with a Python backend for a modern look

This UI will simplify the conversion process and make the tool more accessible for designers and makers.
