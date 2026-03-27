import streamlit as st
import urllib.parse
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Niloş Balları | Erzurum Yöresel Lezzetleri", page_icon=":honey_pot:", layout="centered")

# --- PREMIUM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Playfair+Display:wght@500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #FAF8F5;
        color: #2C241B;
    }
    .stApp { background-color: #FAF8F5; }
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
        box-shadow: 0 20px 40px rgba(186,153,113,0.08);
        margin-bottom: 40px;
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
        font-size: 2.5rem; font-weight: 700;
        margin: 15px 0 0; letter-spacing: 2px; color: #1A1510;
    }
    .brand-subtitle {
        font-size: 1rem; color: #8C7A61;
        letter-spacing: 4px; text-transform: uppercase; margin: 8px 0 20px;
    }
    .phone-badge {
        background-color: #1C3322; color: #E2ECD8;
        padding: 10px 25px; border-radius: 30px;
        display: inline-block; font-weight: 600; font-size: 1rem;
    }
    .info-card {
        background: rgba(255,255,255,0.9);
        border-radius: 0 0 20px 20px;
        padding: 20px 25px;
        border: 1px solid rgba(234,221,199,0.5);
        border-top: none;
        margin-top: -8px;
        margin-bottom: 5px;
    }
    .cat-label {
        background: #2C241B; color: #FFDF73;
        font-size: 0.7rem; font-weight: 800;
        padding: 5px 15px; border-radius: 12px;
        letter-spacing: 2px; display: inline-block; margin-bottom: 5px;
    }
    .p-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem; font-weight: 700; color: #2C241B; margin: 8px 0;
    }
    .p-desc { color: #635848; font-size: 0.95rem; line-height: 1.6; }
    .p-tags { margin: 10px 0; }
    .p-tags span {
        background: #F4EEDF; padding: 4px 10px;
        border-radius: 8px; font-size: 0.8rem; color: #A69680;
        margin-right: 8px;
    }
    .price-box {
        font-size: 1.6rem; font-weight: 800; color: #1A1510; margin-top: 10px;
    }
    .price-box span { font-size: 0.9rem; color: #A69680; font-weight: 400; }
    .stButton>button {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white; border: none; border-radius: 20px;
        font-weight: 600; box-shadow: 0 10px 20px rgba(16,185,129,0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #059669, #047857);
        transform: scale(1.03);
    }
    .whatsapp-btn {
        background: linear-gradient(135deg, #25D366, #128C7E);
        color: white; text-decoration: none;
        padding: 18px 30px; border-radius: 16px;
        display: block; font-weight: 800; font-size: 1.2rem;
        text-align: center; width: 100%; margin-top: 25px;
        box-shadow: 0 15px 30px rgba(37,211,102,0.3);
    }
    .whatsapp-btn:hover { transform: translateY(-3px); }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state['cart'] = {}

# --- ÜRÜN VERİLERİ ---
products = {
    "kaset_bal": {
        "category": "ÖZEL SERİ",
        "name": "Kaset Bal (Şeker Hastalarına Uygun)",
        "description": "El değmeden sofranıza gelen katkısız doğal kaset balımız.",
        "tags": ["Erzurum Yaylaları", "Saf"],
        "price": 1250,
        "image": "images/kaset_bal.png"
    },
    "cicek_bali": {
        "category": "KLASİK BAL",
        "name": "Erzurum Çiçek Balı",
        "description": "Erzurum yaylalarının binbir çeşit gülünden ve çiçeğinden elde edilmiş nefis aromalı.",
        "tags": ["Tamamen Doğal", "Saf Bal"],
        "price": 850,
        "image": "images/cicek_bali.png"
    },
    "karakovan": {
        "category": "GELENEKSEL",
        "name": "Hakiki Karakovan Balı",
        "description": "Atalarımızın yöntemleriyle hazırlanan tamamen doğal karakovan balı.",
        "tags": ["Yüksek Aromalı", "Katkısız"],
        "price": 1250,
        "image": "images/karakovan.png"
    },
    "nilay_altin": {
        "category": "PREMIUM",
        "name": "Nilay Altın Kovan Özel Bal",
        "description": "Sadece belirli dönemlerde, en öz kovanlardan sınırlı sayıda üretilen Premium serimiz.",
        "tags": ["Sınırlı Üretim", "En Yüksek Kalite"],
        "price": 1500,
        "image": "images/nilay_altin.png"
    },
    "dut_pekmezi": {
        "category": "ŞİFA DEPOSU",
        "name": "Erzurum Dut Pekmezi",
        "description": "Erzurum yöresinin özenle seçilmiş dutlarından kaynatılan doğal pekmez.",
        "tags": ["Katkısız", "Geleneksel"],
        "price": 750,
        "image": "images/dut_pekmezi.png"
    },
    "uzum_pekmezi": {
        "category": "ŞİFA DEPOSU",
        "name": "Hakiki Üzüm Pekmezi",
        "description": "Geleneksel yöntemlerle, saatlerce kaynatılarak hazırlanan Erzurum üzüm pekmezi.",
        "tags": ["Şeker İlavesiz", "Enerji"],
        "price": 750,
        "image": "images/uzum_pekmezi.png"
    },
    "cevizli_sucuk": {
        "category": "YÖRESEL TATLI",
        "name": "Bol Cevizli Sucuk",
        "description": "Bol cevizli ve nefis üzüm şırası ile hazırlanan mükemmel enerji veren atıştırmalık.",
        "tags": ["Ceviz Dolgulu", "Organik"],
        "price": 550,
        "image": "images/cevizli_sucuk.png"
    },
    "pestil_bastik": {
        "category": "YÖRESEL TATLI",
        "name": "Pestil - Bastık",
        "description": "Güneşte kurutulmuş, doğal meyve aromalı geleneksel Erzurum pestili.",
        "tags": ["Doğal", "Enerji"],
        "price": 450,
        "image": "images/pestil_bastik.png"
    },
    "yayla_tereyagi": {
        "category": "DOĞAL SÜT ÜRÜNÜ",
        "name": "Hakiki Yayla Tereyağı",
        "description": "Erzurum yaylalarında otlayan ineklerin sütünden elde edilen katkısız köy tereyağı.",
        "tags": ["Katkısız", "Mis Kokulu"],
        "price": 550,
        "image": "images/yayla_tereyagi.png"
    }
}

# --- LOGO (st.image ile - kesin çalışır) ---
col_logo_left, col_logo_center, col_logo_right = st.columns([1, 2, 1])
with col_logo_center:
    if os.path.exists("logo.png"):
        logo_bytes = open("logo.png", "rb").read()
        st.image(logo_bytes, width="stretch")

st.markdown("""
<div style="text-align: center; margin-bottom: 40px;">
    <div style="font-family: 'Playfair Display', serif; font-size: 2.5rem; font-weight: 700; color: #1A1510; letter-spacing: 2px;">NİLOŞ BALLARI</div>
    <div style="font-size: 1rem; color: #8C7A61; letter-spacing: 4px; text-transform: uppercase; margin: 8px 0 20px;">ERZURUM YÖRESEL LEZZETLERİ</div>
    <div style="background-color: #1C3322; color: #E2ECD8; padding: 10px 25px; border-radius: 30px; display: inline-block; font-weight: 600;">Sipariş Hattı: 0542 563 32 89</div>
</div>
""", unsafe_allow_html=True)

# --- TANITIM VİDEOSU ---
if os.path.exists("tanitim.mp4"):
    st.markdown("## Tanıtım Videomuz")
    video_bytes = open("tanitim.mp4", "rb").read()
    st.video(video_bytes)
    st.markdown("---")

# --- ÜRÜNLER ---
st.markdown("## Koleksiyonumuz")

for p_id, p in products.items():
    tags_html = "".join([f"<span>{tag}</span>" for tag in p['tags']])
    
    st.markdown(f'<div class="cat-label">{p["category"]}</div>', unsafe_allow_html=True)
    
    # FOTOĞRAF: bytes olarak oku ve st.image ile göster - BU KESİN ÇALIŞIR
    img_path = p['image']
    if os.path.exists(img_path):
        img_bytes = open(img_path, "rb").read()
        st.image(img_bytes, width="stretch")
    
    st.markdown(f"""
    <div class="info-card">
        <div class="p-title">{p['name']}</div>
        <div class="p-desc">{p['description']}</div>
        <div class="p-tags">{tags_html}</div>
        <div class="price-box">{p['price']} <span>TL / kg</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col2:
        if st.button("Sepete Ekle", key=f"btn_{p_id}", use_container_width=True):
            if p_id in st.session_state['cart']:
                st.session_state['cart'][p_id] += 1
            else:
                st.session_state['cart'][p_id] = 1
            st.toast(f"{p['name']} sepete eklendi!")
    st.markdown("")

# --- SEPET ---
st.markdown("## Alışveriş Sepeti")

total_price = 0
if not st.session_state['cart']:
    st.info("Sepetiniz şu an boş. Yukarıdan ürün ekleyebilirsiniz.")
else:
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
    
    st.markdown(f"### Toplam: {total_price} TL")
    
    st.markdown("### Teslimat Bilgileri")
    with st.form("checkout_form"):
        name = st.text_input("Adınız ve Soyadınız")
        address = st.text_area("Açık Teslimat Adresi")
        payment_method = st.selectbox("Ödeme Yöntemi", ["Kapıda Nakit Ödeme", "Kapıda Kredi Kartı", "Havale / EFT"])
        
        submit_order = st.form_submit_button("Siparişi Onayla")
        
        if submit_order:
            if not name or not address:
                st.error("Lütfen bilgileri eksiksiz doldurun.")
            else:
                phone_number = "905425633289"
                msg_lines = [
                    "YENİ SİPARİŞ - NİLOŞ BALLARI",
                    "------------------------",
                    f"Müşteri: {name}",
                    f"Adres: {address}",
                    f"Ödeme: {payment_method}",
                    "------------------------",
                    "Sipariş İçeriği:"
                ]
                for p_id, qty in st.session_state['cart'].items():
                    msg_lines.append(f"- {qty}x {products[p_id]['name']} ({products[p_id]['price'] * qty} TL)")
                msg_lines.append("------------------------")
                msg_lines.append(f"TOPLAM: {total_price} TL")
                
                encoded_msg = urllib.parse.quote("\n".join(msg_lines))
                wa_url = f"https://wa.me/{phone_number}?text={encoded_msg}"
                
                st.success("Siparişiniz hazırlandı! WhatsApp ile göndermek için aşağıya tıklayın.")
                st.markdown(f'<a href="{wa_url}" target="_blank" class="whatsapp-btn">WhatsApp ile Siparişi Gönder</a>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:30px;">
    <div style="font-family: 'Playfair Display', serif; font-size: 1.3rem; color:#2C241B; font-weight: 700;">Niloş Balları</div>
    <div style="color:#A69680; margin-top: 8px;">Doğadan sofranıza, katkısız Erzurum lezzetleri.</div>
    <div style="color:#A69680; margin-top: 5px;">Sipariş: 0542 563 32 89</div>
</div>
""", unsafe_allow_html=True)
