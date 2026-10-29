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

from bridge.windows_controller import get_windows_controller
ctrl = get_windows_controller()

import pyautogui
pyautogui.FAILSAFE = False

user32 = ctypes.windll.user32

VK_CONTROL = 0x11
VK_V = 0x56
VK_RETURN = 0x0D
VK_ESCAPE = 0x1B

def win32_click(x, y):
    user32.SetCursorPos(int(x), int(y))
    time.sleep(0.1)
    user32.mouse_event(2, 0, 0, 0, 0) # LEFTDOWN
    time.sleep(0.05)
    user32.mouse_event(4, 0, 0, 0, 0) # LEFTUP
    time.sleep(0.1)

def win32_hotkey(vk1, vk2):
    user32.keybd_event(vk1, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(vk2, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(vk2, 0, 2, 0)
    user32.keybd_event(vk1, 0, 2, 0)
    time.sleep(0.1)

def win32_press(vk):
    user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(vk, 0, 2, 0)
    time.sleep(0.1)

print("1. Telegram oynasini qidirish...")
tg_win = None
for w in ctrl.list_windows():
    if "telegram" in w.process_name.lower():
        tg_win = w
        break

if not tg_win:
    print("XATO: Telegram oynasi topilmadi!")
    sys.exit(1)

tg_hwnd = tg_win.hwnd
rect = tg_win.rect
print(f"Telegram topildi: HWND {tg_hwnd}, Rect: {rect}")

# 2. Telegram oynasini oldinga olib chiqish
user32.ShowWindow(tg_hwnd, 9) # SW_RESTORE
user32.SetForegroundWindow(tg_hwnd)
time.sleep(0.8)

# 3. 'Izbrannoe' (Saved Messages) tugmasini bosish
# Rect: (left, top, right, bottom)
# Relative coords of Избранное item: x ~ 200, y ~ 532
click_x = rect[0] + 200
click_y = rect[1] + 532
print(f"2. 'Избранное' chatiga bosilmoqda: ({click_x}, {click_y})")
win32_click(click_x, click_y)
time.sleep(1.0)

# 4. Faylni Clipboard ga joylash
video_path = r"C:\Users\MuzaffarZed\ai_workspace\kulguli_dasturchi_video.mp4"
if not os.path.exists(video_path):
    print("XATO: Video fayl topilmadi:", video_path)
    sys.exit(1)

print("3. Fayl buferga (clipboard) nusxalanmoqda...")
ps_cmd = f"""
Add-Type -AssemblyName System.Windows.Forms
$files = New-Object System.Collections.Specialized.StringCollection
$files.Add('{video_path}')
[System.Windows.Forms.Clipboard]::SetFileDropList($files)
"""
subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd], check=True)
time.sleep(0.5)

# 5. Telegram chatiga Paste qilish (Ctrl+V)
print("4. Chat maydoniga Ctrl+V yuborilmoqda...")
# Matn kiritish maydoniga bitta bosish
# Chat maydoni odatda oyna o'ng tomonining pastki qismida
input_x = rect[0] + (rect[2] - rect[0]) * 3 // 4
input_y = rect[3] - 50
win32_click(input_x, input_y)
time.sleep(0.3)

win32_hotkey(VK_CONTROL, VK_V)
time.sleep(1.5)

# 6. Yuborishni tasdiqlash (Enter)
print("5. Yuborishni tasdiqlash (Enter)...")
win32_press(VK_RETURN)
time.sleep(3.0)

# 7. Natijani tekshirish uchun skrinshot olish
res = ctrl.capture_screen()
file_path = res.get('file_path') if res else None
print(f"6. Skrinshot olindi: {file_path}")
