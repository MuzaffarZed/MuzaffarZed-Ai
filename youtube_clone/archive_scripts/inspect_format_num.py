with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('formatNumber(')
print("formatNumber found at:", idx)
if idx != -1:
    print(repr(text[idx-30:idx+200]))
