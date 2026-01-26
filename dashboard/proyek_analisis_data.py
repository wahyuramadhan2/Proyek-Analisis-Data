import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Dashboard Kualitas Udara PM2.5",
    layout="wide"
)

st.title("📊 Dashboard Analisis Kualitas Udara (PM2.5)")
st.caption("Data Kualitas Udara Periode 2013–2017")

# ===============================
# LOAD DATA (GOOGLE DRIVE)
# ===============================
@st.cache_data
def load_data():
    # GANTI FILE_ID_KAMU dengan ID Google Drive CSV
    url = "https://drive.google.com/file/d/1u4I0OvFlXKCKgwQcq0AGr7S_xZxJ6Tqd/view?usp=sharing"
    df = pd.read_csv(url)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df

df = load_data()

# ===============================
# SIDEBAR FILTER
# ===============================
st.sidebar.header("🔎 Filter Data")

stations = st.sidebar.multiselect(
    "Pilih Stasiun",
    options=df["station"].unique(),
    default=df["station"].unique()
)

year_range = st.sidebar.slider(
    "Rentang Tahun",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

filtered_df = df[
    (df["station"].isin(stations)) &
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

# ===============================
# BUSINESS QUESTIONS
# ===============================
st.header("📌 Pertanyaan Bisnis")
st.markdown("""
1. Bagaimana tren konsentrasi PM2.5 dari tahun 2013 hingga 2017?  
2. Bagaimana perbandingan rata-rata PM2.5 antar stasiun pemantauan?
""")

# ===============================
# MONTHLY PM2.5 TREND
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

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(
    data=monthly_pm25,
    x="datetime",
    y="PM2.5",
    hue="station",
    ax=ax
)

ax.set_title("Tren Bulanan Konsentrasi PM2.5")
ax.set_xlabel("Waktu")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.xticks(rotation=45)
plt.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

st.pyplot(fig)

# ===============================
# ANNUAL COMPARISON
# ===============================
st.subheader("🏭 Perbandingan Rata-rata Tahunan PM2.5 Antar Stasiun")

annual_pm25 = (
    filtered_df
    .groupby(["station", "year"])["PM2.5"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(
    data=annual_pm25,
    x="year",
    y="PM2.5",
    hue="station",
    marker="o",
    ax=ax
)

ax.set_title("Rata-rata Tahunan PM2.5 per Stasiun")
ax.set_xlabel("Tahun")
ax.set_ylabel("PM2.5 (µg/m³)")
plt.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

st.pyplot(fig)

# ===============================
# WEEKDAY vs WEEKEND
# ===============================
st.subheader("📅 Perbandingan PM2.5: Hari Kerja vs Akhir Pekan")

filtered_df["day_type"] = np.where(
    filtered_df["datetime"].dt.weekday < 5,
    "Hari Kerja",
    "Akhir Pekan"
)

avg_daytype = (
    filtered_df
    .groupby(["station", "day_type"])["PM2.5"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(
    data=avg_daytype,
    x="station",
    y="PM2.5",
    hue="day_type",
    ax=ax
)

ax.set_title("Rata-rata PM2.5 per Stasiun")
ax.set_xlabel("Stasiun")
ax.set_ylabel("PM2.5 (µg/m³)")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# ===============================
# FOOTER
# ===============================
st.caption("© 2026 | Mochammad Wahyu Ramadhan | Dashboard Analisis Data (Streamlit)")
