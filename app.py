import streamlit as st
import urllib.parse
import base64
import os

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

logo_base64 = get_base64_of_bin_file('logo.png')

# --- PAGE CONFIG ---
st.set_page_config(page_title="Niloş Balları | Lüks Yöresel Lezzetler", page_icon="🍯", layout="centered")

# --- ULTRA PREMIUM CUSTOM CSS ---
st.markdown("""
<style>
    /* Premium Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,500;0,700;1,500&display=swap');

    /* Background and Global */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #FAF8F5; /* Very soft luxurious milk/cream color */
        color: #2C241B;
    }
    
    .stApp {
        background-color: #FAF8F5;
        background-image: radial-gradient(#E8DFD3 1px, transparent 0);
        background-size: 40px 40px; /* Subtle dot pattern for texture */
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #2C241B;
    }

    /* The 'Niloş' Brand Header */
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
    /* Gold accent bar */
    .brand-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 6px;
        background: linear-gradient(90deg, #D4AF37, #FFDF73, #D4AF37);
    }
    
    .logo-circle {
        background-color: transparent;
        width: 120px; height: 120px;
        margin: 0 auto 20px;
        display: flex;
        align-items: center; justify-content: center;
    }
    .logo-circle img {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 10px 20px rgba(212, 175, 55, 0.4);
        border: 2px solid #D4AF37;
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

    /* Product Cards */
    .product-glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(234, 221, 199, 0.5);
        box-shadow: 0 15px 35px rgba(0,0,0,0.03);
        margin-bottom: 25px;
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

    /* Custom Buttons */
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

    /* WhatsApp Checkout */
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

# --- UPDATED PRODUCT DATA (+250 TL added from previous) ---
products = {
    "kaset_bal": {
        "category": "ÖZEL SERİ",
        "name": "Kaset Bal (Şeker Hastalarına Uygun)",
        "description": "El değmeden sofranıza gelen katkısız doğal kaset balımız.",
        "tags": ["Erzurum Yaylaları", "Saf"],
        "price": 1250 # Was 1000 + 250
    },
    "cicek_bali": {
        "category": "KLASİK BAL",
        "name": "Erzurum Çiçek Balı",
        "description": "Erzurum yaylalarının binbir çeşit gülünden ve çiçeğinden elde edilmiş nefis aromalı.",
        "tags": ["Tamamen Doğal", "Saf Bal"],
        "price": 850
    },
    "karakovan": {
        "category": "GELENEKSEL",
        "name": "Hakiki Karakovan Balı",
        "description": "Atalarımızın yöntemleriyle hazırlanan tamamen doğal karakovan balı.",
        "tags": ["Yüksek Aromalı", "Katkısız"],
        "price": 1250 # Was 1000 + 250
    },
    "nilay_altin": {
        "category": "PREMIUM",
        "name": "Nilay Altın Kovan Özel Bal",
        "description": "Sadece belirli dönemlerde, en öz kovanlardan sınırlı sayıda üretilen Premium serimiz.",
        "tags": ["Sınırlı Üretim", "En Yüksek Kalite"],
        "price": 1500 # Was 1250 + 250
    },
    "dut_pekmezi": {
        "category": "ŞİFA DEPOSU",
        "name": "Erzurum Dut Pekmezi",
        "description": "Erzurum yöresinin özenle seçilmiş dutlarından kaynatılan doğal pekmez.",
        "tags": ["Katkısız", "Geleneksel"],
        "price": 750
    },
    "uzum_pekmezi": {
        "category": "ŞİFA DEPOSU",
        "name": "Hakiki Üzüm Pekmezi",
        "description": "Geleneksel yöntemlerle, saatlerce kaynatılarak hazırlanan Erzurum üzüm pekmezi.",
        "tags": ["Şeker İlavesiz", "Enerji"],
        "price": 750
    },
    "cevizli_sucuk": {
        "category": "YÖRESEL TATLI",
        "name": "Bol Cevizli Sucuk",
        "description": "Bol cevizli ve nefis üzüm şırası ile hazırlanan mükemmel enerji veren atıştırmalık.",
        "tags": ["Ceviz Dolgulu", "Organik"],
        "price": 850 # Was 600 + 250
    }
}

# --- HEADER SECTION ---
st.markdown(f"""
<div class="brand-header">
    <div class="logo-circle"><img src="data:image/png;base64,{logo_base64}" alt="Niloş Balları Logo"></div>
    <h1 class="brand-title">NİLOŞ BALLARI</h1>
    <div class="brand-subtitle">Erzurum Yöresel Lezzetleri</div>
    <div class="phone-badge">☎ 0542 563 32 89</div>
</div>
""", unsafe_allow_html=True)

# --- PRODUCTS LIST ---
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Koleksiyonumuz</h2>", unsafe_allow_html=True)

for p_id, p in products.items():
    tags_html = "".join([f"<span>{tag}</span>" for tag in p['tags']])
    
    st.markdown(f"""
    <div class="product-glass-card">
        <div class="cat-tag">{p['category']}</div>
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
            st.toast(f"✨ {p['name']} sepete eklendi!")
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# --- CART SECTION ---
st.markdown("<h2 style='text-align: center; margin-top: 50px;'>Alışveriş Sepeti</h2>", unsafe_allow_html=True)

total_price = 0
if not st.session_state['cart']:
    st.markdown("""
    <div style='text-align:center; padding: 40px; border: 1px dashed #D4AF37; border-radius: 20px; color: #8C7A61;'>
        Sepetiniz şu an zarif lezzetler için bekliyor.
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
            st.write(f"<span style='font-family: Outfit; font-weight: 600;'>{product['name']}</span> <br> <span style='color:#A69680;'>{qty} adet x {product['price']} TL</span>", unsafe_allow_html=True)
        with c2:
            if st.button("Sil", key=f"del_{p_id}"):
                del st.session_state['cart'][p_id]
                st.rerun()
                
    st.markdown(f"<div style='text-align:right; font-size:1.5rem; font-weight:800; font-family: Outfit; color: #2C241B; border-top: 1px solid #EADDC7; margin-top: 20px; padding-top: 20px;'>Toplam: {total_price} TL</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- CHECKOUT FORM ---
    st.markdown("<h3 style='margin-top:40px;'>Teslimat Detayları</h3>", unsafe_allow_html=True)
    with st.form("checkout_form"):
        name = st.text_input("Adınız ve Soyadınız")
        address = st.text_area("Açık Teslimat Adresi")
        payment_method = st.selectbox("Tercih Edilen Ödeme", ["Kapıda Nakit", "Kapıda Kredi Kartı", "Havale / EFT"])
        
        submit_order = st.form_submit_button("💳 Siparişi Onayla")
        
        if submit_order:
            if not name or not address:
                st.error("Lütfen bilgileri eksiksiz doldurun.")
            else:
                phone_number = "905425633289"
                msg_lines = [
                    "✨ *NİLOŞ BALLARI LÜKS SİPARİŞ*",
                    "------------------------",
                    f"👤 *Misafir:* {name}",
                    f"📍 *Adres:* {address}",
                    f"💳 *Ödeme:* {payment_method}",
                    "------------------------",
                    "📦 *Sipariş İçeriği:*"
                ]
                for p_id, qty in st.session_state['cart'].items():
                    msg_lines.append(f"• {qty}x {products[p_id]['name']} ({products[p_id]['price'] * qty} TL)")
                
                msg_lines.append("------------------------")
                msg_lines.append(f"💎 *TOPLAM:* {total_price} TL")
                
                encoded_msg = urllib.parse.quote("\n".join(msg_lines))
                wa_url = f"https://wa.me/{phone_number}?text={encoded_msg}"
                
                st.success("Siparişiniz sevgiyle hazırlandı. WhatsApp üzerinden iletmek için butona tıklayın.")
                st.markdown(f'<a href="{wa_url}" target="_blank" class="whatsapp-btn">Siparişi Whatsapp ile İlet</a>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div style="text-align:center; padding:40px 20px; margin-top: 40px; border-top: 1px solid #EADDC7;">
    <div style="font-family: 'Playfair Display', serif; font-size: 1.5rem; color:#2C241B; font-weight: 700;">Niloş Balları</div>
    <div style="color:#A69680; margin-top: 10px; font-size: 0.9rem;">Doğadan sofranıza, lüks ve katkısız Erzurum lezzetleri.</div>
    <div style="color:#A69680; margin-top: 5px; font-size: 0.9rem;">☎ 0542 563 32 89</div>
</div>
""", unsafe_allow_html=True)
