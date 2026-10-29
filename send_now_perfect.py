import sys
import time
import subprocess
import ctypes
from pathlib import Path

# Force UTF-8 console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Attach to interactive default desktop
user32 = ctypes.windll.user32
h_desk = user32.OpenDesktopW("default", 0, False, 0x01FF)
if h_desk:
    user32.SetThreadDesktop(h_desk)

# Force 1:1 physical pixel DPI awareness (1920x1080)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        user32.SetProcessDPIAware()
    except Exception:
        pass

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
KEYEVENTF_KEYUP = 0x0002
VK_CONTROL = 0x11
VK_V = 0x56
VK_RETURN = 0x0D

def click(x: int, y: int):
    user32.SetCursorPos(int(x), int(y))
    time.sleep(0.08)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.08)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def hotkey_ctrl_v():
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.08)
    user32.keybd_event(VK_V, 0, 0, 0)
    time.sleep(0.08)
    user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.08)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

def key_enter():
    user32.keybd_event(VK_RETURN, 0, 0, 0)
    time.sleep(0.08)
    user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)

print("[1] Putting SavdoPro.apk into clipboard...")
apk_path = r"C:\Users\MuzaffarZed\ai_workspace\SavdoPro.apk"
ps_cmd = f"""
Add-Type -AssemblyName System.Windows.Forms
$files = New-Object System.Collections.Specialized.StringCollection
$files.Add('{apk_path}')
[System.Windows.Forms.Clipboard]::SetFileDropList($files)
"""
subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
print("Clipboard ready with APK.")

workspace = Path(r"C:\Users\MuzaffarZed\ai_workspace")
sys.path.insert(0, str(workspace))
from bridge.windows_controller import get_windows_controller

ctrl = get_windows_controller()
ctrl.focus_window("Telegram")
time.sleep(0.5)

print("[2] Clicking Избранное at physical (600, 538)...")
click(600, 538)
time.sleep(1.0)

print("[3] Clicking message input box at physical (1100, 840)...")
click(1100, 840)
time.sleep(0.5)

print("[4] Ensuring clipboard has APK...")
subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
time.sleep(0.3)

print("[5] Pasting file (Ctrl+V)...")
hotkey_ctrl_v()
time.sleep(2.0)

print("[6] Confirming Send (Enter)...")
key_enter()
time.sleep(2.5)

print("[7] Capturing screenshot...")
ctrl.capture_screen(save_path=r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\776c4a96-8eb4-4dda-9f36-a6e771149a78\final_sent_result.png")
print("Done!")
