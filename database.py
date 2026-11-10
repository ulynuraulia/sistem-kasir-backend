import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load file .env jika dijalankan secara lokal
load_dotenv()

# Ambil URL database dari environment variable Vercel atau .env lokal
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    try:
        # Jika menggunakan DATABASE_URL (seperti di Vercel)
        if DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        else:
            # Fallback jika dijalankan manual di lokal dengan parameter terpisah
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