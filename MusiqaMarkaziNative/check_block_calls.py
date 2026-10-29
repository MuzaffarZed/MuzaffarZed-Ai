import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
app_path = os.path.join(base, 'ui', 'app.js')

with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

block_lines = lines[3838:5370]
block_text = "".join(block_lines)

before_text = "".join(lines[:3838])
after_text = "".join(lines[5370:])
outside_text = before_text + after_text

funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', block_text)
print(f"Functions defined in block 3839..5370: {len(funcs)}")
used_outside = []
for fn in funcs:
    if re.search(r'\b' + re.escape(fn) + r'\b', outside_text):
        used_outside.append(fn)

print(f"Functions called outside the block ({len(used_outside)}):")
for u in used_outside:
    print(" -", u)
