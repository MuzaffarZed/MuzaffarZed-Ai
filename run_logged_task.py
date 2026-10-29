import ctypes
import os
import time

bat_path = r'C:\Users\MuzaffarZed\ai_workspace\create_task.bat'
log_path = r'C:\Users\MuzaffarZed\ai_workspace\create_task.log'

with open(bat_path, 'w', encoding='utf-8') as f:
    f.write(f'schtasks /create /tn "MuzaffarZed_Lock_UTC5" /tr "C:\\Users\\MuzaffarZed\\ai_workspace\\lock_tz_utc5.cmd" /sc HOURLY /ru "SYSTEM" /f > "{log_path}" 2>&1\n')

ret = ctypes.windll.shell32.ShellExecuteW(None, 'runas', 'cmd.exe', f'/c "{bat_path}"', None, 0)
time.sleep(2)

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='cp866', errors='ignore') as f:
        print("Log output:", f.read())
else:
    print("Log file not found.")
