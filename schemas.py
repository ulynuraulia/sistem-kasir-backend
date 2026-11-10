from pydantic import BaseModel
from typing import Optional

class BarangCreate(BaseModel):
    id_kategori: int
    nama_barang: str
    harga_satuan: float
    stok: int

class BarangUpdate(BaseModel):
    id_kategori: Optional[int] = None
    nama_barang: Optional[str] = None
    harga_satuan: Optional[float] = None
    stok: Optional[int] = None