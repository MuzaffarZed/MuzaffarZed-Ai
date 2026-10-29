import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
app_path = os.path.join(base, 'ui', 'app.js')

with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if l.startswith('// ============================================================================') or 'SECTION' in l or 'STUDIO' in l or 'VAULT' in l or 'KIOSK' in l or 'REELS' in l or 'DJ' in l:
        print(f"Line {i+1}: {l.strip()[:90]}")
