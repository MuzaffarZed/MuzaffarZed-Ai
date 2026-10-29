#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_system.py
Tester Agent: Tizim resurslari monitori uchun avtomatik unit va integratsion testlar.
Dasturchi: MuzaffarZed
"""

import sys
import json
import time
import threading
import urllib.request
from pathlib import Path

# Windows console UTF-8 handling
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add test_app to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app import get_system_metrics, HTTPServer, SystemDashboardHandler

def test_metrics_schema():
    print("🧪 Test 1: get_system_metrics() sxemasi va qiymatlarini tekshirish...")
    data = get_system_metrics()
    assert isinstance(data, dict), "Natija lug'at bo'lishi shart"
    assert "cpu" in data and "ram" in data and "disk" in data and "uptime_seconds" in data
    
    # CPU
    assert 0 <= data["cpu"]["percent"] <= 100, f"CPU foizi noto'g'ri: {data['cpu']['percent']}"
    assert data["cpu"]["cores"] > 0, f"Yadrolar soni musbat bo'lishi kerak: {data['cpu']['cores']}"

    # RAM
    assert 0 <= data["ram"]["percent"] <= 100, f"RAM foizi noto'g'ri: {data['ram']['percent']}"
    assert data["ram"]["total_gb"] > 0, "RAM umumiy hajmi 0 dan katta bo'lishi shart"
    assert data["ram"]["used_gb"] >= 0, "RAM ishlatilgan hajmi manfiy bo'lishi mumkin emas"

    # Disk
    assert 0 <= data["disk"]["percent"] <= 100, f"Disk foizi noto'g'ri: {data['disk']['percent']}"
    assert data["disk"]["total_gb"] > 0, "Disk umumiy hajmi 0 dan katta bo'lishi shart"

    # Uptime
    assert data["uptime_seconds"] >= 0, "Tizim uptime vaqti musbat bo'lishi shart"
    print("✅ Test 1 muvaffaqiyatli o'tdi!")

def test_http_api_and_static():
    print("🧪 Test 2: HTTP Server, /api/stats va / (index.html) integratsiyasi...")
    test_port = 8765
    server = HTTPServer(("127.0.0.1", test_port), SystemDashboardHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.3)

    try:
        # Test 2a: /api/stats
        api_url = f"http://127.0.0.1:{test_port}/api/stats"
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req, timeout=3) as resp:
            assert resp.status == 200, f"HTTP status kutilgan 200 emas: {resp.status}"
            content_type = resp.headers.get("Content-Type", "")
            assert "application/json" in content_type, f"Content-Type JSON emas: {content_type}"
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            assert data["status"] == "success"
            assert "cpu" in data

        # Test 2b: / (index.html)
        home_url = f"http://127.0.0.1:{test_port}/"
        with urllib.request.urlopen(home_url, timeout=3) as resp:
            assert resp.status == 200, f"HTTP status kutilgan 200 emas: {resp.status}"
            html = resp.read().decode("utf-8")
            assert "System Monitor Dashboard" in html, "HTML sarlavhasi topilmadi"
            assert "Dasturchi: MuzaffarZed" in html, "Mualliflik imzosi topilmadi"

        print("✅ Test 2 muvaffaqiyatli o'tdi!")
    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    test_metrics_schema()
    test_http_api_and_static()
    print("🎉 Barcha testlar (Unit + Integration) 100% muvaffaqiyatli yakunlandi!")
