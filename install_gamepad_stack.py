import os
import sys
import urllib.request
import zipfile
import subprocess
import ctypes
import time

tools_dir = r"C:\Users\MuzaffarZed\ai_workspace\tools"
os.makedirs(tools_dir, exist_ok=True)

vigem_url = "https://github.com/nefarius/ViGEmBus/releases/download/v1.22.0/ViGEmBus_1.22.0_x64_x86_arm64.exe"
vigem_exe = os.path.join(tools_dir, "ViGEmBus_Setup.exe")

x360ce_url = "https://github.com/x360ce/x360ce/releases/download/4.26.0.0/x360ce.zip"
x360ce_zip = os.path.join(tools_dir, "x360ce.zip")
x360ce_dir = r"C:\Users\MuzaffarZed\ai_workspace\x360ce"
os.makedirs(x360ce_dir, exist_ok=True)

def download_file(url, target):
    if os.path.exists(target) and os.path.getsize(target) > 100000:
        print(f"[+] Already downloaded: {target} ({os.path.getsize(target)/1024/1024:.2f} MB)")
        return True
    print(f"[*] Downloading {url} -> {target}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as response, open(target, 'wb') as out_file:
        total = int(response.headers.get('Content-Length', 0))
        downloaded = 0
        chunk_size = 65536
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            if total > 0:
                print(f"\r    {downloaded/1024/1024:.2f}/{total/1024/1024:.2f} MB ({downloaded*100//total}%)", end='', flush=True)
        print()
    print(f"[+] Finished download: {target}")
    return True

def install_vigem():
    print("[*] Installing ViGEmBus driver (elevated /quiet)...")
    ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", vigem_exe, "/quiet /norestart", None, 0)
    print(f"[+] ShellExecute returned: {ret}")
    # Wait for installation to complete
    for _ in range(15):
        time.sleep(1)
        res = subprocess.run(['sc', 'query', 'ViGEmBus'], capture_output=True, text=True, errors='ignore')
        if 'STATE' in res.stdout and 'RUNNING' in res.stdout:
            print("[+] ViGEmBus is successfully RUNNING!")
            return True
        elif 'STATE' in res.stdout:
            print(f"[*] ViGEmBus state: {res.stdout.strip()}")
            return True
    return False

def extract_x360ce():
    print("[*] Extracting x360ce...")
    with zipfile.ZipFile(x360ce_zip, 'r') as z:
        z.extractall(x360ce_dir)
    print(f"[+] x360ce extracted to: {x360ce_dir}")
    for f in os.listdir(x360ce_dir):
        print(f"    - {f}")

if __name__ == '__main__':
    download_file(vigem_url, vigem_exe)
    download_file(x360ce_url, x360ce_zip)
    extract_x360ce()
    install_vigem()
