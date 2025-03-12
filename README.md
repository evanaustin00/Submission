# Analisis Interaktif Data Penyewaan Sepeda

Dashboard ini memungkinkan eksplorasi data penyewaan sepeda untuk mengidentifikasi tren dan faktor-faktor kunci yang memengaruhi penggunaan.

## Ikhtisar Proyek

Proyek ini menganalisis data penyewaan sepeda dengan fokus pada bagaimana kondisi cuaca dan kecepatan angin berkorelasi dengan jumlah pengguna. Tujuan utamanya adalah memberikan wawasan yang dapat menjawab pertanyaan bisnis berikut:

1. Bagaimana pengaruh kondisi cuaca terhadap jumlah pengguna terdaftar (registered) pada hari kerja selama bulan Januari 2011?
2. Apakah terdapat hubungan antara kecepatan angin (windspeed) dan jumlah total pengguna (cnt) pada akhir pekan selama minggu pertama Januari 2011?

Analisis mencakup:

*   Evaluasi dampak kondisi cuaca terhadap jumlah pengguna terdaftar.
*   Investigasi hubungan antara kecepatan angin dan total pengguna.
*   Identifikasi pola penggunaan sepeda berdasarkan bulan.

## Struktur Proyek

submission/
├── dashboard/
│   ├── dashboard.py          
│   └── main_data.csv      
├── data/
│   ├── day.csv               
│   └── hour.csv              
├── notebook.ipynb           
├── README.md                 
└── requirements.txt          
└── url.txt

## Instalasi

Untuk menjalankan aplikasi ini, ikuti langkah-langkah berikut:

1.  **Buat Virtual Environment** (direkomendasikan):

    
    python3 -m venv venv    # Membuat virtual environment
    source venv/bin/activate # Aktifkan (Linux/macOS)
    venv\Scripts\activate    # Aktifkan (Windows)
    

2.  **Instal Dependensi**:
    Kami merekomendasikan instalasi menggunakan `requirements.txt`:

    
    pip install -r requirements.txt
    

    File `requirements.txt` berisi daftar pustaka yang dibutuhkan:

    
    streamlit
    pandas
    seaborn
    matplotlib
    

## Penggunaan

1.  Pastikan Anda berada di direktori root proyek (direktori yang sama dengan berkas `dashboard.py`).
2.  Aktifkan virtual environment (jika Anda menggunakannya).
3.  Jalankan aplikasi Streamlit:

    
    streamlit run dashboard.py
    

4.  Dashboard akan terbuka di peramban web Anda.

## Fitur Utama

Dashboard ini menyediakan:

1.  **Penyaringan Data**:

    *   Pilih bulan yang akan ditampilkan untuk memfokuskan analisis Anda.
    *   Data yang telah difilter akan ditampilkan dalam tabel.

2.  **Visualisasi Data**:

    *   **Pengaruh Cuaca**: Menampilkan total pengguna terdaftar berdasarkan kondisi cuaca tertentu di bulan Januari 2011 (hari kerja).
    *   **Hubungan Kecepatan Angin**: Menggambarkan hubungan antara kecepatan angin dan total pengguna pada akhir pekan selama minggu pertama Januari 2011.

## Sumber Data

Proyek ini menggunakan dua dataset:

*   `day.csv`: Data agregat harian.
*   `hour.csv`: Data per jam.

Fitur-fitur utama meliputi:

*   `dteday`: Tanggal.
*   `season`: Musim (1: semi, 2: panas, 3: gugur, 4: dingin).
*   `yr`: Tahun (0: 2011, 1: 2012).
*   `mnth`: Bulan (1-12).
*   `hr`: Jam (0-23).
*   `holiday`: Menunjukkan apakah hari libur atau tidak.
*   `weekday`: Hari dalam seminggu.
*   `workingday`: Menunjukkan apakah hari kerja atau bukan.
*   `weathersit`: Kondisi cuaca.
*   `temp`: Suhu (d normalisasi).
*   `atemp`: Suhu terasa (d normalisasi).
*   `hum`: Kelembaban (d normalisasi).
*   `windspeed`: Kecepatan angin (d normalisasi).
*   `casual`: Jumlah pengguna casual.
*   `registered`: Jumlah pengguna terdaftar.
*   `cnt`: Total jumlah pengguna.

## Kesimpulan Analisis

Berdasarkan data yang divisualisasikan, berikut adalah kesimpulan utama:

1.  **Kondisi Cuaca**: Kondisi cuaca sangat memengaruhi jumlah pengguna terdaftar, terutama pada hari kerja di bulan Januari 2011.
2.  **Kecepatan Angin**: Tidak ada korelasi yang jelas antara kecepatan angin dan total pengguna pada akhir pekan selama minggu pertama Januari 2011.

## Kontributor

*   `Evan Austin`
*   `evanaustin64@gmail.com` atau `mc185d5y0640@student.devacademy.id`
*   `MC185D5Y0640`
