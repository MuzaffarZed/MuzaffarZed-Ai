import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

cmd = [r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"]
print("Running:", cmd)
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
try:
    stdout, stderr = p.communicate(timeout=6)
    print("Return code:", p.returncode)
    print("STDOUT:\n", stdout)
    print("STDERR:\n", stderr)
except subprocess.TimeoutExpired:
    print("Process is still running normally after 6 seconds!")
    p.terminate()
