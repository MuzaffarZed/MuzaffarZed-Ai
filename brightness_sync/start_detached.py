"""
Spawn a completely detached, persistent background process via WMI Win32_Process.Create.
Eski jarayonlarni tozalab, yagona yangi fondagi xizmatni ishga tushiradi.
"""

import win32com.client
import os
import sys
import time


def kill_existing_services():
    """Mavjud barcha brightness_sync jarayonlarini to'xtatadi."""
    wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
    procs = wmi.ExecQuery(
        "SELECT ProcessId, CommandLine FROM Win32_Process WHERE Name = 'pythonw.exe' OR Name = 'python.exe'"
    )
    my_pid = os.getpid()
    for p in procs:
        cmd = p.CommandLine or ""
        pid = p.ProcessId
        if pid != my_pid and "brightness_sync" in cmd and "service.py" in cmd:
            try:
                os.kill(pid, 9)
                print(f"[CLEANUP] Eski jarayon to'xtatildi: PID {pid}")
            except Exception:
                pass
    time.sleep(0.3)


def start_detached():
    kill_existing_services()

    wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
    proc_startup = wmi.Get("Win32_ProcessStartup").SpawnInstance_()
    proc_startup.ShowWindow = 0  # SW_HIDE (butunlay yashirin)

    proc = wmi.Get("Win32_Process")
    pythonw = r"C:\Users\MuzaffarZed\ai_workspace\venv\Scripts\pythonw.exe"
    script = r"C:\Users\MuzaffarZed\ai_workspace\brightness_sync\service.py"
    work_dir = r"C:\Users\MuzaffarZed\ai_workspace\brightness_sync"

    in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
    in_params.CommandLine = f'"{pythonw}" "{script}" --daemon'
    in_params.CurrentDirectory = work_dir
    in_params.ProcessStartupInformation = proc_startup

    out = proc.ExecMethod_("Create", in_params)
    res = out.ReturnValue
    pid = out.ProcessId

    if res == 0:
        print(f"[OK] Jarayon mustaqil ravishda fonda ishga tushirildi! PID: {pid}")
        return pid
    else:
        print(f"[!] WMI orqali jarayonni yaratishda xatolik: kod {res}")
        return None


if __name__ == "__main__":
    start_detached()
