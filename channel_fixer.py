import numpy as np
import tifffile
from ome_types.model import OME, Image, Pixels, Channel

my_image = "tree_image_2018_SJER_3_258000_4106000.tiff"

# Load RGB image
img_rgb = tifffile.imread(my_image)  # shape: (H, W, 3)

# Rearrange to (C, Y, X)
img_planar = np.moveaxis(img_rgb, -1, 0)

# Build OME metadata (no tiff_data)
channels = [Channel(id=f'Channel:0:{i}', name=name) for i, name in enumerate(['Red', 'Green', 'Blue'])]
pixels = Pixels(
    dimension_order='XYZCT',
    type='uint8',
    size_c=3,
    size_z=1,
    size_t=1,
    size_x=img_rgb.shape[1],
    size_y=img_rgb.shape[0],
    channels=channels
)
ome = OME(images=[Image(id='Image:0', name='RGB split', pixels=pixels)])

# Save OME-TIFF
tifffile.imwrite(
    'rgb_planar.ome.tif',
    img_planar,
    photometric='minisblack',  # Force non-RGB
    description=ome.to_xml()
)
# tifffile.imwrite(
#     'rgb_planar.ome.tif',
#     img_planar,
#     metadata={'axes': 'CYX'},
#     description=ome.to_xml()
# )

with tifffile.TiffFile('rgb_planar.ome.tif') as tif:
    print("Axes:", tif.series[0].axes)
    print("Shape:", tif.series[0].shape)
    print("SamplesPerPixel:", tif.pages[0].samplesperpixel)
    print("Photometric:", tif.pages[0].photometric)

tifffile.imwrite('rgb_preview.tif', img_rgb)  # standard interleaved RGB just for 
