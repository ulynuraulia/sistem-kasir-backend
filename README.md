# Sistem Kasir Toko - Backend API

REST API untuk sistem kasir toko yang dibangun menggunakan **Python (FastAPI)** dan **PostgreSQL**. Project ini dibuat untuk memenuhi Tugas Akhir Learning Labs Backend Development.

## 📊 Skema Database (5 Tabel)
Project ini menggunakan 5 tabel relasional yang saling berelasi:
1. `kategori` - Master kategori barang
2. `barang` - Data barang (Foreign Key ke `kategori`)
3. `kasir` - Data akun kasir
4. `transaksi` - Header riwayat transaksi (Foreign Key ke `kasir`)
5. `detail_transaksi` - Tabel pivot / relasi many-to-many antara `transaksi` dan `barang`

## 🚀 Link Deployment
- **URL Vercel:** *(Akan diisi setelah deploy ke Vercel)*
- **Dokumentasi Otomatis (Swagger):** `https://nama-project.vercel.app/docs`

---

## 📄 Daftar Endpoint API

### 1. Ambil Seluruh Daftar Barang (`getDaftarBarang`)
- **Method** : `GET`
- **URL** : `https://nama-project.vercel.app/barang`
- **Deskripsi** : Menampilkan seluruh daftar barang yang tersedia.
- **Response Sukses (200)**:
  ```json
  {
    "message": "Berhasil mengambil daftar barang",
    "data": [
      {
        "id_barang": 1,
        "id_kategori": 1,
        "nama_barang": "Minyak Goreng 1L",
        "harga_satuan": 18000,
        "stok": 50
      }
    ]
  }