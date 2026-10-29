import win32com.client
import time
import psutil

fl_exe = r"C:\Program Files\Image-Line\FL Studio 2025\FL64.exe"
fl_dir = r"C:\Program Files\Image-Line\FL Studio 2025"
proj = r"C:\Users\MuzaffarZed\Desktop\vakal minus\Mani_Izlab_Ovvora_Bolmang_Studio_Project.flp"

print("Launching via Shell.Application (Explorer)...")
shell = win32com.client.Dispatch("Shell.Application")
shell.ShellExecute(fl_exe, f'"{proj}"', fl_dir, "open", 1)
print("ShellExecute sent to Explorer.")

time.sleep(3)
procs = [p for p in psutil.process_iter(['pid', 'name', 'memory_info']) if 'fl64' in p.info['name'].lower()]
if procs:
    p = procs[0]
    print(f"FL64 is RUNNING under Explorer! PID: {p.pid}, Memory: {p.info['memory_info'].rss/1024/1024:.1f} MB, Parent: {p.parent().name()} (PID {p.parent().pid})")
else:
    print("FL64 not found.")
