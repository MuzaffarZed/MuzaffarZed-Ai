import sys
import time
import os
from pathlib import Path

root_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(root_dir))

import win32gui
import win32con
import ctypes
from PIL import ImageGrab

user32 = ctypes.windll.user32

# Find "vakal minus" explorer window
target_hwnd = None
def enum_cb(hwnd, lparam):
    global target_hwnd
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            if "vakal minus" in title.lower():
                target_hwnd = hwnd
                print(f"Found Explorer window HWND: {hwnd}, Title: '{title}'")
    return 1

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
user32.EnumWindows(WNDENUMPROC(enum_cb), 0)

if not target_hwnd:
    # If not found, open it
    print("Opening Explorer for vakal minus...")
    os.startfile(r"C:\Users\MuzaffarZed\Desktop\vakal minus")
    time.sleep(2)
    user32.EnumWindows(WNDENUMPROC(enum_cb), 0)

if target_hwnd:
    print(f"Bringing HWND {target_hwnd} to foreground and maximizing...")
    user32.ShowWindow(target_hwnd, win32con.SW_RESTORE)
    user32.ShowWindow(target_hwnd, win32con.SW_MAXIMIZE)
    
    # Simulate ALT keystroke to unlock SetForegroundWindow
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
    
    user32.BringWindowToTop(target_hwnd)
    user32.SwitchToThisWindow(target_hwnd, True)
    try:
        user32.SetForegroundWindow(target_hwnd)
    except Exception:
        pass
    
    # Set topmost momentarily then normal to guarantee it is on top of Antigravity
    user32.SetWindowPos(target_hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
    time.sleep(0.5)
    user32.SetWindowPos(target_hwnd, -2, 0, 0, 0, 0, 0x0001 | 0x0002)
    time.sleep(1.0)
    
    # Capture screen
    shot = ImageGrab.grab()
    out_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\vakal_minus_real_proof.png"
    shot.save(out_path)
    print(f"Successfully captured real proof: {out_path} ({os.path.getsize(out_path)} bytes)")
else:
    print("Could not find or open vakal minus window.")
