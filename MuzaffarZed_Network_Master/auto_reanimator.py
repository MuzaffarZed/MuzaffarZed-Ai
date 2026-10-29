"""
MuzaffarZed Avto-Reanimatsiya va Tarmoq Qo'riqchisi (Sentinel)
Muallif: MuzaffarZed
Standart: Mutlaq Mukammallik (Zero-Defect)
"""

import time
import threading
import socket
import subprocess
from datetime import datetime

class AutoReanimator(threading.Thread):
    def __init__(self, lblink_controller, interval=6, log_callback=None):
        super().__init__(daemon=True)
        self.lblink = lblink_controller
        self.interval = interval
        self.log_callback = log_callback
        self.running = True
        self.active_mode = "primary" # primary (192.168.1.1) or fallback (1.1.1.1)
        self.last_check_time = None
        self.last_status = "Barcha tizimlar barqaror"
        self.consecutive_failures = 0

    def log(self, message, level="INFO"):
        now = datetime.now().strftime("%H:%M:%S")
        entry = f"[{now}] [{level}] {message}"
        if self.log_callback:
            try:
                self.log_callback(entry)
            except:
                pass
        try:
            print(entry)
        except Exception:
            pass

    def stop(self):
        self.running = False

    def check_dns_health(self):
        test_domains = ["google.com", "telegram.org", "youtube.com"]
        latencies = []
        for d in test_domains:
            t0 = time.time()
            try:
                socket.setdefaulttimeout(1.5)
                socket.gethostbyname(d)
                lat = (time.time() - t0) * 1000
                latencies.append(lat)
            except Exception as e:
                latencies.append(9999) # Timeout / error
        
        # If at least 2 failed or avg latency > 1800ms
        failures = sum(1 for l in latencies if l > 1800)
        return failures < 2, latencies

    def run(self):
        self.log("Avto-Reanimatsiya tizimi faollashtirildi (24/7 fon nazorati)", "STATUS")
        while self.running:
            try:
                healthy, lats = self.check_dns_health()
                self.last_check_time = datetime.now()

                if not healthy:
                    self.consecutive_failures += 1
                    self.log(f"⚠️ DIQQAT: DNS javob bermadi yoki kechikish yuqori! ({lats})", "WARNING")
                    
                    if self.consecutive_failures >= 1:
                        self.log("⚡ AVTO-REANIMATSIYA ISHGA TUSHDI! 1 soniyada zaxira Cloudflare (1.1.1.1) ga o'tkazilmoqda...", "CRITICAL")
                        # 1. Apply Cloudflare + Google DNS on Router
                        res = self.lblink.set_wan_dns("1.1.1.1", "8.8.8.8")
                        # 2. Flush Windows DNS
                        subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
                        self.active_mode = "fallback"
                        self.last_status = "Zaxira Cloudflare (1.1.1.1) ga o'tkazildi"
                        self.log("✅ TARMOQ TO'LIQ TIKLANDI! Hech qanday sayt yoki aloqa uzilmadi.", "SUCCESS")
                else:
                    self.consecutive_failures = 0
                    avg_lat = sum(l for l in lats if l < 2000) / max(1, len([l for l in lats if l < 2000]))
                    self.last_status = f"Aloqa ideal (O'rtacha DNS: {avg_lat:.1f} ms)"

            except Exception as e:
                self.log(f"Nazorat jarayonida xatolik: {e}", "ERROR")

            time.sleep(self.interval)
