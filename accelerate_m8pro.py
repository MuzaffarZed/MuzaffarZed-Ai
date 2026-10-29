import subprocess
import time

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def run_cmd(cmd):
    # Run with su 0
    full_cmd = [adb, "shell", f"su 0 sh -c '{cmd}'"]
    try:
        r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=8)
        return r.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

print("=== STARTING M8 PRO MINI TURBO ACCELERATION ===")

# 1. CPU Cores & Governors
print("\n[1] CPU Cores & Governor Acceleration...")
for i in range(4):
    run_cmd(f"echo 1 > /sys/devices/system/cpu/cpu{i}/online 2>/dev/null")
    run_cmd(f"echo performance > /sys/devices/system/cpu/cpu{i}/cpufreq/scaling_governor 2>/dev/null")
    # If performance is not accepted, raise min_freq to max
    max_freq = run_cmd(f"cat /sys/devices/system/cpu/cpu{i}/cpufreq/scaling_max_freq 2>/dev/null")
    if max_freq.isdigit():
        run_cmd(f"echo {max_freq} > /sys/devices/system/cpu/cpu{i}/cpufreq/scaling_min_freq 2>/dev/null")
    gov = run_cmd(f"cat /sys/devices/system/cpu/cpu{i}/cpufreq/scaling_governor 2>/dev/null")
    cur = run_cmd(f"cat /sys/devices/system/cpu/cpu{i}/cpufreq/scaling_cur_freq 2>/dev/null")
    print(f"  CPU Core {i}: Governor={gov}, Current Freq={cur} kHz")

# 2. GPU Devfreq Acceleration (Mali-G31)
print("\n[2] GPU Devfreq Acceleration...")
gpu_paths = run_cmd("ls -d /sys/class/devfreq/* 2>/dev/null").split()
for p in gpu_paths:
    if p:
        run_cmd(f"echo performance > {p}/governor 2>/dev/null")
        gov = run_cmd(f"cat {p}/governor 2>/dev/null")
        cur = run_cmd(f"cat {p}/cur_freq 2>/dev/null")
        print(f"  Device {p}: Governor={gov}, Freq={cur}")

# 3. I/O SD Card & Internal Storage Read-Ahead Cache
print("\n[3] Storage I/O Read-Ahead Acceleration...")
# Set 2048 KB (2MB) read-ahead for mmcblk0 (eMMC) and mmcblk1 (SD Card)
run_cmd("echo 2048 > /sys/block/mmcblk0/queue/read_ahead_kb 2>/dev/null")
run_cmd("echo 2048 > /sys/block/mmcblk1/queue/read_ahead_kb 2>/dev/null")
# Also set for all loop/dm devices if any
run_cmd("for q in /sys/block/*/queue/read_ahead_kb; do echo 2048 > $q 2>/dev/null; done")
ra0 = run_cmd("cat /sys/block/mmcblk0/queue/read_ahead_kb 2>/dev/null")
print(f"  eMMC mmcblk0 read_ahead_kb: {ra0} KB (was 128 KB - now 16x larger buffer!)")

# 4. Virtual Memory (RAM) & Cache Optimization
print("\n[4] RAM & Cache Kernel Tuning...")
run_cmd("sysctl -w vm.vfs_cache_pressure=50")
run_cmd("sysctl -w vm.swappiness=50")
run_cmd("sysctl -w vm.dirty_ratio=20")
run_cmd("sysctl -w vm.dirty_background_ratio=5")
run_cmd("echo 3 > /proc/sys/vm/drop_caches")
print("  vfs_cache_pressure:", run_cmd("cat /proc/sys/vm/vfs_cache_pressure"))
print("  swappiness:", run_cmd("cat /proc/sys/vm/swappiness"))
print("  Memory freed! Current free RAM:")
print(run_cmd("free -m"))

# 5. Disable background bloat launcher (mboxlauncher)
print("\n[5] Suspending background TV launcher to free RAM for gamebox...")
run_cmd("am force-stop com.droidlogic.mboxlauncher")
# Ensure com.jh.gamebox is in foreground
run_cmd("monkey -p com.jh.gamebox -c android.intent.category.LAUNCHER 1")

# 6. Android UI Rendering Properties
print("\n[6] UI Hardware Acceleration Properties...")
run_cmd("setprop debug.sf.hw 1")
run_cmd("setprop debug.egl.hw 1")
run_cmd("setprop debug.performance.tuning 1")
run_cmd("setprop video.accelerate.hw 1")
run_cmd("setprop persist.sys.ui.hw 1")

print("\n=== ACCELERATION COMPLETE ===")
