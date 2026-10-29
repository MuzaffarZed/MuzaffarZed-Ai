import win32gui, sys
sys.stdout.reconfigure(encoding='utf-8')

all_windows = []
def enum_cb(hwnd, _):
    txt = win32gui.GetWindowText(hwnd)
    if "Musiqa" in txt or "DirectX" in txt or "MuzaffarZed" in txt:
        all_windows.append((hwnd, win32gui.IsWindowVisible(hwnd), txt))

win32gui.EnumWindows(enum_cb, None)
print("All matching windows (visible or not):", all_windows)
