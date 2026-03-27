import streamlit as st
import urllib.parse
from PIL import Image
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Niloş Balları | Doğadan Sofranıza", page_icon="🍯", layout="wide")

# --- CUSTOM CSS FOR PREMIUM AESTHETICS ---
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@300;400;600&display=swap');

    /* Global Styles */
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
        background-color: #fdfbf7;
        color: #333333;
    }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #b8860b;
    }

    /* Hero Section */
    .hero-container {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1587049352847-4d4b1f63dc88?q=80&w=2070&auto=format&fit=crop') center/cover;
        padding: 100px 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .hero-title {
        font-size: 4rem;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        letter-spacing: 2px;
    }

    /* Product Cards */
    .product-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #f0e6d2;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(184, 134, 11, 0.2);
    }
    .product-price {
        font-size: 1.5rem;
        font-weight: 600;
        color: #b8860b;
        margin: 15px 0;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #b8860b;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #996515;
        box-shadow: 0 4px 15px rgba(184, 134, 11, 0.4);
        color: white;
    }

    /* Whatsapp Button */
    .whatsapp-btn {
        background-color: #25D366;
        color: white;
        text-decoration: none;
        padding: 12px 30px;
        border-radius: 25px;
        display: inline-block;
        font-weight: bold;
        text-align: center;
        width: 100%;
        margin-top: 15px;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
        transition: all 0.3s;
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
        color: white;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- INIT SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state['cart'] = {}

# --- PRODUCT DATA ---
products = {
    "cicek_bali": {
        "name": "Hakiki Çiçek Balı",
        "description": "Yaylaların binbir çeşit çiçeğinden süzülen saf lezzet.",
        "price": 350,
        "image": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2?w=500&auto=format&fit=crop"
    },
    "cam_bali": {
        "name": "Marmaris Çam Balı",
        "description": "Koyu rengi ve yoğun aromasıyla şifa deposu.",
        "price": 400,
        "image": "https://images.unsplash.com/photo-1587049352851-8d4e89134781?w=500&auto=format&fit=crop"
    },
    "kestane_bali": {
        "name": "Kestane Balı",
        "description": "Karadeniz'in organik kestane ormanlarından, hafif acımsı gerçek şifa.",
        "price": 750,
        "image": "https://images.unsplash.com/photo-1620063236306-381c00f3c5b5?w=500&auto=format&fit=crop"
    },
    "karakovan": {
        "name": "Karakovan Petek Balı",
        "description": "Arının kendi yaptığı doğal petek, el değmeden sofranıza.",
        "price": 600,
        "image": "https://images.unsplash.com/photo-1594895642597-20092224a18a?w=500&auto=format&fit=crop"
    }
}

# --- HEADER SECTION ---
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">Niloş Balları</h1>
    <p class="hero-subtitle">Doğanın Altın Damlası, Sofranızın Şifası</p>
</div>
""", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
col_main, col_sidebar = st.columns([7, 3])

with col_main:
    st.markdown("### 🍯 Premium Ürünlerimiz")
    
    # Store rows setup
    cols = st.columns(2)
    
    for idx, (p_id, p_info) in enumerate(products.items()):
        col = cols[idx % 2]
        with col:
            st.markdown(f"""
            <div class="product-card">
                <img src="{p_info['image']}" style="width:100%; height:250px; object-fit:cover; border-radius:10px; margin-bottom:15px;" alt="{p_info['name']}">
                <h3 style="margin:0; font-size:1.4rem;">{p_info['name']}</h3>
                <p style="color:#666; font-size:0.9rem; margin:10px 0;">{p_info['description']}</p>
                <div class="product-price">{p_info['price']} ₺ <span style="font-size:0.8rem; color:#999; font-weight:normal;">/ kg</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Use Streamlit buttons for functionality
            if st.button(f"🛒 Sepete Ekle", key=f"btn_{p_id}", use_container_width=True):
                if p_id in st.session_state['cart']:
                    st.session_state['cart'][p_id] += 1
                else:
                    st.session_state['cart'][p_id] = 1
                st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)

with col_sidebar:
    st.markdown("### 🛍️ Sepetiniz")
    st.markdown("---")
    
    total_price = 0
    if not st.session_state['cart']:
        st.info("Sepetiniz şu an boş.")
    else:
        for p_id, qty in st.session_state['cart'].items():
            product = products[p_id]
            price = product['price'] * qty
            total_price += price
            
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**{product['name']}**  \n{qty} adet x {product['price']}₺")
            with c2:
                if st.button("🗑️", key=f"del_{p_id}"):
                    del st.session_state['cart'][p_id]
                    st.rerun()
        
        st.markdown("---")
        st.markdown(f"<h3 style='text-align:right;'>Toplam: {total_price} ₺</h3>", unsafe_allow_html=True)
        
        st.markdown("### 📝 Sipariş Bilgileri")
        with st.form("checkout_form"):
            name = st.text_input("Ad Soyad", placeholder="Örn: Ahmet Yılmaz")
            address = st.text_area("Teslimat Adresi", placeholder="Açık adresinizi giriniz...")
            payment_method = st.radio("Ödeme Yöntemi", ["Kapıda Nakit Ödeme", "Kapıda Kredi Kartı"])
            
            submit_order = st.form_submit_button("✅ Siparişi Tamamla (WhatsApp)")
            
            if submit_order:
                if not name or not address:
                    st.error("Lütfen ad ve adres bilgilerinizi eksiksiz doldurunuz.")
                else:
                    # Construct Whatsapp Message
                    phone_number = "905425633289" # Format with country code
                    msg_lines = [
                        "🍯 *YENİ SİPARİŞ - NİLOŞ BALLARI*",
                        "------------------------",
                        f"👤 *Müşteri:* {name}",
                        f"📍 *Adres:* {address}",
                        f"💳 *Ödeme:* {payment_method}",
                        "------------------------",
                        "📦 *Sipariş Detayı:*"
                    ]
                    
                    for p_id, qty in st.session_state['cart'].items():
                        msg_lines.append(f"- {qty}x {products[p_id]['name']} ({products[p_id]['price'] * qty} ₺)")
                    
                    msg_lines.append("------------------------")
                    msg_lines.append(f"💰 *TOPLAM TUTAR: {total_price} ₺*")
                    
                    msg_text = "\n".join(msg_lines)
                    encoded_msg = urllib.parse.quote(msg_text)
                    
                    wa_url = f"https://wa.me/{phone_number}?text={encoded_msg}"
                    
                    st.success("Siparişiniz hazır! Lütfen aşağıdaki butona tıklayarak bilgileri bize WhatsApp üzerinden iletin.")
                    st.markdown(f'<a href="{wa_url}" target="_blank" class="whatsapp-btn">📱 WhatsApp ile Gönder</a>', unsafe_allow_html=True)


# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#888; padding:20px;">
    <strong>Niloş Balları</strong> © 2026 | Tamamen doğal ve şekersizdir.<br>
    Müşteri Hizmetleri & Sipariş: <strong>0542 563 32 89</strong>
</div>
""", unsafe_allow_html=True)
