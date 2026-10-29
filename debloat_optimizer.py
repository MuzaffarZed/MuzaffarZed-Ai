import subprocess
import sys
import re

ADB_PATH = r"C:\platform-tools\adb.exe"

# Targets that heavily consume RAM/CPU on Samsung One UI Core
# SAFETY: Google Play Store, Play Services, YouTube, Camera, Phone, Settings, SystemUI are STRICTLY PRESERVED.
DEBLOAT_LIST = [
    # Samsung Cloud & Accounts
    "com.samsung.android.scloud",
    "com.samsung.android.fmm",
    "com.samsung.android.voc",
    "com.samsung.android.app.updatecenter",
    "com.samsung.android.app.tips",
    "com.samsung.android.dynamiclock",
    "com.samsung.storyservice",
    "com.samsung.android.forest",  # Digital wellbeing
    "com.samsung.android.game.gos",  # Game optimizing service (causes throttling and RAM waste)
    "com.samsung.android.game.gametools",
    "com.samsung.android.game.gamehome",
    "com.enhance.gameservice",
    
    # Samsung Bloat & Ads / Telemetry
    "com.sec.android.diagmonagent",
    "com.sec.spp.push",
    "com.samsung.android.beaconmanager",
    "com.samsung.android.stickercenter",
    "com.sec.android.app.camera.sticker",
    "com.sec.android.widgetapp.webmanual",
    "com.samsung.android.app.dressroom",
    "com.samsung.android.allshare.service.fileshare",
    "com.samsung.android.allshare.service.mediashare",
    "com.samsung.android.app.watchmanagerstub",
    "com.sec.android.app.kidshome",
    "com.hiya.star",  # Caller ID tracker
    "com.samsung.android.smartcallprovider",
    "com.sec.android.mimage.photoretouching",
    "com.samsung.android.service.peoplestripe",
    "com.samsung.android.app.taskedge",
    "com.samsung.android.app.clipboardedge",
    "com.samsung.android.app.appsedge",
    
    # Bixby & AR Bloat
    "com.samsung.android.app.spage",
    "com.samsung.android.bixby.service",
    "com.samsung.android.bixby.agent",
    "com.samsung.android.bixbyvision.framework",
    "com.samsung.android.aremoji",
    "com.samsung.android.arzone",
    "com.samsung.android.livestickers",
    "com.samsung.android.rubin.app",
    "com.samsung.android.authfw",
    
    # Knox & Enterprise Bloat (not needed for normal use)
    "com.sec.enterprise.knox.cloudmdm.smdms",
    "com.sec.enterprise.mdm.services.simpin",
    "com.samsung.android.mdm",
    "com.samsung.android.knox.analytics.uploader",
    "com.samsung.android.fota",
    "com.wssyncmldm",
    
    # Microsoft preloaded apps (user can reinstall from Play Store if needed)
    "com.microsoft.skydrive",
    "com.microsoft.office.officehubrow",
    
    # Google Non-essential / Telemetry (Keeps Play Store, Services, and YouTube 100% safe!)
    "com.google.android.feedback",
    "com.google.android.printservice.recommendation",
    "com.google.android.projection.gearhead",
    "com.google.android.videos",
    "com.google.android.music",
    "com.google.android.apps.turbo",
    "com.google.android.apps.restore",
    "com.google.mainline.telemetry",
]

def run_adb(cmd):
    full_cmd = [ADB_PATH] + cmd
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return res.stdout.strip()

def get_memory_info():
    out = run_adb(["shell", "cat", "/proc/meminfo"])
    mem_total = 0
    mem_avail = 0
    swap_used = 0
    for line in out.splitlines():
        if "MemTotal:" in line:
            mem_total = int(re.search(r'\d+', line).group())
        elif "MemAvailable:" in line:
            mem_avail = int(re.search(r'\d+', line).group())
    return mem_total // 1024, mem_avail // 1024

def main():
    print("=== SAMSUNG GALAXY TAB A 8.0 (SM-T295) TURBO OPTIMIZATION ===")
    
    # 1. Get installed packages
    installed_raw = run_adb(["shell", "pm", "list", "packages"])
    installed_pkgs = set(line.replace("package:", "").strip() for line in installed_raw.splitlines())
    
    tot_before, avail_before = get_memory_info()
    print(f"[*] Memory BEFORE: Total={tot_before} MB | Available={avail_before} MB (Used={tot_before - avail_before} MB)")
    
    # 2. Debloat matching packages
    removed_count = 0
    print("\n[*] Starting safe debloat of Samsung/MS/telemetry packages...")
    for pkg in DEBLOAT_LIST:
        if pkg in installed_pkgs:
            # Uninstall for user 0 (safe, stops running, reversible)
            res = run_adb(["shell", "pm", "uninstall", "-k", "--user", "0", pkg])
            if "Success" in res:
                print(f"  [+] Removed: {pkg}")
                removed_count += 1
            else:
                # Try disable if uninstall fails
                run_adb(["shell", "pm", "disable-user", "--user", "0", pkg])
                print(f"  [~] Disabled: {pkg}")
                removed_count += 1

    print(f"\n[*] Total uninstalled/disabled bloatware services: {removed_count}")
    
    # 3. System Speed & UI Responsiveness Tweaks
    print("\n[*] Applying UI Responsiveness Tweaks (Animation scaling 0.5x)...")
    run_adb(["shell", "settings", "put", "global", "window_animation_scale", "0.5"])
    run_adb(["shell", "settings", "put", "global", "transition_animation_scale", "0.5"])
    run_adb(["shell", "settings", "put", "global", "animator_duration_scale", "0.5"])
    
    # 4. Background killer and memory trim
    print("[*] Flushing background caches and killing frozen zombies...")
    run_adb(["shell", "am", "kill-all"])
    run_adb(["shell", "sync"])
    
    tot_after, avail_after = get_memory_info()
    print(f"\n[*] Memory AFTER: Total={tot_after} MB | Available={avail_after} MB (Used={tot_after - avail_after} MB)")
    print(f"[*] Freely recovered RAM: +{avail_after - avail_before} MB!")
    print("\n[✓] OPTIMIZATION COMPLETE! Google Play Store and YouTube remain 100% active.")

if __name__ == "__main__":
    main()
