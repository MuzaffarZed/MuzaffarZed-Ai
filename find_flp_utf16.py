import os
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

flp_path = r"C:\Users\MuzaffarZed\Documents\Image-Line\FL Studio\Projects\Project_1\Project_1.flp"
with open(flp_path, "rb") as f:
    data = f.read()

# UTF-16LE regex for printable characters
pattern = b'(?:[\x20-\x7E]\x00){3,}'
matches = re.findall(pattern, data)

print(f"Total UTF-16LE string chunks found: {len(matches)}")
for m in matches:
    try:
        s = m.decode('utf-16le')
        if any(k in s.lower() for k in ['wav', 'mp3', 'flp', 'fruity', 'pitcher', 'reverb', 'delay', 'eq', 'soundgoodizer', 'maximus', 'vocal', 'insert', 'track', 'shag', 'mani', 'image-line']):
            print("  ->", s)
    except Exception:
        pass
