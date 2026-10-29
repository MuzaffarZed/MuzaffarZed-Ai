import sys, os
sys.stdout.reconfigure(encoding='utf-8')

engine_path = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\StudioEngine.cs'
with open(engine_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'public static List<UsbDriveInfo> DetectUsbDrives' in l or 'DetectUsbDrives' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(len(lines), i+35)):
            print(f"  {j+1}: {lines[j].strip()}")
        break
