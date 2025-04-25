import sys
import os
from pathlib import Path
import numpy as np
import tifffile
from ome_types.model import OME, Image as OMEImage, Pixels, Channel

# --- Check function call ---
if len(sys.argv) != 2:
    print("Usage: python3 channel_fixer.py <input_rgb.tiff>")
    sys.exit(1)

input_path = Path(sys.argv[1])
base_name = input_path.stem.replace(".tiff", "")  # strip repeated extensions
base_name = base_name.replace(".tif", "")
output_path = base_name + "_3channels.tiff"

# --- Load RGB image ---
img_rgb = tifffile.imread(input_path)  # shape: (H, W, 3)

if img_rgb.ndim != 3 or img_rgb.shape[2] != 3:
    print("Error: Expected RGB image with shape (H, W, 3)")
    sys.exit(1)

# --- Convert to planar format: (3, H, W) ---
img_3_channels = np.moveaxis(img_rgb, -1, 0)

# --- Build OME metadata ---
channels = [
    Channel(id=f"Channel:0:{i}", name=name)
    for i, name in enumerate(["Red", "Green", "Blue"])
]
pixels = Pixels(
    dimension_order="XYZCT",
    type="uint8",
    size_c=3,
    size_z=1,
    size_t=1,
    size_x=img_rgb.shape[1],
    size_y=img_rgb.shape[0],
    channels=channels,
)
ome = OME(
    images=[OMEImage(id="Image:0", name=os.path.basename(base_name), pixels=pixels)]
)

# --- Save planar TIFF with OME metadata ---
tifffile.imwrite(
    output_path, img_3_channels, photometric="minisblack", description=ome.to_xml()
)

print(f"Saved planar image: {output_path}")

# --- Optional: Save interleaved preview (comment out if not needed) ---
tifffile.imwrite(base_name + "_preview.tiff", img_rgb)
