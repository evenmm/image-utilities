import json
from PIL import Image, ImageDraw

json_path = "2018_SJER_3_258000_4106000_image.tif.tiff.json"

with open(json_path, 'r') as f:
    data = json.load(f)

width = data["size"]["width"]
height = data["size"]["height"]

img = Image.new('L', (width, height), 255)  # 255 = white
draw = ImageDraw.Draw(img)

for obj in data["objects"]:
    exterior = obj["points"]["exterior"]
    # Typically we assume these are [(x1, y1), (x2, y2)].
    # If you suspect they're (row, col), swap them:
    (x1, y1), (x2, y2) = exterior[0], exterior[1]

    # Find center
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    # Print to confirm in-range
    print(f"Center: ({center_x}, {center_y})")

    # Draw a small circle (radius 5) so you can see it
    r = 5
    draw.ellipse(
        [
            (center_x - r, center_y - r),
            (center_x + r, center_y + r)
        ],
        fill=0
    )  # 0 = black

img.save("2018_SJER_3_258000_4106000_tree_seeds.png")
