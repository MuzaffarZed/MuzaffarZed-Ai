import os
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

flp_path = r"C:\Users\MuzaffarZed\Documents\Image-Line\FL Studio\Projects\Project_1\Project_1.flp"
print(f"Inspecting FLP: {flp_path} ({os.path.getsize(flp_path)} bytes)")

with open(flp_path, "rb") as f:
    data = f.read()

# Extract all readable ASCII/UTF strings of length >= 3
strings = re.findall(b"[\x20-\x7E]{3,}", data)
decoded_strings = [s.decode('latin1', errors='ignore') for s in strings]

print("\n--- Detected Project Metadata & File Paths ---")
for s in decoded_strings:
    if any(k in s.lower() for k in ['wav', 'mp3', 'flp', 'image-line', 'fruity', 'pitcher', 'reverb', 'delay', 'eq', 'soundgoodizer', 'maximus', 'autotune', 'insert']):
        print("  ->", s)

print("\n--- Detected Plugins / Effects ---")
known_plugins = [
    'Fruity Parametric EQ 2', 'Pitcher', 'NewTone', 'Fruity Reeverb 2', 
    'Fruity Delay 3', 'Fruity Delay 2', 'Soundgoodizer', 'Maximus', 
    'Fruity Limiter', 'Fruity Compressor', 'Fruity Fast Dist', 'Fruity Chorus',
    'Edison', 'Vocal Enhancer', 'Auto-Tune', 'FabFilter', 'iZotope'
]

for p in known_plugins:
    if p.encode('latin1') in data or p.lower().encode('latin1') in data:
        print(f"  [FOUND PLUGIN]: {p}")
