import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

r = subprocess.run([adb, "shell", "su", "0", "sh", "/data/local/tmp/list_vps1_gui.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
output = r.stdout.decode("utf-8", errors="replace")
print("=== VPS1 GUI LIST ===")
for line in output.splitlines()[:25]:
    print(line)
