import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Fungsi untuk mengambil koneksi database PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Koneksi database gagal: {str(e)}")
        raise 