import win32gui
def enum_cb(hwnd, results):
    if win32gui.IsWindowVisible(hwnd):
        txt = win32gui.GetWindowText(hwnd)
        if txt and ("Musiqa" in txt or "Markazi" in txt or "Pro" in txt or "O'zbek" in txt):
            results.append((hwnd, txt))
res = []
win32gui.EnumWindows(enum_cb, res)
print("Found windows:", res)
