with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.rfind('openShortsSoundModal(soundName, authorName) {')
print(text[idx:idx+350].encode('ascii', errors='replace').decode('ascii'))
