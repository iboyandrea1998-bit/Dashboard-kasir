import json
import sqlite3
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Membuat file database baru yang dijamin tidak rusak di server Vercel
        db_path = '/tmp/kasir_clean.db'
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Membuat tabel transaksi kasir otomatis
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tx_tsale (
                    faktur TEXT,
                    total_faktur REAL,
                    time_tx TEXT
                )
            ''')
            
            # Mengecek apakah data sudah ada, jika kosong kita isi data transaksi baru
            cursor.execute("SELECT COUNT(*) FROM tx_tsale")
            if cursor.fetchone()[0] == 0:
                data_dummy = [
                    ('TRX-20260819-001', 45500.0, '2026-08-19 08:12:34'),
                    ('TRX-20260819-002', 125000.0, '2026-08-19 09:45:12'),
                    ('TRX-20260819-003', 23000.0, '2026-08-19 11:20:01'),
                    ('TRX-20260819-004', 67000.0, '2026-08-19 14:05:55'),
                    ('TRX-20260819-005', 15000.0, '2026-08-19 16:30:22')
                ]
                cursor.executemany("INSERT INTO tx_tsale VALUES (?, ?, ?)", data_dummy)
                conn.commit()
            
            # Mengambil 5 data transaksi terbaru
            cursor.execute("SELECT faktur, total_faktur, time_tx FROM tx_tsale ORDER BY time_tx DESC LIMIT 5")
            rows = cursor.fetchall()
            
            data_penjualan = []
            for row in rows:
                data_penjualan.append({
                    "no_faktur": row[0],
                    "total_belanja": f"Rp {row[1]:,}",
                    "jam_transaksi": row[2]
                })
            
            response = {
                "status": "sukses",
                "lokasi_gerai": "Alfamart Cipageran",
                "data_terbaru": data_penjualan
            }
        except Exception as e:
            response = {"error": f"Gagal memproses data kasir: {str(e)}"}
        finally:
            if 'conn' in locals():
                conn.close()
                
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
        return
