import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\CatalogData.cs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Ahmadaliyev' in l:
        print(f"Ahmadaliyev at line {i+1}: {l.strip()}")
        for j in range(max(0, i-5), min(len(lines), i+30)):
            print(f"  {j+1}: {lines[j].strip()}")
        break
