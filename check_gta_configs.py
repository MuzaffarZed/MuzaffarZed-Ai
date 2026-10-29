import os

for base in [r"D:\KANPIYUTER O'YINLARI\GTA Vice City - Deluxe\scripts", r"D:\KANPIYUTER O'YINLARI\GTA-Vice City MATRIX\scripts"]:
    for f in os.listdir(base):
        if f.endswith('.toml') or f.endswith('.ini'):
            p = os.path.join(base, f)
            print(f"=== {p} ===")
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                for line in fp:
                    if any(k in line.lower() for k in ['notify', 'notification', 'message', 'text', 'intro', 'welcome', 'banner', 'tip', 'update', 'show']):
                        print("  ", line.strip())
