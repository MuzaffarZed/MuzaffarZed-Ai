import sys, os
sys.stdout.reconfigure(encoding='utf-8')

app_path = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'artistCategoryPills' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(max(0, i-5), min(len(lines), i+30)):
            print(f"  {j+1}: {lines[j].strip()}")
        break
