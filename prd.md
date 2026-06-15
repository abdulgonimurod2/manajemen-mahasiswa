# Product Requirements Document (PRD)
## Aplikasi Web "Manajemen Data Mahasiswa"

**Versi:** 3.0.0  
**Tanggal:** 14 Juni 2026  
**Author:** Mahasiswa TI Semester 3  
**Status:** Draft  
**Platform Deployment:** Vercel (via GitHub)  
**Tech Stack:** Python + FastAPI (Backend) · HTML/JS/Bootstrap CDN (Frontend) · JSON (Penyimpanan Data)

---

## 1. Latar Belakang & Tujuan

Aplikasi ini dibuat sebagai tugas akhir mata kuliah yang menguji pemahaman mahasiswa terhadap konsep-konsep fundamental pemrograman: OOP, algoritma pencarian dan pengurutan, validasi input, penanganan error, dan file I/O. Backend menggunakan FastAPI (Python) yang di-deploy ke Vercel sebagai serverless function, sementara frontend menggunakan HTML/JS/Bootstrap CDN.

**Tujuan Utama:**
- Memenuhi seluruh 9 kriteria penilaian tugas kuliah.
- Menghasilkan aplikasi web full-stack yang dapat diakses publik via Vercel.
- Menunjukkan pemahaman OOP, algoritma, dan best practices penulisan kode Python.

---

## 2. Scope & Batasan

| In Scope | Out of Scope |
|---|---|
| CRUD data mahasiswa via REST API | Database relasional (MySQL, PostgreSQL) |
| Login admin (1 akun) | Multi-user / role management |
| Pencarian & pengurutan data | Export ke Excel/PDF |
| Validasi input via Regex (Python + JS) | Notifikasi email/SMS |
| File I/O JSON (baca/tulis di server) | Mobile native app |
| OOP Python di backend | OAuth / SSO |
| Deployment FastAPI ke Vercel | Framework frontend (React, Vue, dll) |

---

## 3. Arsitektur Sistem

```
┌──────────────────────────────────────────────────────────────┐
│                      VERCEL (Deployment)                     │
│                                                              │
│  ┌─────────────────────┐      ┌───────────────────────────┐ │
│  │  Frontend (Static)  │      │  Backend (Serverless)     │ │
│  │  index.html         │◄────►│  FastAPI (Python)         │ │
│  │  dashboard.html     │      │  /api/mahasiswa  (CRUD)   │ │
│  │  JS + Bootstrap CDN │      │  /api/auth/login          │ │
│  └─────────────────────┘      └──────────────┬────────────┘ │
│                                              │               │
│                                   ┌──────────▼──────────┐   │
│                                   │  data/              │   │
│                                   │  └── students.json  │   │
│                                   └─────────────────────┘   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                   GITHUB → VERCEL (Workflow)                 │
│                                                              │
│        git push → GitHub → Vercel auto-deploy               │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Struktur Direktori Proyek

```
manajemen-mahasiswa/
│
├── api/                              # Backend FastAPI (Vercel Serverless)
│   ├── index.py                      # Entry point FastAPI app
│   ├── models/
│   │   ├── __init__.py
│   │   └── mahasiswa.py              # Class Person, Mahasiswa, User (OOP)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── search_service.py         # Linear, Binary, Sequential Search
│   │   ├── sort_service.py           # Bubble, Selection, Insertion, Merge, Shell Sort
│   │   ├── validation_service.py     # Validasi Regex
│   │   └── file_service.py           # Baca/tulis JSON (File I/O)
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py            # POST /api/auth/login
│       └── mahasiswa_routes.py       # GET/POST/PUT/DELETE /api/mahasiswa
│
├── data/
│   └── students.json                 # Data mahasiswa (seed + live)
│
├── static/
│   ├── css/
│   │   └── style.css                 # Custom styles (override Bootstrap)
│   └── js/
│       ├── auth.js                   # Login / logout / session check
│       ├── crud.js                   # CRUD via Fetch API ke backend
│       ├── search.js                 # Trigger pencarian ke API
│       └── sort.js                   # Trigger pengurutan ke API
│
├── index.html                        # Halaman Login
├── dashboard.html                    # Halaman utama (tabel mahasiswa)
├── requirements.txt                  # Dependensi Python
├── vercel.json                       # Konfigurasi deployment Vercel
├── .gitignore                        # File yang tidak di-push ke GitHub
└── README.md                         # Dokumentasi & panduan penggunaan
```

---

## 5. Fitur & Spesifikasi Fungsional

### 5.1 Fitur Login Admin

**Deskripsi:** Satu-satunya pintu masuk ke aplikasi sebelum bisa mengakses dashboard.

**Flow:**
1. User membuka URL Vercel → diarahkan ke `index.html` (halaman login).
2. Input username & password → divalidasi format via Regex di JavaScript.
3. Fetch `POST /api/auth/login` → backend Python memvalidasi kredensial.
4. Jika cocok → simpan token/status di `sessionStorage` → redirect ke `dashboard.html`.
5. Jika gagal → tampilkan pesan error di bawah form.
6. Setiap halaman selain login mengecek `sessionStorage` — jika kosong, redirect ke login.

**Akun Admin (hardcoded di backend):**

```json
{
  "username": "admin",
  "password": "Admin@2026",
  "nama_lengkap": "Administrator Sistem"
}
```

**Endpoint:**

| Method | Endpoint | Deskripsi |
|---|---|---|
| POST | `/api/auth/login` | Validasi kredensial, return token sesi |
| POST | `/api/auth/logout` | Hapus sesi |

**Validasi Input Login (Regex — Python & JS):**
- Username: `^[a-zA-Z0-9_]{4,20}$`
- Password: `^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%])[A-Za-z\d@#$%]{6,}$`

---

### 5.2 Fitur CRUD Data Mahasiswa

**Kriteria Penilaian yang Dipenuhi:** Poin 1 (Input, Edit, Hapus, Tampilkan), Poin 2 (File I/O)

**Mekanisme Penyimpanan:**
- Semua data dibaca dari dan ditulis ke `data/students.json` oleh backend Python.
- Frontend berkomunikasi ke backend via `fetch()` (REST API).
- Setiap perubahan (tambah/edit/hapus) langsung disimpan ke file JSON di server.

**Endpoint API:**

| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/api/mahasiswa` | Ambil semua data mahasiswa |
| GET | `/api/mahasiswa/{nim}` | Ambil data by NIM |
| POST | `/api/mahasiswa` | Tambah data baru |
| PUT | `/api/mahasiswa/{nim}` | Update data mahasiswa |
| DELETE | `/api/mahasiswa/{nim}` | Hapus data mahasiswa |
| GET | `/api/mahasiswa/search` | Cari data (param: query, method, field) |
| GET | `/api/mahasiswa/sort` | Urutkan data (param: field, method, order) |

#### 5.2.1 Tampilkan Data (Read)
- Tabel responsif Bootstrap menampilkan semua data dari `GET /api/mahasiswa`.
- Kolom: No, NIM, Nama, Jurusan, Angkatan, IPK, Status, Aksi.
- Pagination (5 data per halaman, dilakukan di frontend).

#### 5.2.2 Tambah Data (Create)
- Form modal Bootstrap. Field:
  - NIM → Regex: `^\d{10}$`
  - Nama Lengkap → Regex: `^[A-Za-z\s\.]{3,50}$`
  - Jurusan → dropdown: Teknik Informatika, Sistem Informasi, Teknik Komputer
  - Angkatan → Regex: `^20[0-9]{2}$`
  - IPK → Regex: `^([0-3](\.\d{1,2})?|4(\.0{1,2})?)$`
  - Email → Regex: `^[\w\.\-]+@[\w\-]+\.\w{2,6}$`
  - No. Telepon → Regex: `^(\+62|0)[0-9]{9,12}$`
  - Status → dropdown: Aktif, Cuti, Lulus, DO

#### 5.2.3 Edit Data (Update)
- Tombol Edit → modal terisi data existing → `PUT /api/mahasiswa/{nim}`.

#### 5.2.4 Hapus Data (Delete)
- Konfirmasi dialog → `DELETE /api/mahasiswa/{nim}`.

---

### 5.3 Fitur Pencarian Data

**Kriteria Penilaian yang Dipenuhi:** Poin 4  
**Endpoint:** `GET /api/mahasiswa/search?query=<keyword>&method=<metode>&field=<field>`

| Algoritma | Deskripsi | Time Complexity |
|---|---|---|
| **Linear Search** | Iterasi satu per satu dari awal hingga akhir array | O(n) |
| **Binary Search** | Pencarian pada data terurut dengan membagi dua array | O(log n) |
| **Sequential Search** | Sama seperti Linear, berhenti di kecocokan pertama | O(n) |

**UI Pencarian:**
- Search bar + dropdown metode (Linear / Binary / Sequential) + dropdown field (NIM / Nama / Jurusan / Angkatan).
- Badge info: metode yang digunakan + waktu eksekusi (ms) dari response backend.

---

### 5.4 Fitur Pengurutan Data

**Kriteria Penilaian yang Dipenuhi:** Poin 5  
**Endpoint:** `GET /api/mahasiswa/sort?field=<field>&method=<metode>&order=<asc|desc>`

| Algoritma | Time Complexity (Avg) | Time Complexity (Worst) | Space Complexity |
|---|---|---|---|
| **Bubble Sort** | O(n²) | O(n²) | O(1) |
| **Selection Sort** | O(n²) | O(n²) | O(1) |
| **Insertion Sort** | O(n²) | O(n²) | O(1) |
| **Merge Sort** | O(n log n) | O(n log n) | O(n) |
| **Shell Sort** | O(n log n) | O(n²) | O(1) |

**UI Pengurutan:**
- Klik header kolom tabel → sort asc/desc (toggle).
- Dropdown manual pilih algoritma sort.
- Badge info: algoritma, arah sort, kompleksitas, waktu eksekusi.

---

### 5.5 OOP Design (Python)

**Kriteria Penilaian yang Dipenuhi:** Poin 3

```
Person (Base Class)
├── __init__(nama, email, no_telp)
├── get_info()          → abstract-like, di-override subclass (polimorfisme)
└── validate_email()    → shared method (enkapsulasi)

Mahasiswa(Person)
├── __init__(nim, nama, jurusan, angkatan, ipk, email, no_telp, status)
├── get_info()          → override (polimorfisme)
├── to_dict()           → serialisasi ke JSON
└── validate_nim()      → enkapsulasi validasi NIM

User(Person)
├── __init__(username, password, nama_lengkap)
├── get_info()          → override (polimorfisme)
└── check_password()    → enkapsulasi autentikasi
```

**Penerapan Prinsip OOP:**
- **Enkapsulasi:** Atribut private (`_nim`, `_ipk`) dengan getter/setter + validasi internal.
- **Pewarisan:** `Mahasiswa` dan `User` mewarisi `Person`.
- **Polimorfisme:** `get_info()` di-override tiap subclass dengan output berbeda.

---

### 5.6 Validasi Input (Regex)

**Kriteria Penilaian yang Dipenuhi:** Poin 6

| Field | Pattern Regex | Keterangan |
|---|---|---|
| NIM | `^\d{10}$` | Tepat 10 digit angka |
| Nama | `^[A-Za-z\s\.]{3,50}$` | Huruf, spasi, titik, 3–50 karakter |
| Email | `^[\w\.\-]+@[\w\-]+\.\w{2,6}$` | Format email standar |
| No. Telepon | `^(\+62\|0)[0-9]{9,12}$` | Format nomor Indonesia |
| Angkatan | `^20[0-9]{2}$` | Tahun 2000–2099 |
| IPK | `^([0-3](\.\d{1,2})?|4(\.0{1,2})?)$` | Range 0.00–4.00 |
| Username | `^[a-zA-Z0-9_]{4,20}$` | Alphanumeric + underscore |
| Password | `^(?=.*[A-Z])(?=.*\d)(?=.*[@#\$%])[A-Za-z\d@#\$%]{6,}$` | Min 1 kapital, 1 angka, 1 simbol |

Validasi dilakukan di **dua sisi**:
- **Backend Python** (`validation_service.py`): modul `re`, sebagai gate terakhir sebelum data disimpan.
- **Frontend JavaScript**: real-time saat user mengetik (UX feedback).

---

### 5.7 Penanganan Error (Try-Catch & Exception)

**Kriteria Penilaian yang Dipenuhi:** Poin 7

**Custom Exception Classes (Python):**
```python
class AppException(Exception): pass
class ValidationError(AppException): pass
class DataNotFoundError(AppException): pass
class DuplicateNIMError(AppException): pass
class FileIOError(AppException): pass
class AuthenticationError(AppException): pass
```

**Skenario Error & HTTP Response:**

| Skenario | Exception | HTTP Status | Pesan |
|---|---|---|---|
| NIM sudah terdaftar | `DuplicateNIMError` | 409 Conflict | "NIM sudah terdaftar dalam sistem" |
| Data tidak ditemukan | `DataNotFoundError` | 404 Not Found | "Data mahasiswa tidak ditemukan" |
| Format input tidak valid | `ValidationError` | 422 Unprocessable | "Format [field] tidak valid" |
| Gagal baca/tulis file | `FileIOError` | 500 Server Error | "Gagal membaca/menulis file data" |
| Login gagal | `AuthenticationError` | 401 Unauthorized | "Username atau password salah" |
| JSON corrupt | `json.JSONDecodeError` | 500 Server Error | "File data tidak dapat dibaca" |

**Di Frontend JavaScript:**
- `try-catch` pada setiap `fetch()`.
- Toast Bootstrap ditampilkan jika response bukan 2xx.

---

### 5.8 Estimasi Time Complexity

**Kriteria Penilaian yang Dipenuhi:** Poin 8

Panel collapsible di bawah tabel dashboard, diupdate setiap operasi search/sort:

| Operasi | Metode | Time Complexity | Space Complexity |
|---|---|---|---|
| Tampilkan semua data | Baca JSON + render | O(n) | O(n) |
| Tambah mahasiswa | Append + tulis JSON | O(1) append | O(n) |
| Hapus mahasiswa | Linear search + remove | O(n) | O(n) |
| Cari (Linear/Sequential) | Iterasi array | O(n) | O(1) |
| Cari (Binary) | Divide & conquer | O(log n) | O(1) |
| Urut (Bubble/Selection/Insertion) | Nested loop | O(n²) | O(1) |
| Urut (Merge Sort) | Recursive split & merge | O(n log n) | O(n) |
| Urut (Shell Sort) | Gap sequence | O(n log n) avg | O(1) |

---

### 5.9 Data Dummy Mahasiswa (students.json)

```json
[
  {"nim": "2024110001", "nama": "Zephyra Aldaine", "jurusan": "Teknik Informatika", "angkatan": 2024, "ipk": 3.85, "email": "zephyra.aldaine@student.ac.id", "no_telp": "081234567890", "status": "Aktif"},
  {"nim": "2024110002", "nama": "Corvyn Duskwell", "jurusan": "Sistem Informasi", "angkatan": 2024, "ipk": 3.72, "email": "corvyn.duskwell@student.ac.id", "no_telp": "082345678901", "status": "Aktif"},
  {"nim": "2023110003", "nama": "Isolde Marvyn", "jurusan": "Teknik Komputer", "angkatan": 2023, "ipk": 3.45, "email": "isolde.marvyn@student.ac.id", "no_telp": "083456789012", "status": "Aktif"},
  {"nim": "2023110004", "nama": "Theron Quillan", "jurusan": "Teknik Informatika", "angkatan": 2023, "ipk": 3.90, "email": "theron.quillan@student.ac.id", "no_telp": "084567890123", "status": "Aktif"},
  {"nim": "2022110005", "nama": "Vesper Cailwyn", "jurusan": "Sistem Informasi", "angkatan": 2022, "ipk": 2.95, "email": "vesper.cailwyn@student.ac.id", "no_telp": "085678901234", "status": "Cuti"},
  {"nim": "2022110006", "nama": "Elowen Draxford", "jurusan": "Teknik Komputer", "angkatan": 2022, "ipk": 3.60, "email": "elowen.draxford@student.ac.id", "no_telp": "086789012345", "status": "Aktif"},
  {"nim": "2021110007", "nama": "Caelum Wyndris", "jurusan": "Teknik Informatika", "angkatan": 2021, "ipk": 3.20, "email": "caelum.wyndris@student.ac.id", "no_telp": "087890123456", "status": "Aktif"},
  {"nim": "2021110008", "nama": "Lyria Stonveth", "jurusan": "Sistem Informasi", "angkatan": 2021, "ipk": 3.78, "email": "lyria.stonveth@student.ac.id", "no_telp": "088901234567", "status": "Aktif"},
  {"nim": "2020110009", "nama": "Ryndal Ashcroft", "jurusan": "Teknik Komputer", "angkatan": 2020, "ipk": 3.10, "email": "ryndal.ashcroft@student.ac.id", "no_telp": "089012345678", "status": "Lulus"},
  {"nim": "2020110010", "nama": "Sylvara Noctwyn", "jurusan": "Teknik Informatika", "angkatan": 2020, "ipk": 3.35, "email": "sylvara.noctwyn@student.ac.id", "no_telp": "081123456789", "status": "Lulus"}
]
```

---

## 6. Spesifikasi UI/UX

### Halaman 1: Login (`index.html`)
- Background gradient gelap.
- Card login terpusat dengan shadow.
- Field username & password + ikon Bootstrap Icons.
- Tombol Login (`btn-primary`).
- Alert merah jika login gagal (dari response API).
- Validasi real-time per field (border merah + teks error kecil).

### Halaman 2: Dashboard (`dashboard.html`)
- **Navbar:** Nama sistem + nama admin + tombol Logout.
- **Kartu Statistik:** Total Mahasiswa, Aktif, Cuti, Lulus (dari `GET /api/mahasiswa`).
- **Toolbar:** Search bar + dropdown metode + dropdown field + tombol Tambah + dropdown sort.
- **Tabel Responsif Bootstrap:**
  - Header kolom klikable untuk sort.
  - Badge warna Status (Aktif=hijau, Cuti=kuning, Lulus=biru, DO=merah).
  - Tombol Edit + Hapus per baris.
- **Panel Info (collapsible):** Tabel time complexity operasi terakhir.
- **Pagination** di bawah tabel.

### Modal Form Tambah/Edit
- Modal Bootstrap ukuran `lg`, layout dua kolom.
- Validasi real-time, tombol Simpan + Batal.

---

## 7. Guidelines & Best Practices

**Kriteria Penilaian yang Dipenuhi:** Poin 9

### Penamaan (Python)
```python
# Variabel & fungsi → snake_case
nama_mahasiswa = "Zephyra Aldaine"
def cari_linear(data: list, keyword: str) -> list: ...

# Class → PascalCase
class Mahasiswa(Person): ...

# Konstanta → UPPER_SNAKE_CASE
MAX_IPK = 4.0
FILE_PATH_STUDENTS = "data/students.json"
```

### Penamaan (JavaScript)
```javascript
// Variabel & fungsi → camelCase
let dataMahasiswa = [];
function tampilkanTabel(data) { ... }

// Konstanta → UPPER_SNAKE_CASE
const API_BASE_URL = "/api";
const MAX_PER_PAGE = 5;
```

### Modularisasi
- Satu file Python = satu tanggung jawab (models, services, routes terpisah).
- Fungsi tidak lebih dari 30 baris.
- JS dipisah per domain (auth.js, crud.js, search.js, sort.js).

### Format Komentar Python (Docstring)
```python
def merge_sort(data: list, field: str) -> list:
    """
    Mengurutkan data mahasiswa menggunakan Merge Sort.

    Time Complexity  : O(n log n) — best, average, worst case
    Space Complexity : O(n)

    Args:
        data  : List dict mahasiswa yang akan diurutkan.
        field : Nama field sebagai kunci pengurutan (nim, nama, ipk, dll).

    Returns:
        List dict mahasiswa yang sudah terurut ascending.
    """
```

---

## 8. Setup GitHub & Deployment Vercel

### Langkah-langkah:
```
1. Buat repository baru di GitHub (public)
2. git init
3. git add .
4. git commit -m "initial commit: manajemen data mahasiswa"
5. git remote add origin https://github.com/<username>/<repo>.git
6. git push -u origin main
7. Login ke vercel.com → "Add New Project"
8. Import repository dari GitHub
9. Framework Preset: Other
10. Klik Deploy → tunggu selesai
11. Setiap git push ke main → Vercel auto-redeploy otomatis
```

### `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "api/index.py" },
    { "src": "/(.*)", "dest": "/$1" }
  ]
}
```

### `.gitignore`:
```
__pycache__/
*.py[cod]
.env
.DS_Store
node_modules/
venv/
.venv/
*.egg-info/
```

---

## 9. Dependensi

### Python (`requirements.txt`)
```
fastapi==0.111.0
uvicorn==0.29.0
```

### Frontend
- Bootstrap 5.3 (CDN)
- Bootstrap Icons (CDN)
- Vanilla JavaScript ES6+

### Cara Install & Jalankan Lokal
```bash
# Install dependensi
pip install -r requirements.txt

# Jalankan server lokal
uvicorn api.index:app --reload

# Buka browser
# http://localhost:8000
```

---

## 10. Acceptance Criteria

| No | Fitur | Kriteria |
|---|---|---|
| 1 | Login | Berhasil masuk dengan akun admin via API |
| 2 | Login | Menampilkan error jika kredensial salah (401) |
| 3 | Tampilkan Data | Tabel menampilkan 10 data dari `GET /api/mahasiswa` |
| 4 | Tambah Data | `POST /api/mahasiswa` menyimpan ke JSON |
| 5 | Edit Data | `PUT /api/mahasiswa/{nim}` mengupdate JSON |
| 6 | Hapus Data | `DELETE /api/mahasiswa/{nim}` menghapus dari JSON |
| 7 | Pencarian | Ketiga metode search berfungsi via API |
| 8 | Pengurutan | Semua 5 algoritma sort berfungsi via API |
| 9 | Validasi | Regex dijalankan di Python backend + JS frontend |
| 10 | Error Handling | Custom exception + HTTP status code yang tepat |
| 11 | OOP | Class Person, Mahasiswa, User terimplementasi |
| 12 | Time Complexity | Info kompleksitas tampil di UI dari response API |
| 13 | Deployment | Aplikasi live dan dapat diakses via URL Vercel |
| 14 | Lokal | `uvicorn api.index:app --reload` berjalan tanpa error |

---

## 11. Rencana Pengerjaan

| Fase | Task | Estimasi |
|---|---|---|
| **1** | Setup folder + vercel.json + requirements.txt + .gitignore | 20 menit |
| **2** | OOP: models/mahasiswa.py (Person, Mahasiswa, User) | 1 jam |
| **3** | services: file_service.py + validation_service.py | 45 menit |
| **4** | services: search_service.py + sort_service.py | 1.5 jam |
| **5** | routes: auth_routes.py + mahasiswa_routes.py | 1 jam |
| **6** | api/index.py (entry point, register routes, CORS) | 30 menit |
| **7** | Frontend: index.html (login) + auth.js | 45 menit |
| **8** | Frontend: dashboard.html + tabel + pagination | 1 jam |
| **9** | Frontend: crud.js + search.js + sort.js | 1 jam |
| **10** | Testing lokal + push GitHub + deploy Vercel | 30 menit |

**Total Estimasi:** ±8,5 jam

---

*Dokumen ini bersifat living document — dapat diperbarui seiring perkembangan pengerjaan proyek.*