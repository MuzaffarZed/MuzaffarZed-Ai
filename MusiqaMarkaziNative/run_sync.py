import subprocess, time

cmd = [r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = p.communicate()
print("Exit code:", p.returncode)
print("STDOUT:", stdout)
print("STDERR:", stderr)
