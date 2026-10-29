import urllib.request
import re

url = 'https://sourceforge.net/projects/andyyan-gsi/files/lineage-19.x/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'href=["\'](/projects/andyyan-gsi/files/lineage-19\.x/[^"\']*arm64_bgN[^"\']*)["\']', html)
        for m in sorted(set(matches)):
            print('https://sourceforge.net' + m)
except Exception as e:
    print('Error:', e)
