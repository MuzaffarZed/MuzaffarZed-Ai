import sys
import os
import time
import win32gui
import win32ui
import win32process
import ctypes
from PIL import Image

sys.path.append(r"C:\Users\MuzaffarZed\ai_workspace")
from bridge.windows_controller import WindowsController

wc = WindowsController()

def capture():
    target_hwnd = None
    all_wins = []
    def cb():
        nonlocal target_hwnd
        def enum_cb(hwnd, _):
            nonlocal target_hwnd
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                all_wins.append((hwnd, title))
                if "JOSTIK" in title or "GAMEPAD" in title or "MuzaffarZed" in title:
                    target_hwnd = hwnd
        win32gui.EnumWindows(enum_cb, None)
    
    wc.run_on_default_desktop(cb)
    
    print(f"Total visible windows: {len(all_wins)}")
    for h, t in all_wins:
        if t:
            print(f"  [{h}] {t}")
            
    if target_hwnd:
        print(f"Target found: {target_hwnd}")
        proof_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\twin_gamepad_studio_proof.png"
        
        left, top, right, bot = win32gui.GetWindowRect(target_hwnd)
        w = max(right - left, 100)
        h = max(bot - top, 100)
        
        hwndDC = win32gui.GetWindowDC(target_hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
        
        ctypes.windll.user32.PrintWindow(target_hwnd, saveDC.GetSafeHdc(), 2)
        
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(target_hwnd, hwndDC)
        
        im.save(proof_path)
        print(f"[+] Saved screenshot: {proof_path} ({im.size})")

if __name__ == '__main__':
    capture()
