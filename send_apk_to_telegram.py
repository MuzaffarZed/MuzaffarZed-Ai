import sys
import time
import subprocess
from pathlib import Path

# Ensure ai_workspace is in path
workspace = Path(r"C:\Users\MuzaffarZed\ai_workspace")
sys.path.insert(0, str(workspace))

# UTF-8 console output protection
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


from bridge.windows_controller import get_windows_controller
import pyautogui
import pyperclip

# Disable PyAutoGUI failsafe
pyautogui.FAILSAFE = False

print("[1] Putting SavdoPro.apk into clipboard...")
apk_path = r"C:\Users\MuzaffarZed\ai_workspace\SavdoPro.apk"
ps_cmd = f"""
Add-Type -AssemblyName System.Windows.Forms
$files = New-Object System.Collections.Specialized.StringCollection
$files.Add('{apk_path}')
[System.Windows.Forms.Clipboard]::SetFileDropList($files)
"""
subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
print("Clipboard file set successfully.")

print("[2] Getting WindowsController and focusing Telegram...")
ctrl = get_windows_controller()
pyautogui.FAILSAFE = False

# List windows and find Telegram main window
windows = ctrl.list_windows()
tg_win = None
for w in windows:
    name_l = w.process_name.lower()
    title_l = w.title.lower()
    width = w.rect[2] - w.rect[0]
    height = w.rect[3] - w.rect[1]
    if ("telegram" in name_l or "telegram" in title_l or "xotin" in title_l) and width > 500 and height > 400:
        tg_win = w
        break

if not tg_win:
    print("ERROR: Main Telegram window not found!")
    sys.exit(1)

print(f"Found Telegram: HWND={tg_win.hwnd}, Title={tg_win.title}, Rect={tg_win.rect}")
import ctypes
pyautogui.press("alt")
ctypes.windll.user32.ShowWindow(tg_win.hwnd, 9)  # SW_RESTORE
ctypes.windll.user32.SwitchToThisWindow(tg_win.hwnd, True)
ctypes.windll.user32.SetForegroundWindow(tg_win.hwnd)
time.sleep(1.0)


left, top, right, bottom = tg_win.rect

print("[3] Clearing state with ESC...")
pyautogui.press("esc")
time.sleep(0.2)
pyautogui.press("esc")
time.sleep(0.2)

print("[4] Opening Telegram search with Ctrl+F...")
pyautogui.hotkey("ctrl", "f")
time.sleep(0.5)

print("[5] Clicking Избранное in frequent contacts at (left + 325, top + 188)...")
fav_x = left + 325
fav_y = top + 188
ctrl.mouse_click(fav_x, fav_y)
time.sleep(0.8)

# Now Избранное should be open. Let's make sure message box is focused
print("[6] Clicking chat message input area...")
msg_x = left + 450
msg_y = bottom - 45
ctrl.mouse_click(msg_x, msg_y)
time.sleep(0.4)

# Ensure clipboard STILL has the file (in case typing or clipboard changed)
subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
time.sleep(0.2)

print("[7] Pasting SavdoPro.apk (Ctrl+V)...")
pyautogui.hotkey("ctrl", "v")
time.sleep(1.5)

print("[8] Confirming file send (Enter)...")
pyautogui.press("enter")
time.sleep(1.0)

print("[9] Capturing screenshot of result...")
out_screenshot = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\776c4a96-8eb4-4dda-9f36-a6e771149a78\telegram_sent_verification.png"
ctrl.capture_screen(out_screenshot)
print(f"Done! Screenshot saved to {out_screenshot}")
