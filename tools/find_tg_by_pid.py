import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
PID = 16372

hwnds = []
def enum_cb(hwnd, lparam):
    proc_id = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(proc_id))
    if proc_id.value == PID:
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        is_vis = user32.IsWindowVisible(hwnd)
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        hwnds.append((hwnd, buff.value, is_vis, (rect.left, rect.top, rect.right, rect.bottom)))
    return True

CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
user32.EnumWindows(CMPFUNC(enum_cb), 0)

for h, title, vis, r in hwnds:
    print(f"HWND: {h}, Title: '{title}', Visible: {vis}, Rect: {r}")
