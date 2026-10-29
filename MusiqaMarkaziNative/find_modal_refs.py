import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'

for fname in ['ui/index.html', 'ui/app.js']:
    fpath = os.path.join(base, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"=== References in {fname} ===")
    for keyword in ['duplicatesModal', 'openDuplicatesModal', 'stemSeparatorModal', 'openStemSeparatorModal', 'vaultDecryptModal']:
        matches = list(re.finditer(re.escape(keyword), text))
        print(f"  {keyword}: {len(matches)} occurrences")
