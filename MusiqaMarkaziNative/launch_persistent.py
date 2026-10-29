import subprocess, os, time

exe = r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"
print("Launching detached:", exe)
DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200
p = subprocess.Popen([exe],
                     creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                     close_fds=True)
print("Persistent PID:", p.pid)
time.sleep(3)

port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
if os.path.exists(port_file):
    with open(port_file, "r") as f:
        print("Running Port:", f.read().strip())
