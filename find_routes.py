text = open(r'C:\Users\MuzaffarZed\ai_workspace\flowwise_android\app\src\main\assets\www\assets\main-BZx60Nhf.js', encoding='utf-8', errors='ignore').read()
import re
print("Length:", len(text))
for m in re.finditer(r'import\([\"\'`]([^\"\'`]+)[\"\'`]\)', text):
    print("Dynamic import:", m.group(1))
for m in re.finditer(r'\/assets\/[a-zA-Z0-9_\-\.]+', text):
    print("Asset path:", m.group(0))
