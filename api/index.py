from fastapi import FastAPI
import sqlite3
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Selamat datang di API Dasbor Kasir Alfamart"}

@app.get("/api/penjualan")
def get_sales():
    # Jalur file database di folder utama
    db_path = os.path.join(os.path.dirname(__file__), '..', 'N152_2026-08-19_25040256_android.db')
    
    if not os.path.exists(db_path):
        return {"error": "Berkas database tidak ditemukan"}
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Mengambil 5 data transaksi kasir terbaru dari tabel tx_tsale
        cursor.execute("SELECT faktur, total_faktur, time_tx FROM tx_tsale ORDER BY time_tx DESC LIMIT 5")
        rows = cursor.fetchall()
        
        data_penjualan = []
        for row in rows:
            data_penjualan.append({
                "no_faktur": row[0],
                "total_belanja": row[1],
                "jam_transaksi": row[2]
            })
        return {"data_terbaru": data_penjualan}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
