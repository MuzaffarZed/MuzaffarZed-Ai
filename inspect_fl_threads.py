import ctypes
from ctypes import wintypes
import psutil

pid = 8072
p = psutil.Process(pid)
user32 = ctypes.windll.user32

hwnds = []
def thread_cb(hwnd, lparam):
    length = user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    visible = user32.IsWindowVisible(hwnd)
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    hwnds.append((hwnd, buff.value, visible, (rect.left, rect.top, rect.right, rect.bottom)))
    return 1

cb = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, wintypes.LPARAM)(thread_cb)

for th in p.threads():
    user32.EnumThreadWindows(th.id, cb, 0)

print(f"Total thread windows across {p.num_threads()} threads: {len(hwnds)}")
for h, t, v, r in hwnds:
    print(f"HWND: {h} | Visible: {v} | Rect: {r} | Title: '{t}'")
