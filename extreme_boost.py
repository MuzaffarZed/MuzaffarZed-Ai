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
    print("=== SAMSUNG SM-T295 EXTREME TURBO BOOST (LEVEL 2) ===")
    
    # 1. Zero Animation Scale (Instant UI response, no GPU animation latency)
    print("[*] Setting Animation Scales to 0.0 (Instant UI response)...")
    run_adb(["shell", "settings", "put", "global", "window_animation_scale", "0"])
    run_adb(["shell", "settings", "put", "global", "transition_animation_scale", "0"])
    run_adb(["shell", "settings", "put", "global", "animator_duration_scale", "0"])
    
    # 2. Force GPU 2D hardware rendering (takes load off Snapdragon 429 CPU)
    print("[*] Enabling GPU Hardware Acceleration for 2D UI rendering...")
    run_adb(["shell", "settings", "put", "global", "force_gpu_rendering", "1"])
    run_adb(["shell", "setprop", "debug.egl.hw", "1"])
    run_adb(["shell", "setprop", "debug.sf.hw", "1"])
    
    # 3. Optimize ActivityManager process caching for 2GB RAM devices
    print("[*] Tuning Android ActivityManager process caching (preventing RAM thrashing)...")
    run_adb(["shell", "device_config", "put", "activity_manager", "max_cached_processes", "14"])
    run_adb(["shell", "device_config", "put", "activity_manager", "max_phantom_processes", "8"])
    
    # 4. Secondary Samsung Bloatware removal
    secondary_bloat = [
        "com.samsung.android.themecenter",
        "com.samsung.android.email.provider",
        "com.sec.android.app.sbrowser",  # Samsung Internet (Chrome is present)
        "com.samsung.android.app.notes.addons",
        "com.samsung.android.cidmanager",
        "com.samsung.android.bluelightfilter",
        "com.sec.android.emergencylauncher",
        "com.samsung.android.shortcutbackupservice",
        "com.sec.android.app.quicktool",
        "com.google.android.apps.docs",  # Google Docs stub
    ]
    
    installed_raw = run_adb(["shell", "pm", "list", "packages"])
    installed_pkgs = set(line.replace("package:", "").strip() for line in installed_raw.splitlines())
    
    print("[*] Removing secondary non-critical packages...")
    for pkg in secondary_bloat:
        if pkg in installed_pkgs:
            res = run_adb(["shell", "pm", "uninstall", "-k", "--user", "0", pkg])
            print(f"  [+] Uninstalled: {pkg} -> {res}")
            
    # 5. Background Execution Restriction for 3rd-party Social / Media apps
    # These apps will NOT run in background eating RAM, but will open normally when tapped.
    social_apps = [
        "com.zhiliaoapp.musically",       # TikTok
        "video.like",                     # Likee
        "com.instagram.android",          # Instagram
        "com.imo.android.imoim",           # IMO
        "ru.yandex.yandexmaps",           # Yandex Maps
        "com.dywx.larkplayer",             # Lark Player
        "com.shazam.android",             # Shazam
        "com.ysxlite.cam",
        "ringtone.maker.mp3.cutter.audio",
        "sound.effect.equalizer.musicplayer",
        "com.themausoft.wpsapp",
        "com.jetappfactory.jetaudio",
        "com.shenyaocn.android.usbcamera",
    ]
    
    print("[*] Restricting background background-drain on heavy third-party apps...")
    for app in social_apps:
        if app in installed_pkgs:
            run_adb(["shell", "cmd", "appops", "set", app, "RUN_IN_BACKGROUND", "ignore"])
            run_adb(["shell", "cmd", "appops", "set", app, "RUN_ANY_IN_BACKGROUND", "ignore"])
            run_adb(["shell", "am", "stop-app", app])
            print(f"  [+] Restricted background activity for: {app}")

    # 6. Trim Memory and clear caches
    print("[*] Performing deep RAM cleanup...")
    run_adb(["shell", "am", "kill-all"])
    run_adb(["shell", "sync"])
    
    # 7. Print RAM info
    out = run_adb(["shell", "cat", "/proc/meminfo"])
    mem_avail = 0
    for line in out.splitlines():
        if "MemAvailable:" in line:
            mem_avail = int(re.search(r'\d+', line).group()) // 1024
            break
            
    print(f"\n[*] Available RAM after Extreme Boost: {mem_avail} MB!")
    print("[OK] Extreme Boost successfully applied!")

if __name__ == "__main__":
    main()
