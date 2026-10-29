import sys
import os
import time
import subprocess
import ctypes
from pathlib import Path

# Add ai_workspace to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import pyautogui
import pyperclip

pyautogui.FAILSAFE = False

# Enable Per-Monitor DPI Awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass

from bridge.windows_controller import get_windows_controller
ctrl = get_windows_controller()

user32 = ctypes.windll.user32

# 1. Find Telegram window
tg_win = None
for w in ctrl.list_windows():
    if "telegram" in w.process_name.lower():
        tg_win = w
        break

if not tg_win:
    print("Telegram topilmadi!")
    sys.exit(1)

tg_hwnd = tg_win.hwnd
print(f"Telegram topildi: HWND {tg_hwnd}")

# 2. Focus window
user32.ShowWindow(tg_hwnd, 9)
user32.SwitchToThisWindow(tg_hwnd, True)
user32.SetForegroundWindow(tg_hwnd)
time.sleep(1.0)

# Move mouse to center
left, top, right, bottom = tg_win.rect
width = right - left
height = bottom - top
ctrl.mouse_move(left + width // 2, top + height // 2)
time.sleep(0.3)

# 3. Clear search / state with ESC
pyautogui.press("esc")
time.sleep(0.2)
pyautogui.press("esc")
time.sleep(0.3)

# 4. Open search with Ctrl+F
pyautogui.hotkey("ctrl", "f")
time.sleep(0.5)

# 5. Type "Избранное"
pyperclip.copy("Избранное")
pyautogui.hotkey("ctrl", "v")
time.sleep(0.8)

# 6. Open "Избранное" chat
pyautogui.press("down")
time.sleep(0.2)
pyautogui.press("enter")
time.sleep(1.0)

# 7. Put video into clipboard
video_path = r"C:\Users\MuzaffarZed\ai_workspace\kulguli_dasturchi_video.mp4"
ps_cmd = f"""
Add-Type -AssemblyName System.Windows.Forms
$files = New-Object System.Collections.Specialized.StringCollection
$files.Add('{video_path}')
[System.Windows.Forms.Clipboard]::SetFileDropList($files)
"""
subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd], check=True)
time.sleep(0.5)

# 8. Paste into chat (Ctrl+V)
print("Fayl paste qilinmoqda (Ctrl+V)...")
pyautogui.hotkey("ctrl", "v")
time.sleep(1.5)

# 9. Press Enter to confirm send
print("Tasdiqlash (Enter)...")
pyautogui.press("enter")
time.sleep(2.5)

# 10. Capture screenshot of result
out_img = r"C:\Users\MuzaffarZed\ai_workspace\tools\tg_saved_verified.png"
ctrl.capture_screen(save_path=out_img)
print("Bajarildi! Skrinshot saqlandi:", out_img)
