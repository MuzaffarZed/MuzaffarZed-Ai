import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
app_path = os.path.join(base, 'ui', 'app.js')

with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

print("Occurrences of 'simulator' in app.js:")
for m in re.finditer(r'simulator', text):
    start = max(0, m.start() - 40)
    end = min(len(text), m.end() + 40)
    print(text[start:end].replace('\n', ' '))
