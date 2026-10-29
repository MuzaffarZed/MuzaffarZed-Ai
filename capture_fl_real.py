import time
import ctypes
import win32gui
import win32con
import win32process
from PIL import ImageGrab

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def force_foreground(target_hwnd):
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    cur_thread = kernel32.GetCurrentThreadId()
    
    print(f"Target HWND: {target_hwnd}, FG HWND: {fg_hwnd}, FG Thread: {fg_thread}, Cur Thread: {cur_thread}")
    
    if fg_thread != cur_thread:
        user32.AttachThreadInput(cur_thread, fg_thread, True)
    
    # Simulate ALT keystroke to unlock SetForegroundWindow
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
    
    user32.ShowWindow(target_hwnd, 9) # SW_RESTORE
    user32.ShowWindow(target_hwnd, 3) # SW_MAXIMIZE
    user32.BringWindowToTop(target_hwnd)
    user32.SetForegroundWindow(target_hwnd)
    user32.SwitchToThisWindow(target_hwnd, True)
    
    if fg_thread != cur_thread:
        user32.AttachThreadInput(cur_thread, fg_thread, False)
    
    # Topmost trick
    user32.SetWindowPos(target_hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
    user32.SetWindowPos(target_hwnd, -2, 0, 0, 0, 0, 0x0001 | 0x0002)

# Find FL Studio HWND
fl_hwnd = None
def find_fl(hwnd, extra):
    global fl_hwnd
    if user32.IsWindow(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            if "FL Studio" in buff.value:
                fl_hwnd = hwnd
                print(f"Found FL Studio HWND: {hwnd}, Title: '{buff.value}'")
    return True

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
user32.EnumWindows(WNDENUMPROC(find_fl), 0)

if fl_hwnd:
    force_foreground(fl_hwnd)
    time.sleep(1)
    
    # Capture screen
    shot = ImageGrab.grab()
    out_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\fl_studio_real_proof.png"
    shot.save(out_path)
    print(f"Screenshot saved to: {out_path}")
else:
    print("FL Studio HWND not found via EnumWindows")
