import os

for base in [r"D:\KANPIYUTER O'YINLARI\GTA Vice City - Deluxe\scripts", r"D:\KANPIYUTER O'YINLARI\GTA-Vice City MATRIX\scripts"]:
    print(f"=== {base} ===")
    if os.path.exists(base):
        for f in os.listdir(base):
            print(" ", f)
