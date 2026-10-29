import os
import re

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
for lnk in ['Blur.lnk', 'Counter-Strike 1.6.lnk']:
    target = os.path.join(desktop, lnk)
    if os.path.exists(target):
        with open(target, 'rb') as f:
            raw = f.read().decode('latin1', errors='ignore')
            matches = re.findall(r'[A-Za-z]:\\[A-Za-z0-9_\\\- ]+\.exe', raw)
            print(lnk, 'found paths:', matches)
