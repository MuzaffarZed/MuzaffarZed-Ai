import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

script = """
SD="/storage/3EF8-7461"
ls -1 "$SD/VPS1/GUI" | head -n 30
"""

with open("C:/Users/MuzaffarZed/ai_workspace/tmp_cmd.sh", "w", encoding="utf-8") as f:
    f.write(script)
subprocess.run([adb, "push", "C:/Users/MuzaffarZed/ai_workspace/tmp_cmd.sh", "/data/local/tmp/tmp_cmd.sh"], capture_output=True)
r = subprocess.run([adb, "shell", "su", "0", "sh", "/data/local/tmp/tmp_cmd.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
print("VPS1 GUI files raw:\n", r.stdout.decode("utf-8", errors="replace"))
