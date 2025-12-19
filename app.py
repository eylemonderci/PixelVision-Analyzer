import streamlit as st
import cv2
import numpy as np
import pixel_logic # Kendi yazdığım modülü çağırıyorum

# Sayfa Başlığı Ayarı
st.set_page_config(page_title="Pixel Art Projesi", layout="wide")

st.title("🎨 Pixel Art Analiz Aracı")
st.write("Görüntü İşleme Dersi Final Projesi - Eylem")

# --- SOL MENÜ (SIDEBAR) ---
st.sidebar.title("Ayarlar")
# Kullanıcıdan dosya alma
yuklenen_dosya = st.sidebar.file_uploader("Bir Resim Yükle", type=['jpg', 'png', 'jpeg'])

grid_boyutu = st.sidebar.slider("Kare Boyutu", 10, 50, 20)
renk_sayisi = st.sidebar.slider("Kaç Renk Bulunsun?", 3, 10, 5)

if yuklenen_dosya is not None:
    # --- RESMİ OKUMA ---
    dosya_byte = np.asarray(bytearray(yuklenen_dosya.read()), dtype=np.uint8)
    resim = cv2.imdecode(dosya_byte, 1)
    
    # OpenCV renkleri BGR okur, biz RGB'ye çeviriyoruz
    resim_rgb = cv2.cvtColor(resim, cv2.COLOR_BGR2RGB)

    # --- ANA EKRAN DÜZENİ ---
    col1, col2 = st.columns([1, 1]) # İki tarafı eşit genişlikte yaptım
    
    with col1:
        # GÜNCELLEME: width değerini 500 yaptım (Daha büyük)
        st.image(resim_rgb, caption="Yüklenen Resim", width=500)
    
    with col2:
        st.success("✅ Resim başarıyla işlendi!")
        st.info("Aşağıdaki sekmelerden analiz sonuçlarını inceleyebilirsiniz.")

    # --- SEKMELER ---
    tab1, tab2, tab3 = st.tabs(["🎨 Renkler", "📝 Şablon", "👁️ Renk Körlüğü"])

    # 1. SEKME: RENKLER
    with tab1:
        st.header("Baskın Renk Paleti")
        st.write("K-Means algoritması ile resimdeki en çok kullanılan renkleri buldum.")
        
        renkler = pixel_logic.renkleri_bul(resim_rgb, renk_sayisi)
        
        kolonlar = st.columns(renk_sayisi)
        
        for i in range(renk_sayisi):
            aktif_renk = renkler[i]
            r, g, b = aktif_renk
            hex_kodu = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            
            with kolonlar[i]:
                st.color_picker(f"Renk {i+1}", hex_kodu, disabled=True)
                st.caption(f"RGB: {r}, {g}, {b}")

    # 2. SEKME: ŞABLON
    with tab2:
        st.header("Çizim Şablonu")
        st.write("Resmin kenarlarını Canny algoritması ile bulup ters çevirdim.")
        
        izgarali, sablon = pixel_logic.sablon_cikar(resim_rgb, grid_boyutu)
        
        col1, col2 = st.columns(2)
        with col1:
            # Burayı da büyüttüm
            st.image(izgarali, caption="Kareli Görünüm", width=500)
        with col2:
            st.image(sablon, caption="Boyama Sayfası (Outline)", width=500)

    # 3. SEKME: RENK KÖRLÜĞÜ
    with tab3:
        st.header("Erişilebilirlik Testi")
        st.write("Matris çarpımı yöntemiyle simülasyon yapılıyor.")
        
        secim = st.selectbox("Hangi Göz Bozukluğu?", 
                             ["Protanopia (Kırmızı Yok)", 
                              "Deuteranopia (Yeşil Yok)", 
                              "Tritanopia (Mavi Yok)"])
        
        if "Protanopia" in secim:
            simulasyon = pixel_logic.renk_koru_yap(resim_rgb, 'protanopia')
        elif "Deuteranopia" in secim:
            simulasyon = pixel_logic.renk_koru_yap(resim_rgb, 'deuteranopia')
        else:
            simulasyon = pixel_logic.renk_koru_yap(resim_rgb, 'tritanopia')
            
        col1, col2 = st.columns(2)
        with col1:
            # Burayı da büyüttüm
            st.image(resim_rgb, caption="Normal Göz", width=500)
        with col2:
            st.image(simulasyon, caption=f"Simülasyon: {secim}", width=500)

else:
    st.info("👈 Lütfen soldaki menüden 'Browse files' diyerek bir resim yükleyin.")