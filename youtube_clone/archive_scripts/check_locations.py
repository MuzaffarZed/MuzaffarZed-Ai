with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Occurrences of triggerCenterSplash:")
for m in re.finditer(r'triggerCenterSplash', text):
    print(m.start(), text[m.start()-20:m.start()+40])

print("Occurrences of initScrubBufferAndTooltip:")
for m in re.finditer(r'initScrubBufferAndTooltip', text):
    print(m.start(), text[m.start()-20:m.start()+40])
