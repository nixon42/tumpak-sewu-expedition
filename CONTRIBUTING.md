# Contributing Guidelines

Terima kasih telah tertarik untuk berkontribusi pada pengembangan **Panduan Ekspedisi Motor Kediri ➔ Tumpak Sewu**! 🚀

---

## 🛠️ Persiapan Lingkungan Pengembangan

Proyek ini menggunakan [`uv`](https://github.com/astral-sh/uv) sebagai manajer dependensi dan virtual environment Python yang super cepat.

### 1. Prasyarat
- Python 3.10+ (disarankan 3.12+)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### 2. Setup Awal
```bash
# Clone repository
git clone https://github.com/nixon42/tumpak-sewu-expedition.git
cd tumpak-sewu-expedition

# Sinkronkan dependensi dengan uv
uv sync
```

---

## 💻 Menjalankan Server Lokal

```bash
# Jalankan web server dengan uv
uv run python main.py
```
Aplikasi akan aktif di `http://localhost:8000`.

---

## 🧪 Menjalankan Pengujian (Testing)

Sebelum membuat Pull Request, pastikan seluruh 45 test suite lulus tanpa error:

```bash
# Jalankan test suite end-to-end
uv run python -m unittest tests/test_e2e_suite.py
```

---

## 📐 Standar Kode & Panduan
1. **Zero Runtime Framework Overhead**: Kode backend menggunakan library standar Python (`http.server`, `sqlite3`, `json`) dan Jinja2 untuk rendering template.
2. **Mobile First**: Pastikan perubahan layout diuji pada layar sempit (320px–400px) untuk mencegah horizontal overflow.
3. **In-Context Voting**: Pastikan perubahan API voting tetap menjaga sinkronisasi SQLite WAL dan file JSON.
4. **Commit Message**: Gunakan konvensi [Conventional Commits](https://www.conventionalcommits.org/) (contoh: `feat: ...`, `fix: ...`, `docs: ...`).

---

## 📄 Lisensi
Dengan berkontribusi pada proyek ini, Anda setuju bahwa kontribusi Anda dilisensikan di bawah [MIT License](LICENSE).
