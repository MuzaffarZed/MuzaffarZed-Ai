with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

for t in ['subtitles-menu', 'history-search', 'channel-search', 'sound-modal']:
    print(t, 'in styles.css:', t in text)
