import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\StudioEngine.cs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Jaloliddin' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(max(0, i-5), min(len(lines), i+25)):
            print(f"  {j+1}: {lines[j].strip()}")
        break
