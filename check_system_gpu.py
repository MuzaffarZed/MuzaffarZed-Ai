import os
import subprocess
import winreg

def check_system():
    # 1. GPU info
    print("=== GPU INFO ===")
    try:
        r = subprocess.run(["wmic", "path", "win32_VideoController", "get", "name"], capture_output=True, text=True)
        print(r.stdout.strip())
    except Exception as e:
        print(e)

    # 2. Check GameBar ShowStartupPanel
    print("\n=== GAMEBAR EXTENSIVE REGISTRY ===")
    paths = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\GameDVR"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\PolicyManager\default\ApplicationManagement\AllowGameDVR"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\GameDVR")
    ]
    for root, p in paths:
        try:
            with winreg.OpenKey(root, p) as k:
                print(f"Path: {p}")
                for i in range(winreg.QueryInfoKey(k)[1]):
                    n, v, _ = winreg.EnumValue(k, i)
                    print(f"  {n} = {v}")
        except Exception as e:
            print(f"Path {p}: {e}")

    # 3. Check NVIDIA or AMD or Intel
    print("\n=== RUNNING SERVICES & PROCESSES ===")
    try:
        r = subprocess.run(["tasklist"], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            low = line.lower()
            if any(x in low for x in ['nv', 'geforce', 'shadowplay', 'radeon', 'amd', 'intel', 'gamebar', 'bcast', 'xbox', 'lenovo', 'utility', 'osd']):
                print(line)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    check_system()
