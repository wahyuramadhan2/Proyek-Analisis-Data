# 📊 Dashboard Analisis Kualitas Udara PM2.5

Proyek ini merupakan analisis data kualitas udara dengan fokus pada konsentrasi **PM2.5** di beberapa stasiun pemantauan selama periode **2013–2017**. Analisis dilakukan untuk memahami dinamika historis PM2.5 serta membandingkan tingkat paparan antar stasiun pengukuran.

Hasil analisis disajikan dalam bentuk **dashboard interaktif** menggunakan **Streamlit** agar memudahkan eksplorasi data secara visual.

---

## 🎯 Tujuan Proyek
Proyek ini bertujuan untuk menjawab dua pertanyaan analisis utama:
1. Bagaimana dinamika konsentrasi PM2.5 selama periode 2013–2017 berdasarkan data historis?
2. Stasiun mana yang memiliki tingkat paparan PM2.5 tertinggi selama periode pengamatan 2013–2017?

---

## 📂 Sumber Data
Dataset yang digunakan merupakan data kualitas udara dengan resolusi waktu per jam yang mencakup informasi:
- Konsentrasi PM2.5  
- Stasiun pemantauan  
- Tahun, bulan, hari, dan jam pengamatan  

Data telah diproses terlebih dahulu untuk membentuk satu dataset utama dan disimpan dalam format CSV di Google Drive, kemudian digunakan langsung oleh dashboard.

---

## 🛠️ Tools & Library
- Python  
- Pandas  
- Matplotlib  
- Seaborn  
- Streamlit  

---

## 📊 Fitur Dashboard
Dashboard interaktif menampilkan:
- Tren rata-rata tahunan konsentrasi PM2.5 pada setiap stasiun
- Perbandingan rata-rata PM2.5 antar stasiun
- Filter interaktif berdasarkan stasiun dan rentang tahun

---

## 🧠 Insight Utama
Analisis menunjukkan bahwa konsentrasi PM2.5 selama periode 2013–2017 memiliki pola fluktuatif tahunan yang relatif konsisten di seluruh stasiun pemantauan. Meskipun demikian, terdapat perbedaan tingkat paparan yang cukup jelas antar stasiun, di mana beberapa stasiun secara konsisten mencatat rata-rata PM2.5 yang lebih tinggi dibandingkan stasiun lainnya. Hal ini mengindikasikan bahwa faktor lokasi dan karakteristik lingkungan sekitar stasiun berperan dalam tingkat pencemaran udara.

---

## 🚀 Cara Menjalankan Dashboard
1. Pastikan file Python dashboard tersedia (misalnya `app.py`).
2. Pastikan dataset dapat diakses melalui Google Drive dengan pengaturan *Anyone with the link – Viewer*.
3. Jalankan dashboard dengan perintah:
   ```bash
   streamlit run app.py
