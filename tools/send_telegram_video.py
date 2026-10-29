import os
import sys
import time
import ctypes
from ctypes import wintypes

class DROPFILES(ctypes.Structure):
    _fields_ = [
        ("pFiles", wintypes.DWORD),
        ("pt", wintypes.POINT),
        ("fNC", wintypes.BOOL),
        ("fWide", wintypes.BOOL),
    ]

def copy_file_to_clipboard(file_path):
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Fayl topilmadi: {abs_path}")

    # utf-16le encoded string + double null
    path_bytes = abs_path.encode('utf-16le') + b'\x00\x00\x00\x00'

    dropfiles = DROPFILES()
    dropfiles.pFiles = ctypes.sizeof(DROPFILES)
    dropfiles.pt = wintypes.POINT(0, 0)
    dropfiles.fNC = False
    dropfiles.fWide = True

    data = bytes(dropfiles) + path_bytes

    GMEM_MOVEABLE = 0x0002
    GMEM_ZEROINIT = 0x0040
    CF_HDROP = 15

    h_global = kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(data))
    ptr = kernel32.GlobalLock(h_global)
    ctypes.memmove(ptr, data, len(data))
    kernel32.GlobalUnlock(h_global)

    if not user32.OpenClipboard(None):
        raise RuntimeError("Clipboard ochib bo'lmadi")
    try:
        user32.EmptyClipboard()
        user32.SetClipboardData(CF_HDROP, h_global)
        print("Fayl muvaffaqiyatli clipboardga nusxalandi (CF_HDROP)!")
    finally:
        user32.CloseClipboard()

def find_and_focus_telegram():
    user32 = ctypes.windll.user32
    telegram_hwnd = None

    def enum_windows_callback(hwnd, extra):
        nonlocal telegram_hwnd
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            if "telegram" in title.lower():
                telegram_hwnd = hwnd
                return False
        return True

    CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(CMPFUNC(enum_windows_callback), 0)

    if not telegram_hwnd:
        # Check by class name or process
        import psutil
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] and 'telegram' in proc.info['name'].lower():
                print(f"Telegram jarayoni topildi: PID {proc.info['pid']}")
                break

    return telegram_hwnd

def send_keys_to_window(hwnd, keys_action):
    user32 = ctypes.windll.user32
    # Restore if minimized
    SW_RESTORE = 9
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)

if __name__ == "__main__":
    test_file = r"C:\Users\MuzaffarZed\ai_workspace\qiziqarli_video.mp4"
    print("Testing clipboard preparation...")
    if os.path.exists(test_file):
        copy_file_to_clipboard(test_file)
    else:
        print("Video hali tayyor bo'lishi kutilmoqda...")
