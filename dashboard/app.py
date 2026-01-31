import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
# LOAD DATA (GOOGLE DRIVE)
# =========================
DATA_URL = "https://drive.google.com/uc?export=download&id=1VzRz-g9qG1hKMiSoj9-MqExUoWjOqlFr"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(DATA_URL)
    st.success("✅ Data berhasil dimuat dari Google Drive")
except Exception as e:
    st.error("❌ Gagal memuat data dari Google Drive")
    st.exception(e)
    st.stop()

# =========================
# PREPROCESSING
# =========================
required_cols = ["station", "PM2.5", "year", "month", "day", "hour"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Kolom wajib tidak lengkap: {missing}")
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
selected_stations = st.sidebar.multiselect(
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
    (df["station"].isin(selected_stations)) &
    (df["year"].between(year_range[0], year_range[1]))
]

if filtered_df.empty:
    st.warning("⚠️ Data kosong setelah filter.")
    st.stop()

# =========================
# BUSINESS QUESTIONS (HARUS SAMA DENGAN NOTEBOOK)
# =========================
st.header("📌 Pertanyaan Analisis")

st.markdown("""
1. **Bagaimana distribusi tingkat paparan PM2.5 di setiap stasiun pemantauan selama periode 2013–2017?**  
2. **Stasiun mana yang paling sering mengalami kondisi kualitas udara tidak sehat berdasarkan kategori PM2.5 selama periode 2013–2017?**
""")

# =========================
# VISUALISASI 1 - DISTRIBUSI PM2.5 (BOXPLOT)
# =========================
st.subheader("📦 Distribusi Tingkat Paparan PM2.5 per Stasiun (2013–2017)")

fig, ax = plt.subplots(figsize=(12, 5))
sns.boxplot(
    data=filtered_df,
    x="station",
    y="PM2.5",
    ax=ax
)

ax.set_xlabel("Stasiun")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_title("Distribusi Tingkat Paparan PM2.5 di Setiap Stasiun")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# =========================
# VISUALISASI 2 - FREKUENSI PM2.5 TIDAK SEHAT
# =========================
st.subheader("🚨 Frekuensi Kondisi PM2.5 Tidak Sehat per Stasiun (2013–2017)")

UNHEALTHY_THRESHOLD = 55  # ambang PM2.5 tidak sehat

unhealthy_counts = (
    filtered_df[filtered_df["PM2.5"] > UNHEALTHY_THRESHOLD]
    .groupby("station")
    .size()
    .sort_values(ascending=False)
    .reset_index(name="Jumlah Observasi Tidak Sehat")
)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=unhealthy_counts,
    x="Jumlah Observasi Tidak Sehat",
    y="station",
    ax=ax
)

ax.set_xlabel("Jumlah Observasi Tidak Sehat")
ax.set_ylabel("Stasiun")
ax.set_title("Frekuensi Kondisi PM2.5 Tidak Sehat per Stasiun")
plt.tight_layout()
st.pyplot(fig)

# =========================
# INSIGHT
# =========================
st.subheader("🧠 Insight Utama")

most_unhealthy_station = unhealthy_counts.iloc[0]["station"]
most_unhealthy_count = unhealthy_counts.iloc[0]["Jumlah Observasi Tidak Sehat"]

st.markdown(f"""
- Distribusi PM2.5 di setiap stasiun menunjukkan variasi yang cukup besar, menandakan adanya perbedaan tingkat paparan polusi udara antar lokasi pemantauan selama periode 2013–2017.
- **Stasiun `{most_unhealthy_station}`** merupakan stasiun yang **paling sering mengalami kondisi kualitas udara tidak sehat**, dengan total **{most_unhealthy_count} observasi PM2.5 di atas ambang batas tidak sehat**.
""")

# =========================
# FOOTER
# =========================
st.caption("© 2026 — Dashboard Analisis Data | Streamlit")
