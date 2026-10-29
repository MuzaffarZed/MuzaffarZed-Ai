import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def run_remote_sh(script_content):
    with open("C:/Users/MuzaffarZed/ai_workspace/tmp_cmd.sh", "w", encoding="utf-8") as f:
        f.write(script_content)
    subprocess.run([adb, "push", "C:/Users/MuzaffarZed/ai_workspace/tmp_cmd.sh", "/data/local/tmp/tmp_cmd.sh"], capture_output=True)
    r = subprocess.run([adb, "shell", "su", "0", "sh", "/data/local/tmp/tmp_cmd.sh"], capture_output=True, text=True, timeout=15)
    return r.stdout.strip()

cmd = r"""
ls -la /storage/3EF8-7461/
"""

print(run_remote_sh(cmd))
