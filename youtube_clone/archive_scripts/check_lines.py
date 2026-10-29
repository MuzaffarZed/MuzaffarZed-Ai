with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1180, 1220):
    print(f"{i+1}: {lines[i]}", end='')
