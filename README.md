# Sistem Kasir Toko - Backend API

## 1. Deskripsi Proyek
Sistem Kasir Toko API adalah aplikasi REST API yang digunakan untuk mengelola data kategori barang, barang, kasir, transaksi, dan detail transaksi. Aplikasi dibuat menggunakan Python dengan framework FastAPI dan database PostgreSQL.
Proyek ini menerapkan operasi CRUD (Create, Read, Update, Delete) dan di-deploy menggunakan Vercel agar dapat diakses secara online.

## 2. Teknologi yang Digunakan
- Python
- FastAPI
- PostgreSQL
- Vercel sebagai platform deployment
- Git dan GitHub
- Swagger UI untuk pengujian API

## 3. Struktur Database
Database terdiri dari lima tabel:
1. **kategori**: menyimpan ID kategori dan nama kategori.
2. **barang**: menyimpan ID barang, ID kategori (Foreign Key), nama barang, harga satuan, dan stok.
3. **kasir**: menyimpan ID kasir, nama kasir, dan username.
4. **transaksi**: menyimpan ID transaksi, ID kasir (Foreign Key), tanggal transaksi, dan total harga.
5. **detail_transaksi**: menyimpan ID detail, ID transaksi (Foreign Key), ID barang (Foreign Key), jumlah beli, dan subtotal.

### Relasi Antar Tabel
- `kategori` berelasi dengan `barang` melalui `id_kategori`.
- `kasir` berelasi dengan `transaksi` melalui `id_kasir`.
- `transaksi` berelasi dengan `detail_transaksi` melalui `id_transaksi`.
- `barang` berelasi dengan `detail_transaksi` melalui `id_barang`.

## 4. Daftar Endpoint API
| Metode | Endpoint | Fungsi |
|---|---|---|
| GET | / | Memeriksa status server API |
| GET | /barang | Menampilkan seluruh daftar barang |
| POST | /barang | Menambahkan data barang baru |
| GET | /barang/{id_barang} | Menampilkan detail barang berdasarkan ID |
| PUT | /barang/{id_barang} | Memperbarui data barang |
| DELETE | /barang/{id_barang} | Menghapus data barang |

## 5. URL Proyek
- **GitHub Repository:** 
https://github.com/ulynuraulia/sistem-kasir-backend
- **Deployment URL:** 
https://sistem-kasir-backend.vercel.app/
- **Dokumentasi API:** 
https://sistem-kasir-backend.vercel.app/docs

## 6. Cara Menjalankan API Secara Lokal
### Persyaratan
- Python
- Git
- Database PostgreSQL yang dapat diakses
### Langkah Menjalankan
1. Clone repositori GitHub:
```bash
git clone [https://github.com/ulynuraulia/sistem-kasir-backend.git](https://github.com/ulynuraulia/sistem-kasir-backend.git)
