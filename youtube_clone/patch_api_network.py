with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\api_server.py', 'r', encoding='utf-8') as f:
    c = f.read().replace('\r\n', '\n')

# 1. Add import socket
old_import = "import sqlite3"
new_import = "import sqlite3\nimport socket"
if old_import in c:
    c = c.replace(old_import, new_import, 1)
    print("SUCCESS: import socket added")
else:
    print("WARNING: old_import not found")

# 2. Add /api/network-info endpoint before app.mount
old_mount = '# Mount static frontend\napp.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static")'
endpoint_code = """@app.get("/api/network-info")
def get_network_info():
    hostname = socket.gethostname()
    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
    return {
        "success": True,
        "local_ip": local_ip,
        "hostname": hostname,
        "local_url": f"http://{local_ip}:8000",
        "mdns_url": f"http://{hostname.lower()}.local:8000",
        "loopback_url": "http://localhost:8000"
    }

# Mount static frontend
app.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static")"""

if old_mount in c:
    c = c.replace(old_mount, endpoint_code, 1)
    print("SUCCESS: /api/network-info endpoint added")
else:
    print("WARNING: old_mount not found")

# 3. Update host to 0.0.0.0 and print banner
old_run = """if __name__ == "__main__":
    print("="*60)
    print("  YouTube Pro Supreme Backend (MuzaffarZed Edition)")
    print("  Manzil: http://localhost:8000")
    print("="*60)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")"""

new_run = """if __name__ == "__main__":
    hostname = socket.gethostname()
    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
    print("="*64)
    print("  YouTube Pro Supreme Backend — MuzaffarZed Edition")
    print(f"  Mahalliy PC:     http://localhost:8000")
    print(f"  Wi-Fi / Telefon: http://{local_ip}:8000")
    print(f"  mDNS Manzil:     http://{hostname.lower()}.local:8000")
    print("="*64)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")"""

if old_run in c:
    c = c.replace(old_run, new_run, 1)
    print("SUCCESS: 0.0.0.0 host binding and network banner added")
else:
    print("WARNING: old_run not found")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\api_server.py', 'w', encoding='utf-8') as f:
    f.write(c)
