import psutil
import subprocess
import os

found = False
for p in psutil.process_iter(['pid', 'name', 'exe']):
    try:
        name = p.info['name'] or ''
        if 'telegram' in name.lower():
            print(f"Telegram process: PID {p.info['pid']}, Name: {name}, Exe: {p.info['exe']}")
            found = True
    except Exception:
        pass

if not found:
    print("Telegram is not currently running.")
    lnk = r"C:\Users\MuzaffarZed\Desktop\Telegram Desktop.lnk"
    print(f"Desktop shortcut exists: {os.path.exists(lnk)}")
    # Check default appdata locations
    appdata_tg = os.path.expanduser(r"~\AppData\Roaming\Telegram Desktop\Telegram.exe")
    print(f"AppData Telegram.exe exists: {os.path.exists(appdata_tg)}")
