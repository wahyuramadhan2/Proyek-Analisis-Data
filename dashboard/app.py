# ===============================
# IMPORT LIBRARIES
# ===============================
import streamlit as st

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

import os
import re

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Dashboard Kualitas Udara",
    layout="wide"
)

# ===============================
# BUSINESS QUESTIONS (SESUAI NOTEBOOK)
# ===============================
st.header("📌 Pertanyaan")

st.markdown("""
1. **Bagaimana dinamika konsentrasi PM2.5 sepanjang tahun 2013–2017 berdasarkan data historis??**  
2. **Sejauh mana perbedaan konsentrasi PM2.5 antar stasiun pemantauan selama periode pengamatan 2013–2017?**
""")

st.markdown("---")
st.caption("Catatan: Analisis weekday/weekend dan pola Senin–Minggu disajikan sebagai analisis tambahan untuk memperkuat interpretasi dinamika PM2.5.")

# ===============================
# Q1 - DAILY PM2.5 (SESUAI NOTEBOOK)
# ===============================
daily_pm25 = (
    filtered_df
    .set_index("datetime")
    .groupby("station")["PM2.5"]
    .resample("D")
    .mean()
    .reset_index()
)

st.subheader("📈 Dinamika PM2.5 Harian (2013–2017) per Stasiun")
fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(
    data=daily_pm25,
    x="datetime",
    y="PM2.5",
    hue="station",
    linewidth=1,
    ax=ax
)

ax.set_title("Dinamika Konsentrasi PM2.5 Harian (2013–2017) per Stasiun")
ax.set_xlabel("Waktu")
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)
ax.legend(title="Stasiun", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
st.pyplot(fig)

# ===============================
# Q1 - MONTHLY PM2.5 (SESUAI NOTEBOOK)
# ===============================
monthly_pm25 = (
    filtered_df
    .set_index("datetime")
    .groupby("station")["PM2.5"]
    .resample("M")
    .mean()
    .reset_index()
)

st.subheader("📈 Pola Bulanan PM2.5 (2013–2017) per Stasiun")
fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(
    data=monthly_pm25,
    x="datetime",
    y="PM2.5",
    hue="station",
    linewidth=1,
    ax=ax
)

ax.set_title("Pola Bulanan Konsentrasi PM2.5 (2013–2017) per Stasiun")
ax.set_xlabel("Waktu")
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)
ax.legend(title="Stasiun", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
st.pyplot(fig)

# ===============================
# Q2 - ANNUAL COMPARISON (SESUAI NOTEBOOK: pakai datetime resample Y)
# ===============================
annual_pm25 = (
    filtered_df
    .set_index("datetime")
    .groupby("station")["PM2.5"]
    .resample("Y")
    .mean()
    .reset_index()
)

st.subheader("🏭 Perbandingan Konsentrasi PM2.5 Tahunan Antar Stasiun (2013–2017)")
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

ax.set_title("Perbandingan Konsentrasi PM2.5 Tahunan Antar Stasiun (2013–2017)")
ax.set_xlabel("Tahun")
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.legend(title="Stasiun", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
st.pyplot(fig)

# ===============================
# ANALISIS TAMBAHAN - WEEKDAY vs WEEKEND (SESUAI NOTEBOOK: Indonesia)
# ===============================
st.markdown("---")
st.subheader("📅 Analisis Tambahan: Hari Kerja vs Akhir Pekan")

filtered_df["weekday"] = filtered_df["datetime"].dt.weekday
filtered_df["jenis_hari"] = np.where(
    filtered_df["weekday"] < 5,
    "Hari Kerja",
    "Akhir Pekan"
)

pm25_daytype_avg = (
    filtered_df
    .groupby(["station", "jenis_hari"])["PM2.5"]
    .mean()
    .reset_index()
)

pm25_pivot = pm25_daytype_avg.pivot(
    index="station",
    columns="jenis_hari",
    values="PM2.5"
)

# antisipasi kolom hilang
for col in ["Hari Kerja", "Akhir Pekan"]:
    if col not in pm25_pivot.columns:
        pm25_pivot[col] = np.nan

stations = pm25_pivot.index
x = np.arange(len(stations))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(x - width/2, pm25_pivot["Hari Kerja"], width, label="Hari Kerja")
ax.bar(x + width/2, pm25_pivot["Akhir Pekan"], width, label="Akhir Pekan")

ax.set_title("Rata-rata PM2.5: Hari Kerja vs Akhir Pekan per Stasiun")
ax.set_xlabel("Stasiun Pemantauan")
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
ax.set_xticks(x)
ax.set_xticklabels(stations, rotation=45)
ax.legend()
plt.tight_layout()
st.pyplot(fig)

# ===============================
# ANALISIS TAMBAHAN - POLA SENIN–MINGGU (SESUAI NOTEBOOK)
# ===============================
st.subheader("🗓️ Analisis Tambahan: Pola Harian PM2.5 (Senin–Minggu)")

filtered_df["weekday_name"] = filtered_df["datetime"].dt.day_name()

weekday_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

avg_pm25_weekday = (
    filtered_df
    .groupby(["station", "weekday_name"])["PM2.5"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 5))

for st_name in avg_pm25_weekday["station"].unique():
    subset = avg_pm25_weekday[avg_pm25_weekday["station"] == st_name]
    subset = subset.set_index("weekday_name").reindex(weekday_order)

    ax.plot(
        weekday_order,
        subset["PM2.5"],
        marker="o",
        label=st_name
    )

ax.set_title("Pola Rata-rata PM2.5 Berdasarkan Hari dalam Minggu")
ax.set_xlabel("Hari")
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
plt.xticks(rotation=45)
ax.legend(title="Stasiun", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
st.pyplot(fig)
