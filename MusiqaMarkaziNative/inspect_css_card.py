import sys, os
sys.stdout.reconfigure(encoding='utf-8')

css_path = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '.media-card' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(len(lines), i+30)):
            print(f"  {j+1}: {lines[j].strip()}")
        break
