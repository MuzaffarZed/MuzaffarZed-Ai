with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\Program.cs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Total lines in Program.cs:', len(lines))
for i in range(min(50, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')
