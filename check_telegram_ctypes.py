import ctypes
import ctypes.wintypes
import time
from PIL import ImageGrab

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Find window using ctypes EnumWindows safely
hwnds = []
def enum_cb(hwnd, lparam):
    length = user32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        title = buff.value
        pid = ctypes.wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if "Spam" in title or "Telegram" in title:
            hwnds.append((hwnd, title, pid.value))
    return True

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
cb = WNDENUMPROC(enum_cb)
user32.EnumWindows(cb, 0)
print("Found HWNDs via ctypes:", hwnds)

for h, t, p in hwnds:
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(h, ctypes.byref(rect))
    w = rect.right - rect.left
    h_len = rect.bottom - rect.top
    print(f"HWND: {h}, Title: {t}, PID: {p}, Rect: ({rect.left}, {rect.top}, {rect.right}, {rect.bottom}), Size: {w}x{h_len}")
    if w > 200 and h_len > 200:
        # Show and bring to front
        user32.ShowWindow(h, 9) # SW_RESTORE
        user32.SetForegroundWindow(h)
        time.sleep(1)
        # Capture screen
        bbox = (rect.left, rect.top, rect.right, rect.bottom)
        img = ImageGrab.grab(bbox=bbox)
        save_path = r"C:\Users\MuzaffarZed\ai_workspace\spambot_window.png"
        img.save(save_path)
        print("Captured and saved to", save_path)
        break
