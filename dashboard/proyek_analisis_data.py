import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import numpy as np

# ===============================
# CONFIG
# ===============================
st.set_page_config(
    page_title="Dashboard Kualitas Udara",
    layout="wide"
)

# ===============================
# TITLE
# ===============================
st.title("📊 Dashboard Analisis Kualitas Udara")
st.caption("Visualisasi hasil Exploratory Data Analysis (EDA)")

# ===============================
# LOAD DATA (GOOGLE DRIVE)
# ===============================
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1u4I0OvFlXKCKgwQcq0AGr7S_xZxJ6Tqd"
    return pd.read_csv(url)

try:
    air_quality_df = load_data()
    st.success("Dataset berhasil dimuat dari Google Drive")
except Exception as e:
    st.error("Gagal memuat dataset. Periksa link Google Drive.")
    st.stop()

# ===============================
# PREPROCESS
# ===============================
air_quality_df["datetime"] = pd.to_datetime(air_quality_df["datetime"])

# ===============================
# SIDEBAR FILTER
# ===============================
with st.sidebar:
    st.header("⚙️ Filter Data")

    station_filter = st.multiselect(
        "Pilih Stasiun",
        options=air_quality_df["station"].unique(),
        default=air_quality_df["station"].unique()
    )

    year_range = st.slider(
        "Rentang Tahun",
        int(air_quality_df["year"].min()),
        int(air_quality_df["year"].max()),
        (
            int(air_quality_df["year"].min()),
            int(air_quality_df["year"].max())
        )
    )

filtered_df = air_quality_df[
    (air_quality_df["station"].isin(station_filter)) &
    (air_quality_df["year"] >= year_range[0]) &
    (air_quality_df["year"] <= year_range[1])
]

# ===============================
# BUSINESS QUESTIONS
# ===============================
st.header("📌 Pertanyaan Bisnis")
st.markdown("""
1. Bagaimana tren konsentrasi PM2.5 pada periode 2013–2017?  
2. Bagaimana perbandingan PM2.5 antar stasiun?
""")

# ===============================
# MONTHLY PM2.5
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
fig, ax = plt.subplots(figsize=(14,6))
sns.lineplot(data=monthly_pm25, x="datetime", y="PM2.5", hue="station", ax=ax)

ax.set_title("Tren Bulanan PM2.5 (2013–2017)")
ax.set_xlabel("Waktu")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# ===============================
# FOOTER
# ===============================
st.caption("© 2026 | Dashboard Analisis Data Kualitas Udara - Streamlit")
