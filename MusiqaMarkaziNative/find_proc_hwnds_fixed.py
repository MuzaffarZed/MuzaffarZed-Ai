import psutil, win32gui, win32process, win32con, sys
sys.stdout.reconfigure(encoding='utf-8')

for p in psutil.process_iter(['name', 'pid']):
    if "Musiqa" in p.info['name']:
        print("Found process:", p.info['name'], "PID:", p.info['pid'])
        hwnds = []
        def cb(hwnd, extra):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid == p.info['pid']:
                    hwnds.append((hwnd, win32gui.GetWindowText(hwnd), win32gui.IsWindowVisible(hwnd)))
            except:
                pass
            return True
        win32gui.EnumWindows(cb, None)
        print("  Windows for PID:", hwnds)
        for h, t, v in hwnds:
            if v and t:
                print(f"Maximizing and focusing: {h} - {t}")
                win32gui.ShowWindow(h, win32con.SW_MAXIMIZE)
                win32gui.SetForegroundWindow(h)
