import ctypes
import sys
import os
import time
import subprocess

def main():
    cmd = r'schtasks /create /tn MuzaffarZed_Lock_UTC5 /tr C:\Users\MuzaffarZed\ai_workspace\lock_tz_utc5.cmd /sc HOURLY /ru SYSTEM /f'
    bat_path = r'C:\Users\MuzaffarZed\ai_workspace\create_task.bat'
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(cmd + '\n')
    ret = ctypes.windll.shell32.ShellExecuteW(None, 'runas', 'cmd.exe', f'/c "{bat_path}"', None, 0)
    print('Executed with code:', ret)
    time.sleep(2)
    res = subprocess.run(['schtasks', '/query', '/tn', 'MuzaffarZed_Lock_UTC5'], capture_output=True, text=True, errors='ignore')
    print('Task query result:\n', res.stdout)

if __name__ == '__main__':
    main()
