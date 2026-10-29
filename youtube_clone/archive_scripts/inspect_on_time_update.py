with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('onTimeUpdate() {')
if idx != -1:
    print(text[idx:idx+450])
