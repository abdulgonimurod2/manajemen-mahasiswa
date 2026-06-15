# Manajemen Data Mahasiswa (REST API + Vanilla JS)

Aplikasi web fullstack Manajemen Data Mahasiswa menggunakan Python (FastAPI) sebagai backend dan HTML/JS Vanilla dengan Bootstrap 5 sebagai frontend. Semua data CRUD dilakukan lewat API dan disimpan ke file `students.json`.

## Fitur Tersedia:
- Login Admin (Token Sesi Frontend)
- Create, Read, Update, Delete data mahasiswa
- Pencarian menggunakan 3 jenis algoritma: `Linear Search`, `Binary Search`, `Sequential Search`.
- Pengurutan menggunakan 5 jenis algoritma: `Bubble Sort`, `Selection Sort`, `Insertion Sort`, `Merge Sort`, `Shell Sort`.
- Semua fungsionalitas Backend mencatat waktu `execution_time_ms` dan kompleksitas ruang/waktu.

## Persiapan & Syarat Lingkungan Lokal
- Python 3.9+
- `pip`

## Cara Instalasi & Menjalankan di Local
1. Unduh atau git clone repository ini lalu arahkan Terminal ke folder utama.
2. Pasang library Python untuk Fast API:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan Web Server menggunakan Uvicorn secara real-time reload:
   ```bash
   uvicorn api.index:app --reload
   ```
4. Buka Browser (Chrome / Edge / dll) menuju alamat `http://localhost:8000`.
5. Untuk mencoba fitur, login menggunakan Admin:
   - **Username:** `admin`
   - **Password:** `Admin123`

## Catatan:
- Pastikan folder dan permission direktori lokal saat menjalankan server mencukupi karena file backend akan menulis/update ke path lokal `data/students.json`.
- Seluruh tema UI disesuaikan menjadi Light Modern Theme.
