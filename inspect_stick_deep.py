import subprocess
import os

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def run_adb(cmd_str):
    res = subprocess.run([adb, "shell", "su", "0", "sh", "-c", cmd_str], capture_output=True, text=True)
    return res.stdout.strip()

print("=== GPU DEVFREQ ===")
paths = run_adb("ls -d /sys/class/devfreq/* 2>/dev/null").split()
for p in paths:
    if p:
        gov = run_adb(f"cat {p}/governor 2>/dev/null")
        cur = run_adb(f"cat {p}/cur_freq 2>/dev/null")
        avail = run_adb(f"cat {p}/available_governors 2>/dev/null")
        print(f"{p}: gov={gov}, cur={cur}, avail={avail}")

print("\n=== VM SYSCTL ===")
print("swappiness:", run_adb("cat /proc/sys/vm/swappiness"))
print("vfs_cache_pressure:", run_adb("cat /proc/sys/vm/vfs_cache_pressure"))
print("dirty_ratio:", run_adb("cat /proc/sys/vm/dirty_ratio"))
print("dirty_background_ratio:", run_adb("cat /proc/sys/vm/dirty_background_ratio"))

print("\n=== THERMAL ===")
print("thermal temps:", run_adb("cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null"))

print("\n=== BACKGROUND PACKAGES ===")
print(run_adb("ps -A -o PID,NAME,CMDLINE | grep -E 'launcher|box|droid|media|google'"))

print("\n=== BUILD PROPERTIES RELATED TO PERFORMANCE ===")
print(run_adb("getprop | grep -E 'dalvik|hwui|sf\.|debug\.'"))
