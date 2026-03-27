import streamlit as st
import urllib.parse
import base64
import os

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nilos Ballari | Lux Yoresel Lezzetler", page_icon="images/kaset_bal.png" if os.path.exists("images/kaset_bal.png") else None, layout="centered")

# --- ULTRA PREMIUM CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,500;0,700;1,500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #FAF8F5;
        color: #2C241B;
    }
    .stApp {
        background-color: #FAF8F5;
    }
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #2C241B;
    }

    .brand-header {
        background: linear-gradient(145deg, #ffffff, #FDF7EC);
        border: 1px solid #EADDC7;
        border-radius: 30px;
        padding: 40px 30px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(186, 153, 113, 0.08);
        margin-top: 20px;
        margin-bottom: 50px;
        position: relative;
        overflow: hidden;
    }
    .brand-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 6px;
        background: linear-gradient(90deg, #D4AF37, #FFDF73, #D4AF37);
    }
    .brand-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 2px;
        color: #1A1510;
    }
    .brand-subtitle {
        font-size: 1.1rem;
        color: #8C7A61;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin: 10px 0 25px;
    }
    .phone-badge {
        background-color: #1C3322;
        color: #E2ECD8;
        padding: 10px 25px;
        border-radius: 30px;
        display: inline-block;
        font-weight: 600;
        font-size: 1rem;
        border: 1px solid #284A31;
    }

    .product-glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(234, 221, 199, 0.5);
        box-shadow: 0 15px 35px rgba(0,0,0,0.03);
        margin-bottom: 10px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
    }
    .product-glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(212, 175, 55, 0.1);
        border-color: #D4AF37;
    }
    .cat-tag {
        position: absolute;
        top: -12px;
        left: 30px;
        background: #2C241B;
        color: #FFDF73;
        font-size: 0.7rem;
        font-weight: 800;
        padding: 5px 15px;
        border-radius: 12px;
        letter-spacing: 2px;
    }
    .p-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 10px 0;
        color: #2C241B;
    }
    .p-desc {
        color: #635848;
        font-size: 1rem;
        margin-bottom: 15px;
        line-height: 1.6;
    }
    .p-tags {
        color: #A69680;
        font-size: 0.85rem;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }
    .p-tags span {
        background: #F4EEDF;
        padding: 4px 10px;
        border-radius: 8px;
    }
    .price-box {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1A1510;
        font-family: 'Outfit', sans-serif;
    }
    .price-box span {
        font-size: 1rem;
        color: #A69680;
        font-weight: 400;
    }

    .stButton>button {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 25px rgba(16, 185, 129, 0.4);
        background: linear-gradient(135deg, #059669, #047857);
    }

    .whatsapp-btn {
        background: linear-gradient(135deg, #25D366, #128C7E);
        color: white;
        text-decoration: none;
        padding: 18px 30px;
        border-radius: 16px;
        display: block;
        font-weight: 800;
        font-size: 1.2rem;
        text-align: center;
        letter-spacing: 1px;
        width: 100%;
        margin-top: 30px;
        box-shadow: 0 15px 30px rgba(37, 211, 102, 0.3);
        transition: all 0.4s ease;
    }
    .whatsapp-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(37, 211, 102, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- INIT SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state['cart'] = {}

# --- PRODUCT DATA (LOCAL IMAGES) ---
products = {
    "kaset_bal": {
        "category": "OZEL SERI",
        "name": "Kaset Bal (Seker Hastalarina Uygun)",
        "description": "El degmeden sofraniza gelen katkisiz dogal kaset balimiz.",
        "tags": ["Erzurum Yaylalari", "Saf"],
        "price": 1250,
        "image": "images/kaset_bal.png"
    },
    "cicek_bali": {
        "category": "KLASIK BAL",
        "name": "Erzurum Cicek Bali",
        "description": "Erzurum yaylalarinin binbir cesit gulunden ve ciceginden elde edilmis nefis aromali.",
        "tags": ["Tamamen Dogal", "Saf Bal"],
        "price": 850,
        "image": "images/cicek_bali.png"
    },
    "karakovan": {
        "category": "GELENEKSEL",
        "name": "Hakiki Karakovan Bali",
        "description": "Atalarimizin yontemleriyle hazirlanan tamamen dogal karakovan bali.",
        "tags": ["Yuksek Aromali", "Katkisiz"],
        "price": 1250,
        "image": "images/karakovan.png"
    },
    "nilay_altin": {
        "category": "PREMIUM",
        "name": "Nilay Altin Kovan Ozel Bal",
        "description": "Sadece belirli donemlerde, en oz kovanlardan sinirli sayida uretilen Premium serimiz.",
        "tags": ["Sinirli Uretim", "En Yuksek Kalite"],
        "price": 1500,
        "image": "images/nilay_altin.png"
    },
    "dut_pekmezi": {
        "category": "SIFA DEPOSU",
        "name": "Erzurum Dut Pekmezi",
        "description": "Erzurum yoresinin ozenle secilmis dutlarindan kaynatilan dogal pekmez.",
        "tags": ["Katkisiz", "Geleneksel"],
        "price": 750,
        "image": "images/dut_pekmezi.png"
    },
    "uzum_pekmezi": {
        "category": "SIFA DEPOSU",
        "name": "Hakiki Uzum Pekmezi",
        "description": "Geleneksel yontemlerle, saatlerce kaynatilarak hazirlanan Erzurum uzum pekmezi.",
        "tags": ["Seker Ilavesiz", "Enerji"],
        "price": 750,
        "image": "images/uzum_pekmezi.png"
    },
    "cevizli_sucuk": {
        "category": "YORESEL TATLI",
        "name": "Bol Cevizli Sucuk",
        "description": "Bol cevizli ve nefis uzum sirasi ile hazirlanan mukemmel enerji veren atistirmalik.",
        "tags": ["Ceviz Dolgulu", "Organik"],
        "price": 550,
        "image": "images/cevizli_sucuk.png"
    },
    "pestil_bastik": {
        "category": "YORESEL TATLI",
        "name": "Pestil - Bastik",
        "description": "Guneste kurutulmus, dogal meyve aromali geleneksel Erzurum pestili.",
        "tags": ["Dogal", "Enerji"],
        "price": 450,
        "image": "images/pestil_bastik.png"
    },
    "yayla_tereyagi": {
        "category": "DOGAL SUT URUNU",
        "name": "Hakiki Yayla Tereyagi",
        "description": "Erzurum yaylalarinda otlayan sansl ineklerin sutunden elde edilen katkisiz koy tereyagi.",
        "tags": ["Katkisiz", "Mis Kokulu"],
        "price": 550,
        "image": "images/yayla_tereyagi.png"
    }
}

# --- HEADER SECTION with LOCAL LOGO ---
logo_b64 = get_base64("logo.png")
st.markdown(f"""
<div class="brand-header">
    <img src="data:image/png;base64,{logo_b64}" style="width:120px; height:120px; border-radius:50%; border:3px solid #D4AF37; box-shadow: 0 10px 20px rgba(212, 175, 55, 0.4); margin-bottom: 20px;" alt="Logo">
    <h1 class="brand-title">NILOS BALLARI</h1>
    <div class="brand-subtitle">Erzurum Yoresel Lezzetleri</div>
    <div class="phone-badge">0542 563 32 89</div>
</div>
""", unsafe_allow_html=True)

# --- TANITIM VIDEO ---
if os.path.exists("tanitim.mp4"):
    st.markdown("<h2 style='text-align: center;'>Tanitim Videomuz</h2>", unsafe_allow_html=True)
    st.video("tanitim.mp4")
    st.markdown("<br>", unsafe_allow_html=True)

# --- PRODUCTS LIST ---
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Koleksiyonumuz</h2>", unsafe_allow_html=True)

for p_id, p in products.items():
    tags_html = "".join([f"<span>{tag}</span>" for tag in p['tags']])
    
    # Load image as base64 - same method as logo (which works!)
    img_b64 = get_base64(p['image'])
    
    st.markdown(f"""
    <div class="product-glass-card">
        <div class="cat-tag">{p['category']}</div>
        <img src="data:image/png;base64,{img_b64}" style="width:100%; height:280px; object-fit:cover; border-radius:18px; margin: 15px 0;" alt="{p['name']}">
        <div class="p-title">{p['name']}</div>
        <div class="p-desc">{p['description']}</div>
        <div class="p-tags">{tags_html}</div>
        <div class="price-box">{p['price']} <span>TL / kg</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    col_space, col_btn = st.columns([2,1])
    with col_btn:
        if st.button("Sepete Ekle", key=f"btn_{p_id}", use_container_width=True):
            if p_id in st.session_state['cart']:
                st.session_state['cart'][p_id] += 1
            else:
                st.session_state['cart'][p_id] = 1
            st.toast(f"{p['name']} sepete eklendi!")
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# --- CART SECTION ---
st.markdown("<h2 style='text-align: center; margin-top: 50px;'>Alisveris Sepeti</h2>", unsafe_allow_html=True)

total_price = 0
if not st.session_state['cart']:
    st.markdown("""
    <div style='text-align:center; padding: 40px; border: 1px dashed #D4AF37; border-radius: 20px; color: #8C7A61;'>
        Sepetiniz su an zarif lezzetler icin bekliyor.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<div class='product-glass-card' style='padding: 20px;'>", unsafe_allow_html=True)
    for p_id, qty in st.session_state['cart'].items():
        product = products[p_id]
        price = product['price'] * qty
        total_price += price
        
        c1, c2 = st.columns([5, 1])
        with c1:
            st.write(f"**{product['name']}**  \n{qty} adet x {product['price']} TL")
        with c2:
            if st.button("Sil", key=f"del_{p_id}"):
                del st.session_state['cart'][p_id]
                st.rerun()
                
    st.markdown(f"<div style='text-align:right; font-size:1.5rem; font-weight:800; font-family: Outfit; color: #2C241B; border-top: 1px solid #EADDC7; margin-top: 20px; padding-top: 20px;'>Toplam: {total_price} TL</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='margin-top:40px;'>Teslimat Detaylari</h3>", unsafe_allow_html=True)
    with st.form("checkout_form"):
        name = st.text_input("Adiniz ve Soyadiniz")
        address = st.text_area("Acik Teslimat Adresi")
        payment_method = st.selectbox("Tercih Edilen Odeme", ["Kapida Nakit", "Kapida Kredi Karti", "Havale / EFT"])
        
        submit_order = st.form_submit_button("Siparisi Onayla")
        
        if submit_order:
            if not name or not address:
                st.error("Lutfen bilgileri eksiksiz doldurun.")
            else:
                phone_number = "905425633289"
                msg_lines = [
                    "YENI SIPARIS - NILOS BALLARI",
                    "------------------------",
                    f"Musteri: {name}",
                    f"Adres: {address}",
                    f"Odeme: {payment_method}",
                    "------------------------",
                    "Siparis Icerigi:"
                ]
                for p_id, qty in st.session_state['cart'].items():
                    msg_lines.append(f"- {qty}x {products[p_id]['name']} ({products[p_id]['price'] * qty} TL)")
                
                msg_lines.append("------------------------")
                msg_lines.append(f"TOPLAM: {total_price} TL")
                
                encoded_msg = urllib.parse.quote("\n".join(msg_lines))
                wa_url = f"https://wa.me/{phone_number}?text={encoded_msg}"
                
                st.success("Siparisiniz sevgiyle hazirlandi. WhatsApp uzerinden iletmek icin butona tiklayin.")
                st.markdown(f'<a href="{wa_url}" target="_blank" class="whatsapp-btn">Siparisi Whatsapp ile Ilet</a>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div style="text-align:center; padding:40px 20px; margin-top: 40px; border-top: 1px solid #EADDC7;">
    <div style="font-family: 'Playfair Display', serif; font-size: 1.5rem; color:#2C241B; font-weight: 700;">Nilos Ballari</div>
    <div style="color:#A69680; margin-top: 10px; font-size: 0.9rem;">Dogadan sofraniza, lux ve katkisiz Erzurum lezzetleri.</div>
    <div style="color:#A69680; margin-top: 5px; font-size: 0.9rem;">0542 563 32 89</div>
</div>
""", unsafe_allow_html=True)
