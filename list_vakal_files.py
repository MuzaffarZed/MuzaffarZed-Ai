import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

p = r"C:\Users\MuzaffarZed\Desktop\vakal minus"
for root, dirs, files in os.walk(p):
    print(f"[{root}]")
    for f in files:
        fp = os.path.join(root, f)
        print(f"  - {f} ({os.path.getsize(fp)/1024/1024:.2f} MB)")
