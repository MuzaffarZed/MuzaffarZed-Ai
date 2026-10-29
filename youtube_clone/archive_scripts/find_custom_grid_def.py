with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'renderCustomGrid\s*\(', text)]
print('Matches:', len(matches))
for m in matches:
    print(text[m:m+200].encode('ascii', errors='replace').decode('ascii'))
    print('---')
