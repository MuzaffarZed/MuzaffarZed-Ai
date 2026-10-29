import ctypes
from ctypes import wintypes
import psutil

pid = 8072
p = psutil.Process(pid)
print(f"PID: {pid}, Name: {p.name()}, RAM: {p.memory_info().rss/1024/1024:.1f} MB, Num Threads: {p.num_threads()}")

user32 = ctypes.windll.user32
hwnds = []

def enum_cb(hwnd, lparam):
    proc_id = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(proc_id))
    if proc_id.value == pid:
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        visible = user32.IsWindowVisible(hwnd)
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        hwnds.append((hwnd, buff.value, visible, (rect.left, rect.top, rect.right, rect.bottom)))
    return 1

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, wintypes.LPARAM)
user32.EnumWindows(WNDENUMPROC(enum_cb), 0)

print(f"Total top-level windows for PID {pid}: {len(hwnds)}")
for h, t, v, r in hwnds:
    print(f"HWND: {h} | Visible: {v} | Rect: {r} | Title: '{t}'")
