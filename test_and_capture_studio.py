import sys
import os
import time
import subprocess
import win32gui
import win32ui
import ctypes
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

studio_py = r"C:\Users\MuzaffarZed\ai_workspace\MuzaffarZed_Twin_Gamepad_Studio.py"
proof_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\twin_gamepad_studio_proof.png"

# Launch studio in subprocess
proc = subprocess.Popen([sys.executable, studio_py])
print(f"Launched Studio with PID: {proc.pid}")

time.sleep(3)

# Find window for proc.pid
target_hwnd = None
def cb(hwnd, _):
    global target_hwnd
    import win32process
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid == proc.pid and win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if "JOSTIK" in title or "GAMEPAD" in title:
            target_hwnd = hwnd

win32gui.EnumWindows(cb, None)

if target_hwnd:
    print(f"Found Studio Window HWND: {target_hwnd}")
    left, top, right, bot = win32gui.GetWindowRect(target_hwnd)
    w = right - left
    h = bot - top
    print(f"Bounds: {w}x{h}")

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
    print(f"[+] Saved visual proof: {proof_path}")
else:
    print("[-] Target window not found!")

# Keep running or leave open for user? Leave open so user sees it!
print("Studio is active and running!")
