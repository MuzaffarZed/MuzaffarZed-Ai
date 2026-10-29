import win32gui
import win32con
import time

title = "🎵 O'zbekiston Musiqa Markazi Pro v11.0 — DirectX 12 Studio • Dasturchi: MuzaffarZed"
h = win32gui.FindWindow(None, title)
print(f"HWND: {h}")
if h:
    win32gui.ShowWindow(h, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(h)
    time.sleep(1)
    rect = win32gui.GetWindowRect(h)
    print(f"Window Rect: {rect}")
