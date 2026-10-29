import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Lines 1575 to 1625 ---")
for i in range(1574, min(1625, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')

print("\n--- Lines 1700 to 1775 ---")
for i in range(1699, min(1775, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
