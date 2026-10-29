import sys
import os
import ctypes
import time
from PIL import Image

sys.path.append(r"C:\Users\MuzaffarZed\ai_workspace")
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from bridge.windows_controller import WindowsController

wc = WindowsController()
focused = wc.focus_window("Настройки")
print(f"Focused Настройки: {focused}")
time.sleep(1)

# Now take screenshot of the focused window
proof_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\settings_window_proof.png"

# Use PrintWindow on hwnd 1903234
import win32gui
import win32ui
import win32con

hwnd = 1903234
# Get client or window rect
left, top, right, bot = win32gui.GetWindowRect(hwnd)
w = right - left
h = bot - top
print(f"Window bounds: {w}x{h}")

hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
saveDC.SelectObject(saveBitMap)

# PrintWindow with PW_RENDERFULLCONTENT = 2
ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)

im.save(proof_path)
print(f"Successfully saved window proof: {proof_path} ({im.size})")
