import os
import sys
from datetime import datetime
from pathlib import Path

# === CONFIG ===
INPUT_DIR = Path("input_models")
OUTPUT_DIR = Path("output_gblr")
LOG_DIR = Path("logs")

for d in (INPUT_DIR, OUTPUT_DIR, LOG_DIR):
    d.mkdir(exist_ok=True)

def log(message: str):
    """Write messages to console and log file."""
    print(message)
    with open(LOG_DIR / "conversion.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def generate_placeholder_svg(output_path: Path, model_name: str):
    """Creates a fake SVG file simulating a laser-cut outline."""
    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="200mm" height="200mm" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <title>{model_name} Laser Mock</title>
  <rect x="10" y="10" width="180" height="180" fill="none" stroke="black" stroke-width="1"/>
  <circle cx="100" cy="100" r="50" fill="none" stroke="red" stroke-width="0.5"/>
  <text x="50" y="190" font-size="10" fill="blue">{model_name}</text>
</svg>
"""
    output_path.write_text(svg_content, encoding="utf-8")

def convert_model(file_path: Path):
    """Fake converter (mock) — simulates Blender export."""
    model_name = file_path.stem
    output_svg = OUTPUT_DIR / f"{model_name}.gblr.svg"

    log(f"🟡 Converting: {file_path.name}")
    generate_placeholder_svg(output_svg, model_name)
    log(f"✅ Created: {output_svg}")

def main():
    """Scan input_models folder and convert each file."""
    files = list(INPUT_DIR.glob("*.*"))
    if not files:
        log("⚠️ No models found in 'input_models' folder.")
        return

    for f in files:
        convert_model(f)

if __name__ == "__main__":
    log("\n=== Starting lightweight Blender→GBLR mock conversion ===")
    main()
    log("🏁 Conversion process completed.")
