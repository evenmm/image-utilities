from PIL import Image
from pathlib import Path
import tifffile
import numpy as np
import sys

# --- Check function call ---
if len(sys.argv) != 2:
    print("Usage: python3 greyscale_converter.py <input_image.png>")
    sys.exit(1)

# "tree_image_preview_2019_DELA_5_423000_3601000.png"
# "tree_image_preview_2019_DELA_5_423000_3601000_bw.png"

# --- Load RGB png image ---
input_path = Path(sys.argv[1])
base_name = input_path.stem.replace(".tiff", "")  # strip repeated extensions
base_name = base_name.replace(".tif", "")
base_name = base_name.replace(".png", "")
output_path = base_name + "_bw.tiff"

# Load RGB PNG
img = Image.open(input_path).convert("RGB")
r, g, b = img.split()
# Pick one channel (or convert to grayscale)
gray = img.convert("L")  # Or use r/g/b individually

# Save to TIFF with metadata
gray_array = np.array(gray)
tifffile.imwrite(output_path, gray_array, photometric='minisblack')
