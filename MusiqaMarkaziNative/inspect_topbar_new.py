import sys, os
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(105, 175):
    print(f"{i+1}: {lines[i]}", end='')
