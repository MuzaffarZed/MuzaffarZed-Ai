with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'bindEvents() {' in l:
        print(f"bindEvents starts at line {i+1}")
    if '    bindEvents' in l:
        print(f"mention at line {i+1}")
