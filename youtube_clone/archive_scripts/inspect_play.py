with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'togglePlay|btnPlayPause', text)]
print('Matches for play:', len(matches))
for m in matches[:5]:
    print('---')
    print(text[m:m+250])
