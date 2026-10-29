import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
test_path = os.path.join(base, 'test_pro.py')

with open(test_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Lines 200 to 445 ---")
for i in range(199, min(445, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
