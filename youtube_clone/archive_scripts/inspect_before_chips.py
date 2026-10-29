with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('renderCategoryChips() {')
if idx != -1:
    print(text[idx-700:idx].encode('ascii', errors='replace').decode('ascii'))
