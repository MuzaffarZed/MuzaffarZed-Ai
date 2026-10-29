import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
app_path = os.path.join(base, 'ui', 'app.js')

with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in [3090, 3113, 3304, 3385, 3464, 3519, 3584, 3597, 3648]:
    print(f"Around line {i+1}:")
    for j in range(i, min(i+6, len(lines))):
        print(f"  {j+1}: {lines[j].strip()}")
