with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
vids = re.findall(r'id:\s*["\']([^"\']+)["\'],\s*title:\s*["\']([^"\']+)["\']', text)
print(f'Total videos: {len(vids)}')
for vid, title in vids[:6]:
    print(f'- {vid}: {title}')
