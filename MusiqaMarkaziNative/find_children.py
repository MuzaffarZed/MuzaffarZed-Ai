import psutil, ctypes, sys
sys.stdout.reconfigure(encoding='utf-8')

user32 = ctypes.windll.user32
p = psutil.Process(15024)
all_pids = [15024] + [c.pid for c in p.children(recursive=True)]
print("All PIDs:", all_pids)

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
hwnds = []

def cb(hwnd, lParam):
    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value in all_pids:
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        is_vis = user32.IsWindowVisible(hwnd)
        hwnds.append((hwnd, pid.value, is_vis, buff.value))
    return True

user32.EnumWindows(WNDENUMPROC(cb), 0)
print("HWNDs:", hwnds)
