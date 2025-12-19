# 🎨 PixelVision Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)

PixelVision Analyzer, görüntü işleme algoritmalarını kullanarak resimler üzerinde analiz, dönüşüm ve erişilebilirlik testleri yapan interaktif bir web uygulamasıdır. 

Bu proje **Görüntü İşleme (Image Processing)** dersi kapsamında geliştirilmiştir.

## 🚀 Özellikler

Uygulama 3 ana modülden oluşmaktadır:

### 1. Renk Analizi (K-Means Clustering)
* Yüklenen resimdeki binlerce rengi **K-Means Kümeleme Algoritması** (Unsupervised Learning) ile analiz eder.
* Resmin en baskın renk paletini (Hex kodları ile) çıkarır.
* Tasarımcılar için renk uyumu analizi sağlar.

### 2. Şablon Çıkarma (Boyama Kitabı Modu)
* **Canny Edge Detection** algoritması ile resmin kenarlarını tespit eder.
* **Morfolojik Genişletme (Dilation)** ile çizgileri belirginleştirir ve kopuklukları birleştirir.
* Sonuç olarak yazıcıdan çıktı almaya uygun, siyah-beyaz bir boyama şablonu üretir.

### 3. Renk Körlüğü Simülasyonu (Erişilebilirlik)
* **LMS Renk Uzayı** matrislerini kullanarak, görüntülerin renk körü bireyler tarafından nasıl algılandığını simüle eder.
* Desteklenen Simülasyonlar:
    * **Protanopia** (Kırmızı Körlüğü)
    * **Deuteranopia** (Yeşil Körlüğü)
    * **Tritanopia** (Mavi Körlüğü)

## 🛠️ Kurulum

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/eylemonderci/PixelVision-Analyzer.git](https://github.com/KULLANICI_ADINIZ/PixelVision-Analyzer.git)
    cd PixelVision-Analyzer
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install opencv-python numpy streamlit
    ```

3.  **Uygulamayı Başlatın:**
    ```bash
    python -m streamlit run app.py
    ```

## 📂 Proje Yapısı

* `app.py`: Streamlit arayüz kodları (Frontend). Kullanıcı etkileşimi ve görselleştirme burada yapılır.
* `pixel_logic.py`: Görüntü işleme algoritmalarının bulunduğu çekirdek dosya (Backend).
* `README.md`: Proje dokümantasyonu.

## 🧠 Kullanılan Teknolojiler ve Algoritmalar

* **Dil:** Python
* **Arayüz:** Streamlit
* **Görüntü İşleme:** OpenCV (cv2)
* **Matematiksel İşlemler:** NumPy
* **Algoritmalar:**
    * K-Means Clustering
    * Canny Edge Detection
    * Gaussian Blur
    * Morphological Dilation
    * LMS Color Space Transformation (Linear Algebra)

---
**Geliştirici:** Eylem  
**Tarih:** 2025
