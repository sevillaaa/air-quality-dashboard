import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard Analisis Kualitas Udara"
)

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df

df = load_data()

st.sidebar.header("Filter Data")

selected_station = st.sidebar.multiselect(
    "Pilih Stasiun",
    sorted(df["station"].unique()),
    default=sorted(df["station"].unique())
)

year_list = sorted(df["year"].unique())

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    year_list,
    default=year_list
)

if not selected_station or not selected_year:
    st.info("Silakan pilih minimal satu stasiun dan satu tahun untuk menampilkan dashboard")
    st.stop()

filtered_df = df[
    (df["station"].isin(selected_station)) &
    (df["year"].isin(selected_year))
].copy()

st.title("Dashboard Kualitas Udara")
st.write("Dashboard interaktif ini digunakan untuk memantau konsentrasi PM2.5, tren waktu, dan hubungan antar cuaca.")

st.markdown("""
### Ringkasan Dashboard
Dashboard ini menampilkan kondisi kualitas udara berdasarkan konsentrasi PM2.5,
perbandingan antar stasiun, tren waktu, serta hubungan dengan faktor cuaca.
""")

col1, col2, col3 = st.columns(3)

if filtered_df.empty:
    avg_pm25_display = "-"
    max_pm25_display = "-"
    total_station = 0
else:
    avg_pm25_display = f"{filtered_df['PM2.5'].mean():.2f}"
    max_pm25_display = f"{filtered_df['PM2.5'].max():.2f}"
    total_station = filtered_df["station"].nunique()

col1.metric("Rata-rata PM2.5", avg_pm25_display)
col2.metric("PM2.5 Tertinggi", max_pm25_display)
col3.metric("Jumlah Stasiun", total_station)

st.divider()

st.subheader("Rata-rata PM2.5 per Stasiun")

station_avg = (
    filtered_df.groupby("station")["PM2.5"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
    x=station_avg.values,
    y=station_avg.index,
    ax=ax
)

ax.set_xlabel("Rata-rata PM2.5")
ax.set_ylabel("Stasiun")
st.pyplot(fig, use_container_width=True)

st.caption("Grafik ini menunjukkan rata-rata konsentrasi PM2.5 berdasarkan stasiun yang dipilih.")

st.info("Stasiun dengan nilai PM2.5 lebih tinggi menunjukkan tingkat polusi yang lebih tinggi dan perlu mendapat perhatian lebih.")

st.subheader("Tren PM2.5 Bulanan")

monthly = (
    filtered_df
    .set_index("datetime")
    .resample("ME")["PM2.5"]
    .mean()
)

fig, ax = plt.subplots(figsize=(12,5))
ax.plot(monthly.index, monthly.values, linewidth=2)

ax.set_xlabel("Waktu")
ax.set_ylabel("Rata-rata PM2.5")
st.pyplot(fig, use_container_width=True)

st.caption("Grafik ini menunjukkan tren perubahan PM2.5 dari waktu ke waktu.")

st.info("Terlihat bahwa konsentrasi PM2.5 bersifat fluktuatif sepanjang periode waktu.")

st.subheader("Korelasi Faktor Cuaca dengan PM2.5")

corr_cols = ["PM2.5", "TEMP", "DEWP", "RAIN", "WSPM"]
corr = filtered_df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    ax=ax
)

st.pyplot(fig, use_container_width=True)

st.caption("Heatmap ini menunjukkan hubungan antar variabel cuaca dengan PM2.5.")

st.info("Kecepatan angin memiliki hubungan negatif paling kuat terhadap PM2.5 dibanding faktor lainnya.")

st.subheader("PM2.5 Berdasarkan Kecepatan Angin")

filtered_df["WSPM_Category"] = pd.cut(
    filtered_df["WSPM"],
    bins=[0, 1, 2, 4, 20],
    labels=["Low", "Medium", "High", "Very High"]
)

wind_avg = (
    filtered_df.groupby("WSPM_Category")["PM2.5"]
    .mean()
)

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(
    x=wind_avg.index,
    y=wind_avg.values,
    ax=ax
)

ax.set_xlabel("Kategori WSPM")
ax.set_ylabel("Rata-rata PM2.5")
st.pyplot(fig, use_container_width=True)

st.caption("Grafik ini menunjukkan rata-rata PM2.5 berdasarkan kategori kecepatan angin.")

st.info("Semakin tinggi kecepatan angin, konsentrasi PM2.5 cenderung menurun.")

st.subheader("PM2.5 Berdasarkan Intensitas Curah Hujan")

filtered_df = filtered_df.copy()

filtered_df["RAIN_Category"] = pd.cut(
    filtered_df["RAIN"],
    bins=[-0.1, 0, 5, 20, 100],
    labels=["No Rain", "Light", "Moderate", "Heavy"]
)

rain_avg = (
    filtered_df.groupby("RAIN_Category")["PM2.5"]
    .mean()
)

fig, ax = plt.subplots(figsize=(8,5))

sns.barplot(
    x=rain_avg.index,
    y=rain_avg.values,
    ax=ax
)

ax.set_xlabel("Kategori Curah Hujan")
ax.set_ylabel("Rata-rata PM2.5")
st.pyplot(fig, use_container_width=True)

st.caption("Grafik ini menunjukkan hubungan antara curah hujan dan PM2.5.")

st.info("PM2.5 cenderung lebih tinggi saat tidak hujan dibanding saat hujan.")

st.subheader("Hubungan Suhu (TEMP) dengan PM2.5")

fig, ax = plt.subplots(figsize=(8,5))

sns.regplot(
    data=filtered_df,
    x="TEMP",
    y="PM2.5",
    scatter_kws={"alpha": 0.2},
    line_kws={"color": "orange"},
    ax=ax
)

ax.set_xlabel("Suhu (TEMP)")
ax.set_ylabel("PM2.5")

st.pyplot(fig, use_container_width=True)

st.caption("Grafik ini menunjukkan hubungan antara suhu dan PM2.5.")

st.info("Suhu memiliki hubungan yang relatif lebih lemah terhadap PM2.5.")

st.subheader("🌎 Insight")

st.markdown("""
- Tingkat polusi berbeda antar stasiun.
- PM2.5 bersifat fluktuatif sepanjang waktu.
- Kecepatan angin membantu menurunkan polusi.
- Curah hujan cenderung menurunkan polusi.""")
