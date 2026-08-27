# 🏍️ Panduan Ekspedisi Touring Motor Kediri ➔ Tumpak Sewu 2026

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Package Manager](https://img.shields.io/badge/managed%20by-uv-purple.svg)](https://github.com/astral-sh/uv)
[![Tests](https://img.shields.io/badge/tests-45%20passed-emerald.svg)](tests/test_e2e_suite.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Aplikasi web interaktif dan panduan taktis perjalanan turing motor 1 hari (**Kediri – Lumajang PP**) untuk rombongan **4 orang (2 motor matic)** menuju **Air Terjun Tumpak Sewu** dan destinasi wisata sekitarnya.

> **🤖 Disclaimer:** *Travel plan ini disusun dengan bantuan AI. Harap hanya digunakan sebagai panduan awal (baseline) dan sesuaikan dengan kondisi fisik, cuaca, serta regulasi lalu lintas di lapangan.*

---

## 🌟 Fitur Utama

### 1. 🗺️ Visualisasi Peta Interaktif (Leaflet GIS)
- Rute lengkap Kediri ➔ Lumajang dengan visualisasi garis lintasan resolusi tinggi.
- Highlight titik elevasi kritis dan **zona waspada rem blong** (Pujon Pass 1.180 mdpl & Pronojiwo).
- Penanda (*markers*) SPBU 24 jam, rest area, pos darurat, dan spot wisata.

### 2. 🗳️ Real-Time In-Context Voting System
- Pemilihan kolektif untuk **Rute Ekspedisi (Plan 1 - Plan 4)** dan **Destinasi Kedua (Opsi A - S)**.
- Integrasi ganda: **SQLite (Mode WAL)** untuk transaksi konkuren tinggi dan sinkronisasi atomik ke **JSON**.
- Distribusi suara live dengan visualisasi bar diagram yang seimbang dan responsif.

### 3. 🧭 Destinasi Kedua (Mobile Carousel)
- Pilihan 6 destinasi wisata pelengkap (Goa Tetes, Kapas Biru, Kabut Pelangi, Dasar Lembah, Teras Semeru, Sarkawi).
- Tampilan kartu geser horizontal (*horizontal scroll-snap carousel*) dengan tombol navigasi instan pada layar HP.

### 4. 💰 Kalkulator Anggaran Dinamis
- Simulasi biaya fleksibel: tampilan **Per Orang** vs **Total Rombongan (4 Orang)**.
- Filter toggle untuk bensin (pertamax/pertalite) dan konsumsi harian.
- Perhitungan tiket masuk dan parkir otomatis berdasarkan destinasi kedua yang dipilih.

### 5. 📱 Mobile-First Ergonomic UX
- **Floating Collapsible Nav**: Tombol menu navigasi melayang `[ 🧭 Menu ]` di sudut kanan bawah layar HP yang nyaman dijangkau jempol dan bebas halangan konten.
- Layout tahan overflow horizontal (100% responsif dari layar 320px hingga 4K Ultra-wide).

### 6. 🚨 SOP Keamanan & Bahaya Rem Blong
- Standar keselamatan berkendara motor matic di turunan curam pegunungan.
- Protokol pendinginan rem (*brake fade prevention*), interval istirahat, dan kontak darurat BPBD/Polsek Lumajang & Malang.

### 7. 🎒 Checklist Persiapan Touring Interaktif
- Daftar perlengkapan pribadi, kendaraan, P3K, dan logistik darurat.
- Status checklist tersimpan otomatis secara lokal (*persistent LocalStorage*).

---

## 🛠️ Arsitektur & Teknologi

- **Backend**: Python 3.10+ dengan server ringan zero-dependency (`http.server`), thread-safe SQLite WAL, dan Jinja2 template engine.
- **Dependency & Environment Manager**: [`uv`](https://github.com/astral-sh/uv) (Astral).
- **Frontend**: Vanilla JavaScript (ES6+), Modern Semantic HTML5, Vanilla CSS3 (CSS Custom Properties & Glassmorphism).
- **Mapping Engine**: Leaflet.js v1.9.4 & OpenStreetMap Tiles.
- **Testing**: Python `unittest` + BeautifulSoup4 (45 end-to-end test suite).

---

## 🚀 Memulai Cepat (Quick Start)

### 1. Prasyarat
Pastikan Anda telah menginstal [Python](https://www.python.org/) dan [uv](https://docs.astral.sh/uv/):
```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Instalasi & Menjalankan Aplikasi
```bash
# 1. Clone repository
git clone https://github.com/your-username/tumpak-sewu-expedition.git
cd tumpak-sewu-expedition

# 2. Sinkronkan dependensi secara instan
uv sync

# 3. Jalankan server aplikasi
uv run python main.py
```

Buka peramban (*browser*) Anda di:
👉 **`http://localhost:8000`**

---

## 🧪 Menjalankan Pengujian (Testing)

Proyek ini dilengkapi dengan 45 pengujian komprehensif yang memvalidasi integritas DOM, endpoint API, kalkulasi anggaran, database SQLite, dan proteksi layout:

```bash
uv run python -m unittest tests/test_e2e_suite.py
```

---

## 📁 Struktur Direktori

```text
.
├── .editorconfig              # Standar pemformatan kode editor
├── .gitattributes             # Normalisasi line-ending Git
├── .gitignore                 # Daftar file & folder yang diabaikan Git
├── CONTRIBUTING.md            # Panduan kontribusi komunitas
├── LICENSE                    # Lisensi Open Source (MIT)
├── README.md                  # Dokumentasi utama proyek
├── database.py                # Engine database SQLite WAL & handler REST API
├── itinerary_tumpak_sewu.md   # Catatan riset taktis & spesifikasi rute
├── main.py                    # Entry point server web Jinja2
├── pyproject.toml             # Konfigurasi dependensi uv & paket Python
├── requirements.txt           # File fallback dependensi pip standar
├── uv.lock                    # Deterministic lockfile dependensi uv
├── static/
│   ├── css/
│   │   └── main.css           # Styling utama, tema gelap, & layout responsif
│   └── js/
│       └── app.js             # Engine routing Leaflet, kalkulator, & floating nav
├── templates/
│   ├── index.html             # Template HTML utama
│   └── components/            # Komponen modular Jinja2
│       ├── checklist.html     # Komponen checklist perlengkapan
│       ├── cost_calc.html     # Komponen kalkulator biaya dinamis
│       ├── destinations.html  # Komponen carousel destinasi kedua
│       ├── emergency.html     # Komponen kontak darurat & faskes
│       ├── hero_header.html   # Header hero & identitas pemilih
│       ├── safety.html        # SOP rem blong & mitigasi risiko
│       ├── unified_route.html # Peta Leaflet & perbandingan rute
│       └── vote_charts.html   # Live vote bar charts & toggle tab
└── tests/
    ├── __init__.py
    └── test_e2e_suite.py      # 45 automated test suite
```

---

## 📡 REST API Reference

| Method | Endpoint | Deskripsi | Parameter / Payload |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/votes` | Mengambil rekapitulasi data suara voting | - |
| `POST` | `/api/vote` | Mengirim suara voting rute/destinasi | `{"voter_name": "Nixon", "category": "route", "choice": "Plan 2"}` |
| `GET` | `/api/health` | Healthcheck server & konektivitas DB | - |

---

## 📄 Lisensi

Didistribusikan di bawah Lisensi MIT. Lihat file [`LICENSE`](LICENSE) untuk informasi lebih lanjut.
