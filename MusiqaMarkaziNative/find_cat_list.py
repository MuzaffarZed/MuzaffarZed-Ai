import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\CatalogData.cs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'ArtistCategories' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(len(lines), i+15)):
            print(f"  {j+1}: {lines[j].strip()}")
        break
