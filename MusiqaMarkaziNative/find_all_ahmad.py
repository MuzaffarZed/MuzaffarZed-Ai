import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(('.cs', '.js', '.html', '.json')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                if 'Ahmadaliyev' in content:
                    print(f"Found Ahmadaliyev in {p}")
            except:
                pass
