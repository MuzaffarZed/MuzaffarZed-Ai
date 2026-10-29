with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('cacheDom() {')
if idx != -1:
    end_idx = text.find('initTheme() {', idx)
    print('cacheDom section:\n', text[end_idx-400:end_idx].encode('ascii', errors='replace').decode('ascii'))
