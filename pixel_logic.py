import cv2
import numpy as np

# --- 1. RENK BULMA KISMI ---
def renkleri_bul(resim, renk_sayisi=5):
    # Resmi düzleştiriyoruz (Tek sıra haline getiriyoruz)
    # Çünkü K-Means piksellerin nerede olduğuyla ilgilenmez, sadece rengiyle ilgilenir.
    pikseller = resim.reshape((-1, 3))
    pikseller = np.float32(pikseller)
    
    # K-Means Algoritması ayarları (Burası standart koddur)
    # Algoritma 100 kere deneme yapsın veya hata 0.2'nin altına düşünce dursun.
    kriterler = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    
    # K-Means'i çalıştırıyoruz
    _, labels, merkezler = cv2.kmeans(pikseller, renk_sayisi, None, kriterler, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Bulunan merkez renkleri tam sayıya çeviriyoruz (Örn: 255.4 -> 255)
    baskin_renkler = np.uint8(merkezler)
    
    return baskin_renkler

# --- 2. ÇİZİM ŞABLONU ÇIKARMA KISMI ---
def sablon_cikar(resim, kare_boyutu=20):
    yukseklik, genislik, _ = resim.shape
    
    # Izgara (Grid) çizmek için resmin kopyasını alıyoruz
    izgarali_resim = resim.copy()
    
    # Dikey çizgiler çekiyoruz (Gri renkte: 200, 200, 200)
    # range fonksiyonu 0'dan başlayıp genişliğe kadar 'kare_boyutu' kadar atlayarak gider
    for x in range(0, genislik, kare_boyutu):
        cv2.line(izgarali_resim, (x, 0), (x, yukseklik), (200, 200, 200), 1)
        
    # Yatay çizgiler çekiyoruz
    for y in range(0, yukseklik, kare_boyutu):
        cv2.line(izgarali_resim, (0, y), (genislik, y), (200, 200, 200), 1)

    # --- KENAR BULMA (CANNY) ---
    # Önce resmi biraz bulanıklaştırıyorum ki gereksiz detaylar (gürültü) gitsin
    bulanik = cv2.GaussianBlur(resim, (5, 5), 0)
    
    # Canny algoritması ile kenarları buluyoruz
    # 50 ve 150 eşik değerleridir.
    kenarlar = cv2.Canny(bulanik, 50, 150)
    
    # Çizgiler bazen kopuk oluyor, onları birleştirmek için "Dilation" (Genişletme) yapıyoruz
    kernel = np.ones((2,2), np.uint8) # 2x2'lik bir kutu
    kalin_kenarlar = cv2.dilate(kenarlar, kernel, iterations=1)
    
    # Şu an elimizde Siyah zemin üzerine Beyaz çizgiler var.
    # Ama biz kağıt çıktısı alacağız, o yüzden tam tersini yapıyoruz (Beyaz kağıt, Siyah kalem)
    ters_kenarlar = 255 - kalin_kenarlar
    
    return izgarali_resim, ters_kenarlar

# --- 3. RENK KÖRLÜĞÜ SİMÜLASYONU KISMI ---
def renk_koru_yap(resim, tur='protanopia'):
    # İşlem yapabilmek için resmi 0-1 arasına sıkıştırıyoruz (Float yapıyoruz)
    simule_resim = resim.copy().astype(np.float32) / 255.0
    
    # Matris değerleri (Bilimsel LMS renk uzayı değerleri)
    if tur == 'protanopia':
        # Kırmızı rengi göremezler
        matris = np.array([[0.567, 0.433, 0.000], 
                           [0.558, 0.442, 0.000], 
                           [0.000, 0.242, 0.758]])
                           
    elif tur == 'deuteranopia':
        # Yeşil rengi göremezler
        matris = np.array([[0.625, 0.375, 0.000], 
                           [0.700, 0.300, 0.000], 
                           [0.000, 0.300, 0.700]])
                           
    elif tur == 'tritanopia':
        # Mavi rengi göremezler (Nadir görülür)
        matris = np.array([[0.95, 0.05, 0.00], 
                           [0.00, 0.433, 0.567], 
                           [0.00, 0.475, 0.525]])
    else:
        return resim

    # Resmin her pikselini bu matrisle çarpıyoruz (Lineer Cebir işlemi)
    simule_resim = cv2.transform(simule_resim, matris)
    
    # Resmi tekrar 0-255 arasına çekiyoruz
    simule_resim = np.clip(simule_resim, 0, 1.0) * 255
    
    return np.uint8(simule_resim)