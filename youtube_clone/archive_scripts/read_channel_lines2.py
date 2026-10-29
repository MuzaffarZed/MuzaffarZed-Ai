with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(703, 745):
    print(f"{i+1}: {lines[i]}", end='')
