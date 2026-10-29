with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'([a-zA-Z0-9_]+)\s*\([^\)]*\)\s*\{', text)
print("All methods in app.js:")
print(matches)
