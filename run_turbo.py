import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

# 1. Push turbo.sh
print("Pushing turbo.sh to stick...")
subprocess.run([adb, "push", "C:/Users/MuzaffarZed/ai_workspace/turbo.sh", "/data/local/tmp/turbo.sh"], check=True)

# 2. Make executable
subprocess.run([adb, "shell", "su", "0", "chmod", "755", "/data/local/tmp/turbo.sh"], check=True)

# 3. Execute turbo.sh
print("Executing turbo.sh with root privileges...")
res = subprocess.run([adb, "shell", "su", "0", "sh", "/data/local/tmp/turbo.sh"], capture_output=True, text=True, timeout=15)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
