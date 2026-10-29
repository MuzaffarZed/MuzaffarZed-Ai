import json
import base64
from PIL import Image
import io
import os

json_file = r'C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\.system_generated\steps\2581\output.txt'
artifact_dir = r'C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f'

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

img_bytes = base64.b64decode(data['base64'])
img = Image.open(io.BytesIO(img_bytes))

full_path = os.path.join(artifact_dir, 'date_and_time_settings_proof.png')
img.save(full_path)
print(f"Saved: {full_path}")
