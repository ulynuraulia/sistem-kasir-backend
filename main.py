from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from schemas import BarangCreate, BarangUpdate

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Sistem Kasir Toko", version="1.0.0")
from fastapi.responses import Response

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/")
def read_root():
    return {"message": "Selamat datang di API Sistem Kasir Toko!"}

@app.get("/barang", status_code=status.HTTP_200_OK)
def get_daftar_barang(db: Session = Depends(get_db)):
    barang_list = db.query(models.Barang).all()
    return {"message": "Berhasil mengambil daftar barang", "data": barang_list}

@app.get("/barang/{id_barang}", status_code=status.HTTP_200_OK)
def get_barang_by_id(id_barang: int, db: Session = Depends(get_db)):
    barang = db.query(models.Barang).filter(models.Barang.id_barang == id_barang).first()
    if not barang:
        raise HTTPException(status_code=404, detail={"error": "Barang tidak ditemukan"})
    return {"message": "Detail barang ditemukan", "data": barang}

@app.post("/barang", status_code=status.HTTP_201_CREATED)
def tambah_barang(barang_data: BarangCreate, db: Session = Depends(get_db)):
    kategori = db.query(models.Kategori).filter(models.Kategori.id_kategori == barang_data.id_kategori).first()
    if not kategori:
        raise HTTPException(status_code=400, detail={"error": "Kategori tidak valid / tidak ditemukan"})
    
    barang_baru = models.Barang(
        id_kategori=barang_data.id_kategori,
        nama_barang=barang_data.nama_barang,
        harga_satuan=barang_data.harga_satuan,
        stok=barang_data.stok
    )
    db.add(barang_baru)
    db.commit()
    db.refresh(barang_baru)
    return {"message": "Barang berhasil ditambahkan", "data": barang_baru}

@app.put("/barang/{id_barang}", status_code=status.HTTP_200_OK)
def update_barang(id_barang: int, barang_data: BarangUpdate, db: Session = Depends(get_db)):
    barang = db.query(models.Barang).filter(models.Barang.id_barang == id_barang).first()
    if not barang:
        raise HTTPException(status_code=404, detail={"error": "Barang tidak ditemukan"})
    
    if barang_data.nama_barang is not None:
        barang.nama_barang = barang_data.nama_barang
    if barang_data.harga_satuan is not None:
        barang.harga_satuan = barang_data.harga_satuan
    if barang_data.stok is not None:
        barang.stok = barang_data.stok
    if barang_data.id_kategori is not None:
        barang.id_kategori = barang_data.id_kategori

    db.commit()
    db.refresh(barang)
    return {"message": "Barang berhasil diperbarui", "data": barang}

@app.delete("/barang/{id_barang}", status_code=status.HTTP_200_OK)
def hapus_barang(id_barang: int, db: Session = Depends(get_db)):
    barang = db.query(models.Barang).filter(models.Barang.id_barang == id_barang).first()
    if not barang:
        raise HTTPException(status_code=404, detail={"error": "Barang tidak ditemukan"})
    
    db.delete(barang)
    db.commit()
    return {"message": f"Barang dengan ID {id_barang} berhasil dihapus"}