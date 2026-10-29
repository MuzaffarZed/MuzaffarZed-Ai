import subprocess
import time
import sys
import os

fl_exe = r"C:\Program Files\Image-Line\FL Studio 2025\FL64.exe"
fl_dir = r"C:\Program Files\Image-Line\FL Studio 2025"
proj = r"C:\Users\MuzaffarZed\Desktop\vakal minus\Mani_Izlab_Ovvora_Bolmang_Studio_Project.flp"

print(f"Daemon: Starting FL Studio 2025 with project: {proj}")
sys.stdout.flush()

proc = subprocess.Popen([fl_exe, proj], cwd=fl_dir)
print(f"Daemon: FL Studio PID {proc.pid} started. Keeping daemon alive...")
sys.stdout.flush()

# Keep process running
proc.wait()
print(f"Daemon: FL Studio exited with code {proc.returncode}")
