from PIL import Image, ImageDraw, ImageFont
import os

images_dir = "images"

# Products to brand
product_files = [f for f in os.listdir(images_dir) if f.endswith('.png') or f.endswith('.jpg')]

def add_brand_label(image_path, brand_text="Niloş Balları"):
    try:
        img = Image.open(image_path).convert("RGBA")
        W, H = img.size
        
        # Scale label size based on image size
        label_w = int(W * 0.35)
        label_h = int(label_w * 0.5)
        
        # Create a drawing surface for the label
        label = Image.new("RGBA", (label_w, label_h), (0,0,0,0))
        draw = ImageDraw.Draw(label)
        
        # Draw White Oval (the label base)
        draw.ellipse([5, 5, label_w-5, label_h-5], fill=(255, 255, 255, 245), outline=(180, 140, 30), width=4)
        
        # Inner gold border
        draw.ellipse([10, 10, label_w-10, label_h-10], outline=(212, 175, 55, 180), width=1)
        
        # Load fonts
        try:
            font_title = ImageFont.truetype("arial.ttf", int(label_h * 0.25))
            font_subtitle = ImageFont.truetype("arial.ttf", int(label_h * 0.12))
        except:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            
        # Draw small Hexagon (Honeycomb) icon instead of emoji
        import math
        hx, hy = label_w//2, label_h * 0.22
        h_size = 12
        hex_pts = []
        for a in range(6):
            angle = math.pi / 3 * a + math.pi / 6
            px = hx + h_size * math.cos(angle)
            py = hy + h_size * math.sin(angle)
            hex_pts.append((px, py))
        draw.polygon(hex_pts, fill=(212, 175, 55), outline=(150, 110, 20))
        
        # Draw Brand Text
        draw.text((label_w//2, label_h * 0.52), brand_text, fill=(70, 45, 10), font=font_title, anchor="mm")
        
        # Draw Region
        draw.text((label_w//2, label_h * 0.78), "Erzurum Yöresel Lezzetleri", fill=(130, 90, 30), font=font_subtitle, anchor="mm")
        
        # Position label in bottom right
        pos_x = W - label_w - int(W * 0.03)
        pos_y = H - label_h - int(H * 0.03)
        
        # Paste onto main image
        img.paste(label, (pos_x, pos_y), label)
        
        # Save
        img.convert("RGB").save(image_path, "PNG")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

for pfile in product_files:
    add_brand_label(os.path.join(images_dir, pfile))
print("DONE")
