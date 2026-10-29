#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app.py - System Resource Monitor Backend
Ponytail standartida: eng kam yangi kod, standart http.server va psutil.
Dasturchi: MuzaffarZed
"""

import json
import time
import psutil
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

PUBLIC_DIR = Path(__file__).resolve().parent / "public"

def get_system_metrics():
    """Tizim ko'rsatkichlarini real vaqt rejimida yig'uvchi optimal funksiya."""
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_cores = psutil.cpu_count(logical=True)
    
    vm = psutil.virtual_memory()
    ram_total_gb = round(vm.total / (1024 ** 3), 2)
    ram_used_gb = round(vm.used / (1024 ** 3), 2)
    ram_percent = vm.percent

    disk = psutil.disk_usage('/')
    disk_total_gb = round(disk.total / (1024 ** 3), 2)
    disk_used_gb = round(disk.used / (1024 ** 3), 2)
    disk_percent = disk.percent

    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    return {
        "status": "success",
        "timestamp": time.time(),
        "cpu": {
            "percent": cpu_percent,
            "cores": cpu_cores
        },
        "ram": {
            "percent": ram_percent,
            "used_gb": ram_used_gb,
            "total_gb": ram_total_gb
        },
        "disk": {
            "percent": disk_percent,
            "used_gb": disk_used_gb,
            "total_gb": disk_total_gb
        },
        "uptime_seconds": uptime_seconds
    }

class SystemDashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/stats":
            data = json.dumps(get_system_metrics()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            super().do_GET()

def run_server(host="127.0.0.1", port=8000):
    server = HTTPServer((host, port), SystemDashboardHandler)
    print(f"🚀 System Dashboard ishga tushdi: http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server to'xtatildi.")

if __name__ == "__main__":
    run_server()
