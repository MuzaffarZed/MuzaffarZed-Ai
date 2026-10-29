import sys
import time
import os
from pathlib import Path

# Safe UTF-8 console output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

root_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(root_dir))

import win32gui
import win32con
import ctypes
from PIL import ImageGrab
from bridge.windows_controller import get_windows_controller

controller = get_windows_controller()

print("Listing all current windows:")
wins = controller.list_windows()
fl_win = None
exp_win = None
for w in wins:
    try:
        print(f"HWND: {w.hwnd} | Proc: {w.process_name} | Title: '{w.title}'")
    except Exception:
        pass
    if "FL" in w.process_name or "FL Studio" in w.title:
        fl_win = w
    if "vakal minus" in w.title.lower() or "проводник" in w.title.lower():
        exp_win = w

if fl_win:
    print(f"\nFocusing FL Studio window (HWND: {fl_win.hwnd})...")
    # Restore & maximize FL Studio
    win32gui.ShowWindow(fl_win.hwnd, win32con.SW_RESTORE)
    win32gui.ShowWindow(fl_win.hwnd, win32con.SW_MAXIMIZE)
    
    # Robust foreground
    ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)
    win32gui.BringWindowToTop(fl_win.hwnd)
    ctypes.windll.user32.SwitchToThisWindow(fl_win.hwnd, True)
    try:
        win32gui.SetForegroundWindow(fl_win.hwnd)
    except Exception:
        pass
    
    time.sleep(1.5)
    
    # Save full screenshot with FL Studio front-and-center
    shot = ImageGrab.grab()
    out1 = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\fl_studio_proof_real.png"
    shot.save(out1)
    print(f"Saved FL Studio proof screenshot: {out1} ({os.path.getsize(out1)} bytes)")
else:
    print("FL Studio window not found in active windows list!")
