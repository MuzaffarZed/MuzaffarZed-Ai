import sys
import os
import time
import subprocess
import ctypes
from pathlib import Path

# Add ai_workspace to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from bridge.windows_controller import get_windows_controller
ctrl = get_windows_controller()

user32 = ctypes.windll.user32

VK_CONTROL = 0x11
VK_V = 0x56
VK_RETURN = 0x0D

def send_actions():
    h_desk = user32.OpenDesktopW('default', 0, False, 0x01FF)
    if h_desk:
        user32.SetThreadDesktop(h_desk)

    # 1. Telegram window
    wins = [w for w in ctrl.list_windows() if 'telegram' in w.process_name.lower()]
    if not wins:
        print('Telegram oynasi topilmadi!')
        return False
    tg = wins[0]
    user32.ShowWindow(tg.hwnd, 9)
    user32.SetForegroundWindow(tg.hwnd)
    time.sleep(0.5)

    # 2. Focus input box at bottom (relative x: 600, y: bottom - 40)
    rect = tg.rect
    input_x = rect[0] + 600
    input_y = rect[3] - 40
    print(f"Chat maydoniga bosilmoqda: ({input_x}, {input_y})")
    user32.SetCursorPos(input_x, input_y)
    time.sleep(0.1)
    user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.05)
    user32.mouse_event(4, 0, 0, 0, 0)
    time.sleep(0.5)

    # 3. Clipboard ga videoni qo'shish
    video_path = r"C:\Users\MuzaffarZed\ai_workspace\kulguli_dasturchi_video.mp4"
    if not os.path.exists(video_path):
        print("XATO: Video topilmadi:", video_path)
        return False

    print("Videoni clipboard ga qo'yish...")
    ps_cmd = f"""
    Add-Type -AssemblyName System.Windows.Forms
    $files = New-Object System.Collections.Specialized.StringCollection
    $files.Add('{video_path}')
    [System.Windows.Forms.Clipboard]::SetFileDropList($files)
    """
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd], check=True)
    time.sleep(0.5)

    # 4. Ctrl + V yuborish
    print("Ctrl+V yuborilmoqda...")
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_V, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_V, 0, 2, 0)
    user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(1.5)

    # 5. Enter bosish (yuborish dialogini tasdiqlash)
    print("Enter (yuborish) bosilmoqda...")
    user32.keybd_event(VK_RETURN, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_RETURN, 0, 2, 0)
    time.sleep(3.5)

    return True

print("Jarayon boshlandi...")
success = ctrl.run_on_default_desktop(send_actions)
print("Natija:", success)

# 6. Skrinshot olish
time.sleep(1.0)
res = ctrl.capture_screen()
print("Yangi skrinshot:", res.get('file_path'))
