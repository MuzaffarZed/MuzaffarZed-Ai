import urllib.request
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = 'https://zafaruzb.lovable.app'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

dest_dir = r'C:\Users\MuzaffarZed\ai_workspace\flowwise_android\app\src\main\assets\www\assets'
os.makedirs(dest_dir, exist_ok=True)

def fetch(path):
    url = base + path if path.startswith('/') else base + '/' + path
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except Exception as e:
        print(f"Failed {path}: {e}")
        return None

# Find all chunks from main-BZx60Nhf.js
text = open(os.path.join(dest_dir, 'main-BZx60Nhf.js'), encoding='utf-8', errors='ignore').read()
queue = set()
for m in re.finditer(r'import\([\"\'`]\.\/([^\"\'`]+)[\"\'`]\)', text):
    queue.add(m.group(1))

downloaded = set(os.listdir(dest_dir))

while queue:
    curr = queue.pop()
    filename = os.path.basename(curr)
    if filename in downloaded:
        continue
    
    print(f"Downloading route chunk: {filename}")
    data = fetch('/assets/' + filename)
    if not data:
        continue
    
    downloaded.add(filename)
    open(os.path.join(dest_dir, filename), 'wb').write(data)
    
    # Check if this route imports any further components/chunks
    subtext = data.decode('utf-8', errors='ignore')
    for m in re.finditer(r'import\([\"\'`]\.\/([^\"\'`]+)[\"\'`]\)', subtext):
        if m.group(1) not in downloaded:
            queue.add(m.group(1))
    for m in re.finditer(r'from[\"\'`]\.\/([^\"\'`]+)[\"\'`]', subtext):
        if m.group(1) not in downloaded:
            queue.add(m.group(1))

print(f"Successfully downloaded all routes! Total files in assets: {len(os.listdir(dest_dir))}")
