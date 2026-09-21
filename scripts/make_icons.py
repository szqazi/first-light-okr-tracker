from PIL import Image, ImageDraw
import math, os

OUT = os.path.join(os.path.dirname(__file__), "..", "icons")
os.makedirs(OUT, exist_ok=True)

TEAL = (22, 31, 35, 255)      # --paper dark
GOLD = (224, 169, 79, 255)    # --accent dark
GOLD_STRONG = (242, 192, 119, 255)

def draw_mark(size, pad_ratio):
    img = Image.new("RGBA", (size, size), TEAL)
    d = ImageDraw.Draw(img)
    cx = size / 2
    pad = size * pad_ratio
    r_outer = size / 2 - pad
    cy = size / 2 + r_outer * 0.12  # optical center, nudged down slightly
    r_sun = r_outer * 0.62
    line_w = max(3, int(size * 0.022))

    # sun disc, clipped by a horizon line partway down
    d.ellipse([cx - r_sun, cy - r_sun, cx + r_sun, cy + r_sun], fill=GOLD)
    d.rectangle([0, cy + r_sun * 0.28, size, size], fill=TEAL)
    d.rectangle([cx - r_outer, cy + r_sun * 0.28 - line_w / 2, cx + r_outer, cy + r_sun * 0.28 + line_w / 2], fill=GOLD_STRONG)

    # a few rays above the sun
    ray_len = r_outer * 0.22
    ray_gap = r_sun * 1.22
    for deg in (200, 245, 270, 295, 340):
        a = math.radians(deg)
        x0 = cx + math.cos(a) * ray_gap
        y0 = cy + math.sin(a) * ray_gap
        x1 = cx + math.cos(a) * (ray_gap + ray_len)
        y1 = cy + math.sin(a) * (ray_gap + ray_len)
        d.line([x0, y0, x1, y1], fill=GOLD_STRONG, width=line_w)
    return img

def make(size, name, pad_ratio=0.16):
    img = draw_mark(size, pad_ratio)
    img.save(os.path.join(OUT, name))

make(192, "icon-192.png", 0.18)
make(512, "icon-512.png", 0.18)
make(512, "icon-maskable-512.png", 0.28)  # extra safe-zone padding for maskable
make(180, "apple-touch-icon.png", 0.16)   # apple wants edge-to-edge-ish, no forced transparency

print("icons written to", os.path.abspath(OUT))
