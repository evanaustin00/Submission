import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Interaktif Penyewaan Sepeda",
    page_icon=":bike:",
    layout="wide",
)

# Load dataset
@st.cache_data
def load_data():
    url_hour = 'https://raw.githubusercontent.com/evanaustin00/bike-sharing-dataset/refs/heads/main/hour.csv'
    url_day = 'https://raw.githubusercontent.com/evanaustin00/bike-sharing-dataset/refs/heads/main/day.csv'
    hour_df = pd.read_csv(url_hour)
    day_df = pd.read_csv(url_day)

    # Konversi kolom 'dteday' menjadi datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return hour_df, day_df

hour_df, day_df = load_data()

# Judul Dashboard
st.title("Dashboard Interaktif Penyewaan Sepeda")
st.markdown("""
Dashboard ini menyajikan analisis data penyewaan sepeda berdasarkan dataset `day` dan `hour`.
Gunakan filter di bawah untuk melakukan eksplorasi data lebih lanjut.
""")

# Sidebar untuk Filter Data
st.sidebar.header("Filter Data")

# Filter Musim (Season) untuk Visualisasi 1
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
selected_season_vis1 = st.sidebar.selectbox(
    "Pilih Musim untuk Visualisasi 1:",
    options=["All Seasons"] + list(season_labels.keys()),
    format_func=lambda x: season_labels.get(x, "All Seasons"),
)

# Filter Hari Kerja (Working Day) untuk Visualisasi 1
working_day_filter_vis1 = st.sidebar.radio(
    "Pilih Jenis Hari untuk Visualisasi 1:",
    options=["Semua Hari", "Hari Kerja", "Akhir Pekan"],
)

# Terapkan filter ke dataset untuk Visualisasi 1
filtered_day_df_vis1 = day_df.copy()

if selected_season_vis1 != "All Seasons":
    filtered_day_df_vis1 = filtered_day_df_vis1[filtered_day_df_vis1['season'] == selected_season_vis1]

if working_day_filter_vis1 == "Hari Kerja":
    filtered_day_df_vis1 = filtered_day_df_vis1[filtered_day_df_vis1['workingday'] == 1]
elif working_day_filter_vis1 == "Akhir Pekan":
    filtered_day_df_vis1 = filtered_day_df_vis1[filtered_day_df_vis1['workingday'] == 0]

# Kolom Layout untuk Visualisasi
col1, col2 = st.columns(2)

# Visualisasi 1: Boxplot Pengaruh Kondisi Cuaca terhadap Jumlah Pengguna Terdaftar
with col1:
    st.subheader("Pengaruh Kondisi Cuaca Terhadap Jumlah Pengguna Terdaftar")
    
    # Mapping untuk weathersit
    weather_labels = {
        1: 'Cerah',
        2: 'Berkabut',
        3: 'Hujan Ringan/Salju',
        4: 'Hujan Lebat/Es'
    }
    
    filtered_day_df_vis1['weathersit_label'] = filtered_day_df_vis1['weathersit'].map(weather_labels)

    # Visualisasi Boxplot
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        x='weathersit_label', 
        y='registered', 
        data=filtered_day_df_vis1, 
        palette='coolwarm', 
        notch=True,
        ax=ax1
    )
    
    ax1.set_title('Pengaruh Kondisi Cuaca Terhadap Jumlah Pengguna Terdaftar')
    ax1.set_xlabel('Kondisi Cuaca')
    ax1.set_ylabel('Jumlah Pengguna Terdaftar')
    
    # Tambahkan anotasi median
    medians = filtered_day_df_vis1.groupby('weathersit_label')['registered'].median().values
    for i, median in enumerate(medians):
        ax1.text(i, median + 50, f'Median: {int(median)}', ha='center', color='red')

    st.pyplot(fig1)

# Sidebar untuk Filter Data Visualisasi Kedua
st.sidebar.header("Filter Data untuk Visualisasi Kedua")

# Filter Musim (Season) untuk Visualisasi 2
selected_season_vis2 = st.sidebar.selectbox(
    "Pilih Musim untuk Visualisasi 2:",
    options=["All Seasons"] + list(season_labels.keys()),
    format_func=lambda x: season_labels.get(x, "All Seasons"),
)

# Filter Hari Kerja (Working Day) untuk Visualisasi 2
working_day_filter_vis2 = st.sidebar.radio(
    "Pilih Jenis Hari untuk Visualisasi 2:",
    options=["Semua Hari", "Hari Kerja", "Akhir Pekan"],
)

# Terapkan filter ke dataset untuk Visualisasi 2
filtered_hour_df_vis2 = hour_df.copy()

if selected_season_vis2 != "All Seasons":
    filtered_hour_df_vis2 = filtered_hour_df_vis2[filtered_hour_df_vis2['season'] == selected_season_vis2]

if working_day_filter_vis2 == "Hari Kerja":
    filtered_hour_df_vis2 = filtered_hour_df_vis2[filtered_hour_df_vis2['weekday'] < 5]  # weekday < 5 berarti Senin-Jumat
elif working_day_filter_vis2 == "Akhir Pekan":
    filtered_hour_df_vis2 = filtered_hour_df_vis2[filtered_hour_df_vis2['weekday'] >= 5]  # weekday >= 5 berarti Sabtu-Minggu
# Visualisasi 2: Scatter Plot Hubungan Kecepatan Angin dan Jumlah Total Pengguna
with col2:
    st.subheader("Hubungan Kecepatan Angin dan Jumlah Total Pengguna")

    # Scatter plot dengan regresi dan kategori kecepatan angin
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    sns.scatterplot(
        x='windspeed', 
        y='cnt', 
        data=filtered_hour_df_vis2, 
        alpha=0.7,
        edgecolor='black',
        ax=ax2,
    )
    
    sns.regplot(
        x='windspeed', 
        y='cnt', 
        data=filtered_hour_df_vis2, 
        scatter=False, 
        color='red',
        line_kws={'linestyle': '--', 'alpha': 0.5},
        ax=ax2,
    )
    
    ax2.set_title(f'Hubungan Kecepatan Angin dan Jumlah Total Pengguna\nMusim: {season_labels.get(selected_season_vis2, "All Seasons")}')
    ax2.set_xlabel('Kecepatan Angin (Normalisasi)')
    ax2.set_ylabel('Jumlah Total Pengguna')
    
    ax2.grid(linestyle='--')
    
    st.pyplot(fig2)