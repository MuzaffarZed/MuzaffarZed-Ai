import sys, os
sys.stdout.reconfigure(encoding='utf-8')

app_path = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(40, 95):
    print(f"{i+1}: {lines[i]}", end='')
