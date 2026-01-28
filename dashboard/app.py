import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Kualitas Udara",
    layout="wide"
)

st.title("📊 Dashboard Kualitas Udara PM2.5")
st.caption("Hasil Analisis Data Kualitas Udara (2013–2017)")

# =========================
# LOAD DATA
# =========================
DATA_PATH = os.path.join(os.path.dirname(__file__), "main_data.csv")

if not os.path.exists(DATA_PATH):
    st.error("File main_data.csv tidak ditemukan.")
    st.stop()

df = pd.read_csv(DATA_PATH)

# =========================
# PREPROCESS
# =========================
df["datetime"] = pd.to_datetime(df["datetime"])
df["year"] = df["datetime"].dt.year

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔎 Filter Data")

station_selected = st.sidebar.multiselect(
    "Pilih Stasiun",
    options=df["station"].unique(),
    default=df["station"].unique()
)

year_range = st.sidebar.slider(
    "Rentang Tahun",
    int(df["year"].min()),
    int(df["year"].max()),
    (2013, 2017)
)

filtered_df = df[
    (df["station"].isin(station_selected)) &
    (df["year"].between(year_range[0], year_range[1]))
]

# =========================
# VISUALISASI 1
# =========================
st.subheader("📈 Tren Rata-rata PM2.5 per Tahun")

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
ax.set_title("Tren Tahunan PM2.5")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# =========================
# VISUALISASI 2
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
