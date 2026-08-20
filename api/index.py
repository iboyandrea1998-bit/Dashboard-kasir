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
        
        # Mencari file .db secara otomatis di folder utama
        base_dir = os.path.join(os.path.dirname(__file__), '..')
        db_files = [f for f in os.listdir(base_dir) if f.endswith('.db')]
        
        if not db_files:
            response = {
                "error": "Berkas database .db tidak ditemukan di folder utama",
                "isi_folder_saat_ini": os.listdir(base_dir)
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return

        # Menggunakan file database pertama yang ditemukan
        db_path = os.path.join(base_dir, db_files[0])

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
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
            
            response = {
                "status": "sukses", 
                "nama_file_database": db_files[0],
                "data_terbaru": data_penjualan
            }
        except Exception as e:
            response = {"error": f"Gagal membaca database {db_files[0]}: {str(e)}"}
        finally:
            if 'conn' in locals():
                conn.close()
                
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
