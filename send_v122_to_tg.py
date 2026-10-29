import sys
import time
import ctypes
import subprocess
from pathlib import Path

# UTF-8 console output protection
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Step 1: Set file drop list into clipboard via .ps1
ps1_path = r"C:\Users\MuzaffarZed\ai_workspace\set_clipboard.ps1"
res = subprocess.run(
    ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", ps1_path],
    capture_output=True,
    text=True,
    check=True
)
print("Clipboard output:", res.stdout.strip())

# Step 2: Target main Telegram window (HWND 919014)
user32 = ctypes.windll.user32
hwnd = 919014

# Simulate Alt key to bypass foreground lock
user32.keybd_event(0x12, 0, 0, 0)
user32.keybd_event(0x12, 0, 2, 0)

user32.ShowWindow(hwnd, 9) # SW_RESTORE
user32.SwitchToThisWindow(hwnd, True)
user32.SetForegroundWindow(hwnd)
time.sleep(0.8)

# Step 3: Click inside message input box at (1153, 982)
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
user32.SetCursorPos(1153, 982)
time.sleep(0.1)
user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
time.sleep(0.1)
user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
time.sleep(0.5)

# Step 4: Paste Ctrl+V
VK_CONTROL = 0x11
VK_V = 0x56
VK_RETURN = 0x0D
KEYEVENTF_KEYUP = 0x0002

user32.keybd_event(VK_CONTROL, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_V, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
time.sleep(0.1)
user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
print("Pasted file via Ctrl+V")

time.sleep(1.8)

# Step 5: Press Enter to confirm send
user32.keybd_event(VK_RETURN, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)
print("Pressed Enter to send")

time.sleep(3.5)

# Step 6: Capture verification screenshot
sys.path.insert(0, r"C:\Users\MuzaffarZed\ai_workspace")
from bridge.windows_controller import get_windows_controller
ctrl = get_windows_controller()
shot_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\776c4a96-8eb4-4dda-9f36-a6e771149a78\tg_v122_sent_proof.png"
ctrl.capture_screen(save_path=shot_path)
print("Saved verification screenshot to:", shot_path)
