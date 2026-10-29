with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

terms = ['yt-context-menu', 'yt-timestamp-link', 'btn-chapters']
for t in terms:
    print(t, 'exists:', t in text)
