import re

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# find chapters or descriptions
for match in re.finditer(r'description:\s*[`"\'](.*?)[`"\']', text, re.DOTALL):
    print("Found description sample:")
    print(match.group(1)[:300])
    break

# check if any video has chapters property
if 'chapters' in text:
    print("Chapters property already mentioned in data.js!")
else:
    print("Chapters property not yet in data.js")
