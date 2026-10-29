import json
import base64

with open(r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\c08adf9a-ed40-460e-805a-52abd9a90f03\.system_generated\steps\1247\output.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

b64 = data["base64"]
with open(r"C:\Users\MuzaffarZed\ai_workspace\tools\current_screen5.png", "wb") as f:
    f.write(base64.b64decode(b64))

print("Saved current_screen5.png!")
