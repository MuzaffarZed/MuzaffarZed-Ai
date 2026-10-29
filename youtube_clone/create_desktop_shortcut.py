# -*- coding: utf-8 -*-
import os

desktop_dir = os.path.expanduser(r"~\Desktop")
shortcut_content = """[InternetShortcut]
URL=http://localhost:8000
IconIndex=0
IconFile=https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/play-square.svg
"""

# 1. In workspace
workspace_url = r"C:\Users\MuzaffarZed\ai_workspace\youtube_clone\YouTube_Pro.url"
with open(workspace_url, "w", encoding="utf-8") as f:
    f.write(shortcut_content)
print(f"Created: {workspace_url}")

# 2. On user desktop
desktop_url = os.path.join(desktop_dir, "YouTube Pro.url")
try:
    with open(desktop_url, "w", encoding="utf-8") as f:
        f.write(shortcut_content)
    print(f"Created on Desktop: {desktop_url}")
except Exception as e:
    print(f"Desktop shortcut error: {e}")
