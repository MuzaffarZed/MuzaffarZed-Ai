import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\CatalogData.cs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(50, min(140, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')
