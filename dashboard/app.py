# ===============================
# IMPORT LIBRARIES
# ===============================
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import re

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Dashboard Kualitas Udara",
    layout="wide"
)

# ===============================
# TITLE
# ===============================
st.title("📊 Dashboard Analisis Kualitas Udara")
st.caption("Visualisasi hasil Exploratory Data Analysis (EDA) PM2.5")

# ===============================
# GOOGLE DRIVE HELPER
# ===============================
def gdrive_to_direct(url: str) -> str:
    """
    Convert Google Drive link or file-id to direct CSV download URL
    """
    patterns = [
        r"drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)",
        r"id=([a-zA-Z0-9_-]+)"
    ]

    file_id = None
    for p in patterns:
        m = re.search(p, url)
        if m:
            file_id = m.group(1)
            break

    if not file_id:
        return None

    return f"https://drive.google.com/uc?export=download&id={file_id}"

# ===============================
# LOAD DATA FROM GOOGLE DRIVE
# ===============================
DRIVE_LINK = "https://drive.google.com/file/d/1jtCEpbC0Vy-z8mxtse0FBRQH3Gcxg8vt/"

@st.cache_data
def load_data_from_drive(link):
    direct_url = gdrive_to_direct(link)
    if direct_url is None:
        raise ValueError("Link Google Drive tidak valid")
    return pd.read_csv(direct_url)

try:
    air_quality_df = load_data_from_drive(DRIVE_LINK)
    st.success("✅ Data berhasil dimuat dari Google Drive")
except Exception as e:
    st.error("❌ Gagal memuat data dari Google Drive")
    st.exception(e)
    st.stop()

# ===============================
# PREPROCESSING DASAR
# ===============================
required_cols = ["datetime", "station", "PM2.5"]
missing_cols = [c for c in required_cols if c not in air_quality_df.columns]

if missing_cols:
    st.error(f"Kolom wajib tidak ditemukan: {missing_cols}")
    st.write("Kolom tersedia:", air_quality_df.columns.tolist())
    st.stop()

air_quality_df["datetime"] = pd.to_datetime(
    air_quality_df["datetime"], errors="coerce"
)
air_quality_df = air_quality_df.dropna(subset=["datetime"])
air_quality_df["year"] = air_quality_df["datetime"].dt.year

# ===============================
# SIDEBAR FILTER
# ===============================
with st.sidebar:
    st.header("⚙️ Filter Data")

    stations = sorted(air_quality_df["station"].unique())
    selected_stations = st.multiselect(
        "Pilih Stasiun",
        stations,
        default=stations
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
    (air_quality_df["station"].isin(selected_stations)) &
    (air_quality_df["year"] >= year_range[0]) &
    (air_quality_df["year"] <= year_range[1])
]

if filtered_df.empty:
    st.warning("Data kosong setelah filter.")
    st.stop()

# ===============================
# BUSINESS QUESTIONS
# ===============================
st.header("📌 Pertanyaan Analisis")

st.markdown("""
1. **Bagaimana dinamika konsentrasi PM2.5 sepanjang tahun 2013–2017 berdasarkan data historis?**  
2. **Bagaimana variasi konsentrasi PM2.5 antar stasiun pemantauan selama periode 2013–2017?**
""")

# ===============================
# Q1 – TREN BULANAN PM2.5
# ===============================
monthly_pm25 = (
    filtered_df
    .set_index("datetime")
    .groupby("station")["PM2.5"]
    .resample("M")
    .mean()
    .reset_index()
)

st.subheader("📈 Tren Bulanan PM2.5")

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(
    data=monthly_pm25,
    x="datetime",
    y="PM2.5",
    hue="station",
    linewidth=1.2,
    ax=ax
)

ax.set_title("Tren Bulanan Konsentrasi PM2.5 (2013–2017)")
ax.set_xlabel("Waktu")
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.xticks(rotation=45)
ax.legend(title="Stasiun", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
st.pyplot(fig)

# ===============================
# Q2 – PERBANDINGAN TAHUNAN ANTAR STASIUN
# ===============================
annual_pm25 = (
    filtered_df
    .set_index("datetime")
    .groupby("station")["PM2.5"]
    .resample("Y")
    .mean()
    .reset_index()
)

st.subheader("🏭 Perbandingan PM2.5 Tahunan Antar Stasiun")

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(
    data=annual_pm25,
    x="datetime",
    y="PM2.5",
    hue="station",
    marker="o",
    linewidth=1.5,
    ax=ax
)

ax.set_title("Perbandingan Konsentrasi PM2.5 Tahunan (2013–2017)")
ax.set_xlabel("Tahun")
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.legend(title="Stasiun", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
st.pyplot(fig)

# ===============================
# FOOTER
# ===============================
st.caption("© 2026 – Dashboard Analisis Kualitas Udara (Streamlit)")
