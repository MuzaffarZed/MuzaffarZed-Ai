import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'openDuplicatesModal' in l or 'openStemSeparatorModal' in l:
        print(f"Line {i+1}: {l.strip()}")
