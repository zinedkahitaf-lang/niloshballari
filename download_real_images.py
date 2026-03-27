import urllib.request
import ssl
import os

os.makedirs("images", exist_ok=True)

# SSL context to bypass certificate verification
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Reliable Unsplash Image IDs
image_ids = {
    "images/kaset_bal.png": "1563729784400-589574bf4120", # Honeycomb
    "images/cicek_bali.png": "1587049352846-df6365f5a8ad", # Honey
    "images/karakovan.png": "1471374586948-4cc93576412c", # Dark Honey
    "images/nilay_altin.png": "1555035336-d762956cf9dc", # Premium Honey
    "images/dut_pekmezi.png": "1510629954389-c1e0da47d415", # Dark Syrup
    "images/uzum_pekmezi.png": "1528490159114-64463a73c2b7", # Grape/Molasses look
    "images/cevizli_sucuk.png": "1591151608674-87be7d47228a", # Sweets/Nuts
    "images/pestil_bastik.png": "1596455607563-ad6193f76b17", # Fruit leather look
    "images/yayla_tereyagi.png": "1589985270826-4b7bb135bc9d", # Butter
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for filename, photo_id in image_ids.items():
    url = f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&q=80&w=800&h=600"
    print(f"Downloading {filename} from Unsplash ID {photo_id}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as response:
            data = response.read()
            with open(filename, 'wb') as f:
                f.write(data)
            print(f"  OK ({len(data)} bytes)")
    except Exception as e:
        print(f"  FAILED: {e}")

print("ALL DONE!")
