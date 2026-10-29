# -*- coding: utf-8 -*-

api_path = r"C:\Users\MuzaffarZed\ai_workspace\youtube_clone\api_server.py"
with open(api_path, "r", encoding="utf-8") as f:
    code = f.read()

target = '''@app.get("/api/network-info")
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
    }'''

replacement = '''@app.get("/api/network-info")
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

    public_tunnel_url = None
    tunnel_file = os.path.join(BASE_DIR, "public_url.txt")
    if os.path.exists(tunnel_file):
        try:
            with open(tunnel_file, "r", encoding="utf-8") as tf:
                u = tf.read().strip()
                if u.startswith("https://"):
                    public_tunnel_url = u
        except Exception:
            pass

    return {
        "success": True,
        "local_ip": local_ip,
        "hostname": hostname,
        "local_url": f"http://{local_ip}:8000",
        "mdns_url": f"http://{hostname.lower()}.local:8000",
        "loopback_url": "http://localhost:8000",
        "public_tunnel_url": public_tunnel_url
    }'''

if target in code:
    code = code.replace(target, replacement)
    with open(api_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("api_server.py updated with public_tunnel_url support!")
else:
    print("Target not found in api_server.py")
