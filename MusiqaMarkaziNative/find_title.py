import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\Program.cs', 'r', encoding='utf-8') as f:
    text = f.read()

import re
titles = re.findall(r'Text\s*=\s*\"([^\"]+)\"', text)
print("Form titles in Program.cs:", titles)
