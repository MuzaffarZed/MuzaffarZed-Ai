import os
import time
import ctypes
from ctypes import wintypes
import psutil

user32 = ctypes.windll.user32

# 1. Launch / Bring Telegram to front
lnk_path = r"C:\Users\MuzaffarZed\Desktop\Telegram Desktop.lnk"
print("Launching / Activating Telegram Desktop...")
os.startfile(lnk_path)
time.sleep(2.0)

# 2. Find all visible windows
def enum_windows():
    wins = []
    def enum_cb(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            cls_buff = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, cls_buff, 256)
            proc_id = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(proc_id))
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            wins.append((hwnd, buff.value, cls_buff.value, proc_id.value, (rect.left, rect.top, rect.right, rect.bottom)))
        return True

    CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(CMPFUNC(enum_cb), 0)
    return wins

wins = enum_windows()
tg_wins = []
for h, title, cls, pid, r in wins:
    if "telegram" in title.lower() or "qt5" in cls.lower() or "qt6" in cls.lower() or "telegram" in cls.lower():
        tg_wins.append((h, title, cls, pid, r))

# Check by process name as well
for p in psutil.process_iter(['pid', 'name']):
    if p.info['name'] and 'telegram' in p.info['name'].lower():
        for h, title, cls, pid, r in wins:
            if pid == p.info['pid'] and (h, title, cls, pid, r) not in tg_wins:
                tg_wins.append((h, title, cls, pid, r))

print(f"Found {len(tg_wins)} Telegram windows:")
for w in tg_wins:
    print(w)
