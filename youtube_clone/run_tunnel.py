# -*- coding: utf-8 -*-
import subprocess
import re
import sys
import os
import time

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

CLOUDFLARED_PATH = r"C:\Users\MuzaffarZed\ai_workspace\youtube_clone\cloudflared.exe"
URL_FILE_PATH = r"C:\Users\MuzaffarZed\ai_workspace\youtube_clone\public_url.txt"
TARGET_PORT = "http://127.0.0.1:8000"

def main():
    print(f"[TUNNEL] Starting Cloudflare Tunnel for {TARGET_PORT} ...", flush=True)
    if not os.path.exists(CLOUDFLARED_PATH):
        print(f"[ERROR] cloudflared.exe not found: {CLOUDFLARED_PATH}", flush=True)
        sys.exit(1)

    cmd = [CLOUDFLARED_PATH, "tunnel", "--url", TARGET_PORT]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace"
    )

    url_found = None
    pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    for line in iter(proc.stdout.readline, ''):
        line_str = line.strip()
        print(f"[CLOUDFLARE] {line_str}", flush=True)
        if not url_found:
            m = pattern.search(line_str)
            if m:
                url_found = m.group(0)
                print(f"\n=======================================================", flush=True)
                print(f"[SUCCESS] GLOBAL PUBLIC HTTPS URL: {url_found}", flush=True)
                print(f"=======================================================\n", flush=True)
                try:
                    with open(URL_FILE_PATH, "w", encoding="utf-8") as f:
                        f.write(url_found)
                    print(f"[SAVED] Written to {URL_FILE_PATH}", flush=True)
                except Exception as e:
                    print(f"[ERROR] Could not save url file: {e}", flush=True)

    proc.wait()

if __name__ == "__main__":
    main()
