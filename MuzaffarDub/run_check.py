import subprocess
import time

p = subprocess.Popen(
    ["C:\\Users\\MuzaffarZed\\ai_workspace\\venv\\Scripts\\python.exe", "C:\\Users\\MuzaffarZed\\ai_workspace\\MuzaffarDub\\server.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
time.sleep(2)
poll = p.poll()
print("POLL:", poll)
if poll is not None:
    out, err = p.communicate()
    print("STDOUT:", out)
    print("STDERR:", err)
else:
    print("Process is running! PID:", p.pid)
    p.terminate()
