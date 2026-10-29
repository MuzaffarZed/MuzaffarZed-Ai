import win32gui
import win32process
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def find_x360ce_windows():
    found = []
    def enum_cb(hwnd, _):
        if win32gui.IsWindow(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            text = win32gui.GetWindowText(hwnd)
            visible = win32gui.IsWindowVisible(hwnd)
            if pid == 1968 or 'x360' in text.lower():
                found.append((hwnd, text, visible))
    win32gui.EnumWindows(enum_cb, None)
    return found

wins = find_x360ce_windows()
print(f"Found {len(wins)} windows for x360ce:")
for w in wins:
    print(w)
