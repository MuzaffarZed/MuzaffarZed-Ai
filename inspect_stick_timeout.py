import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def run_adb(args):
    cmd = [adb, "shell", "su", "0"] + args
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return res.stdout.strip()
    except subprocess.TimeoutExpired:
        return "<TIMEOUT>"
    except Exception as e:
        return f"<ERROR: {e}>"

print("CPU0 Gov:", run_adb(["cat", "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"]))
print("CPU0 Cur Freq:", run_adb(["cat", "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"]))
print("CPU0 Min Freq:", run_adb(["cat", "/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq"]))
print("CPU0 Max Freq:", run_adb(["cat", "/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"]))
print("swappiness:", run_adb(["cat", "/proc/sys/vm/swappiness"]))
print("vfs_cache_pressure:", run_adb(["cat", "/proc/sys/vm/vfs_cache_pressure"]))
print("read_ahead_kb:", run_adb(["cat", "/sys/block/mmcblk0/queue/read_ahead_kb"]))

# Check thermal
print("Thermal 0:", run_adb(["cat", "/sys/class/thermal/thermal_zone0/temp"]))

# Check if there are other CPU cores (cpu1, cpu2, cpu3)
for i in range(4):
    online = run_adb(["cat", f"/sys/devices/system/cpu/cpu{i}/online"])
    gov = run_adb(["cat", f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_governor"])
    print(f"Core {i}: online={online}, gov={gov}")
