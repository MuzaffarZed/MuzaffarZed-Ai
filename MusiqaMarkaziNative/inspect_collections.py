import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Lines 235 to 270 (Collections & Search start) ---")
for i in range(235, min(270, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
