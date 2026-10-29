import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

with open("C:/Users/MuzaffarZed/ai_workspace/tmp_cmd.sh", "w", encoding="utf-8") as f:
    f.write("dmesg | tail -n 25\n")
subprocess.run([adb, "push", "C:/Users/MuzaffarZed/ai_workspace/tmp_cmd.sh", "/data/local/tmp/tmp_cmd.sh"], capture_output=True)
r = subprocess.run([adb, "shell", "su", "0", "sh", "/data/local/tmp/tmp_cmd.sh"], capture_output=True, text=True, timeout=10)
print(r.stdout.strip())
