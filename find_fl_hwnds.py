import ctypes
from ctypes import wintypes
import psutil

user32 = ctypes.windll.user32
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, wintypes.LPARAM)

pid = 5148
proc = psutil.Process(pid)
threads = proc.threads()

print(f"PID {pid} has {len(threads)} threads.")

found_windows = []

def thread_enum_cb(hwnd, lparam):
    length = user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    visible = user32.IsWindowVisible(hwnd)
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    found_windows.append((hwnd, buff.value, visible, (rect.left, rect.top, rect.right, rect.bottom)))
    return 1

cb = WNDENUMPROC(thread_enum_cb)

for th in threads:
    user32.EnumThreadWindows(th.id, cb, 0)

print(f"Found {len(found_windows)} windows across all threads:")
for hwnd, title, visible, r in found_windows:
    print(f"HWND: {hwnd} | Visible: {visible} | Rect: {r} | Title: '{title}'")
