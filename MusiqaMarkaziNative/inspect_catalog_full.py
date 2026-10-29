import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\CatalogData.cs', 'r', encoding='utf-8') as f:
    text = f.read()

artists = re.findall(r'new ArtistInfo\("([^"]+)"', text)
print(f'Total Artists in CatalogData.cs: {len(artists)}')
for a in artists:
    print(" -", a)

genres = re.findall(r'new CollectionInfo\("([^"]+)"', text)
print(f'\nTotal Collections in CatalogData.cs: {len(genres)}')
for g in genres:
    print(" *", g)
