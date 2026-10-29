import os
import sys
import subprocess
import winreg
import ctypes
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def setup_permanent_lock():
    print("[1/5] Setting TimeZone to West Asia Standard Time (UTC+05:00: Ashgabat, Tashkent)...")
    res = subprocess.run(['tzutil', '/s', 'West Asia Standard Time'], capture_output=True, text=True)
    print("      tzutil:", res.stdout.strip())

    print("[2/5] Disabling tzautoupdate service (Auto Time Zone Updater)...")
    subprocess.run(['sc', 'config', 'tzautoupdate', 'start=', 'disabled'], capture_output=True)
    subprocess.run(['sc', 'stop', 'tzautoupdate'], capture_output=True)

    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\tzautoupdate", 0, winreg.KEY_SET_VALUE) as k:
        winreg.SetValueEx(k, "Start", 0, winreg.REG_DWORD, 4)

    print("[3/5] Disabling Windows TimeZone scheduled tasks...")
    subprocess.run(['schtasks', '/change', '/tn', r'\Microsoft\Windows\Time Zone\SynchronizeTimeZone', '/disable'], capture_output=True)

    print("[4/5] Configuring NTP Windows Time Service (W32Time)...")
    subprocess.run(['sc', 'config', 'W32Time', 'start=', 'auto'], capture_output=True)
    subprocess.run(['net', 'start', 'W32Time'], capture_output=True)
    subprocess.run(['w32tm', '/config', '/manualpeerlist:time.windows.com,0x8 pool.ntp.org,0x8', '/syncfromflags:manual', '/update'], capture_output=True)
    subprocess.run(['w32tm', '/resync', '/nowait'], capture_output=True)

    print("[5/5] Creating MuzaffarZed_Lock_UTC5 Watchdog Scheduled Task...")
    # Create a batch/cmd file in ai_workspace that runs tzutil and disables tzautoupdate
    cmd_file = os.path.join(r"C:\Users\MuzaffarZed\ai_workspace", "lock_tz_utc5.cmd")
    with open(cmd_file, "w", encoding="utf-8") as f:
        f.write('@echo off\n')
        f.write('tzutil /s "West Asia Standard Time"\n')
        f.write('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\tzautoupdate" /v Start /t REG_DWORD /d 4 /f >nul 2>&1\n')
    
    # Register scheduled task to run as SYSTEM at startup and every 1 hour
    task_xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Permanent UTC+5 Tashkent TimeZone Enforcer by MuzaffarZed</Description>
    <Author>MuzaffarZed</Author>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Enabled>true</Enabled>
    </BootTrigger>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
    <TimeTrigger>
      <StartBoundary>2026-01-01T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <Repetition>
        <Interval>PT1H</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-18</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT10M</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{cmd_file}</Command>
    </Exec>
  </Actions>
</Task>'''
    xml_path = os.path.join(r"C:\Users\MuzaffarZed\ai_workspace", "task_utc5.xml")
    with open(xml_path, "w", encoding="utf-16") as f:
        f.write(task_xml)
    
    res = subprocess.run(['schtasks', '/create', '/tn', 'MuzaffarZed_Lock_UTC5', '/xml', xml_path, '/f'], capture_output=True, text=True)
    print("      schtasks create:", res.stdout.strip())
    
    print("[+] All done successfully! TimeZone is permanently anchored to UTC+05:00 Tashkent.")

if __name__ == '__main__':
    if not is_admin():
        script = os.path.abspath(__file__)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" --elevated', None, 1)
        time.sleep(2)
    else:
        setup_permanent_lock()
