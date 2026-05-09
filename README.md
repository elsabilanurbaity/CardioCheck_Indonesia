# ❤️ CardioCheck Indonesia
### Sistem Prediksi Risiko Penyakit Jantung berbasis Machine Learning

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/ScikitLearn-1.5-orange?style=flat-square&logo=scikit-learn)
![Dataset](https://img.shields.io/badge/Dataset-158.355%20pasien-green?style=flat-square)

---

## 📋 Tentang Proyek

CardioCheck Indonesia adalah sistem berbasis web yang membantu masyarakat umum untuk mendeteksi dini risiko penyakit jantung. Sistem ini menggunakan model Machine Learning (Random Forest) yang dilatih dengan **158.355 data pasien Indonesia**.

### Fitur Utama
- ✅ **Prediksi Risiko** — Ya/Tidak risiko penyakit jantung dengan probabilitas
- 📊 **Analisis Parameter Klinis** — Interpretasi tekanan darah, kolesterol, gula darah, dll
- 🍽️ **Rekomendasi Makanan** — Personal sesuai kondisi kesehatan
- 🎨 **UI Modern** — Desain glass-morphism yang elegan

---

## 📁 Struktur File

```
heart-attack-prediction/
├── app.py                          # Aplikasi Streamlit utama
├── model.pkl                       # Model Random Forest terlatih
├── encoders.json                   # Mapping encoding kategorikal
├── train_model.ipynb               # Google Colab notebook training
├── heart_attack_prediction_indonesia.csv  # Dataset
├── requirements.txt                # Dependencies Python
├── .streamlit/
│   └── config.toml                 # Konfigurasi Streamlit
└── README.md                       # Dokumentasi ini
```

---

## 🚀 Cara Deploy ke Streamlit Cloud

### 1. Upload ke GitHub
```bash
git init
git add .
git commit -m "Initial commit: CardioCheck Indonesia"
git branch -M main
git remote add origin https://github.com/USERNAME/cardiocheck-indonesia.git
git push -u origin main
```

### 2. Deploy di Streamlit Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan akun GitHub
3. Klik **"New app"**
4. Pilih repository ini
5. Set **Main file path**: `app.py`
6. Klik **"Deploy!"**

### 3. Jalankan Lokal (Opsional)
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧠 Model Machine Learning

| Parameter | Nilai |
|-----------|-------|
| Algoritma | Random Forest Classifier |
| Dataset | 158.355 pasien Indonesia |
| Fitur Input | 23 variabel |
| Target | Serangan Jantung (Ya/Tidak) |
| Akurasi | ~73% |
| Train/Test Split | 80% / 20% |

### Fitur Terpenting (Feature Importance)
1. Tingkat Kolesterol (8.18%)
2. Riwayat Penyakit Jantung (7.52%)
3. Usia (7.21%)
4. Gula Darah Puasa (7.03%)
5. Hipertensi (7.03%)

---

## 📊 Interpretasi Parameter

### Tekanan Darah
| Kategori | Sistolik | Diastolik |
|----------|----------|-----------|
| Normal | < 120 | < 80 |
| Elevasi | 120–129 | < 80 |
| Hipertensi Std 1 | 130–139 | 80–89 |
| Hipertensi Std 2 | ≥ 140 | ≥ 90 |
| Krisis | > 180 | > 120 |

### Gula Darah Puasa
| Kategori | Nilai (mg/dL) |
|----------|---------------|
| Normal | 70–99 |
| Prediabetes | 100–125 |
| Diabetes | ≥ 126 |

### Kolesterol LDL
| Kategori | Nilai (mg/dL) |
|----------|---------------|
| Optimal | < 100 |
| Hampir Optimal | 100–129 |
| Batas Tinggi | 130–159 |
| Tinggi | 160–189 |
| Sangat Tinggi | ≥ 190 |

---

## ⚠️ Disclaimer

> Sistem ini bersifat **informatif** dan **tidak menggantikan diagnosis medis profesional**.
> Selalu konsultasikan hasil dengan dokter atau tenaga kesehatan yang berkualifikasi.

---

## 📖 Training Notebook

Lihat file `train_model.ipynb` untuk Google Colab notebook lengkap berisi:
- Eksplorasi data (EDA)
- Preprocessing & encoding
- Training model
- Evaluasi & visualisasi
- Export model

---

*Dibuat untuk keperluan edukasi dan deteksi dini penyakit jantung di Indonesia* 🇮🇩
