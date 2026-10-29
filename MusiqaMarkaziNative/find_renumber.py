import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
app_path = os.path.join(base, 'ui', 'app.js')

with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

print("renumber in app.js:", "renumber" in text)
print("renumberActiveFolderForCarAction in app.js:", "renumberActiveFolderForCarAction" in text)
