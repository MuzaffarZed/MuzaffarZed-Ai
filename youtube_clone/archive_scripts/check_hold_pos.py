with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'init2xSpeedHold', text):
    print(m.start(), text[m.start()-20:m.start()+40])
