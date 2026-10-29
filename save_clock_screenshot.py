import json
import base64
from PIL import Image
import io
import os

json_file = r'C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\.system_generated\steps\2567\output.txt'
artifact_dir = r'C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f'

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

img_bytes = base64.b64decode(data['base64'])
img = Image.open(io.BytesIO(img_bytes))

# Save full desktop
full_path = os.path.join(artifact_dir, 'desktop_time_proof.png')
img.save(full_path)
print(f"Saved full desktop image: {img.size} to {full_path}")

# Crop clock area (bottom right of 1920x1080 taskbar: x from 1700 to 1920, y from 1030 to 1080)
w, h = img.size
clock_crop = img.crop((w - 250, h - 60, w, h))
clock_path = os.path.join(artifact_dir, 'clock_proof.png')
clock_crop.save(clock_path)
print(f"Saved clock crop to {clock_path}")
