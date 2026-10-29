import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

tabs = re.findall(r'<div class="nav-tab[^"]*"[^>]*>.*?</div>', text, re.DOTALL)
print("--- ALL TABS ---")
for t in tabs:
    print(' '.join(t.split()))

print("\n--- ALL PANES ---")
panes = re.findall(r'<section id="tab-[^"]*"[^>]*>', text)
for p in panes:
    print(p)

print("\n--- ALL MODALS ---")
modals = re.findall(r'<div[^>]+id="[^"]*modal[^"]*"[^>]*>|<div[^>]+class="[^"]*modal[^"]*"[^>]*>', text, re.IGNORECASE)
for m in modals:
    print(m)
