import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
test_path = os.path.join(base, 'test_pro.py')

with open(test_path, 'r', encoding='utf-8') as f:
    text = f.read()

tests = re.findall(r'def (test_[a-zA-Z0-9_]+)', text)
print(f"Total tests: {len(tests)}")
for t in tests:
    print(t)
