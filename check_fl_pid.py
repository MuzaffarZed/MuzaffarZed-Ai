import psutil
import ctypes
from ctypes import wintypes
import win32gui

user32 = ctypes.windll.user32
fl_pid = 2344

print(f"Checking PID {fl_pid}: exists = {psutil.pid_exists(fl_pid)}")
if psutil.pid_exists(fl_pid):
    p = psutil.Process(fl_pid)
    print(f"Status: {p.status()}, RAM: {p.memory_info().rss/1024/1024:.1f} MB")

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
        print(f"FL Window: HWND {hwnd}, Visible: {visible}, Title: '{buff.value}', Rect: ({rect.left}, {rect.top}, {rect.right}, {rect.bottom})")
    return 1

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, wintypes.LPARAM)
user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
