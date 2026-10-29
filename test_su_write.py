import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

# Pass the entire command as single string inside su 0
cmd = [adb, "shell", "su 0 sh -c \"echo 1 > /sys/devices/platform/soc/sdc0/sunxi_insert\""]
r = subprocess.run(cmd, capture_output=True, text=True)
print("Output:", r.stdout, r.stderr)
