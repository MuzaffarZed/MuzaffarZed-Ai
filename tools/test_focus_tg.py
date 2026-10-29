import os
import time
import ctypes
from ctypes import wintypes
import pyautogui
pyautogui.FAILSAFE = False

user32 = ctypes.windll.user32

# 1. Focus Telegram
def focus_tg():
    # Find Telegram window
    tg_hwnd = 263354
    if not user32.IsWindow(tg_hwnd):
        # find by title
        def enum_cb(h, _):
            nonlocal tg_hwnd
            if user32.IsWindowVisible(h):
                buff = ctypes.create_unicode_buffer(256)
                user32.GetWindowTextW(h, buff, 256)
                if "telegram" in buff.value.lower():
                    tg_hwnd = h
                    return False
            return True
        CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        user32.EnumWindows(CMPFUNC(enum_cb), 0)

    print(f"Target HWND: {tg_hwnd}")
    user32.ShowWindow(tg_hwnd, 9) # SW_RESTORE
    user32.SetForegroundWindow(tg_hwnd)
    time.sleep(0.5)
    return tg_hwnd

hwnd = focus_tg()
print("Pressing Ctrl+0...")
pyautogui.hotkey('ctrl', '0')
time.sleep(1.0)

# Capture screen
shot = pyautogui.screenshot()
out_shot = r"C:\Users\MuzaffarZed\ai_workspace\tools\tg_after_ctrl0.png"
shot.save(out_shot)
print(f"Saved screenshot to: {out_shot}")
