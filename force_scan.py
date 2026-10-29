import subprocess
import time

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

# Write 1 to sunxi_insert via su
cmd = [adb, "shell", "su", "-c", "echo 1 > /sys/devices/platform/soc/sdc0/sunxi_insert"]
r = subprocess.run(cmd, capture_output=True, text=True)
print("CMD output:", r.stdout, r.stderr)

time.sleep(2)

print("\n=== SM LIST-DISKS ===")
print(subprocess.run([adb, "shell", "sm", "list-disks"], capture_output=True, text=True).stdout)

print("\n=== SM LIST-VOLUMES ===")
print(subprocess.run([adb, "shell", "sm", "list-volumes"], capture_output=True, text=True).stdout)

print("\n=== BLOCK DEVICES (mmc/sd) ===")
devs = subprocess.run([adb, "shell", "ls", "-la", "/dev/block"], capture_output=True, text=True).stdout
for l in devs.splitlines():
    if "mmc" in l or "sd" in l:
        print(l)

print("\n=== DMESG LAST 20 LINES ===")
dmesg = subprocess.run([adb, "shell", "dmesg"], capture_output=True, text=True).stdout
print("\n".join(dmesg.splitlines()[-20:]))
