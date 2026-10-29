import urllib.request
import zipfile
import os

target = r"C:\Users\MuzaffarZed\ai_workspace\tools\x360ce_x86.zip"
extract_dir = r"C:\Users\MuzaffarZed\ai_workspace\tools\x86"
os.makedirs(extract_dir, exist_ok=True)

url = "https://www.x360ce.com/Files/x360ce_x86.zip"
print(f"Downloading {url}...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as r, open(target, 'wb') as f:
    f.write(r.read())

print("Downloaded! Extracting...")
with zipfile.ZipFile(target, 'r') as z:
    z.extractall(extract_dir)

print("Files in x86:")
for f in os.listdir(extract_dir):
    print("  -", f)
