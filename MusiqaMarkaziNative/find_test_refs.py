import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
test_path = os.path.join(base, 'test_pro.py')

with open(test_path, 'r', encoding='utf-8') as f:
    text = f.read()

import ast
tree = ast.parse(text)
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
        source = ast.get_source_segment(text, node)
        for kw in ['duplicates', 'stem', 'kiosk', 'turbo', 'vault', 'reels', 'dj']:
            if kw in node.name.lower() or kw in source.lower():
                print(f"{node.name} mentions {kw}")
                break
