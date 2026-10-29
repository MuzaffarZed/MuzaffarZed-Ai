import sys
import os
sys.path.append(r"C:\Users\MuzaffarZed\ai_workspace")

# Fix stdout encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from bridge.windows_controller import WindowsController

wc = WindowsController()
wins = wc.list_windows()
for w in wins:
    print(f"[{w.hwnd}] {w.process_name} | {w.title}")
