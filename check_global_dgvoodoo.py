import os

appdata = os.environ.get('APPDATA', '')
localappdata = os.environ.get('LOCALAPPDATA', '')

for base in [appdata, localappdata, r"C:\Users\MuzaffarZed"]:
    for root, dirs, files in os.walk(base):
        if 'dgvoodoo.conf' in [f.lower() for f in files]:
            print("Found global dgVoodoo.conf:", os.path.join(root, 'dgVoodoo.conf'))
        # Don't recurse too deep in appdata
        if root.count(os.sep) - base.count(os.sep) > 3:
            dirs.clear()
