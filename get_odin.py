import urllib.request
import re
import os
import zipfile
import html

url = "https://sourceforge.net/projects/j4lte/files/Tools/Odin3_v3.14.4.zip/download"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode("utf-8", errors="ignore")

links = re.findall(r'https://downloads\.sourceforge\.net/project/j4lte/Tools/Odin3_v3\.14\.4\.zip\?[^\s"\'<>]+', content)
if not links:
    print("Direct link not found!")
    exit(1)

download_url = html.unescape(links[0])
print("Downloading from:", download_url)

dest_zip = r"C:\Users\MuzaffarZed\Downloads\Odin3_v3.14.4_Verified.zip"
dest_dir = r"C:\Users\MuzaffarZed\Downloads\Odin_Latest"

req2 = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
with urllib.request.urlopen(req2) as resp, open(dest_zip, "wb") as f:
    f.write(resp.read())

print("Downloaded successfully! Size:", os.path.getsize(dest_zip))

os.makedirs(dest_dir, exist_ok=True)
with zipfile.ZipFile(dest_zip, "r") as z:
    z.extractall(dest_dir)

print(f"Extracted to: {dest_dir}")
for f in os.listdir(dest_dir):
    full_p = os.path.join(dest_dir, f)
    print(f" - {f} ({os.path.getsize(full_p)} bytes)")
