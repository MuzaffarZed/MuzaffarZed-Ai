import win32gui

def cb(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        t = win32gui.GetWindowText(hwnd)
        if t:
            print(f"{hwnd}: {t}")

win32gui.EnumWindows(cb, None)
