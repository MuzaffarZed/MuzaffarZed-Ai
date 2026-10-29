import pefile
import sys
sys.stdout.reconfigure(encoding='utf-8')

for p in [r"D:\KANPIYUTER O'YINLARI\GTA Vice City - Deluxe\d3d8.dll", r"D:\KANPIYUTER O'YINLARI\GTA-Vice City MATRIX\d3d8.dll"]:
    print(f"=== {p} ===")
    try:
        pe = pefile.PE(p)
        for fileinfo in getattr(pe, 'FileInfo', []):
            for fi in fileinfo:
                if hasattr(fi, 'Key') and fi.Key.decode('latin1', 'ignore') == 'StringFileInfo':
                    for st in fi.StringTable:
                        for k, v in st.entries.items():
                            print(f"  {k.decode('latin1', 'ignore')}: {v.decode('latin1', 'ignore')}")
    except Exception as e:
        print("Error:", e)
