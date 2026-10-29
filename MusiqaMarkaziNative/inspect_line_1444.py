import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Lines 1435 to 1455 ---")
for i in range(1434, min(1455, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
