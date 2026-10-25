from sqlalchemy import Column, Integer, String, Numeric, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Kategori(Base):
    __tablename__ = "kategori"
    id_kategori = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama_kategori = Column(String(50), nullable=False)
    deskripsi = Column(Text)

class Barang(Base):
    __tablename__ = "barang"
    id_barang = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_kategori = Column(Integer, ForeignKey("kategori.id_kategori", ondelete="RESTRICT"), nullable=False)
    nama_barang = Column(String(100), nullable=False)
    harga_satuan = Column(Numeric(12, 2), nullable=False)
    stok = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Kasir(Base):
    __tablename__ = "kasir"
    id_kasir = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama_kasir = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class Transaksi(Base):
    __tablename__ = "transaksi"
    id_transaksi = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_kasir = Column(Integer, ForeignKey("kasir.id_kasir", ondelete="RESTRICT"), nullable=False)
    tanggal_transaksi = Column(TIMESTAMP, server_default=func.now())
    total_biaya = Column(Numeric(12, 2), nullable=False, default=0)
    jumlah_bayar = Column(Numeric(12, 2), nullable=False, default=0)
    kembalian = Column(Numeric(12, 2), nullable=False, default=0)

class DetailTransaksi(Base):
    __tablename__ = "detail_transaksi"
    id_detail = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_transaksi = Column(Integer, ForeignKey("transaksi.id_transaksi", ondelete="CASCADE"), nullable=False)
    id_barang = Column(Integer, ForeignKey("barang.id_barang", ondelete="RESTRICT"), nullable=False)
    jumlah = Column(Integer, nullable=False)
    harga_saat_ini = Column(Numeric(12, 2), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)