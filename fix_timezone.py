import sys
import os
import subprocess
import ctypes
import winreg
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def apply_timezone_fix():
    print(f"[+] Running as Admin: {is_admin()}")
    
    # 1. Set Timezone to West Asia Standard Time (UTC+05:00: Ashgabat, Tashkent)
    res = subprocess.run(['tzutil', '/s', 'West Asia Standard Time'], capture_output=True, text=True)
    print(f"[+] tzutil set result: code {res.returncode}, out: {res.stdout.strip()}")

    # 2. Disable Auto Time Zone Updater Service (tzautoupdate) so Windows never overrides it
    try:
        subprocess.run(['sc', 'config', 'tzautoupdate', 'start=', 'disabled'], capture_output=True, text=True)
        subprocess.run(['sc', 'stop', 'tzautoupdate'], capture_output=True, text=True)
        print("[+] Disabled tzautoupdate service successfully via sc.exe")
    except Exception as e:
        print(f"[-] sc error: {e}")

    # 3. Disable in Registry directly
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\tzautoupdate", 0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, "Start", 0, winreg.REG_DWORD, 4)
        print("[+] Registry tzautoupdate Start set to 4 (Disabled)")
    except Exception as e:
        print(f"[-] Registry error: {e}")

    # 4. Disable Scheduled Task for SynchronizeTimeZone
    try:
        res = subprocess.run(['schtasks', '/change', '/tn', r'\Microsoft\Windows\Time Zone\SynchronizeTimeZone', '/disable'], capture_output=True, text=True)
        print(f"[+] SynchronizeTimeZone task disabled: {res.stdout.strip()}")
    except Exception as e:
        print(f"[-] schtasks error: {e}")

    # 5. Enable automatic internet time synchronization (W32Time / NTP)
    # This ensures exact time is always kept synchronized with time.windows.com / pool.ntp.org without changing timezone!
    try:
        subprocess.run(['sc', 'config', 'W32Time', 'start=', 'auto'], capture_output=True, text=True)
        subprocess.run(['net', 'start', 'W32Time'], capture_output=True, text=True)
        subprocess.run(['w32tm', '/resync', '/force'], capture_output=True, text=True)
        print("[+] W32Time (Auto Clock Sync) synchronized successfully")
    except Exception as e:
        print(f"[-] W32Time error: {e}")

    # Check final state
    res_tz = subprocess.run(['tzutil', '/g'], capture_output=True, text=True)
    print(f"[+] Final Current Timezone: {res_tz.stdout.strip()}")

if __name__ == '__main__':
    if not is_admin():
        print("[*] Re-launching with administrator privileges (RunAs)...")
        # Run elevated
        script = os.path.abspath(__file__)
        ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" --elevated', None, 1)
        print(f"[*] ShellExecuteW returned: {ret}")
        time.sleep(2)
    else:
        apply_timezone_fix()
