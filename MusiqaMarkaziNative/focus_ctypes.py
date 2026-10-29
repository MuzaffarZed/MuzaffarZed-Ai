import ctypes, psutil, time, sys
sys.stdout.reconfigure(encoding='utf-8')

user32 = ctypes.windll.user32

pids = [p.pid for p in psutil.process_iter(['name', 'pid']) if 'Musiqa' in p.info['name']]
print("Musiqa PIDs:", pids)

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

found_hwnds = []

def enum_windows_callback(hwnd, lParam):
    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value in pids:
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        is_vis = user32.IsWindowVisible(hwnd)
        found_hwnds.append((hwnd, pid.value, is_vis, buff.value))
    return True

user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)
print("Found HWNDs:", found_hwnds)

for hwnd, pid, vis, title in found_hwnds:
    if vis and title:
        print(f"Maximizing and focusing window: {hwnd} [{title}]")
        user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE = 3
        user32.SetForegroundWindow(hwnd)

time.sleep(1.5)
