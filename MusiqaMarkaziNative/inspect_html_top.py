import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(85, 125):
    print(f"{i+1}: {lines[i]}", end='')
