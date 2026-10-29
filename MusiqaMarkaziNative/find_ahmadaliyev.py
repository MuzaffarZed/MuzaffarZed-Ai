import sys, os
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['ui/app.js', 'ui/index.html']:
    p = os.path.join(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative', fname)
    with open(p, 'r', encoding='utf-8') as f:
        t = f.read()
    if 'Ahmadaliyev' in t:
        print(f"Found Ahmadaliyev in {fname}!")
