import sys, os, ast
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
test_path = os.path.join(base, 'test_pro.py')

with open(test_path, 'r', encoding='utf-8') as f:
    text = f.read()

tree = ast.parse(text)
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
        if any(k in node.name.lower() for k in ['duplicate', 'stem', 'kiosk', 'turbo', 'vault', 'reels', 'virtual_dj']):
            print(f"=== {node.name} ===")
            source = ast.get_source_segment(text, node)
            lines = source.splitlines()
            for l in lines[:15]:
                print(" ", l)
