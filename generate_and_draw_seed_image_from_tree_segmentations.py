import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw

# --- Check input ---
if len(sys.argv) != 2:
    print("Usage: python generate.py path/to/annotations.json")
    sys.exit(1)

input_path = Path(sys.argv[1])
with open(input_path, "r") as f:
    data = json.load(f)

width = data["size"]["width"]
height = data["size"]["height"]
img = Image.new("L", (width, height), 0)  # 0 = black
draw = ImageDraw.Draw(img)

for obj in data["objects"]:
    exterior = obj["points"]["exterior"]
    (x1, y1), (x2, y2) = exterior[0], exterior[1]
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    r = 5
    draw.ellipse(
        [(center_x - r, center_y - r), (center_x + r, center_y + r)], fill=255
    )  # 255 = white

# Base output filename
base_name = input_path.stem.replace(".tiff", "")  # strip repeated extensions
base_name = base_name.replace(".tif", "")
output_path = base_name + "_seeds.tiff"

# Save as TIFF
img.save(output_path, format="TIFF")
print(f"Saved: {output_path}")
