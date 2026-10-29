import os

d_games = r"D:\KANPIYUTER O'YINLARI"
for root, dirs, files in os.walk(d_games):
    for f in files:
        low = f.lower()
        if any(x in low for x in ['enb', 'reshade', 'd3d9.dll', 'dxgi.dll', 'cleo', 'fastman', 'asi_loader']):
            print(os.path.join(root, f))
