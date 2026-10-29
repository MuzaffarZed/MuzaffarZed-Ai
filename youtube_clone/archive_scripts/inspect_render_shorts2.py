with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

print(text[103500:104800].encode('ascii', errors='replace').decode('ascii'))
