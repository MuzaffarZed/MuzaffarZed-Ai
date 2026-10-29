with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.yt-ambient-glow')
if idx != -1:
    print(text[idx:idx+350])
else:
    print('Not found')
