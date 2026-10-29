import sys, os
sys.stdout.reconfigure(encoding='utf-8')

app_path = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function previewArtistTracks' in l or 'function downloadArtistTop5' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(len(lines), i+35)):
            print(f"  {j+1}: {lines[j].strip()}")
        break
