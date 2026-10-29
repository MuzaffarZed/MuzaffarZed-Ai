import win32gui
import win32con
import win32process
import time
from PIL import ImageGrab
import os

def bring_and_capture():
    target_hwnd = None
    def enum_cb(hwnd, extra):
        nonlocal target_hwnd
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Настройки" in title or "Параметры" in title or "Settings" in title:
                target_hwnd = hwnd
    win32gui.EnumWindows(enum_cb, None)
    
    if not target_hwnd:
        print("Window not found via EnumWindows")
        return
    
    print(f"Found hwnd: {target_hwnd}, title: {win32gui.GetWindowText(target_hwnd)}")
    
    win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(target_hwnd)
    win32gui.SetWindowPos(target_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    win32gui.SetWindowPos(target_hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    time.sleep(1)
    
    rect = win32gui.GetWindowRect(target_hwnd)
    print(f"Window rect: {rect}")
    
    # Capture window
    img = ImageGrab.grab(bbox=rect)
    save_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\settings_window_proof.png"
    img.save(save_path)
    print(f"Saved proof to {save_path}")

if __name__ == '__main__':
    bring_and_capture()
