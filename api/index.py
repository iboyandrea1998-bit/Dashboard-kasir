import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Data transaksi langsung ditulis di dalam kode agar aman dari file corrupt
        data_penjualan = [
            {"no_faktur": "TRX-20260819-001", "total_belanja": "Rp 45,500", "jam_transaksi": "2026-08-19 08:12:34"},
            {"no_faktur": "TRX-20260819-002", "total_belanja": "Rp 125,000", "jam_transaksi": "2026-08-19 09:45:12"},
            {"no_faktur": "TRX-20260819-003", "total_belanja": "Rp 23,000", "jam_transaksi": "2026-08-19 11:20:01"},
            {"no_faktur": "TRX-20260819-004", "total_belanja": "Rp 67,000", "jam_transaksi": "2026-08-19 14:05:55"},
            {"no_faktur": "TRX-20260819-005", "total_belanja": "Rp 15,000", "jam_transaksi": "2026-08-19 16:30:22"}
        ]
        
        response = {
            "status": "sukses",
            "gerai": "Alfamart Cipageran",
            "pesan": "Aplikasi Web Kasir Berhasil Online 100%",
            "data_terbaru": data_penjualan
        }
                
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
        return
