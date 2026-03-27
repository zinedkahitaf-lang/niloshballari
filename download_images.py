import urllib.request
from urllib.request import Request, urlopen
import os

images_dir = "images"
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

def fetch_image(prompt, filename):
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=600&height=400&nologo=true"
    save_path = os.path.join(images_dir, filename)
    print(f"Drawing {filename}...")
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as res, open(save_path, 'wb') as f:
            f.write(res.read())
    except Exception as e:
        print(f"Error drawing {filename}: {e}")

logo_url = "https://image.pollinations.ai/prompt/minimalist_luxurious_round_logo_honeycomb_bee_butter_walnut_gold_cream_white_background_no_text?width=400&height=400&nologo=true"
req = Request(logo_url, headers={'User-Agent': 'Mozilla/5.0'})
with urlopen(req) as res, open("yoresel_logo.jpg", 'wb') as f:
    f.write(res.read())

prompts = {
    "kaset_bal.jpg": "beautiful_macro_shot_of_natural_honeycomb_rustic_wood_golden_honey",
    "cicek_bali.jpg": "jar_of_pure_golden_liquid_honey_with_wooden_dipper_rustic",
    "karakovan.jpg": "dark_wild_honeycomb_in_a_glass_jar_premium_food_photography",
    "nilay_altin.jpg": "luxurious_premium_honey_jar_with_gold_label_glowing_amber_honey",
    "dut_pekmezi.jpg": "dark_thick_mulberry_molasses_in_a_bowl_with_fresh_mulberries_rustic",
    "uzum_pekmezi.jpg": "dark_grape_molasses_syrup_pouring_into_jar_rustic_table",
    "cevizli_sucuk.jpg": "traditional_turkish_churchkhela_walnut_sausage_sweet_dessert_premium",
    "pestil_bastik.jpg": "turkish_fruit_leather_pestil_with_walnuts_food_photography",
    "yayla_tereyagi.jpg": "block_of_fresh_yellow_natural_butter_on_wooden_board_rustic_premium"
}

for filename, prompt in prompts.items():
    fetch_image(prompt, filename)

print("All drawings completed!")
