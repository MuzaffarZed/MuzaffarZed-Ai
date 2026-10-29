import os
import sys
import time
import ssl
import threading
import urllib.request
from concurrent.futures import ThreadPoolExecutor

def download_range(url, dest_path, start, end, part_id, progress_tracker):
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Range': f'bytes={start}-{end}'
    })
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=30) as res:
                with open(dest_path, 'r+b') as f:
                    f.seek(start)
                    cur = start
                    while cur <= end:
                        chunk_size = min(256 * 1024, end - cur + 1)
                        chunk = res.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        cur += len(chunk)
                        progress_tracker.add(len(chunk))
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"\nPart {part_id} failed after {max_retries} attempts: {e}")
                raise e
            time.sleep(1)

class ProgressTracker:
    def __init__(self, total_size):
        self.total_size = total_size
        self.downloaded = 0
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.last_print = 0

    def add(self, n):
        with self.lock:
            self.downloaded += n
            now = time.time()
            if now - self.last_print >= 1.0 or self.downloaded == self.total_size:
                self.last_print = now
                elapsed = max(now - self.start_time, 0.01)
                speed = (self.downloaded / (1024 * 1024)) / elapsed
                percent = (self.downloaded / self.total_size) * 100
                print(f"\r[MULTI-THREAD] {self.downloaded / (1024*1024):.1f}MB / {self.total_size / (1024*1024):.1f}MB ({percent:.1f}%) | {speed:.2f} MB/s", end="", flush=True)

def multi_thread_download(url, dest_path, num_threads=16):
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method='HEAD')
    with urllib.request.urlopen(req, context=ctx) as res:
        total_size = int(res.headers.get('content-length', 0))
        final_url = res.geturl()

    print(f"Total size: {total_size / (1024*1024):.1f} MB")
    print(f"Direct URL: {final_url}")
    print(f"Threads: {num_threads}")
    print(f"Destination: {dest_path}")

    # Pre-allocate file
    with open(dest_path, 'wb') as f:
        f.seek(total_size - 1)
        f.write(b'\0')

    tracker = ProgressTracker(total_size)
    chunk_size = total_size // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            start = i * chunk_size
            end = total_size - 1 if i == num_threads - 1 else (start + chunk_size - 1)
            futures.append(executor.submit(download_range, final_url, dest_path, start, end, i, tracker))
        
        for f in futures:
            f.result()

    print(f"\nDownload finished successfully! Saved to: {dest_path}")

if __name__ == "__main__":
    url = "https://archive.org/download/return-of-the-king_202601/The%20Lord%20of%20the%20Rings%20-%20The%20Return%20of%20the%20King.zip"
    dest = os.path.join("D:\\", "KANPIYUTER O'YINLARI", "LOTR_Uzuklar_Hukmdori", "The_Lord_of_the_Rings_ROTK.zip")
    multi_thread_download(url, dest, num_threads=16)
