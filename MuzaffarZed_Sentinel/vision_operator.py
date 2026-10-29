import os
import time
import ctypes
from ctypes import wintypes
from PIL import Image

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0009

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

def get_mouse_position():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return (pt.x, pt.y)

def set_mouse_position(x, y):
    user32.SetCursorPos(int(x), int(y))

def click_mouse(x=None, y=None, button="left", double=False):
    if x is not None and y is not None:
        set_mouse_position(x, y)
        time.sleep(0.05)
    down = MOUSEEVENTF_LEFTDOWN if button == "left" else MOUSEEVENTF_RIGHTDOWN
    up = MOUSEEVENTF_LEFTUP if button == "left" else MOUSEEVENTF_RIGHTUP
    user32.mouse_event(down, 0, 0, 0, 0)
    time.sleep(0.03)
    user32.mouse_event(up, 0, 0, 0, 0)
    if double:
        time.sleep(0.1)
        user32.mouse_event(down, 0, 0, 0, 0)
        time.sleep(0.03)
        user32.mouse_event(up, 0, 0, 0, 0)

def capture_screen_gdi(save_path):
    """
    Robust GDI desktop capture that works across Windows sessions.
    """
    w = user32.GetSystemMetrics(0)
    h = user32.GetSystemMetrics(1)
    
    hdc_screen = user32.GetDC(0)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
    hbm = gdi32.CreateCompatibleBitmap(hdc_screen, w, h)
    gdi32.SelectObject(hdc_mem, hbm)
    
    # SRCCOPY = 0x00CC0020
    gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc_screen, 0, 0, 0x00CC0020)
    
    # Save using PIL or BMP if needed
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    
    # Clean up handles
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(0, hdc_screen)
    gdi32.DeleteObject(hbm)
    return True

def get_all_visible_windows():
    windows = []
    def enum_windows_proc(hwnd, extra):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                title = buff.value
                rect = RECT()
                user32.GetWindowRect(hwnd, ctypes.byref(rect))
                w = rect.right - rect.left
                h = rect.bottom - rect.top
                if w > 50 and h > 50:
                    windows.append({
                        "hwnd": hwnd,
                        "title": title,
                        "rect": (rect.left, rect.top, rect.right, rect.bottom),
                        "width": w,
                        "height": h
                    })
        return True
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)
    return windows

if __name__ == "__main__":
    print("Vision Operator resilient module initialized!")
    pos = get_mouse_position()
    print("Cursor:", pos)
    wins = get_all_visible_windows()
    print("Found windows:", len(wins))
