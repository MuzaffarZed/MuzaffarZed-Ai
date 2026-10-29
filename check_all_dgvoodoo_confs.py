import os

d_games = r"D:\KANPIYUTER O'YINLARI"
for root, dirs, files in os.walk(d_games):
    for f in files:
        if f.lower() == 'dgvoodoo.conf':
            p = os.path.join(root, f)
            print(f"=== {p} ===")
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                for line in fp:
                    if any(k in line.lower() for k in ['watermark', 'splash', 'banner', 'osd']):
                        print("  ", line.strip())
