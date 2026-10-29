import psutil
import ctypes
from ctypes import wintypes

pid = 12500
try:
    p = psutil.Process(pid)
    print(f"PID: {p.pid}, Name: {p.name()}, Status: {p.status()}")
    print("Cmdline:", p.cmdline())
    print("Children:", p.children(recursive=True))
    print(f"Num threads: {p.num_threads()}")
    print("Memory:", p.memory_info())
except Exception as e:
    print("Error:", e)

user32 = ctypes.windll.user32

def enum_all(hwnd, lparam):
    proc_id = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(proc_id))
    if proc_id.value == pid:
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        print(f"FL Window: HWND {hwnd}, Visible: {user32.IsWindowVisible(hwnd)}, Title: '{buff.value}', Rect: ({rect.left}, {rect.top}, {rect.right}, {rect.bottom})")
    return 1

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, wintypes.LPARAM)
user32.EnumWindows(WNDENUMPROC(enum_all), 0)
