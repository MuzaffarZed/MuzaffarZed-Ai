import time
import win32gui
import win32con
import win32process
import psutil
from PIL import ImageGrab

def find_telegram_hwnd():
    # Find Telegram PID first
    tg_pids = set()
    for p in psutil.process_iter(['pid', 'name']):
        try:
            if 'telegram' in p.info['name'].lower():
                tg_pids.add(p.info['pid'])
        except Exception:
            pass
    print("Telegram PIDs:", tg_pids)

    hwnds = []
    def enum_cb(hwnd, extra):
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid in tg_pids:
            title = win32gui.GetWindowText(hwnd)
            visible = win32gui.IsWindowVisible(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            hwnds.append((hwnd, title, pid, visible, rect))
        return True

    win32gui.EnumWindows(enum_cb, None)
    return hwnds

def main():
    hwnds = find_telegram_hwnd()
    print("Found windows for Telegram PID:", hwnds)
    if not hwnds:
        print("No windows found!")
        return

    # Filter to visible or main window with area > 0
    valid_hwnds = [h for h in hwnds if (h[4][2] - h[4][0]) > 200 and (h[4][3] - h[4][1]) > 200]
    if not valid_hwnds:
        valid_hwnds = hwnds

    target_hwnd, title, pid, visible, rect = valid_hwnds[0]
    print(f"Targeting HWND: {target_hwnd}, Title: '{title}', Rect: {rect}")

    # Bring to front
    win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
    win32gui.ShowWindow(target_hwnd, win32con.SW_SHOW)
    time.sleep(0.5)
    try:
        win32gui.SetForegroundWindow(target_hwnd)
    except Exception as e:
        print("SetForegroundWindow warning:", e)
    time.sleep(0.5)

    rect = win32gui.GetWindowRect(target_hwnd)
    print("Updated window rect:", rect)
    if rect[2] > rect[0] and rect[3] > rect[1]:
        img = ImageGrab.grab(bbox=rect)
        img_path = r"C:\Users\MuzaffarZed\ai_workspace\telegram_bot_screen.png"
        img.save(img_path)
        print(f"Saved screenshot to: {img_path}")

if __name__ == "__main__":
    main()
