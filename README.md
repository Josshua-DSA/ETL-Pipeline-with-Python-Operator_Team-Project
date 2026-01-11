# ETL Pipeline dengan Apache Airflow 🌦️
**Integrasi Data Cuaca Otomatis menggunakan Open-Meteo API**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.0+-red.svg)](https://airflow.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)

---

## 🎯 Tentang Proyek

Proyek ini mengimplementasikan **pipeline ETL (Extract, Transform, Load)** yang terotomatisasi menggunakan **Apache Airflow** untuk mengumpulkan, memproses, dan menyimpan data cuaca dari **Open-Meteo API**. Pipeline ini dirancang untuk mengambil data cuaca secara berkala, mentransformasikannya ke dalam format terstruktur, dan menyimpannya ke dalam **database PostgreSQL** serta **file CSV** sebagai backup.

**Mengapa Proyek Ini Penting?**
- ⚡ **Otomasi Penuh**: Tidak perlu intervensi manual untuk pengambilan data
- 📊 **Data Terstruktur**: Data cuaca tersimpan rapi dan siap untuk analisis
- 🔄 **Update Berkala**: Jadwal otomatis untuk data terkini
- 💾 **Redundansi**: Dual storage untuk keamanan data
- 📈 **Skalabilitas**: Mudah dikembangkan untuk kebutuhan yang lebih besar

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🔄 **Pipeline Otomatis** | Ekstraksi, transformasi, dan loading data secara terjadwal |
| 🌐 **API Integration** | Koneksi ke Open-Meteo API untuk data cuaca real-time |
| 🧹 **Data Cleaning** | Pembersihan dan transformasi data mentah menjadi terstruktur |
| 💾 **Dual Storage** | Penyimpanan ke PostgreSQL (untuk query) + CSV (untuk backup) |
| 🔁 **UPSERT Logic** | Mencegah duplikasi data dengan operasi insert/update cerdas |
| 📊 **Airflow Dashboard** | Monitoring visual untuk workflow ETL |
| 🛡️ **Error Handling** | Logging komprehensif dan mekanisme retry otomatis |
| 📦 **Modular Design** | Kode terorganisir untuk maintenance dan pengembangan mudah |

---

## 📁 Struktur Proyek

```
ETL_PROJECT/
│
├── dags/
│   └── weather_etl.py              # DAG utama Airflow untuk orkestrasi ETL
│
├── ConnectUpsert/
│   ├── __init__.py                 # Inisialisasi package
│   ├── connect_postgres.py        # Koneksi ke PostgreSQL via PostgresHook
│   └── upsert_postgres.py         # Fungsi UPSERT untuk insert/update data
│
├── data/
│   ├── landing/                    # Folder untuk data mentah (JSON dari API)
│   │   └── weather_raw_YYYYMMDD.json
│   └── staging/                    # Folder untuk data hasil transformasi (CSV)
│       └── weather_clean_YYYYMMDD.csv
│
├── etl_weather/
│   ├── __init__.py                 # Inisialisasi package ETL
│   ├── config.py                   # File konfigurasi (koordinat, timezone, dll)
│   ├── extract.py                  # Modul ekstraksi data dari API
│   ├── transform.py                # Modul transformasi dan cleaning data
│   └── load.py                     # Modul loading ke CSV dan PostgreSQL
│
├── requirements.txt                # Daftar dependencies Python
└── README.md                       # Dokumentasi proyek (file ini)
```

### Penjelasan Folder:

- **`dags/`**: Berisi file DAG (Directed Acyclic Graph) yang mendefinisikan workflow ETL di Airflow
- **`ConnectUpsert/`**: Modul untuk koneksi database dan operasi UPSERT
- **`data/landing/`**: Menyimpan data mentah hasil ekstraksi API dalam format JSON
- **`data/staging/`**: Menyimpan data yang sudah dibersihkan dalam format CSV
- **`etl_weather/`**: Package utama berisi logika Extract, Transform, Load

---

## 🔧 Persyaratan Sistem

Sebelum memulai, pastikan sistem Anda memenuhi persyaratan berikut:

### Software
- **Python**: Versi 3.8 atau lebih tinggi
- **PostgreSQL**: Versi 13 atau lebih tinggi
- **Apache Airflow**: Versi 2.0 atau lebih tinggi
- **pip**: Package manager Python

### Python Libraries
Semua library tercantum di `requirements.txt`:
```
apache-airflow>=2.0.0
pandas>=1.3.0
requests>=2.26.0
psycopg2-binary>=2.9.0
python-dotenv>=0.19.0
```

### Hardware (Rekomendasi Minimum)
- **RAM**: 4 GB
- **Storage**: 10 GB free space
- **CPU**: 2 cores

---

## 🚀 Instalasi

Ikuti langkah-langkah berikut untuk menginstal dan menjalankan proyek:

### 1. Clone Repository

```bash
git clone https://github.com/username/etl-weather-pipeline.git
cd etl-weather-pipeline
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Untuk Linux/Mac:
source venv/bin/activate

# Untuk Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Apache Airflow

```bash
# Set Airflow Home directory (opsional)
export AIRFLOW_HOME=~/airflow

# Inisialisasi database Airflow
airflow db init

# Buat user admin untuk Airflow UI
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

### 5. Setup PostgreSQL Database

```sql
-- Login ke PostgreSQL
psql -U postgres

-- Buat database baru
CREATE DATABASE weather_db;

-- Buat tabel untuk menyimpan data cuaca
CREATE TABLE public.weather_hourly (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    temperature FLOAT,
    humidity INT,
    wind_speed FLOAT,
    weather_code INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(timestamp)
);
```

---

## ⚙️ Konfigurasi

### 1. Konfigurasi Airflow Connection

Buka Airflow Web UI di `http://localhost:8080` dan login dengan kredensial yang telah dibuat.

**Tambahkan Koneksi PostgreSQL:**

1. Navigasi ke **Admin** → **Connections**
2. Klik tombol **+** untuk menambah koneksi baru
3. Isi form dengan detail berikut:

```
Conn Id       : postgres_default
Conn Type     : Postgres
Host          : localhost
Schema        : weather_db
Login         : postgres
Password      : [password_anda]
Port          : 5432
```

4. Klik **Save**

### 2. Konfigurasi Airflow Variables

Tambahkan variabel konfigurasi di Airflow:

1. Navigasi ke **Admin** → **Variables**
2. Tambahkan variabel berikut:

```
Key: PG_CONN_ID
Value: postgres_default

Key: PG_TABLE
Value: public.weather_hourly

Key: API_LATITUDE
Value: -6.9175

Key: API_LONGITUDE
Value: 107.6191

Key: API_TIMEZONE
Value: Asia/Jakarta
```

### 3. Konfigurasi File `etl_weather/config.py`

Edit file konfigurasi sesuai kebutuhan:

```python
# API Configuration
API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = -6.9175  # Koordinat Bandung
LONGITUDE = 107.6191
TIMEZONE = "Asia/Jakarta"

# Data Storage Configuration
LANDING_PATH = "data/landing/"
STAGING_PATH = "data/staging/"

# PostgreSQL Configuration
PG_TABLE = "public.weather_hourly"
```

---

## 💻 Cara Penggunaan

### 1. Jalankan Airflow Webserver

Buka terminal pertama dan jalankan:

```bash
airflow webserver --port 8080
```

### 2. Jalankan Airflow Scheduler

Buka terminal kedua dan jalankan:

```bash
airflow scheduler
```

### 3. Akses Airflow UI

Buka browser dan navigasi ke:
```
http://localhost:8080
```

### 4. Aktifkan DAG

1. Cari DAG dengan nama `weather_etl_dag`
2. Toggle switch untuk mengaktifkan DAG
3. Klik tombol **Trigger DAG** (▶️) untuk menjalankan manual

### 5. Monitor Eksekusi

- Klik nama DAG untuk melihat detail
- Tab **Graph View**: Visualisasi alur task
- Tab **Tree View**: History eksekusi
- Tab **Logs**: Detail log setiap task

---

## ✅ Verifikasi Data

### 1. Cek File CSV

Pastikan file CSV terbuat di folder staging:

```bash
ls -lh data/staging/
cat data/staging/weather_clean_*.csv
```

### 2. Cek Data di PostgreSQL

```sql
-- Login ke PostgreSQL
psql -U postgres -d weather_db

-- Lihat jumlah data
SELECT COUNT(*) FROM public.weather_hourly;

-- Lihat sample data
SELECT * FROM public.weather_hourly 
ORDER BY timestamp DESC 
LIMIT 10;

-- Lihat data terbaru
SELECT 
    timestamp,
    temperature,
    humidity,
    wind_speed
FROM public.weather_hourly
WHERE timestamp::date = CURRENT_DATE
ORDER BY timestamp DESC;
```

### 3. Cek Log Airflow

```bash
# Lihat log task tertentu
airflow tasks test weather_etl_dag extract_weather_data 2024-01-01

# Lihat semua log
tail -f $AIRFLOW_HOME/logs/dag_id=weather_etl_dag/
```

---

## 🔍 Troubleshooting

### Problem 1: DAG tidak muncul di Airflow UI

**Solusi:**
```bash
# Pastikan DAG file ada di folder yang benar
ls -l $AIRFLOW_HOME/dags/

# Cek syntax error di DAG
python $AIRFLOW_HOME/dags/weather_etl.py

# Restart scheduler
pkill -f "airflow scheduler"
airflow scheduler
```

### Problem 2: Koneksi PostgreSQL Gagal

**Solusi:**
```bash
# Cek PostgreSQL berjalan
sudo systemctl status postgresql

# Test koneksi manual
psql -h localhost -U postgres -d weather_db

# Cek connection di Airflow
airflow connections test postgres_default
```

### Problem 3: Error saat Extract Data

**Solusi:**
```bash
# Test API secara manual
curl "https://api.open-meteo.com/v1/forecast?latitude=-6.9175&longitude=107.6191&hourly=temperature_2m"

# Cek konfigurasi API di config.py
cat etl_weather/config.py

# Periksa log detail
airflow tasks test weather_etl_dag extract_weather_data 2024-01-01
```

### Problem 4: Permission Denied di Folder Data

**Solusi:**
```bash
# Berikan akses write ke folder data
chmod -R 755 data/
chown -R $USER:$USER data/

# Buat folder jika belum ada
mkdir -p data/landing data/staging
```

### Problem 5: UPSERT Gagal (Duplicate Key)

**Solusi:**
```sql
-- Cek constraint di tabel
\d public.weather_hourly

-- Hapus duplikasi manual jika perlu
DELETE FROM public.weather_hourly a USING (
    SELECT MIN(ctid) as ctid, timestamp
    FROM public.weather_hourly 
    GROUP BY timestamp HAVING COUNT(*) > 1
) b
WHERE a.timestamp = b.timestamp 
AND a.ctid <> b.ctid;
```

---

## 📊 Alur Kerja ETL

```
┌─────────────────┐
│  Open-Meteo API │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│   EXTRACT TASK      │  ← Ambil data cuaca via HTTP Request
│   (extract.py)      │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Save to Landing    │  ← Simpan JSON mentah
│  (data/landing/)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  TRANSFORM TASK     │  ← Bersihkan & strukturkan data
│  (transform.py)     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Save to Staging    │  ← Simpan CSV bersih
│  (data/staging/)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│    LOAD TASK        │  ← UPSERT ke database
│    (load.py)        │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   PostgreSQL DB     │  ← Data siap untuk analisis
│ (weather_hourly)    │
└─────────────────────┘
```

---

## 📝 Catatan Penting

⚠️ **Hal yang Perlu Diperhatikan:**

1. **API Rate Limit**: Open-Meteo API memiliki batasan request. Jangan set schedule terlalu sering (minimal 1 jam sekali)
2. **Disk Space**: Pastikan ada cukup ruang untuk log Airflow dan file data
3. **Backup Regular**: Lakukan backup database PostgreSQL secara berkala
4. **Security**: Jangan commit file yang berisi password atau API key ke repository
5. **Timezone**: Pastikan timezone konsisten antara Airflow, PostgreSQL, dan konfigurasi API

💡 **Tips Optimasi:**

- Gunakan connection pooling untuk PostgreSQL
- Implementasi data retention policy untuk menghapus data lama
- Monitor performa query dengan `EXPLAIN ANALYZE`
- Gunakan index pada kolom `timestamp` untuk query lebih cepat

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Jika Anda ingin berkontribusi:

1. **Fork** repository ini
2. Buat **branch** baru (`git checkout -b feature/AmazingFeature`)
3. **Commit** perubahan (`git commit -m 'Add some AmazingFeature'`)
4. **Push** ke branch (`git push origin feature/AmazingFeature`)
5. Buat **Pull Request**

### Area yang Bisa Dikembangkan:
- [ ] Tambah support untuk multiple lokasi
- [ ] Implementasi data visualization dashboard
- [ ] Tambah unit tests
- [ ] Integrasi dengan weather forecast alerts
- [ ] Export data ke format lain (Parquet, Excel)

---

## 📄 Lisensi

Proyek ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk detail lebih lanjut.

---

## 👨‍💻 Author

**Nama Anda**
- GitHub: [@username](https://github.com/username)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [Open-Meteo](https://open-meteo.com/) untuk API cuaca gratis
- [Apache Airflow](https://airflow.apache.org/) untuk platform orkestrasi
- [PostgreSQL](https://www.postgresql.org/) untuk database management
- Komunitas open-source yang telah berkontribusi

---

**⭐ Jika proyek ini membantu, jangan lupa berikan star!**

---

*Terakhir diupdate: Januari 2025*
