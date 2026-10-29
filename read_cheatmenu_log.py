import os

log = r"D:\KANPIYUTER O'YINLARI\GTA Vice City - Deluxe\scripts\CheatMenuVC.log"
if os.path.exists(log):
    with open(log, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read())
