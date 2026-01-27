import streamlit as st

# ===============================
# CONFIG
# ===============================
st.set_page_config(
    page_title="Dashboard Kualitas Udara",
    layout="wide"
)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import os
import numpy as np
import re

# ===============================
# TITLE
# ===============================
st.title("📊 Dashboard Analisis Kualitas Udara")
st.caption("Visualisasi hasil Exploratory Data Analysis (EDA)")

# ===============================
# GOOGLE DRIVE HELPERS
# ===============================
def gdrive_to_direct(url: str) -> str:
    """
    Convert Google Drive share link or file-id to a direct download URL.
    Supports:
    - https://drive.google.com/file/d/<id>/view?...
    - https://drive.google.com/open?id=<id>
    - https://drive.google.com/uc?id=<id>&export=download
    - raw file id
    """
    if not url:
        return ""

    url = url.strip()

    patterns = [
        r"drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)",
        r"drive\.google\.com\/open\?id=([a-zA-Z0-9_-]+)",
        r"drive\.google\.com\/uc\?id=([a-zA-Z0-9_-]+)",
        r"id=([a-zA-Z0-9_-]+)"
    ]
    file_id = None
    for p in patterns:
        m = re.search(p, url)
        if m:
            file_id = m.group(1)
            break

    # If user pasted only the file-id
    if file_id is None and re.fullmatch(r"[a-zA-Z0-9_-]{10,}", url):
        file_id = url

    if not file_id:
        return ""

    return f"https://drive.google.com/uc?export=download&id={file_id}"


# ===============================
# LOAD DATA
# ===============================
with st.sidebar:
    st.header("⚙️ Pengaturan Data")

    uploaded_file = st.file_uploader(
        "Upload dataset kualitas udara (CSV)",
        type=["csv"]
    )

    st.markdown("---")
    st.subheader("☁️ Muat dari Google Drive")

    # Default link dari kamu
    default_drive_link = "https://drive.google.com/file/d/1u4I0OvFlXKCKgwQcq0AGr7S_xZxJ6Tqd/view?usp=drive_link"
    drive_url = st.text_input(
        "Paste link Google Drive (share link / file id)",
        value=default_drive_link
    )

    use_drive = st.checkbox("Gunakan Google Drive (jika tidak upload)", value=True)

    st.markdown("---")
    st.caption("Tips: Pastikan file Drive sudah 'Anyone with the link' (Viewer).")


@st.cache_data
def load_data(file=None, path=None, url=None):
    if file is not None:
        file.seek(0)
        return pd.read_csv(file)
    elif url is not None:
        return pd.read_csv(url)
    elif path is not None:
        return pd.read_csv(path)
    else:
        raise ValueError("Tidak ada sumber data yang diberikan")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(BASE_DIR, "air_quality_cleaned.csv")

# Prioritas: Upload -> Google Drive -> Default lokal
data_source_note = ""

if uploaded_file is not None:
    air_quality_df = load_data(file=uploaded_file)
    data_source_note = "✅ Data berhasil dimuat dari file upload!"
elif use_drive and drive_url.strip():
    direct_url = gdrive_to_direct(drive_url.strip())
    if not direct_url:
        st.error("Link Google Drive tidak valid. Pastikan paste share link atau file id.")
        st.stop()
    try:
        air_quality_df = load_data(url=direct_url)
        data_source_note = "☁️ Data berhasil dimuat dari Google Drive!"
    except Exception as e:
        st.error("Gagal memuat CSV dari Google Drive. Pastikan aksesnya 'Anyone with the link'.")
        st.exception(e)
        st.stop()
elif os.path.exists(DEFAULT_PATH):
    air_quality_df = load_data(path=DEFAULT_PATH)
    data_source_note = "ℹ️ Data dimuat dari file default lokal."
else:
    st.error("Dataset default tidak ditemukan dan tidak ada file yang diupload / link Drive belum diisi.")
    st.stop()

st.info(data_source_note)

# ===============================
# FIX DATETIME
# ===============================
# pastikan kolom datetime ada
if "datetime" not in air_quality_df.columns:
    st.error("Kolom 'datetime' tidak ditemukan di dataset. Pastikan nama kolomnya benar.")
    st.write("Kolom yang tersedia:", list(air_quality_df.columns))
    st.stop()

air_quality_df['datetime'] = pd.to_datetime(air_quality_df['datetime'], errors="coerce")
air_quality_df = air_quality_df.dropna(subset=["datetime"])

# pastikan kolom year ada (kalau tidak, bikin dari datetime)
if "year" not in air_quality_df.columns:
    air_quality_df["year"] = air_quality_df["datetime"].dt.year

# pastikan kolom station dan PM2.5 ada
required_cols = ["station", "PM2.5", "year"]
missing = [c for c in required_cols if c not in air_quality_df.columns]
if missing:
    st.error(f"Kolom wajib tidak ditemukan: {missing}")
    st.write("Kolom yang tersedia:", list(air_quality_df.columns))
    st.stop()

# ===============================
# FILTER
# ===============================
with st.sidebar:
    station_filter = st.multiselect(
        "Pilih Stasiun",
        options=sorted(air_quality_df["station"].dropna().unique().tolist()),
        default=sorted(air_quality_df["station"].dropna().unique().tolist())
    )

    year_min = int(air_quality_df["year"].min())
    year_max = int(air_quality_df["year"].max())

    year_range = st.slider(
        "Rentang Tahun",
        year_min,
        year_max,
        (year_min, year_max)
    )

filtered_df = air_quality_df[
    (air_quality_df["station"].isin(station_filter)) &
    (air_quality_df["year"] >= year_range[0]) &
    (air_quality_df["year"] <= year_range[1])
].copy()

if filtered_df.empty:
    st.warning("Filter menghasilkan data kosong. Coba perluas pilihan stasiun atau rentang tahun.")
    st.stop()

# ===============================
# BUSINESS QUESTIONS
# ===============================
st.header("📌 Pertanyaan Bisnis")

st.markdown("""
1. Bagaimana dinamika konsentrasi PM2.5 selama periode 2013–2017 di seluruh stasiun pemantauan?  
2. Stasiun mana yang cenderung memiliki rata-rata PM2.5 tertinggi dan terendah selama 2013–2017?
3. Bagaimana perbedaan pola konsentrasi PM2.5 antara hari kerja dan akhir pekan serta bagaimana variasi pola hariannya dari Senin hingga Minggu selama periode 2013–2017?
""")

# ===============================
# MONTHLY PM2.5
# ===============================
monthly_pm25 = (
    filtered_df
    .set_index('datetime')
    .groupby('station')['PM2.5']
    .resample('M')
    .mean()
    .reset_index()
)

st.subheader("📈 Tren Bulanan PM2.5")
fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(
    data=monthly_pm25,
    x='datetime',
    y='PM2.5',
    hue='station',
    ax=ax
)

ax.set_title("Tren Bulanan PM2.5")
ax.set_xlabel("Waktu")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# ===============================
# ANNUAL COMPARISON
# ===============================
st.subheader("🏭 Perbandingan Rata-rata PM2.5 Antar Stasiun")

annual_pm25 = (
    filtered_df
    .groupby(['station', 'year'])['PM2.5']
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(
    data=annual_pm25,
    x='year',
    y='PM2.5',
    hue='station',
    marker='o',
    ax=ax
)

ax.set_title("Rata-rata Tahunan PM2.5 per Stasiun")
ax.set_xlabel("Tahun")
ax.set_ylabel("PM2.5 (µg/m³)")
plt.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig)

# ===============================
# WEEKDAY vs WEEKEND
# ===============================
st.subheader("📅 Weekday vs Weekend")

filtered_df['day_of_week'] = filtered_df['datetime'].dt.dayofweek
filtered_df['day_type'] = filtered_df['day_of_week'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')

station_day_avg = (
    filtered_df
    .groupby(['station', 'day_type'])['PM2.5']
    .mean()
    .unstack()
)

# Pastikan kolom Weekday/Weekend ada (kalau ada stasiun yg datanya cuma weekday/weekend)
for col in ["Weekday", "Weekend"]:
    if col not in station_day_avg.columns:
        station_day_avg[col] = np.nan

fig, ax = plt.subplots(figsize=(12, 5))

x = np.arange(len(station_day_avg.index))
width = 0.35

ax.bar(x - width/2, station_day_avg['Weekday'], width, label='Weekday')
ax.bar(x + width/2, station_day_avg['Weekend'], width, label='Weekend')

ax.set_xticks(x)
ax.set_xticklabels(station_day_avg.index, rotation=45)
ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_title("Rata-rata PM2.5: Weekday vs Weekend")
ax.legend()

plt.tight_layout()
st.pyplot(fig)

# ===============================
# 📆 POLA HARIAN PM2.5 (SENIN–MINGGU)
# ===============================
st.subheader("🗓️ Pola Harian PM2.5 (Senin–Minggu)")

day_map = {
    0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
    3: 'Thursday', 4: 'Friday',
    5: 'Saturday', 6: 'Sunday'
}
filtered_df['day_name'] = filtered_df['day_of_week'].map(day_map)

day_order = [
    'Monday', 'Tuesday', 'Wednesday',
    'Thursday', 'Friday', 'Saturday', 'Sunday'
]

fig, ax = plt.subplots(figsize=(12, 5))

for station in filtered_df['station'].unique():
    station_df = filtered_df[filtered_df['station'] == station]
    daily_avg = (
        station_df
        .groupby('day_name')['PM2.5']
        .mean()
        .reindex(day_order)
    )
    ax.plot(day_order, daily_avg, marker='o', label=station)

ax.set_title("Pola Harian PM2.5 di Seluruh Stasiun")
ax.set_xlabel("Hari")
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
ax.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# ===============================
# ANALISIS LANJUTAN
# ===============================
st.header("📌 Analisis Lanjutan")

st.markdown("""
Tujuan analisis lanjutan ini adalah untuk mengidentifikasi dan mengevaluasi perubahan distribusi durasi jam kategori kualitas udara (Baik, Sedang, Tidak Sehat, dan Sangat Tidak Sehat) berdasarkan konsentrasi PM2.5 pada data kualitas udara per jam selama periode 2013–2017 melalui teknik manual grouping.
""")

# ===============================
# 🌫️ TREN BULANAN KATEGORI KUALITAS UDARA PM2.5
# ===============================
st.subheader("🌫️ Tren Bulanan Kategori Kualitas Udara PM2.5")

bins = [0, 50, 100, 150, float('inf')]
labels = ['Baik', 'Sedang', 'Tidak Sehat', 'Sangat Tidak Sehat']

filtered_df['air_quality_category'] = pd.cut(
    filtered_df['PM2.5'],
    bins=bins,
    labels=labels
)

filtered_df['year_month'] = filtered_df['datetime'].dt.to_period('M')

air_quality_month = (
    filtered_df
    .groupby(['year_month', 'air_quality_category'])
    .size()
    .reset_index(name='hour_count')
)

air_quality_month['datetime'] = air_quality_month['year_month'].dt.to_timestamp()

air_quality_month_pivot = air_quality_month.pivot(
    index='datetime',
    columns='air_quality_category',
    values='hour_count'
)

fig, ax = plt.subplots(figsize=(12, 6))

for category in air_quality_month_pivot.columns:
    ax.plot(
        air_quality_month_pivot.index,
        air_quality_month_pivot[category],
        marker='o',
        label=category
    )

ax.set_title("Tren Bulanan Durasi Jam Kategori PM2.5")
ax.set_xlabel("Waktu")
ax.set_ylabel("Jumlah Jam")
ax.legend(title="Kategori Kualitas Udara")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# ===============================
# FOOTER
# ===============================
st.caption("2026 - Dashboard Analisis Data - Streamlit")
