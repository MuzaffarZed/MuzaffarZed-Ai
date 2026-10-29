import win32api
import time
import psutil

lnk_path = r"C:\Users\MuzaffarZed\Desktop\Mani Izlab - FL Studio Loyihasi.lnk"
print(f"Launching shortcut via ShellExecute: {lnk_path}")

ret = win32api.ShellExecute(0, "open", lnk_path, "", "", 1)
print(f"ShellExecute returned: {ret}")

for i in range(10):
    time.sleep(1)
    procs = [p for p in psutil.process_iter(['pid', 'name', 'memory_info']) if 'fl64' in p.info['name'].lower()]
    if procs:
        p = procs[0]
        print(f"Second {i+1}: FL64 running! PID={p.pid}, RAM={p.info['memory_info'].rss/1024/1024:.1f} MB")
    else:
        print(f"Second {i+1}: FL64 not found")
