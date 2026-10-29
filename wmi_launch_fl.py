import win32com.client
import time
import psutil

fl_exe = r"C:\Program Files\Image-Line\FL Studio 2025\FL64.exe"
wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
proc_startup = wmi.Get("Win32_ProcessStartup").SpawnInstance_()
proc = wmi.Get("Win32_Process")

print("Launching FL Studio via WMI (completely outside Job Object)...")
res, pid = proc.Create(f'"{fl_exe}"', r"C:\Program Files\Image-Line\FL Studio 2025", proc_startup)
print(f"WMI Create result: {res}, PID: {pid}")

time.sleep(2)
if psutil.pid_exists(pid):
    p = psutil.Process(pid)
    print(f"PID {pid} is RUNNING! RAM={p.memory_info().rss/1024/1024:.1f} MB, Parent={p.parent().name()}")
