import ctypes
from ctypes import wintypes
import time

user32 = ctypes.windll.user32

def inspect_windows():
    wins = []
    def enum_cb(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                title = buff.value
                rect = wintypes.RECT()
                user32.GetWindowRect(hwnd, ctypes.byref(rect))
                wins.append((hwnd, title, rect.left, rect.top, rect.right, rect.bottom))
        return True

    CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(CMPFUNC(enum_cb), 0)

    for hwnd, title, l, t, r, b in wins:
        if any(k in title.lower() for k in ["telegram", "избранное", "saved messages", "saqlangan"]):
            print(f"Found Window: HWND={hwnd}, Title='{title}', Rect=({l},{t},{r},{b})")

if __name__ == "__main__":
    inspect_windows()
