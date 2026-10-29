import sys
import time
import subprocess
import ctypes
from pathlib import Path

# Add workspace to path
workspace = Path(r"C:\Users\MuzaffarZed\ai_workspace")
sys.path.insert(0, str(workspace))

# UTF-8 console output protection
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import pyautogui
pyautogui.FAILSAFE = False

from bridge.windows_controller import get_windows_controller

video_path = r"C:\Users\MuzaffarZed\ai_workspace\kulguli_dasturchi_video.mp4"
if not Path(video_path).exists():
    print(f"Error: Video file not found at {video_path}")
    sys.exit(1)

print("[1] Putting video into Windows Clipboard...")
ps_cmd = f"""
Add-Type -AssemblyName System.Windows.Forms
$files = New-Object System.Collections.Specialized.StringCollection
$files.Add('{video_path}')
[System.Windows.Forms.Clipboard]::SetFileDropList($files)
"""
subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd], check=True)
print("✅ Video clipboardga joylandi.")

print("[2] Finding and focusing Telegram window...")
ctrl = get_windows_controller()
windows = ctrl.list_windows()
tg_win = None
for w in windows:
    if "telegram" in w.process_name.lower():
        tg_win = w
        break

if not tg_win:
    print("Error: Telegram window not found.")
    sys.exit(1)

# Focus and restore Telegram window
ctypes.windll.user32.ShowWindow(tg_win.hwnd, 9)  # SW_RESTORE
ctypes.windll.user32.SwitchToThisWindow(tg_win.hwnd, True)
ctypes.windll.user32.SetForegroundWindow(tg_win.hwnd)
time.sleep(1.0)

left, top, right, bottom = tg_win.rect
width = right - left
height = bottom - top
print(f"Telegram Window: {left}, {top}, {right}, {bottom} (WxH: {width}x{height})")

pyautogui.FAILSAFE = False
# Move mouse safely to center of window
ctrl.mouse_move(left + int(width / 2), top + int(height / 2))
time.sleep(0.3)

# Clear state
pyautogui.FAILSAFE = False
pyautogui.press("esc")
time.sleep(0.3)

# Click on 'Избранное' (Saved Messages) in the chat list
# Exact position: image x=220, y=520
click_x = left + 220
click_y = top + 520
print(f"[3] Clicking 'Избранное' at ({click_x}, {click_y})...")
ctrl.mouse_click(click_x, click_y)
time.sleep(1.2)

# Click message input box in the right pane
input_x = left + int(width * 0.65)
input_y = bottom - 45
print(f"[4] Focusing message input box at ({input_x}, {input_y})...")
ctrl.mouse_click(input_x, input_y)
time.sleep(0.5)

# Ensure clipboard has the file
subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd], check=True)
time.sleep(0.3)

# Paste the video (Ctrl + V)
print("[5] Pasting video with Ctrl+V...")
pyautogui.hotkey("ctrl", "v")
time.sleep(1.5)

# Telegram shows modal dialog: 'Отправить как видео' or confirmation
print("[6] Confirming send with Enter...")
pyautogui.press("enter")
time.sleep(2.0)

# Capture verification screenshot
print("[7] Capturing verification screenshot...")
out_screenshot = r"C:\Users\MuzaffarZed\ai_workspace\tools\telegram_sent_comedy.png"
ctrl.capture_screen(save_path=out_screenshot)
print(f"✅ Bajarildi! Skrinshot: {out_screenshot}")
