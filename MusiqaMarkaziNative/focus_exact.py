import win32gui, win32con, time, sys
sys.stdout.reconfigure(encoding='utf-8')

found = []
def enum_cb(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        txt = win32gui.GetWindowText(hwnd)
        if "Musiqa" in txt or "DirectX" in txt or "MuzaffarZed" in txt:
            found.append((hwnd, txt))

win32gui.EnumWindows(enum_cb, None)
print("Found visible windows:", found)
for h, t in found:
    win32gui.ShowWindow(h, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(h)
    print("Brought to front:", t)
