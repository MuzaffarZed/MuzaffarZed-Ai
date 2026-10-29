import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
app_path = os.path.join(base, 'ui', 'app.js')

with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Lines 600 to 625 of app.js ---")
for i in range(599, min(625, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
