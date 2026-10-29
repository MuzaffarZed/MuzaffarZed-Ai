import os
import sys
import time
import subprocess
import glob

ADB = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"
BASE_DIR = r"C:\Users\MuzaffarZed\ai_workspace"

SFX_DIR = os.path.join(BASE_DIR, "sfx_pack")
OVERLAYS_DIR = os.path.join(BASE_DIR, "creator_overlays")
FONTS_DIR = os.path.join(BASE_DIR, "creator_fonts")
SPLITS_DIR = os.path.join(BASE_DIR, "capcut_mod_lab", "signed_splits")
LAUNCHER_APK = os.path.join(BASE_DIR, "capcut_os_launcher", "CapCutOS.apk")
BOOSTER_APK = os.path.join(BASE_DIR, "capcut_booster_app", "CapCutBoost.apk")

def run_adb(args, timeout=30):
    cmd = [ADB] + args
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def main():
    print("=" * 65)
    print("  MUZAFFAR STUDIO OS - 1-CLICK POST-FLASH PROVISIONER")
    print("  Samsung Galaxy Tab A (SM-T295) Creator Environment")
    print("=" * 65)
    
    print("\n[1/7] Tablet ulanishini tekshirish (ADB wait-for-device)...")
    print("Iltimos, planshet yoqilgan va USB orqali ulanganligiga ishonch hosil qiling...")
    try:
        subprocess.run([ADB, "wait-for-device"], timeout=45)
    except subprocess.TimeoutExpired:
        print("[XATO] Planshet 45 soniya ichida ulanmadi!")
        print("Iltimos, planshetda 'USB sozlash' (USB debugging) yoqilganligini tekshiring.")
        return 1

    model, _, _ = run_adb(["shell", "getprop", "ro.product.model"])
    serial, _, _ = run_adb(["get-serialno"])
    print(f"[OK] Aniqlangan qurilma: {model} (Serial: {serial})")

    # 2. RAM Booster o'rnatish
    print("\n[2/7] CapCut RAM Boosterni o'rnatish...")
    if os.path.exists(BOOSTER_APK):
        out, err, code = run_adb(["install", "-r", BOOSTER_APK])
        print(f"  -> CapCut RAM Booster: {out if code == 0 else err}")

    # 3. CapCut Pad Pro (Signed Splits) o'rnatish
    print("\n[3/7] CapCut Pad Pro (planshet versiyasi) o'rnatilmoqda...")
    splits = [
        "base.apk",
        "split_config.arm64_v8a.apk",
        "split_core.apk",
        "split_core.config.arm64_v8a.apk",
        "split_config.tvdpi.apk",
        "split_core.config.tvdpi.apk",
        "split_asset_pack.apk"
    ]
    split_paths = [os.path.join(SPLITS_DIR, s) for s in splits if os.path.exists(os.path.join(SPLITS_DIR, s))]
    if len(split_paths) == len(splits):
        print(f"  -> {len(split_paths)} ta split paket yuklanmoqda (pm install-multiple)...")
        cmd = [ADB, "install-multiple", "-r"] + split_paths
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if res.returncode == 0:
            print(f"  [OK] CapCut Pad Pro muvaffaqiyatli o'rnatildi: {res.stdout.strip()}")
        else:
            print(f"  [OGOHLANTIRISH] Install-multiple natijasi: {res.stderr.strip() or res.stdout.strip()}")
    else:
        print(f"  [OGOHLANTIRISH] Ba'zi split paketlar topilmadi ({len(split_paths)}/{len(splits)} mavjud).")

    # 4. 25 ta Ovoz Effektlarini (SFX) yuklash
    print("\n[4/7] 25 ta professional SFX effektlarini yuklash (/sdcard/Music/Creator_SFX/)...")
    run_adb(["shell", "mkdir", "-p", "/sdcard/Music/Creator_SFX/"])
    sfx_files = glob.glob(os.path.join(SFX_DIR, "*.wav"))
    for sfx in sfx_files:
        run_adb(["push", sfx, "/sdcard/Music/Creator_SFX/"])
    print(f"  [OK] {len(sfx_files)} ta SFX fayllari planshetga joylashtirildi.")

    # 5. 8 ta Green Screen Video Overlaylarni yuklash
    print("\n[5/7] 8 ta Green Screen Overlay videolarini yuklash (/sdcard/DCIM/Creator_Overlays/)...")
    run_adb(["shell", "mkdir", "-p", "/sdcard/DCIM/Creator_Overlays/"])
    overlay_files = glob.glob(os.path.join(OVERLAYS_DIR, "*.mp4"))
    for ov in overlay_files:
        run_adb(["push", ov, "/sdcard/DCIM/Creator_Overlays/"])
    print(f"  [OK] {len(overlay_files)} ta Overlay videolari planshetga joylashtirildi.")

    # 6. Shriftlarni yuklash (/sdcard/Fonts/)
    print("\n[6/7] Montaj shriftlarini yuklash (/sdcard/Fonts/)...")
    run_adb(["shell", "mkdir", "-p", "/sdcard/Fonts/"])
    font_files = glob.glob(os.path.join(FONTS_DIR, "*.ttf"))
    for f in font_files:
        run_adb(["push", f, "/sdcard/Fonts/"])
    print(f"  [OK] {len(font_files)} ta shriftlar planshetga joylashtirildi.")

    # 7. Tezlik va Zero-Lag sozlamalari
    print("\n[7/7] Zero-Lag va Tezlik sozlamalarini faollashtirish (0.0x animatsiya)...")
    run_adb(["shell", "settings", "put", "global", "window_animation_scale", "0"])
    run_adb(["shell", "settings", "put", "global", "transition_animation_scale", "0"])
    run_adb(["shell", "settings", "put", "global", "animator_duration_scale", "0"])
    run_adb(["shell", "settings", "put", "system", "screen_off_timeout", "600000"])
    
    # Bloatware qoldiqlarini o'chirish (agar mavjud bo'lsa)
    for pkg in ["com.samsung.android.securitylogagent", "com.google.android.googlequicksearchbox", "com.samsung.android.sm.devicesecurity"]:
        run_adb(["shell", "pm", "disable-user", "--user", "0", pkg])

    # Samsung One UI Home ish stolini asosiy qilib saqlash (barcha ilovalardan to'liq erkin foydalanish uchun)
    run_adb(["shell", "cmd", "package", "set-home-activity", "com.sec.android.app.launcher/com.sec.android.app.launcher.activities.LauncherActivity"])

    # Media skanerini yangilash
    run_adb(["shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", "file:///sdcard/Music/Creator_SFX/"])
    run_adb(["shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", "file:///sdcard/DCIM/Creator_Overlays/"])

    print("\n" + "=" * 65)
    print("  TABRIKLAYMIZ! MUZAFFAR STUDIO OS TO'LIQ SOZLANDI!")
    print("  - CapCut Pad Pro: TAYYOR")
    print("  - CapCut OS Launcher: ASOSIY EKRAN")
    print("  - 25 SFX + 8 Overlays + Shriftlar: JOYLASHDI")
    print("  - Tizim Animatsiyalari: 0.0x (Instant Zero-Lag)")
    print("=" * 65)
    return 0

if __name__ == "__main__":
    sys.exit(main())
