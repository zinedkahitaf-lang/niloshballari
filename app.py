import streamlit as st
import urllib.parse
import os
import pathlib
from PIL import Image
import openai

BASE_DIR = pathlib.Path(__file__).parent

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
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# --- ÜRÜN VERİLERİ ---
products = {
    "kaset_bal": {
        "category": "ÖZEL SERİ",
        "name": "Kaset Balı (Şeker Hastalarına Uygun)",
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
        "name": "Nilay Altın Kovan Özel Balı",
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

# --- LOGO ---
col_logo_left, col_logo_center, col_logo_right = st.columns([1, 2, 1])
with col_logo_center:
    logo_path = BASE_DIR / "logo.png"
    if logo_path.exists():
        st.image(Image.open(logo_path))

st.markdown("""
<div style="text-align: center; margin-bottom: 40px;">
    <div style="font-family: 'Playfair Display', serif; font-size: 2.5rem; font-weight: 700; color: #1A1510; letter-spacing: 2px;">NİLOŞ BALLARI</div>
    <div style="font-size: 1rem; color: #8C7A61; letter-spacing: 4px; text-transform: uppercase; margin: 8px 0 20px;">ERZURUM YÖRESEL LEZZETLERİ</div>
    <div style="background-color: #1C3322; color: #E2ECD8; padding: 10px 25px; border-radius: 30px; display: inline-block; font-weight: 600;">Sipariş Hattı: 0542 563 32 89</div>
</div>
""", unsafe_allow_html=True)

# --- TANITIM VİDEOSU ---
video_path = BASE_DIR / "tanitim.mp4"
if video_path.exists():
    st.markdown("## Tanıtım Videomuz")
    st.video(str(video_path))
    st.markdown("---")

# --- ÜRÜNLER ---
st.markdown("## Koleksiyonumuz")

for p_id, p in products.items():
    tags_html = "".join([f"<span>{tag}</span>" for tag in p['tags']])
    st.markdown(f'<div class="cat-label">{p["category"]}</div>', unsafe_allow_html=True)
    img_path = BASE_DIR / p['image']
    if img_path.exists():
        st.image(Image.open(img_path))
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
    st.info("Sepetiniz şu an boş.")
else:
    for p_id, qty in st.session_state['cart'].items():
        product = products[p_id]
        price = product['price'] * qty
        total_price += price
        st.markdown(f"**{product['name']}** x {qty}: **{price} TL**")
    
    st.markdown(f"### Toplam: {total_price} TL")
    whatsapp_msg = f"Merhaba, Nilosh Ballari sayfasından şunları sipariş etmek istiyorum:\n"
    for p_id, qty in st.session_state['cart'].items():
        whatsapp_msg += f"- {products[p_id]['name']} x {qty}\n"
    whatsapp_msg += f"\nToplam Tutar: {total_price} TL"
    encoded_msg = urllib.parse.quote(whatsapp_msg)
    whatsapp_link = f'<a href="https://wa.me/905425633289?text={encoded_msg}" class="whatsapp-btn" target="_blank">WhatsApp ile Siparişi Tamamla</a>'
    st.markdown(whatsapp_link, unsafe_allow_html=True)
    if st.button("Sepeti Temizle"):
        st.session_state['cart'] = {}
        st.rerun()

# --- ARIKOVANI ASİSTANI (CHATBOT) ---
with st.sidebar:
    st.markdown("### 🍯 Arıkovanı Asistanı")
    st.info("Ben Niloş Balları'nın şifa uzmanıyım. Sorularınız için buradayım!")
    
    # Güvenli API Anahtarı (Streamlit Cloud Secrets'tan okur)
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        client = openai.OpenAI(api_key=api_key)
        
        # Botun her şeyi bilmesi için ürün listesi
        p_list = "\n".join([f"- {v['name']}: {v['price']} TL, {v['description']}" for k, v in products.items()])
        system_msg = f"Sen Erzurumlu, nazik ve bilgili 'Arıkovanı Asistanı'sın. Ürünler: {p_list}. Kısa, öz ve cana yakın konuş. Sipariş için 0542 563 32 89 WhatsApp hattını hatırlat."

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Bana bir şey sor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"system","content":system_msg}]+st.session_state.messages)
                full_resp = response.choices[0].message.content
                st.markdown(full_resp)
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
    except Exception:
        st.warning("🤖 Asistan şu an kovanında dinleniyor. (API Anahtarı eksik)")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #8C7A61; font-size: 0.8rem;'>© 2026 Niloş Balları - Erzurum Karayazı Köy Ürünleri</div>", unsafe_allow_html=True)
