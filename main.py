from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from database import get_db_connection

app = FastAPI(
    title="API Sistem Kasir Toko",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Endpoint Root / Utama
@app.get("/")
def read_root():
    return {"message": "API Sistem Kasir Toko Terhubung ke PostgreSQL Aktif!"}

# 2. Endpoint untuk mengetes koneksi database secara langsung
@app.get("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        db_version = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"message": "Koneksi database PostgreSQL sukses!", "version": db_version}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Endpoint untuk melihat daftar kategori
@app.get("/kategori")
def get_kategori():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kategori;")
        kategori_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"data_kategori": kategori_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# CRUD BARANG (GET, POST, PUT, DELETE)
# ==========================================

class BarangCreate(BaseModel):
    id_kategori: int = Field(default=1, description="ID Kategori yang valid (misal: 1 atau 2)")
    nama_barang: str = Field(default="Nama Barang", description="Nama produk")
    harga_satuan: float = Field(default=1000.0, description="Harga satuan barang")
    stok: int = Field(default=10, description="Jumlah stok awal")

class BarangUpdate(BaseModel):
    id_kategori: Optional[int] = Field(default=1, description="ID Kategori valid")
    nama_barang: Optional[str] = Field(default="Nama Barang Baru", description="Nama produk")
    harga_satuan: Optional[float] = Field(default=1000.0, description="Harga satuan baru")
    stok: Optional[int] = Field(default=10, description="Stok baru")

# Get Daftar Barang
@app.get("/barang")
def get_barang():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM barang ORDER BY id_barang ASC;")
        barang_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"data_barang": barang_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Barang Berdasarkan ID
@app.get("/barang/{id_barang}")
def get_barang_by_id(id_barang: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM barang WHERE id_barang = %s;", (id_barang,))
        barang = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not barang:
            raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
        return {"data_barang": barang}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Tambah Barang Baru (POST)
@app.post("/barang")
def tambah_barang(data: BarangCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO barang (id_kategori, nama_barang, harga_satuan, stok)
            VALUES (%s, %s, %s, %s) RETURNING id_barang;
            """,
            (data.id_kategori, data.nama_barang, data.harga_satuan, data.stok)
        )
        new_id = cursor.fetchone()['id_barang']
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Barang berhasil ditambahkan!", "id_barang": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update Barang (PUT)
@app.put("/barang/{id_barang}")
def update_barang(id_barang: int, data: BarangUpdate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM barang WHERE id_barang = %s;", (id_barang,))
        barang_lama = cursor.fetchone()
        if not barang_lama:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Barang tidak ditemukan")

        kategori_baru = data.id_kategori if (data.id_kategori is not None and data.id_kategori != 0) else barang_lama['id_kategori']
        nama_baru = data.nama_barang if (data.nama_barang is not None and data.nama_barang != "string") else barang_lama['nama_barang']
        harga_baru = data.harga_satuan if (data.harga_satuan is not None and data.harga_satuan != 0) else barang_lama['harga_satuan']
        stok_baru = data.stok if data.stok is not None else barang_lama['stok']

        cursor.execute(
            """
            UPDATE barang 
            SET id_kategori = %s,
                nama_barang = %s,
                harga_satuan = %s,
                stok = %s
            WHERE id_barang = %s;
            """,
            (kategori_baru, nama_baru, harga_baru, stok_baru, id_barang)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Barang dengan ID {id_barang} berhasil diperbarui!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Hapus Barang (DELETE)
@app.delete("/barang/{id_barang}")
def hapus_barang(id_barang: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM barang WHERE id_barang = %s;", (id_barang,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Barang tidak ditemukan")

        cursor.execute("DELETE FROM barang WHERE id_barang = %s;", (id_barang,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Barang dengan ID {id_barang} berhasil dihapus!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# FITUR TRANSAKSI KASIR
# ==========================================

class ItemTransaksi(BaseModel):
    id_barang: int = Field(default=1)
    jumlah: int = Field(default=1)

class TransaksiCreate(BaseModel):
    id_kasir: int = Field(default=1)
    jumlah_bayar: float = Field(default=50000.0)
    items: List[ItemTransaksi]

@app.post("/transaksi")
def buat_transaksi(data: TransaksiCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        total_biaya = 0
        detail_data = []

        for item in data.items:
            cursor.execute("SELECT harga_satuan, stok FROM barang WHERE id_barang = %s;", (item.id_barang,))
            barang = cursor.fetchone()
            
            if not barang:
                raise HTTPException(status_code=404, detail=f"Barang dengan ID {item.id_barang} tidak ditemukan")
            
            if barang['stok'] < item.jumlah:
                raise HTTPException(status_code=400, detail=f"Stok barang ID {item.id_barang} tidak mencukupi!")

            harga_satuan = float(barang['harga_satuan'])
            subtotal = harga_satuan * item.jumlah
            total_biaya += subtotal

            detail_data.append({
                "id_barang": item.id_barang,
                "jumlah": item.jumlah,
                "harga_saat_ini": harga_satuan,
                "subtotal": subtotal
            })

        if data.jumlah_bayar < total_biaya:
            raise HTTPException(status_code=400, detail="Uang pembayaran kurang dari total biaya!")

        kembalian = data.jumlah_bayar - total_biaya

        cursor.execute(
            """
            INSERT INTO transaksi (id_kasir, total_biaya, jumlah_bayar, kembalian) 
            VALUES (%s, %s, %s, %s) RETURNING id_transaksi;
            """,
            (data.id_kasir, total_biaya, data.jumlah_bayar, kembalian)
        )
        id_transaksi = cursor.fetchone()['id_transaksi']

        for detail in detail_data:
            cursor.execute(
                """
                INSERT INTO detail_transaksi (id_transaksi, id_barang, jumlah, harga_saat_ini, subtotal)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (id_transaksi, detail['id_barang'], detail['jumlah'], detail['harga_saat_ini'], detail['subtotal'])
            )
            
            cursor.execute(
                """
                UPDATE barang SET stok = stok - %s WHERE id_barang = %s;
                """,
                (detail['jumlah'], detail['id_barang'])
            )

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": "Transaksi berhasil disimpan dan stok diperbarui!",
            "id_transaksi": id_transaksi,
            "total_biaya": total_biaya,
            "jumlah_bayar": data.jumlah_bayar,
            "kembalian": kembalian
        }

    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))