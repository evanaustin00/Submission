import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Data Penyewaan Sepeda",
    page_icon=":bike:",
    layout="wide",
)

# Load dataset
url_hour = 'https://raw.githubusercontent.com/evanaustin00/bike-sharing-dataset/refs/heads/main/hour.csv'
url_day = 'https://raw.githubusercontent.com/evanaustin00/bike-sharing-dataset/refs/heads/main/day.csv'
hour_df = pd.read_csv(url_hour)
day_df = pd.read_csv(url_day)

# Konversi kolom 'dteday' menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Tambahkan Judul dan Deskripsi
st.title("Analisis Data Penyewaan Sepeda")
st.markdown("""
Dashboard ini menyajikan analisis data penyewaan sepeda berdasarkan dataset `day` dan `hour`.
Gunakan filter di sidebar untuk melakukan eksplorasi data lebih lanjut.
""")

# Sidebar untuk Filter Data
with st.sidebar:
    st.header("Filter Data")

    # Filter Bulan dengan slider range
    selected_months = st.select_slider(
        "Pilih Rentang Bulan:",
        options=day_df['mnth'].unique(),
        value=(day_df['mnth'].min(), day_df['mnth'].max()),
        help="Pilih rentang bulan untuk memfilter data."
    )

    # Filter Musim (Season) dengan radio button
    selected_seasons = st.radio(
        "Pilih Musim:",
        options=day_df['season'].unique(),
        index=0,
        horizontal=True,
        help="Pilih musim untuk memfilter data."
    )

    # Filter Kondisi Cuaca (Weathersit) dengan checkbox
    selected_weathersit = st.multiselect(
        "Pilih Kondisi Cuaca:",
        options=day_df['weathersit'].unique(),
        default=day_df['weathersit'].unique(),
        help="Pilih kondisi cuaca untuk memfilter data."
    )

    # Deskripsi tambahan
    st.sidebar.markdown("---")
    st.sidebar.info("Pilih filter untuk melihat visualisasi yang diperbarui.")

# Filter dataset berdasarkan pilihan pengguna
filtered_day_df = day_df[
    (day_df['mnth'] >= selected_months[0]) & (day_df['mnth'] <= selected_months[1]) &
    (day_df['season'] == selected_seasons) &
    (day_df['weathersit'].isin(selected_weathersit))
]

# Kolom Layout untuk Visualisasi
col1, col2 = st.columns(2)

# Pertanyaan 1: Pengaruh Kondisi Cuaca Terhadap Jumlah Pengguna Terdaftar
with col1:
    st.header("Pengaruh Kondisi Cuaca Terhadap Jumlah Pengguna Terdaftar")

    # Agregasi data berdasarkan kondisi cuaca
    aggregated_weather = filtered_day_df.groupby('weathersit')['registered'].sum().reset_index()

    # Visualisasi Data untuk Pertanyaan 1
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weathersit', y='registered', data=aggregated_weather, palette='viridis', ax=ax1)
    ax1.set_title('Total Jumlah Pengguna Terdaftar Berdasarkan Kondisi Cuaca')
    ax1.set_xlabel('Kondisi Cuaca (1: Cerah, 2: Kabut, 3: Hujan/Salju)')
    ax1.set_ylabel('Total Jumlah Pengguna Terdaftar')
    ax1.grid(axis='y', linestyle='--')
    st.pyplot(fig1)

# Pertanyaan 2: Hubungan Antara Kecepatan Angin dan Jumlah Total Pengguna
with col2:
    st.header("Hubungan Antara Kecepatan Angin dan Jumlah Total Pengguna")

    # Filter data untuk akhir pekan di minggu pertama Januari 2011
    weekend_first_week_jan_2011 = hour_df[
        (hour_df['dteday'] <= '2011-01-07') &
        (hour_df['weekday'].isin([0, 6]))
    ]

    # Scatter plot hubungan kecepatan angin dan jumlah total pengguna
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='windspeed', y='cnt', data=weekend_first_week_jan_2011, alpha=0.7, color='teal', ax=ax2)
    ax2.set_title('Hubungan Kecepatan Angin dan Total Jumlah Pengguna')
    ax2.set_xlabel('Kecepatan Angin')
    ax2.set_ylabel('Total Jumlah Pengguna')
    ax2.grid(True, linestyle='--')
    st.pyplot(fig2)

# Kesimpulan
st.subheader("Kesimpulan")
st.markdown("""
- Kondisi cuaca memiliki pengaruh signifikan terhadap total jumlah pengguna terdaftar pada hari kerja selama bulan Januari 2011. Cuaca yang lebih baik (kondisi 1: Cerah) cenderung memiliki total jumlah pengguna terdaftar yang lebih tinggi dibandingkan dengan cuaca yang kurang baik.
- Tidak ada hubungan yang kuat antara kecepatan angin dan total jumlah pengguna pada akhir pekan selama minggu pertama Januari 2011.
- Tren penggunaan sepeda bervariasi berdasarkan musim.
""")

# Tampilan Data yang telah difilter
st.subheader("Data yang Difilter")
st.dataframe(filtered_day_df.head())

# Tambahkan Footer
st.markdown("---")
st.markdown("Dibuat dengan Streamlit")
