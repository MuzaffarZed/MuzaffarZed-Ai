import os

gta_deluxe_log = r"D:\KANPIYUTER O'YINLARI\GTA Vice City - Deluxe\scripts\cleo_redux.log"
if os.path.exists(gta_deluxe_log):
    print("=== GTA Vice City Deluxe cleo_redux.log ===")
    with open(gta_deluxe_log, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read())

gta_matrix_log = r"D:\KANPIYUTER O'YINLARI\GTA-Vice City MATRIX\scripts\cleo_redux.log"
if os.path.exists(gta_matrix_log):
    print("=== GTA Vice City MATRIX cleo_redux.log ===")
    with open(gta_matrix_log, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read())

# Check FlatOut2 d3d9.dll
import pefile
for p in [r"D:\KANPIYUTER O'YINLARI\FlatOut2\d3d9.dll", r"D:\KANPIYUTER O'YINLARI\Speed rof Deen Wast Monted\d3d9.dll"]:
    if os.path.exists(p):
        print(f"\n=== Inspecting {p} ===")
        try:
            pe = pefile.PE(p)
            for fileinfo in getattr(pe, 'FileInfo', []):
                for fi in fileinfo:
                    if fi.Key.decode() == 'StringFileInfo':
                        for st in fi.StringTable:
                            for k, v in st.entries.items():
                                print(f"  {k.decode()}: {v.decode()}")
        except Exception as e:
            print("  Error:", e)
