import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(root_dir))

import traceback
import win32gui
import win32con
import win32process
import ctypes
from bridge.windows_controller import get_windows_controller

controller = get_windows_controller()

target_hwnd = 592748

print("Testing direct focus on 592748:")
try:
    if win32gui.IsIconic(target_hwnd):
        win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
    else:
        win32gui.ShowWindow(target_hwnd, win32con.SW_SHOW)
    
    current_thread = ctypes.windll.kernel32.GetCurrentThreadId()
    target_thread, _ = win32process.GetWindowThreadProcessId(target_hwnd)
    print(f"Current thread: {current_thread}, Target thread: {target_thread}")
    
    if current_thread != target_thread:
        res1 = ctypes.windll.user32.AttachThreadInput(current_thread, target_thread, True)
        print(f"AttachThreadInput attach result: {res1}")
        win32gui.SetForegroundWindow(target_hwnd)
        res2 = ctypes.windll.user32.AttachThreadInput(current_thread, target_thread, False)
        print(f"AttachThreadInput detach result: {res2}")
    else:
        win32gui.SetForegroundWindow(target_hwnd)
    print("SetForegroundWindow succeeded!")
except Exception as e:
    print(f"SetForegroundWindow failed: {e}")
    traceback.print_exc()

print("\nNow testing robust focus method:")
try:
    # Keybd event to bypass lock
    ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)
    
    win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
    win32gui.BringWindowToTop(target_hwnd)
    ctypes.windll.user32.SwitchToThisWindow(target_hwnd, True)
    ctypes.windll.user32.SetForegroundWindow(target_hwnd)
    print("Robust focus succeeded!")
except Exception as e:
    print(f"Robust focus failed: {e}")
    traceback.print_exc()
