with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="view-channel"' in l:
        print(f"view-channel at line {i+1}")
    if 'id="view-history"' in l:
        print(f"view-history at line {i+1}")
