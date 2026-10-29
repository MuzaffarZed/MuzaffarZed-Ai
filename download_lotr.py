import urllib.request
import ssl
import os
import sys
import time

url = 'https://arena-files.bfmeladder.com/downloads/AllInOneLauncherSetup.exe'
lotr_dir = os.path.join("D:\\", "KANPIYUTER O'YINLARI", "LOTR_Uzuklar_Hukmdori")
os.makedirs(lotr_dir, exist_ok=True)
dest = os.path.join(lotr_dir, "AllInOneLauncherSetup.exe")

ctx = ssl._create_unverified_context()
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

print(f"Target file: {dest}")
print(f"Downloading from: {url}")
t0 = time.time()
with urllib.request.urlopen(req, context=ctx) as response, open(dest, 'wb') as out_file:
    total_length = int(response.headers.get('content-length', 0))
    dl = 0
    last_print = 0
    while True:
        chunk = response.read(1024 * 512)
        if not chunk:
            break
        dl += len(chunk)
        out_file.write(chunk)
        now = time.time()
        if now - last_print > 1.0 or dl == total_length:
            last_print = now
            if total_length:
                percent = dl / total_length * 100
                speed = dl / (1024 * 1024 * max(now - t0, 0.01))
                print(f"Progress: {dl / (1024*1024):.1f}MB / {total_length / (1024*1024):.1f}MB ({percent:.1f}%) - {speed:.2f} MB/s", flush=True)

dt = time.time() - t0
print(f"Download complete in {dt:.1f}s. Size: {os.path.getsize(dest)} bytes")
