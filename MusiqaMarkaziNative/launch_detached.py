import os, time, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

# Kill any existing
subprocess.run(["taskkill", "/F", "/IM", "Musiqa_Markazi_Pro.exe"], capture_output=True)
time.sleep(1)

# Start process
DETACHED_PROCESS = 0x00000008
p = subprocess.Popen([r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"],
                     creationflags=DETACHED_PROCESS,
                     close_fds=True)
print("Started PID:", p.pid)
time.sleep(3)

# Check if alive
import psutil
try:
    proc = psutil.Process(p.pid)
    print("Process is alive:", proc.is_running(), proc.name(), proc.status())
except Exception as e:
    print("Process check error:", e)

# Find port
port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
if os.path.exists(port_file):
    with open(port_file, "r") as f:
        print("Running port:", f.read().strip())
