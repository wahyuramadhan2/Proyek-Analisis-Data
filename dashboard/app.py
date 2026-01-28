import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Kualitas Udara PM2.5",
    layout="wide"
)

st.title("📊 Dashboard Kualitas Udara PM2.5")
st.caption("Analisis Data Kualitas Udara Periode 2013–2017")

# =========================
# GOOGLE DRIVE HELPER
# =========================
def gdrive_to_direct(url):
    """
    Convert Google Drive share link to direct download link
    """
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if not match:
        return None
    file_id = match.group(1)
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# =========================
# SIDEBAR - DATA SOURCE
# =========================
st.sidebar.header("📂 Sumber Data")

DEFAULT_DRIVE_LINK = "https://drive.google.com/file/d/1lVLq4IkZk_aFlZxPC7skeJu-kq98IoQY/"

drive_link = st.sidebar.text_input(
    "Link Google Drive (CSV)",
    value=DEFAULT_DRIVE_LINK
)

direct_url = gdrive_to_direct(drive_link)

if not direct_url:
    st.error("❌ Link Google Drive tidak valid.")
    st.stop()

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(direct_url)
    st.sidebar.success("✅ Data berhasil dimuat")
except Exception as e:
    st.error("❌ Gagal memuat data dari Google Drive")
    st.exception(e)
    st.stop()

# =========================
# PREPROCESSING
# =========================
required_cols = ["datetime", "station", "PM2.5"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Kolom wajib `{col}` tidak ditemukan di dataset.")
        st.stop()

# =========================
# FIX DATETIME (PRSA DATASET)
# =========================
required_time_cols = ["year", "month", "day", "hour"]

missing_cols = [c for c in required_time_cols if c not in df.columns]
if missing_cols:
    st.error(f"Kolom waktu tidak lengkap: {missing_cols}")
    st.stop()

df["datetime"] = pd.to_datetime(
    df[["year", "month", "day", "hour"]],
    errors="coerce"
)

df = df.dropna(subset=["datetime"])
df["year"] = df["datetime"].dt.year

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔎 Filter Data")

stations = sorted(df["station"].unique())
station_selected = st.sidebar.multiselect(
    "Pilih Stasiun",
    options=stations,
    default=stations
)

year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider(
    "Rentang Tahun",
    year_min,
    year_max,
    (2013, 2017)
)

filtered_df = df[
    (df["station"].isin(station_selected)) &
    (df["year"].between(year_range[0], year_range[1]))
]

if filtered_df.empty:
    st.warning("⚠️ Data kosong setelah filter.")
    st.stop()

# =========================
# BUSINESS QUESTIONS
# =========================
st.header("📌 Pertanyaan Analisis")

st.markdown("""
1. **Bagaimana dinamika konsentrasi PM2.5 selama periode 2013–2017 berdasarkan data historis?**  
2. **Stasiun mana yang memiliki tingkat paparan PM2.5 tertinggi selama periode pengamatan 2013–2017?**
""")

# =========================
# VISUALISASI 1 - TREN TAHUNAN
# =========================
st.subheader("📈 Tren Rata-rata PM2.5 Tahunan")

annual_pm25 = (
    filtered_df
    .groupby(["year", "station"])["PM2.5"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(
    data=annual_pm25,
    x="year",
    y="PM2.5",
    hue="station",
    marker="o",
    ax=ax
)

ax.set_xlabel("Tahun")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_title("Tren Tahunan Konsentrasi PM2.5")
ax.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
st.pyplot(fig)

# =========================
# VISUALISASI 2 - PER STASIUN
# =========================
st.subheader("🏭 Rata-rata PM2.5 per Stasiun")

station_avg = (
    filtered_df
    .groupby("station")["PM2.5"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=station_avg,
    x="PM2.5",
    y="station",
    ax=ax
)

ax.set_xlabel("Rata-rata PM2.5 (µg/m³)")
ax.set_ylabel("Stasiun")
ax.set_title("Perbandingan Rata-rata PM2.5 Antar Stasiun")
plt.tight_layout()
st.pyplot(fig)

# =========================
# INSIGHT (GABUNG P1 & P2)
# =========================
st.subheader("🧠 Insight Utama")

highest_station = station_avg.iloc[0]["station"]
highest_value = station_avg.iloc[0]["PM2.5"]

lowest_station = station_avg.iloc[-1]["station"]
lowest_value = station_avg.iloc[-1]["PM2.5"]

st.markdown(f"""
- Selama periode **2013–2017**, konsentrasi PM2.5 menunjukkan **pola fluktuatif tahunan** yang relatif konsisten di seluruh stasiun, mengindikasikan adanya pengaruh faktor musiman terhadap kualitas udara.
- **Stasiun `{highest_station}`** tercatat memiliki **rata-rata PM2.5 tertinggi** sebesar **{highest_value:.2f} µg/m³**, sedangkan **stasiun `{lowest_station}`** memiliki tingkat paparan terendah dengan rata-rata **{lowest_value:.2f} µg/m³**.
""")

# =========================
# FOOTER
# =========================
