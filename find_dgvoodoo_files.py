import os

d_games = r"D:\KANPIYUTER O'YINLARI"
for root, dirs, files in os.walk(d_games):
    for f in files:
        if f.lower() in ['dgvoodoo.conf', 'd3d9.dll', 'd3d8.dll', 'ddraw.dll']:
            p = os.path.join(root, f)
            print(f"Found: {p} ({os.path.getsize(p)} bytes)")
