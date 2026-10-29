import os

for root, dirs, files in os.walk(r"D:\KANPIYUTER O'YINLARI\GTA Vice City - Deluxe"):
    for f in files:
        if 'cheatmenu' in f.lower():
            print(os.path.join(root, f))
