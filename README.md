📊 Dashboard Analisis Kualitas Udara PM2.5

Proyek ini merupakan analisis dan visualisasi data kualitas udara PM2.5 periode 2013–2017 menggunakan Python dan Streamlit.
Dashboard dibuat untuk menampilkan hasil Exploratory Data Analysis (EDA) secara interaktif.

📁 Struktur Folder
.
├── data/
│   └── air_quality_cleaned.csv
├── dashboard/
│   └── proyek_analisis_data.py
├── Proyek_Analisis_Data.ipynb
├── requirements.txt
└── README.md

❓ Pertanyaan Bisnis

Bagaimana tren konsentrasi PM2.5 selama periode 2013–2017?

Bagaimana perbandingan tingkat PM2.5 antar stasiun pengukuran?

Bagaimana perbedaan konsentrasi PM2.5 antara hari kerja dan akhir pekan?

⚠️ Catatan: Pertanyaan ini konsisten dengan visualisasi pada notebook dan dashboard.

🧪 Tahapan Analisis Data

Data Gathering
Menggabungkan beberapa file CSV dari stasiun pemantauan kualitas udara.

Data Assessing

Mengecek tipe data

Mengidentifikasi missing value dan duplikasi data

Data Cleaning

Imputasi missing value (mean untuk numerik, modus untuk kategorik per stasiun)

Membentuk kolom datetime

Exploratory Data Analysis (EDA)

Analisis tren PM2.5 (harian, bulanan, tahunan)

Perbandingan antar stasiun

Analisis weekday vs weekend

📊 Dashboard Streamlit

Dashboard menampilkan:

Tren PM2.5 bulanan

Perbandingan PM2.5 antar stasiun

Pola PM2.5 berdasarkan hari dalam minggu

Filter interaktif:

Stasiun

Rentang tahun

▶️ Cara Menjalankan Dashboard (End-to-End)
1️⃣ Clone Repository
git clone https://github.com/USERNAME_KAMU/Proyek-Analisis-Data.git
cd Proyek-Analisis-Data

2️⃣ Install Dependency

Disarankan menggunakan virtual environment.

pip install -r requirements.txt

3️⃣ Jalankan Dashboard
streamlit run dashboard/proyek_analisis_data.py


Dashboard akan otomatis terbuka di browser.

🌐 Akses Dashboard Online

Dashboard juga dapat diakses melalui Streamlit Cloud:

🔗 [Link Dashboard Streamlit]
(isi dengan link punyamu)

👤 Author

Nama: Mochammad Wahyu Ramadhan
Email: wahyuramadhan9090@gmail.com

ID Dicoding: wahyuramadhan
