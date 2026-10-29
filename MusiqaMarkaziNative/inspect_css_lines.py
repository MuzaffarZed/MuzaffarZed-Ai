import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(565, 610):
    print(f"{i+1}: {lines[i]}", end='')
