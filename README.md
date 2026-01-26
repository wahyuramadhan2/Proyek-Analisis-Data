# 📊 Dashboard Analisis Kualitas Udara PM2.5

Proyek ini berisi analisis dan visualisasi data kualitas udara **PM2.5 periode 2013–2017** menggunakan **Python** dan **Streamlit**. Dashboard dibuat untuk menampilkan hasil **Exploratory Data Analysis (EDA)** secara interaktif.

---

## 📁 Struktur Folder

```bash
.
├── data/
│   └── air_quality_cleaned.csv
├── dashboard/
│   └── proyek_analisis_data.py
├── Proyek_Analisis_Data.ipynb
├── requirements.txt
└── README.md
```

---

## ❓ Pertanyaan Bisnis

1. Bagaimana tren konsentrasi PM2.5 selama periode 2013–2017?
2. Bagaimana perbandingan tingkat PM2.5 antar stasiun pengukuran?
3. Bagaimana perbedaan konsentrasi PM2.5 antara hari kerja dan akhir pekan?

> Pertanyaan ini konsisten dengan visualisasi pada notebook dan dashboard.

---

## 🧪 Tahapan Analisis Data

* **Data Gathering**: Menggabungkan data dari beberapa stasiun pemantauan kualitas udara.
* **Data Assessing**: Mengecek tipe data, missing value, dan duplikasi data.
* **Data Cleaning**:

  * Imputasi missing value (mean untuk numerik, modus untuk kategorik per stasiun)
  * Membentuk kolom `datetime`
* **Exploratory Data Analysis (EDA)**:

  * Analisis tren PM2.5 (harian, bulanan, tahunan)
  * Perbandingan antar stasiun
  * Analisis weekday vs weekend

---

## 📊 Dashboard Streamlit

Dashboard menampilkan:

* Tren PM2.5 bulanan
* Perbandingan PM2.5 antar stasiun
* Pola PM2.5 berdasarkan hari dalam minggu
* Filter interaktif (stasiun & rentang tahun)

---

## ▶️ Cara Menjalankan Dashboard

1. Install dependency:

```bash
pip install -r requirements.txt
```

2. Jalankan dashboard:

```bash
streamlit run dashboard/proyek_analisis_data.py
```

Dashboard akan otomatis terbuka di browser.

---

## 👤 Author

* **Nama:** Mochammad Wahyu Ramadhan
* **Email:** [wahyuramadhan9090@gmail.com](mailto:wahyuramadhan9090@gmail.com)
* **ID Dicoding:** wahyuramadhan
