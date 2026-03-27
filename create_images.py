from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("images", exist_ok=True)

# Product data with emoji and colors
products = [
    {"file": "kaset_bal.png",     "title": "Kaset Bal",         "emoji": "🍯", "bg1": (180, 130, 50),  "bg2": (120, 80, 20)},
    {"file": "cicek_bali.png",    "title": "Çiçek Balı",        "emoji": "🌸", "bg1": (200, 150, 60),  "bg2": (140, 90, 30)},
    {"file": "karakovan.png",     "title": "Karakovan Balı",    "emoji": "🐝", "bg1": (160, 110, 40),  "bg2": (100, 70, 15)},
    {"file": "nilay_altin.png",   "title": "Altın Kovan Bal",   "emoji": "✨", "bg1": (210, 170, 70),  "bg2": (150, 110, 30)},
    {"file": "dut_pekmezi.png",   "title": "Dut Pekmezi",       "emoji": "🫐", "bg1": (100, 50, 30),   "bg2": (60, 20, 10)},
    {"file": "uzum_pekmezi.png",  "title": "Üzüm Pekmezi",     "emoji": "🍇", "bg1": (110, 40, 50),   "bg2": (70, 15, 25)},
    {"file": "cevizli_sucuk.png", "title": "Cevizli Sucuk",     "emoji": "🥜", "bg1": (130, 80, 40),   "bg2": (80, 45, 15)},
    {"file": "pestil_bastik.png", "title": "Pestil - Bastık",   "emoji": "🍫", "bg1": (140, 70, 35),   "bg2": (90, 40, 10)},
    {"file": "yayla_tereyagi.png","title": "Yayla Tereyağı",    "emoji": "🧈", "bg1": (220, 190, 100), "bg2": (180, 150, 60)},
]

for p in products:
    W, H = 600, 400
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    
    # Gradient background
    for y in range(H):
        r = int(p["bg1"][0] + (p["bg2"][0] - p["bg1"][0]) * y / H)
        g = int(p["bg1"][1] + (p["bg2"][1] - p["bg1"][1]) * y / H)
        b = int(p["bg1"][2] + (p["bg2"][2] - p["bg1"][2]) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # Decorative circles
    for i in range(5):
        x = 50 + i * 130
        draw.ellipse([x-30, 320, x+30, 380], fill=(255, 255, 255, 30), outline=(255, 255, 255))
    
    # Gold border
    draw.rectangle([10, 10, W-10, H-10], outline=(212, 175, 55), width=3)
    draw.rectangle([20, 20, W-20, H-20], outline=(212, 175, 55, 128), width=1)
    
    # Title text
    try:
        font_large = ImageFont.truetype("arial.ttf", 38)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw emoji (large)
    draw.text((W//2, 100), p["emoji"], fill=(255, 255, 255), font=font_large, anchor="mm")
    
    # Draw title
    draw.text((W//2, 200), p["title"], fill=(255, 255, 255), font=font_large, anchor="mm")
    
    # Draw "Niloş Balları" brand
    draw.text((W//2, 260), "NİLOŞ BALLARI", fill=(212, 175, 55), font=font_small, anchor="mm")
    
    # Draw "Erzurum Yöresi" tag
    draw.text((W//2, 290), "Erzurum Yöresel Lezzetleri", fill=(200, 180, 140), font=font_small, anchor="mm")
    
    img.save(os.path.join("images", p["file"]))
    print(f"OK {p['file']} created")

# Logo
W, H = 400, 400
img = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

# Gold circle
draw.ellipse([20, 20, 380, 380], fill=(212, 175, 55), outline=(180, 140, 30), width=4)
draw.ellipse([40, 40, 360, 360], fill=(255, 223, 115), outline=(212, 175, 55), width=2)

# Honeycomb pattern (hexagons)
import math
cx, cy = 200, 160
hex_size = 30
for dx, dy in [(0,0), (52,30), (-52,30), (52,-30), (-52,-30), (0,60), (0,-60)]:
    pts = []
    for a in range(6):
        angle = math.pi / 3 * a + math.pi / 6
        px = cx + dx + hex_size * math.cos(angle)
        py = cy + dy + hex_size * math.sin(angle)
        pts.append((px, py))
    draw.polygon(pts, fill=(200, 160, 40), outline=(180, 140, 20), width=2)

try:
    font_logo = ImageFont.truetype("arial.ttf", 24)
    font_brand = ImageFont.truetype("arial.ttf", 16)
except:
    font_logo = ImageFont.load_default()
    font_brand = ImageFont.load_default()

draw.text((200, 290), "NİLOŞ", fill=(80, 50, 15), font=font_logo, anchor="mm")
draw.text((200, 320), "BALLARI", fill=(80, 50, 15), font=font_logo, anchor="mm")
draw.text((200, 355), "Erzurum Yöresi", fill=(140, 100, 40), font=font_brand, anchor="mm")

img.save("logo.png")
print("OK logo.png created")
print("All images done!")
