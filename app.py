import streamlit as st
import urllib.parse

# --- PAGE CONFIG ---
st.set_page_config(page_title="Niloş Balları | Erzurum Yöresel Lezzetleri", page_icon="🍯", layout="centered")

# --- CUSTOM CSS FOR MOBILE-FRIENDLY & PREMIUM AESTHETICS ---
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Nunito:wght@400;700&display=swap');

    /* Global Styles */
    html, body, [class*="css"]  {
        font-family: 'Nunito', sans-serif;
        background-color: #FDF7EC; /* Beige background from screenshot */
        color: #4A3A28; /* Dark brown text */
    }
    
    .stApp {
        background-color: #FDF7EC;
    }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif;
        color: #4A3A28;
        font-weight: 700;
    }

    /* Top Logo Card */
    .top-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        text-align: left;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 30px;
        border-bottom: 2px solid #EEE6D8;
    }
    .top-card h1 {
        margin: 0;
        font-size: 1.8rem;
        color: #4A2B18;
    }
    .top-card p {
        margin: 5px 0 15px 0;
        font-size: 0.9rem;
        color: #8C7B65;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .contact-badge {
        background-color: #1A4D2E;
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        font-size: 0.9rem;
    }

    /* Main Banner Text */
    .hero-text {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 20px;
        color: #4A3A28;
    }
    .hero-text span {
        color: #D4A373; /* Gold touch */
    }
    .hero-subtext {
        font-size: 1rem;
        color: #554C41;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .tag-container span {
        border: 1px solid #D4A373;
        color: #8B653F;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin-right: 8px;
        margin-bottom: 10px;
    }

    /* Product Cards */
    .product-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    .category-label {
        color: #B28C56;
        font-size: 0.75rem;
        font-weight: bold;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .product-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin:0 0 10px 0;
        color: #333;
    }
    .product-desc {
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 10px;
        line-height: 1.5;
    }
    .product-tags {
        color: #A39171;
        font-size: 0.85rem;
        margin-bottom: 15px;
    }
    .price-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 15px;
    }
    .price-text {
        font-size: 1.4rem;
        font-weight: 800;
        color: #222;
    }
    .price-text span {
        font-size: 0.9rem;
        color: #888;
        font-weight: normal;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #1DB954; /* Bright Green */
        color: white;
        border: none;
        border-radius: 25px;
        padding: 8px 20px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #179643;
        color: white;
    }
    
    .whatsapp-btn {
        background-color: #25D366;
        color: white;
        text-decoration: none;
        padding: 15px 30px;
        border-radius: 30px;
        display: block;
        font-weight: bold;
        font-size: 1.1rem;
        text-align: center;
        width: 100%;
        margin-top: 25px;
        box-shadow: 0 5px 15px rgba(37, 211, 102, 0.3);
        transition: all 0.3s;
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- INIT SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state['cart'] = {}

# --- PRODUCT DATA ---
products = {
    "kaset_bal": {
        "category": "BAL",
        "name": "Kaset Bal (Şeker Hastalarına Uygun)",
        "description": "Katkısız doğal kaset bal.",
        "tags": "Erzurum yaylaları",
        "price": 1000
    },
    "cicek_bali": {
        "category": "BAL",
        "name": "Çiçek Balı",
        "description": "Erzurum yaylalarının nefis aromalı doğal çiçek balı.",
        "tags": "Tamamen doğal · Saf bal",
        "price": 850
    },
    "karakovan": {
        "category": "BAL",
        "name": "Karakovan Balı",
        "description": "Tamamen doğal karakovan balı. Geleneksel yöntemlerle üretilmiştir.",
        "tags": "Saf bal · Yüksek aromalı",
        "price": 1000
    },
    "nilay_altin": {
        "category": "BAL",
        "name": "Nilay Altın Kovan Özel Bal",
        "description": "Sınırlı üretim premium bal.",
        "tags": "Özel seçilmiş kovanlardan · Erzurum yaylaları",
        "price": 1250
    },
    "dut_pekmezi": {
        "category": "PEKMEZ",
        "name": "Dut Pekmezi",
        "description": "Erzurum yöresinin doğal dut pekmezi.",
        "tags": "Katkısız üretim",
        "price": 750
    },
    "uzum_pekmezi": {
        "category": "PEKMEZ",
        "name": "Üzüm Pekmezi",
        "description": "Geleneksel yöntemlerle kaynatılmış Erzurum üzüm pekmezi.",
        "tags": "Şeker ilavesiz",
        "price": 750
    },
    "cevizli_sucuk": {
        "category": "YÖRESEL TATLI",
        "name": "Cevizli Sucuk",
        "description": "Bol cevizli ve nefis üzüm şıralı doğal cevizli sucuk. Enerji deposu.",
        "tags": "Geleneksel yöntem",
        "price": 600
    }
}

# --- HEADER (Top Card like screenshot) ---
st.markdown("""
<div class="top-card">
    <div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 10px;">
        <div style="background-color: #DDA15E; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; margin-right: 15px; color: white; font-size: 24px; font-weight: bold; font-family: 'Montserrat', sans-serif;">N</div>
        <div>
            <h1>NİLOŞ BALLARI</h1>
            <p>ERZURUM YÖRESEL LEZZETLERİ</p>
        </div>
    </div>
    <div style="font-size:0.8rem; color:#888; margin-bottom:5px;">Sipariş & bilgi hattı</div>
    <div class="contact-badge">☎ 0542 563 32 89</div>
</div>
""", unsafe_allow_html=True)

# --- HERO TEXT SECTION ---
st.markdown("""
<div class="hero-text">
    Erzurum yaylalarından <span>doğal bal</span> ve süt ürünleri
</div>
<div class="hero-subtext">
    Niloş Balları; katkısız bal, pekmez, pestil ve sucuk gibi Erzurum yöresine ait ürünleri kapınıza kadar getirir. Ailenizle güvenle tüketebileceğiniz, güvenilir üreticilerden seçilmiş doğal lezzetler sunar.
</div>
<div class="tag-container">
    <span>%100 Doğal</span>
    <span>Erzurum Yöresi</span>
    <span>Kargo / Elden Teslim</span>
</div>
<br>
""", unsafe_allow_html=True)

# --- PRODUCTS LIST ---
st.markdown("<h2>Satışta Olan Ürünler</h2>", unsafe_allow_html=True)

for p_id, p in products.items():
    # We use Streamlit columns to align the price and button
    st.markdown(f"""
    <div style="background: white; border-radius: 20px; padding: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.04); margin-bottom: 5px;">
        <div class="category-label">{p['category']}</div>
        <div class="product-title">{p['name']}</div>
        <div class="product-desc">{p['description']}</div>
        <div class="product-tags">{p['tags']}</div>
        <div class="price-text">{p['price']} TL <span>/ kg</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1])
    with col2:
        if st.button("Sipariş Ver", key=f"btn_{p_id}", use_container_width=True):
            if p_id in st.session_state['cart']:
                st.session_state['cart'][p_id] += 1
            else:
                st.session_state['cart'][p_id] = 1
            st.toast(f"✅ {p['name']} sepete eklendi!")
    st.markdown("<br>", unsafe_allow_html=True)


# --- CART & CHECKOUT ---
st.markdown("<br><br><br><h2>🛒 Sepetiniz ve Sipariş</h2>", unsafe_allow_html=True)

total_price = 0
if not st.session_state['cart']:
    st.info("Sepetinizde henüz ürün bulunmuyor. Yukarıdan 'Sipariş Ver' butonları ile ürün ekleyebilirsiniz.")
else:
    st.markdown("<div style='background: white; border-radius: 20px; padding: 25px; box-shadow: 0 5px 15px rgba(0,0,0,0.04);'>", unsafe_allow_html=True)
    for p_id, qty in st.session_state['cart'].items():
        product = products[p_id]
        price = product['price'] * qty
        total_price += price
        
        c1, c2 = st.columns([4, 1])
        with c1:
            st.write(f"**{product['name']}**  \n{qty} adet x {product['price']} TL")
        with c2:
            if st.button("🗑️", key=f"del_{p_id}"):
                del st.session_state['cart'][p_id]
                st.rerun()
                
    st.markdown(f"<h3 style='text-align:right; margin-top:20px; color:#4A3A28;'>Toplam: {total_price} TL</h3>", unsafe_allow_html=True)
    st.markdown("</div><br>", unsafe_allow_html=True)
    
    st.markdown("### 📝 Teslimat Bilgileri")
    with st.form("checkout_form"):
        name = st.text_input("Ad Soyad", placeholder="Örn: Ahmet Yılmaz")
        address = st.text_area("Açık Teslimat Adresi", placeholder="Mahalle, sokak, no, ilçe/il")
        payment_method = st.selectbox("Ödeme Yöntemi Seçiniz", [ "Kapıda Nakit Ödeme 💵", "Kapıda Kredi Kartı 💳", "Havale / EFT 🏦"])
        
        submit_order = st.form_submit_button("✅ Siparişi Hazırla")
        
        if submit_order:
            if not name or not address:
                st.error("Lütfen ad ve adres bilgilerinizi eksiksiz doldurunuz.")
            else:
                # Construct Whatsapp Message
                phone_number = "905425633289" # Keep original requested number
                msg_lines = [
                    "🍯 *YENİ SİPARİŞ - NİLOŞ BALLARI*",
                    "------------------------",
                    f"👤 *Müşteri:* {name}",
                    f"📍 *Adres:* {address}",
                    f"💰 *Ödeme Yöntemi:* {payment_method}",
                    "------------------------",
                    "📦 *Sipariş Detayı:*"
                ]
                
                for p_id, qty in st.session_state['cart'].items():
                    msg_lines.append(f"- {qty}x {products[p_id]['name']} ({products[p_id]['price'] * qty} TL)")
                
                msg_lines.append("------------------------")
                msg_lines.append(f"🔥 *TOPLAM TUTAR: {total_price} TL*")
                
                msg_text = "\n".join(msg_lines)
                encoded_msg = urllib.parse.quote(msg_text)
                
                wa_url = f"https://wa.me/{phone_number}?text={encoded_msg}"
                
                st.success("Sipariş bilgileriniz hazırlandı! Lütfen aşağıdaki yeşil butona tıklayarak WhatsApp üzerinden gönderin.")
                st.markdown(f'<a href="{wa_url}" target="_blank" class="whatsapp-btn">📱 WhatsApp ile Siparişi Gönder</a>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#A39171; padding:20px; font-size: 0.9rem;">
    <strong>Niloş Balları</strong> © 2026<br>
    %100 Doğal Erzurum Yöresel Ürünler<br>
    Sipariş Hattı: <strong>0542 563 32 89</strong>
</div>
""", unsafe_allow_html=True)
