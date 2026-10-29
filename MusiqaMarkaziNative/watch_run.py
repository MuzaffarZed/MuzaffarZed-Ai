import subprocess, time, sys
sys.stdout.reconfigure(encoding='utf-8')

cmd = [r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print("Started PID:", p.pid)
for i in range(10):
    time.sleep(1)
    ret = p.poll()
    if ret is not None:
        print(f"Process exited after {i+1} seconds with code {ret}")
        stdout, stderr = p.communicate()
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
        sys.exit(0)
    else:
        print(f"Second {i+1}: Still running...")

print("Still running after 10 seconds! Keeping it running.")
