with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('bindEvents() {')
if idx != -1:
    end_idx = text.find('renderCategoryChips() {', idx)
    print('bindEvents end section:\n', text[end_idx-500:end_idx].encode('ascii', errors='replace').decode('ascii'))
