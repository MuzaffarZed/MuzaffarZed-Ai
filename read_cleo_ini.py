import os

p = r"D:\KANPIYUTER O'YINLARI\GTA Vice City - Deluxe\scripts_extra_mods\CLEO\.config\cleo.ini"
if os.path.exists(p):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read())
