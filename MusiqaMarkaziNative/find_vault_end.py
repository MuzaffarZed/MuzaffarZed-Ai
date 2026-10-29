import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Lines 1220 to 1320 ---")
for i in range(1220, min(1320, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
