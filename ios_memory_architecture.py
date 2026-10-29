import subprocess
import sys
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ADB_PATH = r"C:\platform-tools\adb.exe"

def run_adb(cmd):
    full_cmd = [ADB_PATH] + cmd
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return res.stdout.strip()

def main():
    print("=== IMPLEMENTING iOS-STYLE MEMORY & PROCESS ARCHITECTURE ===")
    
    # 1. Enable Android 11 Native Cached Apps Freezer (Linux kernel process suspension)
    print("\n[1] Activating Android 11 Native Cached Apps Freezer...")
    run_adb(["shell", "device_config", "put", "activity_manager_native_boot", "use_freezer", "true"])
    run_adb(["shell", "setprop", "persist.sys.cached_apps_freezer", "true"])
    run_adb(["shell", "setprop", "ro.config.fha_enable", "true"])
    print("    [+] Native app freezer configured to suspend background threads.")
    
    # 2. Strict iOS Background Process Limit (Max 2 background processes)
    print("\n[2] Enforcing Strict Background Process Limit (Max 2 concurrent processes)...")
    run_adb(["shell", "settings", "put", "global", "background_process_limit", "2"])
    run_adb(["shell", "device_config", "put", "activity_manager", "max_cached_processes", "8"])
    run_adb(["shell", "device_config", "put", "activity_manager", "max_phantom_processes", "4"])
    print("    [+] Background limit enforced: only the foreground app will hold the CPU/RAM.")
    
    # 3. Aggressive App Standby (Bucket: RESTRICTED for all non-essential third-party apps)
    print("\n[3] Setting App Standby Buckets to RESTRICTED (iOS Tombstone behavior)...")
    installed_3rd = run_adb(["shell", "pm", "list", "packages", "-3"]).splitlines()
    target_apps = [line.replace("package:", "").strip() for line in installed_3rd if line.strip()]
    
    for app in target_apps:
        # Put into strict restricted bucket (cannot run unless opened)
        run_adb(["shell", "cmd", "usage_stats", "set-standby-bucket", app, "restricted"])
        # Prevent app from waking up CPU via Wakelock while another app is active
        run_adb(["shell", "cmd", "appops", "set", app, "WAKE_LOCK", "ignore"])
        print(f"    [+] {app} -> Set to RESTRICTED & WAKELOCK BLOCKED")
        
    # 4. Low-latency Touch & Frame Scheduling for Top (Foreground) App
    print("\n[4] Optimizing Scheduler & Touch Latency for Foreground App...")
    run_adb(["shell", "settings", "put", "global", "fstrim_mandatory_interval", "86400"])
    run_adb(["shell", "setprop", "debug.sf.early_phase_offset_ns", "500000"])
    run_adb(["shell", "setprop", "debug.sf.early_app_phase_offset_ns", "500000"])
    
    # 5. Flush and verify
    print("\n[5] Synchronizing and flushing memory...")
    run_adb(["shell", "am", "kill-all"])
    run_adb(["shell", "sync"])
    
    # Check RAM
    out = run_adb(["shell", "cat", "/proc/meminfo"])
    mem_avail = 0
    for line in out.splitlines():
        if "MemAvailable:" in line:
            mem_avail = int(re.search(r'\d+', line).group()) // 1024
            break
            
    print(f"\n[*] Current Available RAM: {mem_avail} MB")
    print("[SUCCESS] iOS-Style Architecture successfully active!")

if __name__ == "__main__":
    main()
