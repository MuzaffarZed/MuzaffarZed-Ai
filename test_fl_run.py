import subprocess
import time
import psutil

fl_exe = r"C:\Program Files\Image-Line\FL Studio 2025\FL64.exe"
print(f"Launching {fl_exe}...")
p = subprocess.Popen([fl_exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(f"Process PID: {p.pid}")

for i in range(15):
    time.sleep(1)
    ret = p.poll()
    if ret is not None:
        stdout, stderr = p.communicate()
        print(f"FL64 exited after {i+1} seconds with code: {ret}")
        print("STDOUT:", stdout.decode('utf-8', errors='replace'))
        print("STDERR:", stderr.decode('utf-8', errors='replace'))
        break
    else:
        try:
            proc = psutil.Process(p.pid)
            print(f"Second {i+1}: PID {p.pid} RUNNING, RSS={proc.memory_info().rss/1024/1024:.1f} MB, CPU={proc.cpu_percent()}%")
        except Exception as e:
            print(f"Second {i+1}: Error querying proc: {e}")
