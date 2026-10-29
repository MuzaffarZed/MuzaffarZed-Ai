with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('renderShorts() {')
if idx != -1:
    print('Found renderShorts at:', idx)
    # print safely without unicode error
    print(text[idx:idx+900].encode('ascii', errors='replace').decode('ascii'))
