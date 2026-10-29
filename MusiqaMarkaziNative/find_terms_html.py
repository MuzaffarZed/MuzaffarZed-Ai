import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

for term in ['kiosk', 'reels', 'tab-dj', 'turbo', 'vault']:
    matches = list(re.finditer(term, text, re.IGNORECASE))
    print(f"Term '{term}': {len(matches)} occurrences")
