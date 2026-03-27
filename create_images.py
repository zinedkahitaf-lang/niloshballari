from PIL import Image, ImageDraw, ImageFont
import os, math

os.makedirs("images", exist_ok=True)

products = [
    {"file": "kaset_bal.png",     "title": "KASET BAL",          "sub": "Seker Hastalarina Uygun", "bg1": (180, 130, 50),  "bg2": (100, 65, 15)},
    {"file": "cicek_bali.png",    "title": "CICEK BALI",         "sub": "Erzurum Yaylalarindan",   "bg1": (200, 155, 60),  "bg2": (130, 85, 25)},
    {"file": "karakovan.png",     "title": "KARAKOVAN BALI",     "sub": "Geleneksel Uretim",       "bg1": (145, 100, 35),  "bg2": (80, 50, 10)},
    {"file": "nilay_altin.png",   "title": "ALTIN KOVAN BAL",    "sub": "Premium Seri",            "bg1": (210, 175, 70),  "bg2": (140, 105, 25)},
    {"file": "dut_pekmezi.png",   "title": "DUT PEKMEZI",        "sub": "Sifa Deposu",             "bg1": (100, 50, 30),   "bg2": (50, 20, 8)},
    {"file": "uzum_pekmezi.png",  "title": "UZUM PEKMEZI",       "sub": "Geleneksel Tarif",        "bg1": (110, 40, 55),   "bg2": (60, 15, 25)},
    {"file": "cevizli_sucuk.png", "title": "CEVIZLI SUCUK",      "sub": "Bol Cevizli",             "bg1": (130, 80, 40),   "bg2": (70, 40, 12)},
    {"file": "pestil_bastik.png", "title": "PESTIL - BASTIK",    "sub": "Dogal Enerji",            "bg1": (140, 75, 35),   "bg2": (85, 35, 8)},
    {"file": "yayla_tereyagi.png","title": "YAYLA TEREYAGI",     "sub": "Koy Tereyagi",            "bg1": (220, 195, 100), "bg2": (170, 140, 50)},
]

try:
    font_title = ImageFont.truetype("arial.ttf", 42)
    font_sub = ImageFont.truetype("arial.ttf", 22)
    font_brand = ImageFont.truetype("arial.ttf", 16)
except:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_brand = ImageFont.load_default()

for p in products:
    W, H = 600, 400
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    
    # Gradient
    for y in range(H):
        r = int(p["bg1"][0] + (p["bg2"][0] - p["bg1"][0]) * y / H)
        g = int(p["bg1"][1] + (p["bg2"][1] - p["bg1"][1]) * y / H)
        b = int(p["bg1"][2] + (p["bg2"][2] - p["bg1"][2]) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # Gold double border
    draw.rectangle([8, 8, W-8, H-8], outline=(212, 175, 55), width=3)
    draw.rectangle([18, 18, W-18, H-18], outline=(180, 150, 40), width=1)
    
    # Diamond shapes as decoration
    for cx in [100, 300, 500]:
        pts = [(cx, 50), (cx+15, 65), (cx, 80), (cx-15, 65)]
        draw.polygon(pts, fill=(255, 223, 100), outline=(212, 175, 55))
    
    # Honeycomb hexagons as decoration at bottom
    for cx in [80, 200, 320, 440, 560]:
        hex_pts = []
        for a in range(6):
            angle = math.pi / 3 * a + math.pi / 6
            px = cx + 25 * math.cos(angle)
            py = 340 + 25 * math.sin(angle)
            hex_pts.append((px, py))
        draw.polygon(hex_pts, fill=None, outline=(255, 223, 100, 80), width=2)
    
    # Title
    draw.text((W//2, 160), p["title"], fill="white", font=font_title, anchor="mm")
    
    # Subtitle
    draw.text((W//2, 210), p["sub"], fill=(255, 223, 100), font=font_sub, anchor="mm")
    
    # Brand line
    draw.text((W//2, 270), "NILOS BALLARI", fill=(200, 180, 140), font=font_brand, anchor="mm")
    
    # Horizontal gold line
    draw.line([(150, 240), (450, 240)], fill=(212, 175, 55), width=1)
    
    img.save(os.path.join("images", p["file"]))
    print(f"OK {p['file']}")

# Logo
W, H = 400, 400
img = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

# Gold circle
draw.ellipse([20, 20, 380, 380], fill=(212, 175, 55), outline=(180, 140, 30), width=4)
draw.ellipse([40, 40, 360, 360], fill=(255, 223, 115), outline=(212, 175, 55), width=2)

# Honeycomb pattern
cx, cy = 200, 155
hex_size = 32
for dx, dy in [(0,0), (56,32), (-56,32), (56,-32), (-56,-32), (0,64), (0,-64)]:
    pts = []
    for a in range(6):
        angle = math.pi / 3 * a + math.pi / 6
        px = cx + dx + hex_size * math.cos(angle)
        py = cy + dy + hex_size * math.sin(angle)
        pts.append((px, py))
    draw.polygon(pts, fill=(200, 160, 40), outline=(170, 130, 20), width=2)

try:
    font_logo = ImageFont.truetype("arial.ttf", 28)
    font_logo2 = ImageFont.truetype("arial.ttf", 18)
except:
    font_logo = ImageFont.load_default()
    font_logo2 = ImageFont.load_default()

draw.text((200, 285), "NILOS", fill=(80, 50, 15), font=font_logo, anchor="mm")
draw.text((200, 318), "BALLARI", fill=(80, 50, 15), font=font_logo, anchor="mm")
draw.text((200, 355), "Erzurum Yoresi", fill=(140, 100, 40), font=font_logo2, anchor="mm")

img.save("logo.png")
print("OK logo.png")
print("DONE!")
