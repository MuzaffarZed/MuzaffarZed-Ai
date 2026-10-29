import urllib.request
import re

for tag in ['3.4.0.0', '3.5.0.0', '3.6.0.0', '3.7.0.0', '4.26.0.0']:
    url = f"https://github.com/x360ce/x360ce/releases/tag/{tag}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            html = r.read().decode('utf-8', errors='ignore')
            assets = re.findall(r'href="([^"]*releases/download/[^"]+)"', html)
            print(f"Tag {tag}:", assets)
    except Exception as e:
        print(f"Tag {tag} failed: {e}")
