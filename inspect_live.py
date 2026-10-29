import urllib.request
import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
req = urllib.request.Request('https://zafaruzb.lovable.app', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

print("=== Raw HTML preview ===")
print(html[:1000])

links = re.findall(r'(?:href|src)=["\'](/[^"\']+)["\']', html)
print("\n=== Referenced paths ===")
for l in sorted(set(links)):
    print(l)

open(r"C:\Users\MuzaffarZed\ai_workspace\live_page.html", "w", encoding="utf-8").write(html)
print("\nSaved live_page.html successfully!")
