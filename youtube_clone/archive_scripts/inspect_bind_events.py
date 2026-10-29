with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('bindEvents() {')
if idx != -1:
    print('Found bindEvents at:', idx)
    print(text[idx:idx+800])
