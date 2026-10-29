import os

search_dirs = [
    r'C:\Users\MuzaffarZed\ai_workspace',
    r'C:\Users\MuzaffarZed\Downloads',
    r'D:\Downloads',
]

keywords = ['tekken', 'truck', 'gta', 'mortal', 'contra', 'tank', 'mario', 'blur', 'pepsi', 'strike', 'cs', 'sonic', 'crash']

for d in search_dirs:
    if not os.path.exists(d):
        continue
    print(f'=== SEARCHING {d} ===')
    for root, dirs, files in os.walk(d):
        for f in files:
            fl = f.lower()
            if any(k in fl for k in keywords):
                full = os.path.join(root, f)
                try:
                    sz = os.path.getsize(full)
                    print(f'{full} ({sz} bytes)')
                except:
                    pass
