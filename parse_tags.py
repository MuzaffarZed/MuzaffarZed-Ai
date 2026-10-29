import re

with open(r'C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\.system_generated\steps\2723\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

tags = set(re.findall(r'/releases/tag/([^"\'\s>]+)', text))
print("TAGS:", tags)

zips = set(re.findall(r'([^"\'\s>]+\.zip)', text))
print("ZIPS:", [z for z in zips if 'x360' in z])
