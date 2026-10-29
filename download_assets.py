import urllib.request
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = 'https://zafaruzb.lovable.app'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch(path):
    url = base + path if path.startswith('/') else base + '/' + path
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except Exception as e:
        print(f"Failed {path}: {e}")
        return None

dest_dir = r'C:\Users\MuzaffarZed\ai_workspace\flowwise_android\app\src\main\assets\www\assets'
os.makedirs(dest_dir, exist_ok=True)

# Scan all already downloaded files in dest_dir for more chunk names
new_found = True
while new_found:
    new_found = False
    existing_files = os.listdir(dest_dir)
    for fname in existing_files:
        if not fname.endswith('.js'):
            continue
        filepath = os.path.join(dest_dir, fname)
        text = open(filepath, 'r', encoding='utf-8', errors='ignore').read()
        
        # Matches like /assets/something-hash.js or something-hash.js
        candidates = re.findall(r'["\'](/assets/[a-zA-Z0-9_\-\.]+\.(?:js|css))["\']', text)
        candidates += re.findall(r'["\']([a-zA-Z0-9_\-]+\-[a-zA-Z0-9_\-]{8}\.(?:js|css))["\']', text)
        candidates += re.findall(r'["\']([a-zA-Z0-9_\-]+\-[a-zA-Z0-9_\-]{7,10}\.(?:js|css))["\']', text)
        
        for c in set(candidates):
            c_name = os.path.basename(c)
            if not c.startswith('/assets/'):
                c_path = '/assets/' + c_name
            else:
                c_path = c
                
            target_path = os.path.join(dest_dir, c_name)
            if not os.path.exists(target_path):
                print(f"Discovered new chunk: {c_path}")
                data = fetch(c_path)
                if data:
                    open(target_path, 'wb').write(data)
                    new_found = True

total_bundled = len(os.listdir(dest_dir))
print(f"Total bundled assets now: {total_bundled}")
