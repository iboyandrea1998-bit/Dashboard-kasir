import json
import sqlite3
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Jalur file database di folder utama (satu tingkat di atas folder api)
        db_path = os.path.join(os.path.dirname(__file__), '..', 'N152_2026-08-19_25040256_android.db')
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if not os.path.exists(db_path):
            response = {"error": "Berkas database kasir tidak ditemukan di server"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return

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
            
            response = {"status": "sukses", "data_terbaru": data_penjualan}
        except Exception as e:
            response = {"error": f"Gagal membaca data: {str(e)}"}
        finally:
            if 'conn' in locals():
                conn.close()
                
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
