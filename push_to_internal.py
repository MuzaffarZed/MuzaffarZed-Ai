import subprocess
import os

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def adb_push(local, remote):
    if os.path.exists(local):
        subprocess.run([adb, "push", local, remote], capture_output=True, text=True)
        print(f"Pushed {os.path.basename(local)} -> {remote}")

print("=== PUSHING TOP GAMES TO INTERNAL STORAGE (/storage/emulated/0) ===")

# 1. GBA: Big Mutha Truckers (Fura) & GTA Advance
adb_push("E:/VGBA/roms/Big Mutha Truckers.gba", "/storage/emulated/0/VGBA/roms/")
adb_push("E:/VGBA/roms/Advance GTA.gba", "/storage/emulated/0/VGBA/roms/")
adb_push("E:/VGBA/GUI/VGBA.csv", "/storage/emulated/0/VGBA/GUI/")
adb_push("E:/VGBA/GUI/Big Mutha Truckers_000.png", "/storage/emulated/0/VGBA/GUI/")
adb_push("E:/VGBA/GUI/Big Mutha Truckers_001.png", "/storage/emulated/0/VGBA/GUI/")
adb_push("E:/VGBA/GUI/Advance GTA_000.png", "/storage/emulated/0/VGBA/GUI/")
adb_push("E:/VGBA/GUI/Advance GTA_001.png", "/storage/emulated/0/VGBA/GUI/")

# 2. SEGA: Ultimate Mortal Kombat 3 & Sonic
adb_push("E:/VGEN/roms/Ultimate Mortal Kombat 3.bin", "/storage/emulated/0/VGEN/roms/")
adb_push("E:/VGEN/roms/Sonic the Hedgehog.bin", "/storage/emulated/0/VGEN/roms/")
adb_push("E:/VGEN/GUI/VGEN.csv", "/storage/emulated/0/VGEN/GUI/")
adb_push("E:/VGEN/GUI/Ultimate Mortal Kombat 3_000.png", "/storage/emulated/0/VGEN/GUI/")
adb_push("E:/VGEN/GUI/Ultimate Mortal Kombat 3_001.png", "/storage/emulated/0/VGEN/GUI/")

# 3. DENDY: Tank 1990 & Contra & Mario
adb_push("E:/VNES/roms/TankA1990.nes", "/storage/emulated/0/VNES/roms/")
adb_push("E:/VNES/roms/Contra24in1.nes", "/storage/emulated/0/VNES/roms/")
adb_push("E:/VNES/roms/Bros.nes", "/storage/emulated/0/VNES/roms/")
adb_push("E:/VNES/GUI/VNES.csv", "/storage/emulated/0/VNES/GUI/")
adb_push("E:/VNES/GUI/TankA1990_000.png", "/storage/emulated/0/VNES/GUI/")
adb_push("E:/VNES/GUI/TankA1990_001.png", "/storage/emulated/0/VNES/GUI/")

print("\n=== VERIFYING INTERNAL STORAGE GAMES ===")
for fld in ["VGBA", "VGEN", "VNES"]:
    out = subprocess.run([adb, "shell", "ls", "-la", f"/storage/emulated/0/{fld}/roms"], capture_output=True, text=True).stdout
    print(f"*** {fld}/roms ***\n{out.strip()}\n")
