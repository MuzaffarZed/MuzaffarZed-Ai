import win32gui, win32process, psutil

pids = [p.pid for p in psutil.process_iter(['name', 'pid']) if 'Musiqa' in p.info['name']]
print("Musiqa PIDs:", pids)

hwnds = []
def cb(hwnd, _):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid in pids:
        txt = win32gui.GetWindowText(hwnd)
        vis = win32gui.IsWindowVisible(hwnd)
        hwnds.append((hwnd, pid, vis, txt))

win32gui.EnumWindows(cb, None)
print("Windows for Musiqa:", hwnds)
