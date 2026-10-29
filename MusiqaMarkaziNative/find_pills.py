import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

pills = re.findall(r'id="pillFx[^"]*"', text)
print("Pills found in index.html:")
for p in pills:
    print(p)
