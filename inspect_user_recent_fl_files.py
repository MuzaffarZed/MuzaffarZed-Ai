import os
import time
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

now = time.time()
search_dirs = [
    r"C:\Users\MuzaffarZed\Desktop",
    r"C:\Users\MuzaffarZed\Documents\Image-Line",
    r"C:\Users\MuzaffarZed\Downloads",
    r"C:\Users\MuzaffarZed\Music"
]

print("Recently modified audio/FLP files in last 3 hours:")
for d in search_dirs:
    if not os.path.exists(d): continue
    for root, dirs, files in os.walk(d):
        for f in files:
            if any(f.endswith(ext) for ext in ['.flp', '.mp3', '.wav', '.fst']):
                fp = os.path.join(root, f)
                try:
                    mtime = os.path.getmtime(fp)
                    if now - mtime < 3 * 3600: # 3 hours
                        print(f"[{time.strftime('%H:%M:%S', time.localtime(mtime))}] {fp} ({os.path.getsize(fp)/1024/1024:.2f} MB)")
                except Exception:
                    pass
