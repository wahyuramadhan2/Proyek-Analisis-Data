import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(
    page_title="Dashboard PM2.5",
    layout="wide"
)

# ===============================
# LOAD DATA
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/air_quality_cleaned.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df

df = load_data()

# ===============================
# TITLE
# ===============================
st.title("📊 Dashboard Analisis PM2.5")
st.caption("Analisis kualitas udara berdasarkan waktu dan stasiun pemantauan")

# ===============================
# SIDEBAR FILTER
# ===============================
st.sidebar.header("Filter Data")

stations = st.sidebar.multiselect(
    "Pilih Stasiun",
    options=sorted(df["station"].unique()),
    default=sorted(df["station"].unique())
)

year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider(
    "Rentang Tahun",
    year_min,
    year_max,
    (year_min, year_max)
)

filtered_df = df[
    (df["station"].isin(stations)) &
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

# ===============================
# METRIC
# ===============================
col1, col2 = st.columns(2)
col1.metric("Rata-rata PM2.5", f"{filtered_df['PM2.5'].mean():.2f} µg/m³")
col2.metric("Jumlah Observasi", f"{filtered_df.shape[0]:,}")

# ===============================
# MONTHLY TREND
# ===============================
st.subheader("📈 Tren Bulanan PM2.5")

monthly_pm25 = (
    filtered_df
    .set_index("datetime")
    .groupby("station")["PM2.5"]
    .resample("M")
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(
    data=monthly_pm25,
    x="datetime",
    y="PM2.5",
    hue="station",
    ax=ax
)

ax.set_xlabel("Waktu")
ax.set_ylabel("PM2.5 (µg/m³)")
st.pyplot(fig)

# ===============================
# STATION COMPARISON
# ===============================
st.subheader("🏭 Perbandingan PM2.5 Antar Stasiun")

station_avg = (
    filtered_df
    .groupby("station")["PM2.5"]
    .mean()
    .reset_index()
)

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(
    data=station_avg,
    x="station",
    y="PM2.5",
    ax=ax2
)

ax2.set_xlabel("Stasiun")
ax2.set_ylabel("Rata-rata PM2.5 (µg/m³)")
plt.xticks(rotation=45)
st.pyplot(fig2)

# ===============================
# WEEKDAY VS WEEKEND
# ===============================
st.subheader("📅 Weekday vs Weekend")

filtered_df["day_type"] = filtered_df["datetime"].dt.weekday.map(
    lambda x: "Weekday" if x < 5 else "Weekend"
)

daytype_avg = (
    filtered_df
    .groupby("day_type")["PM2.5"]
    .mean()
    .reset_index()
)

fig3, ax3 = plt.subplots(figsize=(6, 4))
sns.barplot(
    data=daytype_avg,
    x="day_type",
    y="PM2.5",
    ax=ax3
)

ax3.set_xlabel("")
ax3.set_ylabel("Rata-rata PM2.5 (µg/m³)")
st.pyplot(fig3)

# ===============================
# FOOTER
# ===============================
st.caption("© 2026 – Dashboard Analisis PM2.5")
