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

    # Filter Musim (Season) dengan multiselect dan opsi "Semua Musim"
    all_seasons = day_df['season'].unique().tolist()
    selected_seasons = st.multiselect(
        "Pilih Musim:",
        options=all_seasons + ["Semua Musim"],
        default=all_seasons,  # Default: semua musim terpilih
        help="Pilih musim untuk memfilter data. Pilih 'Semua Musim' untuk melihat data dari semua musim."
    )

    # Jika "Semua Musim" dipilih, gunakan semua musim, jika tidak, gunakan musim yang dipilih
    if "Semua Musim" in selected_seasons:
        selected_seasons = all_seasons
    
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
    (day_df['season'].isin(selected_seasons)) &
    (day_df['weathersit'].isin(selected_weathersit))
]

# Kolom Layout untuk Visualisasi
col1, col2 = st.columns(2)

# Pertanyaan 1: Pengaruh Kondisi Cuaca Terhadap Jumlah Pengguna Terdaftar
with col1:
    st.header("Pengaruh Kondisi Cuaca Terhadap Jumlah Pengguna Terdaftar")

    # Filter data untuk hari kerja di Januari 2011
    jan_2011_workingday = day_df[
        (day_df['mnth'] == 1) &
        (day_df['yr'] == 0) &
        (day_df['workingday'] == 1)
    ]

    # Mapping untuk weathersit
    weather_labels = {
        1: 'Cerah',
        2: 'Berkabut',
        3: 'Hujan Ringan/Salju',
        4: 'Hujan Lebat/Es'
    }
    jan_2011_workingday['weathersit_label'] = jan_2011_workingday['weathersit'].map(weather_labels)

    # Visualisasi: Boxplot pengaruh kondisi cuaca terhadap jumlah pengguna terdaftar
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        x='weathersit_label',  # Gunakan label yang lebih deskriptif
        y='registered',
        data=jan_2011_workingday,
        palette='coolwarm',
        notch=True,
        ax=ax1
    )
    ax1.set_title('Pengaruh Kondisi Cuaca Terhadap Jumlah Pengguna Terdaftar (Januari 2011 - Hari Kerja)')
    ax1.set_xlabel('Kondisi Cuaca')
    ax1.set_ylabel('Jumlah Pengguna Terdaftar')
    ax1.grid(axis='y', linestyle='--')

    # Tambahkan anotasi median
    medians = jan_2011_workingday.groupby('weathersit_label')['registered'].median().values
    for i, median in enumerate(medians):
        ax1.text(i, median + 50, f'Median: {int(median)}', ha='center', color='red')

    st.pyplot(fig1)

# Pertanyaan 2: Hubungan Antara Kecepatan Angin dan Jumlah Total Pengguna
with col2:
    st.header("Hubungan Antara Kecepatan Angin dan Jumlah Total Pengguna")

    # Filter data untuk akhir pekan di minggu pertama Januari 2011
    weekend_first_week = hour_df[
        (hour_df['dteday'] <= '2011-01-07') &
        (hour_df['weekday'].isin([0, 6]))  # 0 = Minggu, 6 = Sabtu
    ]

    # Visualisasi Scatter plot dengan regresi
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        x='windspeed',
        y='cnt',
        data=weekend_first_week,
        palette='viridis',
        alpha=0.7,
        edgecolor='black',
        ax=ax2
    )
    sns.regplot(
        x='windspeed',
        y='cnt',
        data=weekend_first_week,
        scatter=False,
        color='red',
        line_kws={'linestyle': '--', 'alpha': 0.5},
        ax=ax2
    )
    ax2.set_title('Hubungan Kecepatan Angin dan Jumlah Total Pengguna\nAkhir Pekan Minggu Pertama Januari 2011')
    ax2.set_xlabel('Kecepatan Angin (Normalisasi)')
    ax2.set_ylabel('Jumlah Total Pengguna')
    ax2.grid(linestyle='--')
    st.pyplot(fig2)

# Kesimpulan
st.subheader("Kesimpulan")
st.markdown("""
- Kondisi cuaca memiliki pengaruh signifikan terhadap total jumlah pengguna terdaftar pada hari kerja selama bulan Januari 2011. Cuaca yang lebih baik (kondisi 1: Cerah) cenderung memiliki total jumlah pengguna terdaftar yang lebih tinggi dibandingkan dengan cuaca yang kurang baik.
- Terdapat hubungan yang lemah antara kecepatan angin dan total jumlah pengguna pada akhir pekan selama minggu pertama Januari 2011.
- Tren penggunaan sepeda bervariasi berdasarkan musim.
""")

# Tampilan Data yang telah difilter
st.subheader("Data yang Difilter")
st.dataframe(filtered_day_df.head())

# Tambahkan Footer
st.markdown("---")
st.markdown("Dibuat dengan Streamlit")
