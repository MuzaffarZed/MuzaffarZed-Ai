import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    line_num = i + 1
    # Check outside lines 650-1305 and 1580-1600
    if not (650 <= line_num <= 1305) and not (1580 <= line_num <= 1600):
        for term in ['kiosk', 'reels', 'tab-dj', 'turbo', 'vault']:
            if term in l.lower():
                print(f"Line {line_num} [{term}]: {l.strip()[:100]}")
