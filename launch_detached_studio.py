import sys
import os
import subprocess
import time

studio_py = r"C:\Users\MuzaffarZed\ai_workspace\MuzaffarZed_Twin_Gamepad_Studio.py"
p = subprocess.Popen(
    [sys.executable, studio_py],
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    close_fds=True
)
print(f"Launched detached PID: {p.pid}")
time.sleep(2)
