import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\LocalStudioServer.cs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '/api/init' in l:
        print(f"Found /api/init at line {i+1}")
        for j in range(i, min(len(lines), i+60)):
            print(f"  {j+1}: {lines[j].strip()}")
        break
