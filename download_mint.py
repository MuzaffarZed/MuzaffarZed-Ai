import os
import sys
import time
import hashlib
import threading
import urllib.request
from pathlib import Path

ISO_URL = "https://mirror.yandex.ru/linuxmint/stable/22.3/linuxmint-22.3-xfce-64bit.iso"
EXPECTED_SHA256 = "45a835b5dddaf40e84d776549e0b19b3fbd49673b6cc6434ebddbfcd217df776"
TOTAL_SIZE = 3033710592

DOWNLOAD_DIR = Path(r"C:\Users\MuzaffarZed\Downloads")
TARGET_ISO = DOWNLOAD_DIR / "linuxmint-22.3-xfce-64bit.iso"
PARTS_DIR = DOWNLOAD_DIR / ".mint_parts"
NUM_THREADS = 6

def download_part(part_index, start, end, progress_dict, lock):
    part_file = PARTS_DIR / f"part_{part_index}.tmp"
    existing_bytes = 0
    if part_file.exists():
        existing_bytes = part_file.stat().st_size
    
    current_start = start + existing_bytes
    if current_start > end:
        with lock:
            progress_dict[part_index] = end - start + 1
        return

    req = urllib.request.Request(ISO_URL)
    req.add_header("Range", f"bytes={current_start}-{end}")
    req.add_header("User-Agent", "Mozilla/5.0")
    
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp, open(part_file, "ab") as f:
                while True:
                    chunk = resp.read(1024 * 1024)  # 1MB buffer
                    if not chunk:
                        break
                    f.write(chunk)
                    with lock:
                        progress_dict[part_index] = part_file.stat().st_size
            break
        except Exception as e:
            time.sleep(2)
            if attempt == 4:
                raise e
            existing_bytes = part_file.stat().st_size if part_file.exists() else 0
            current_start = start + existing_bytes
            req = urllib.request.Request(ISO_URL)
            req.add_header("Range", f"bytes={current_start}-{end}")
            req.add_header("User-Agent", "Mozilla/5.0")

def main():
    print(f"Boshlandi: Linux Mint 22.3 XFCE 64-bit ISO ({TOTAL_SIZE / (1024**3):.2f} GB)")
    PARTS_DIR.mkdir(parents=True, exist_ok=True)
    
    chunk_size = TOTAL_SIZE // NUM_THREADS
    threads = []
    progress_dict = {i: 0 for i in range(NUM_THREADS)}
    lock = threading.Lock()
    
    for i in range(NUM_THREADS):
        start = i * chunk_size
        end = (start + chunk_size - 1) if i < NUM_THREADS - 1 else TOTAL_SIZE - 1
        t = threading.Thread(target=download_part, args=(i, start, end, progress_dict, lock), daemon=True)
        threads.append(t)
        t.start()
    
    start_time = time.time()
    last_print = 0
    while any(t.is_alive() for t in threads):
        time.sleep(1.0)
        with lock:
            total_downloaded = sum(progress_dict.values())
        elapsed = time.time() - start_time
        speed_mb = (total_downloaded / (1024 * 1024)) / elapsed if elapsed > 0 else 0
        pct = (total_downloaded / TOTAL_SIZE) * 100
        if time.time() - last_print >= 5:
            last_print = time.time()
            print(f"Jarayon: {pct:.1f}% | Yuklandi: {total_downloaded / (1024**2):.1f} MB / {TOTAL_SIZE / (1024**2):.1f} MB | Tezlik: {speed_mb:.2f} MB/s")

    for t in threads:
        t.join()
        
    print("\nBarcha qismlar yuklandi. Fayl birlashtirilmoqda...")
    with open(TARGET_ISO, "wb") as outfile:
        for i in range(NUM_THREADS):
            part_file = PARTS_DIR / f"part_{i}.tmp"
            with open(part_file, "rb") as infile:
                while True:
                    buf = infile.read(8 * 1024 * 1024)
                    if not buf:
                        break
                    outfile.write(buf)
            part_file.unlink(missing_ok=True)
            
    PARTS_DIR.rmdir()
    print("Fayl muvaffaqiyatli birlashtirildi!")
    
    print("SHA256 xesh tekshirilmoqda...")
    h = hashlib.sha256()
    with open(TARGET_ISO, "rb") as f:
        while True:
            chunk = f.read(8 * 1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
            
    calculated_hash = h.hexdigest()
    if calculated_hash.lower() == EXPECTED_SHA256.lower():
        print(f"[SUCCESS] SHA256 mos keldi: {calculated_hash}")
        print(f"Fayl tayyor: {TARGET_ISO}")
    else:
        print(f"[ERROR] SHA256 mos kelmadi! Kutildi: {EXPECTED_SHA256}, Chiqdi: {calculated_hash}")

if __name__ == "__main__":
    main()
