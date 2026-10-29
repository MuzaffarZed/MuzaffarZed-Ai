import os
import re

base_smali = r'C:\Users\MuzaffarZed\ai_workspace\capcut_mod_lab\base_smali'
matches = []

keywords = [re.compile(rb'isVip', re.IGNORECASE), re.compile(rb'isPro', re.IGNORECASE), re.compile(rb'is_vip', re.IGNORECASE)]

for root, dirs, files in os.walk(base_smali):
    # Focus on bytedance or lemon packages
    if 'bytedance' not in root and 'lemon' not in root:
        continue
    for f in files:
        if f.endswith('.smali'):
            path = os.path.join(root, f)
            try:
                with open(path, 'rb') as fp:
                    content = fp.read()
                    for kw in keywords:
                        if kw.search(content):
                            rel = os.path.relpath(path, base_smali)
                            matches.append(rel)
                            break
            except Exception:
                pass

print(f"Total matching smali files in bytedance/lemon: {len(matches)}")
for m in sorted(matches)[:25]:
    print(" ", m)
