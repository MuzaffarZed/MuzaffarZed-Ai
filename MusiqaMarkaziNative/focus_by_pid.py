import win32gui, win32process, win32con, time, os

port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
target_hwnds = []

def enum_cb(hwnd, extra):
    if win32gui.IsWindowVisible(hwnd):
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        title = win32gui.GetWindowText(hwnd)
        if "Musiqa" in title or "Markazi" in title:
            target_hwnds.append((hwnd, pid, title))

win32gui.EnumWindows(enum_cb, None)
print("Target windows:", target_hwnds)
for h, pid, t in target_hwnds:
    win32gui.ShowWindow(h, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(h)
    print("Maximized and brought to foreground:", t)
time.sleep(1)
