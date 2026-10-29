import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['ui/app.js', 'LocalStudioServer.cs', 'StudioEngine.cs']:
    path = os.path.join(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative', fname)
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()
    if 'Jaloliddin' in t or 'Hamdam' in t:
        print(f"Found artists in {fname}!")
