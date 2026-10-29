import sys
import os
import time
import win32gui
import win32ui
import ctypes
from PIL import Image

sys.path.append(r"C:\Users\MuzaffarZed\ai_workspace")
from MuzaffarZed_Twin_Gamepad_Studio import TwinGamepadStudio

proof_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\twin_gamepad_studio_proof.png"

app = TwinGamepadStudio()
app.update()
time.sleep(0.5)
app.update()

# Get HWND of Tkinter window
# Tkinter window id is retrieved via app.winfo_id()
hwnd = app.winfo_id()
# Wait, for top-level window:
parent_hwnd = win32gui.GetParent(hwnd) or hwnd
print(f"Tkinter HWND: {hwnd}, Parent HWND: {parent_hwnd}")

# Use PrintWindow on the top-level window
target = parent_hwnd if win32gui.GetWindowText(parent_hwnd) else hwnd
left, top, right, bot = win32gui.GetWindowRect(target)
w = max(right - left, 100)
h = max(bot - top, 100)
print(f"Target HWND: {target}, Size: {w}x{h}, Title: {win32gui.GetWindowText(target)}")

hwndDC = win32gui.GetWindowDC(target)
mfcDC = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()
saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
saveDC.SelectObject(saveBitMap)

ctypes.windll.user32.PrintWindow(target, saveDC.GetSafeHdc(), 2)

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)
im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(target, hwndDC)

im.save(proof_path)
print(f"[+] Saved visual proof: {proof_path} ({im.size})")

app.destroy()
