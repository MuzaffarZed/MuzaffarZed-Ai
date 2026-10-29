with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'openChannelPage\s*\(', text)]
for m in matches:
    print(text[m:m+300].encode('ascii', errors='replace').decode('ascii'))
    print('---')
