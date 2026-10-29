import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
app_path = os.path.join(base, 'ui', 'app.js')

with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function startBatchDownloadRequest' in l:
        print(f"Found startBatchDownloadRequest at line {i+1}")
        for j in range(i, min(i+45, len(lines))):
            print(f"{j+1}: {lines[j]}", end='')
        break
