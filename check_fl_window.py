import ctypes
from ctypes import wintypes
import psutil

user32 = ctypes.windll.user32
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, wintypes.LPARAM)

fl_pid = 5148
fl_hwnds = []

def enum_cb(hwnd, lparam):
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value == fl_pid:
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        visible = user32.IsWindowVisible(hwnd)
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        fl_hwnds.append((hwnd, buff.value, visible, (rect.left, rect.top, rect.right, rect.bottom)))
    return 1

user32.EnumWindows(WNDENUMPROC(enum_cb), 0)

print(f"Windows for PID {fl_pid} (FL64.exe):")
for hwnd, title, visible, r in fl_hwnds:
    print(f"HWND: {hwnd} | Visible: {visible} | Rect: {r} | Title: '{title}'")
