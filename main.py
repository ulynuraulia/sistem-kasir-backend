import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from mangum import Mangum

# Load environment variables dari .env jika dijalankan secara lokal
load_dotenv()

app = FastAPI(title="API Sistem Kasir Toko", version="1.0.0")

# Konfigurasi Database PostgreSQL (Mendukung DATABASE_URL Vercel atau lokal)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    try:
        if DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        else:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "sistem_kasir"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", ""),
                port=os.getenv("DB_PORT", "5432"),
                cursor_factory=RealDictCursor
            )
        return conn
    except Exception as e:
        print(f"Koneksi database gagal: {e}")
        raise e

# --- PYDANTIC MODELS (Schemas) ---

class BarangCreate(BaseModel):
    nama_barang: str
    harga: float
    stok: int
    id_kategori: int

class BarangUpdate(BaseModel):
    nama_barang: Optional[str] = None
    harga: Optional[float] = None
    stok: Optional[int] = None
    id_kategori: Optional[int] = None

class DetailTransaksiCreate(BaseModel):
    id_barang: int
    jumlah: int
    harga_saat_ini: float
    subtotal: float

class TransaksiCreate(BaseModel):
    id_kasir: int
    total_harga: float
    detail: List[DetailTransaksiCreate]

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"message": "Selamat datang di Backend Sistem Kasir FastAPI!"}

@app.get("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        cursor.close()
        conn.close()
        return {
            "message": "Koneksi database PostgreSQL sukses!",
            "version": db_version['version']
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal terhubung ke database: {str(e)}"
        )

# --- CRUD BARANG ---

@app.get("/barang")
def get_semua_barang():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barang;")
    barang = cursor.fetchall()
    cursor.close()
    conn.close()
    return barang

@app.post("/barang", status_code=status.HTTP_201_CREATED)
def tambah_barang(data: BarangCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO barang (nama_barang, harga, stok, id_kategori)
        VALUES (%s, %s, %s, %s) RETURNING id_barang;
        """,
        (data.nama_barang, data.harga, data.stok, data.id_kategori)
    )
    new_id = cursor.fetchone()['id_barang']
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Barang berhasil ditambahkan", "id_barang": new_id}

@app.put("/barang/{id_barang}")
def update_barang(id_barang: int, data: BarangUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Cek apakah barang ada
    cursor.execute("SELECT * FROM barang WHERE id_barang = %s;", (id_barang,))
    barang_lama = cursor.fetchone()
    if not barang_lama:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
    
    nama_barang = data.nama_barang if data.nama_barang is not None else barang_lama['nama_barang']
    harga = data.harga if data.harga is not None else barang_lama['harga']
    stok = data.stok if data.stok is not None else barang_lama['stok']
    id_kategori = data.id_kategori if data.id_kategori is not None else barang_lama['id_kategori']

    cursor.execute(
        """
        UPDATE barang SET nama_barang = %s, harga = %s, stok = %s, id_kategori = %s
        WHERE id_barang = %s;
        """,
        (nama_barang, harga, stok, id_kategori, id_barang)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Barang dengan ID {id_barang} berhasil diperbarui"}

@app.delete("/barang/{id_barang}")
def hapus_barang(id_barang: int):
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
    return {"message": f"Barang dengan ID {id_barang} berhasil dihapus"}

# --- TRANSAKSI KASIR ---

@app.post("/transaksi", status_code=status.HTTP_201_CREATED)
def buat_transaksi(data: TransaksiCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert ke tabel transaksi utama
        cursor.execute(
            """
            INSERT INTO transaksi (id_kasir, tanggal, total_harga)
            VALUES (%s, NOW(), %s) RETURNING id_transaksi;
            """,
            (data.id_kasir, data.total_harga)
        )
        id_transaksi = cursor.fetchone()['id_transaksi']

        # Insert setiap detail transaksi dan kurangi stok barang
        for item in data.detail:
            cursor.execute(
                """
                INSERT INTO detail_transaksi (id_transaksi, id_barang, jumlah, harga_saat_ini, subtotal)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (id_transaksi, item.id_barang, item.jumlah, item.harga_saat_ini, item.subtotal)
            )
            # Mengurangi stok barang secara otomatis
            cursor.execute(
                """
                UPDATE barang SET stok = stok - %s WHERE id_barang = %s;
                """,
                (item.jumlah, item.id_barang)
            )

        conn.commit()
        cursor.close()
        conn.close()
        return {
            "message": "Transaksi berhasil disimpan",
            "id_transaksi": id_transaksi,
            "total_harga": data.total_harga
        }
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gagal memproses transaksi: {str(e)}"
        )

# Handler Mangum wajib untuk Vercel Serverless Function
handler = Mangum(app)