import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
app_path = os.path.join(base, 'ui', 'app.js')

with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
print(f"Total functions in app.js: {len(funcs)}")

bloat_funcs = []
for fn in funcs:
    lower = fn.lower()
    if any(k in lower for k in ['reels', 'dj', 'vault', 'stem', 'duplicate', 'turbo', 'kiosk']):
        bloat_funcs.append(fn)

print(f"Bloat functions ({len(bloat_funcs)}):")
for b in bloat_funcs:
    print(" -", b)
