# Dashboard Analisis Kualitas Udara PM2.5

Proyek ini berisi analisis dan visualisasi data kualitas udara PM2.5
periode 2013–2017 menggunakan Python dan Streamlit.

---

## 📊 Tujuan Proyek
Tujuan dari proyek ini adalah:
1. Menganalisis tren konsentrasi PM2.5 pada periode 2013–2017
2. Membandingkan konsentrasi PM2.5 antar stasiun pengukuran
3. Mengidentifikasi pola harian serta perbedaan weekday dan weekend

---

## 📁 Struktur Folder
.
├── data/
│ └── air_quality_cleaned.csv
├── dashboard/
│ └── proyek_analisis_data.py
├── Proyek_Analisis_Data.ipynb
├── requirements.txt
└── README.md

---

## ⚙️ Cara Menjalankan Dashboard (End-to-End)

### 1. Clone Repository
```bash
git clone https://github.com/USERNAME_KAMU/Proyek-Analisis-Data.git
cd Proyek-Analisis-Data

### 2. Install Dependency

Pastikan Python sudah terinstall, lalu jalankan:

pip install -r requirements.txt

### 3. Jalankan Dashboard Streamlit
streamlit run dashboard/proyek_analisis_data.py

### 4. Akses Dashboard

Buka browser dan akses:

http://localhost:8501

