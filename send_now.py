import sys
import time
import subprocess
import ctypes
from pathlib import Path

# UTF-8 console protection
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

workspace = Path(r"C:\Users\MuzaffarZed\ai_workspace")
sys.path.insert(0, str(workspace))

from bridge.windows_controller import get_windows_controller

user32 = ctypes.windll.user32

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
KEYEVENTF_KEYUP = 0x0002
VK_CONTROL = 0x11
VK_V = 0x56
VK_RETURN = 0x0D
VK_ESCAPE = 0x1B

def win_click(x: int, y: int):
    user32.SetCursorPos(int(x), int(y))
    time.sleep(0.06)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.06)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def win_key(vk: int):
    user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.06)
    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)

def win_ctrl_v():
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.06)
    user32.keybd_event(VK_V, 0, 0, 0)
    time.sleep(0.06)
    user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.06)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

print("[1] Putting SavdoPro.apk into clipboard...")
apk_path = r"C:\Users\MuzaffarZed\ai_workspace\SavdoPro.apk"
ps_cmd = f"""
Add-Type -AssemblyName System.Windows.Forms
$files = New-Object System.Collections.Specialized.StringCollection
$files.Add('{apk_path}')
[System.Windows.Forms.Clipboard]::SetFileDropList($files)
"""
subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
print("Clipboard successfully set with APK.")

print("[2] Focusing Telegram...")
ctrl = get_windows_controller()
ctrl.focus_window("Telegram")
time.sleep(0.5)

print("[3] Clicking hamburger menu at (530, 140)...")
win_click(530, 140)
time.sleep(0.6)

print("[4] Clicking Избранное at (570, 572)...")
win_click(570, 572)
time.sleep(0.8)

print("[5] Re-verifying clipboard...")
subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
time.sleep(0.2)

print("[6] Clicking message box at (1050, 830)...")
win_click(1050, 830)
time.sleep(0.3)

print("[7] Pasting file (Ctrl+V)...")
win_ctrl_v()
time.sleep(1.8)

print("[8] Confirming file send (Enter)...")
win_key(VK_RETURN)
time.sleep(2.0)

print("[9] Capturing proof screenshot...")
ctrl.capture_screen(save_path=r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\776c4a96-8eb4-4dda-9f36-a6e771149a78\final_saved_messages_proof.png")
print("Done! Check screenshot.")
