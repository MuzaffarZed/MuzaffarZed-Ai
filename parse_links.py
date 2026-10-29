import re

with open(r'C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\.system_generated\steps\2723\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

matches = set(re.findall(r'href="([^"]*releases/download[^"]*)"', text))
for m in sorted(matches):
    print("MATCH:", m)
