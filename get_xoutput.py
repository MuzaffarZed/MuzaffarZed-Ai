import urllib.request
import zipfile
import os

target = r"C:\Users\MuzaffarZed\ai_workspace\tools\XOutput.zip"
extract_dir = r"C:\Users\MuzaffarZed\ai_workspace\XOutput"
os.makedirs(extract_dir, exist_ok=True)

url = "https://github.com/csutorasa/XOutput/releases/download/3.32/XOutput.zip"
print(f"Downloading {url}...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as r, open(target, 'wb') as f:
    f.write(r.read())

print("Downloaded! Extracting to XOutput...")
with zipfile.ZipFile(target, 'r') as z:
    z.extractall(extract_dir)

print("Files in XOutput:")
for f in os.listdir(extract_dir):
    print("  -", f)
