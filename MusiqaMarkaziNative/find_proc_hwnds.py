import psutil, win32gui, win32process, sys
sys.stdout.reconfigure(encoding='utf-8')

for p in psutil.process_iter(['name', 'pid']):
    if "Musiqa" in p.info['name']:
        print("Found process:", p.info['name'], "PID:", p.info['pid'])
        hwnds = []
        def cb(hwnd, extra):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid == p.info['pid']:
                hwnds.append((hwnd, win32gui.GetWindowText(hwnd), win32gui.IsWindowVisible(hwnd)))
        win32gui.EnumWindows(cb, None)
        print("  Windows for PID:", hwnds)
