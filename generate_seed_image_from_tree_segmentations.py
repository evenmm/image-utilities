import json
from PIL import Image, ImageDraw

# Path to your JSON annotations and the TIFF (not strictly needed for this step)
json_path = "2018_SJER_3_258000_4106000_image.tif.tiff.json"
tiff_path = "2018_SJER_3_258000_4106000_image.tif.tiff"  # if needed for reference

# Load JSON
with open(json_path, 'r') as f:
    data = json.load(f)

# Read width/height
width = data["size"]["width"]
height = data["size"]["height"]

# print("width", width)
# print("height", height)

# Create a blank white image
img = Image.new('L', (width, height), 255)  # 'L' = 8-bit grayscale, 255 = white
draw = ImageDraw.Draw(img)

# For each annotation, place a black pixel in the bounding-box center
for obj in data["objects"]:
    exterior = obj["points"]["exterior"]
    (x1, y1), (x2, y2) = exterior[0], exterior[1]
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    draw.point((center_x, center_y), fill=0)  # 0 = black
    print(center_x, center_y)

# Save result
img.save("2018_SJER_3_258000_4106000_tree_seeds.png")
