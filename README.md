# PORTLINK Batam (versi Flask)

Aplikasi web Flask untuk ATS praktikum: katalog produk/jasa logistik pelabuhan dan industri Batam dengan login, register, manajemen produk (CRUD), halaman utama/katalog, dan dashboard admin dasar. Ditambah alur pemesanan lengkap (keranjang, ACC admin, bukti pembayaran, riwayat, notifikasi). Data produk adalah data contoh.

## Kesesuaian dengan spesifikasi

| Yang diminta | Di mana |
|---|---|
| Fitur Login | `app/auth/routes.py`, `templates/auth/login.html` |
| Fitur Register | `app/auth/routes.py`, `templates/auth/register.html` |
| Manajemen Produk (CRUD) | `app/products/routes.py` (khusus admin), `templates/products/` |
| Halaman Utama / Katalog | `app/main/routes.py` (cari, filter kategori, halaman), `templates/main/index.html` |
| Dashboard Admin Dasar | `app/admin/routes.py`, `templates/admin/dashboard.html` (penanda hak akses admin) |
| Blueprint | `app/auth`, `app/main`, `app/products`, `app/admin` |
| OOP | Kelas model `User` dan `Product` (+ `TimestampMixin`) di `app/models.py`, dengan method seperti `set_password`, `check_password`, `is_admin` |
| Migration | Flask-Migrate (Alembic), folder `migrations/` |
| Logging | `app/__init__.py` (`RotatingFileHandler` ke `logs/app.log`) dan log pada login, register, dan CRUD |
| SQLAlchemy | Flask-SQLAlchemy, `app/models.py` |
| Template engine | Jinja2 (`templates/`, pewarisan `base.html`, macro `_macros.html`) |
| Validasi client-side | Atribut HTML5 dan `static/js/validate.js` |
| Validasi server-side | Flask-WTF/WTForms di `app/forms.py` |
| Hashing | `werkzeug.security` di `User.set_password` / `check_password` |
| Lainnya | Application factory, CSRF, kontrol akses `@admin_required`, pencegahan open redirect, error handler 403/404/500, CLI `create-admin` dan `seed`, tes otomatis di `tests/` |

## Alur pemesanan (fitur tambahan)

1. Pelanggan menambah produk ke keranjang (session), lalu mengisi data pemesan: perusahaan, kontak, WhatsApp, asal, tujuan, tanggal, catatan. Pesanan berstatus **menunggu konfirmasi** dan stok dikurangi.
2. Admin mendapat notifikasi, memeriksa data lengkap pelanggan di **Pesanan masuk**, lalu **ACC** atau **Tolak** (stok dikembalikan).
3. Setelah disetujui, pelanggan memilih metode pembayaran (simulasi) dan **mengunggah bukti pembayaran** (JPG, PNG, WebP, atau PDF, maksimal 10 MB). Jenis file dicek dari isinya, bukan hanya dari namanya.
4. Admin membuka bukti pembayaran, lalu memilih **valid** atau **tidak valid** (pelanggan bisa membayar ulang).
5. Admin mengubah status menjadi **diproses** lalu **selesai**. Pelanggan mendapat notifikasi di tiap langkah dan bisa melihat riwayat di **Pesanan saya**.

Aturan perpindahan status ditulis sebagai method pada kelas `Order` (`approve`, `reject`, `submit_payment`, `verify_payment`, `advance`, `cancel`) dan masing-masing memeriksa status asalnya. Bukti pembayaran disimpan di `instance/uploads/` (bukan folder `static`) dan hanya bisa dibuka pemilik pesanan dan admin. Produk juga bisa diberi nomor WhatsApp bisnis untuk tombol chat di katalog.

## Menjalankan

```bash
python -m venv venv
venv\Scripts\activate            # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env           # lalu isi SECRET_KEY dengan teks acak panjang (macOS/Linux: cp)
flask db upgrade                 # membuat tabel dari migration
flask create-admin               # membuat akun admin pertama (prompt username, email, password)
flask seed                       # opsional: isi contoh produk
flask run
```

Buka http://127.0.0.1:5000. Pendaftaran biasa selalu menghasilkan peran `user`; admin hanya dibuat lewat `flask create-admin`.

Menjalankan tes: `pytest`

## Struktur

```text
portlink-flask/
├── run.py                  # titik masuk
├── config.py               # konfigurasi (SECRET_KEY dari environment)
├── requirements.txt
├── migrations/             # hasil flask db init / migrate
├── app/
│   ├── __init__.py         # application factory, logging, error handler
│   ├── extensions.py       # db, migrate, login_manager, csrf
│   ├── models.py           # User, Product
│   ├── forms.py            # validasi server-side
│   ├── decorators.py       # admin_required
│   ├── cli.py              # flask create-admin, flask seed
│   ├── uploads.py          # penyimpanan bukti pembayaran (maks 10 MB, cek isi file)
│   ├── auth/ main/ products/ admin/ shop/   # blueprint (routes.py masing-masing)
│   ├── templates/
│   └── static/ (css, js)
└── tests/
```

## Mengubah model (alur migration)

```bash
# ubah app/models.py, lalu:
flask db migrate -m "keterangan perubahan"
flask db upgrade
```

## Pembagian tugas tim (isi sebelum presentasi)

Keterlibatan anggota dinilai. Tiap anggota sebaiknya mengerjakan bagiannya di branch sendiri dan melakukan commit dengan akun GitHub masing-masing, supaya riwayat commit menunjukkan siapa mengerjakan apa. Contoh pembagian:

| Anggota | Bagian | Berkas utama |
|---|---|---|
| ( Raymond Hikaru ) | Login, register, hashing, logout | `app/auth/`, `templates/auth/` |
| ( Angelic Christine ) | CRUD produk dan validasi form | `app/products/`, `app/forms.py` |
| ( Helfrin Meylin ) | Katalog, dashboard admin, hak akses | `app/main/`, `app/admin/`, `app/decorators.py` |
| ( Zelfin Dachi) | Model, migration, logging, CLI | `app/models.py`, `migrations/`, `app/cli.py` |
| ( Mitra Parningotan) | Tampilan dan tes | `templates/`, `static/`, `tests/` |

Alur kerja Git yang disarankan:
```bash
git checkout -b fitur-login        # satu branch per anggota/fitur
git add .
git commit -m "Tambah form login"  # commit kecil dan sering
git push origin fitur-login        # lalu buat Pull Request ke main
```

## Keamanan

- Password disimpan sebagai hash, bukan teks asli.
- Semua form memakai token CSRF; logout hanya lewat POST.
- Hak akses admin dicek di server (`@admin_required`), bukan hanya disembunyikan di tampilan.
- `SECRET_KEY` dibaca dari `.env`. Jangan mengunggah `.env` dan `*.db` ke GitHub (sudah ada di `.gitignore`).

## Batasan

- Pembayaran simulasi: admin memverifikasi sendiri dari bukti yang diunggah, tanpa integrasi bank atau payment gateway.
- Notifikasi hanya di dalam aplikasi (halaman Notifikasi dan angka di navbar), belum lewat email atau WhatsApp.
- Belum ada peran super admin dan penghapusan akun, belum ada timer sesi, belum ada pembatasan percobaan login (bisa ditambah Flask-Limiter), dan belum ada CAPTCHA.
- SQLite cocok untuk demo; untuk penggunaan sungguhan pakai database server (atur `DATABASE_URL`).
- Data produk dan harga adalah data fiktif.
