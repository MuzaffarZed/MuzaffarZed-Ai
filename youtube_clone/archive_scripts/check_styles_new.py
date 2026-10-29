with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

for t in ['notifications-dropdown', 'user-profile-dropdown', 'speed-2x-pill', 'yt-short-progress']:
    print(t, 'exists:', t in text)
