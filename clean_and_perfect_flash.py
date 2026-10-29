import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")

print("=== 1. CLEANING VPS1 (Deleting 25 junk Chinese games) ===")
ps1_roms = "E:/VPS1/roms"
ps1_keep = {
    "铁拳 3": "Tekken 3,,tk3",
    "蛊惑狼赛车": "Crash Team Racing (CTR - Blur kabi),,ctr",
    "百事超人": "Pepsiman,,pepsi",
    "烈火战车 2": "Twisted Metal 2 (Qurolli poyga),,tm2",
    "实况足球胜利十一人2002": "Winning Eleven 2002 (PES Futbol),,we2002",
    "世界足球胜利十一人 2000": "Winning Eleven 2000 (Futbol),,we2000",
    "蛊惑狼 2": "Crash Bandicoot 2,,cb2",
    "蛊惑狼 3": "Crash Bandicoot 3: Warped,,cb3",
    "蛊惑狼 - 嘉年华": "Crash Bash (Mini Games),,cbash",
    "PS_红色警戒": "Command & Conquer: Red Alert,,ra",
    "沙丘2000": "Dune 2000,,dune",
    "真人快打 - 绝对零度": "Mortal Kombat: Sub-Zero,,mk",
    "真人快打 II": "Mortal Kombat II,,mk2",
    "街头霸王 EX2": "Street Fighter EX2 Plus,,sf",
    "恐龙危机 2": "Dino Crisis 2,,dc2",
    "生化危机2A": "Resident Evil 2 (Leon Disc 1),,re2",
    "生化危机2 B": "Resident Evil 2 (Claire Disc 2),,re2",
    "寂静岭": "Silent Hill,,sh",
    "古墓丽影 III": "Tomb Raider III,,tr3",
    "恶魔城 - 月下夜想曲": "Castlevania: Symphony of the Night,,cast",
    "龙珠 - 决战最终回合": "Dragon Ball GT: Final Bout,,dbz",
    "猫和老鼠": "Tom and Jerry in House Trap,,tj"
}

ps1_deleted_count = 0
for item in os.listdir(ps1_roms):
    if item not in ps1_keep:
        full_path = os.path.join(ps1_roms, item)
        try:
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
            ps1_deleted_count += 1
            print(f"Deleted junk: {item}")
        except Exception as e:
            print(f"Error deleting {item}: {e}")

print(f"Total junk PS1 games deleted: {ps1_deleted_count}")

# Rebuild VPS1.csv with ONLY the kept games
vps1_csv = "E:/VPS1/GUI/VPS1.csv"
ps1_csv_lines = []
for folder_name, entry in ps1_keep.items():
    # Find the extension in folder
    full_folder = os.path.join(ps1_roms, folder_name)
    ext = ".img"
    if os.path.exists(full_folder):
        for f in os.listdir(full_folder):
            if f.endswith((".cue", ".img", ".bin", ".iso")):
                ext = os.path.splitext(f)[1]
                break
    line = f"{folder_name}{ext},{entry}"
    ps1_csv_lines.append(line)

with open(vps1_csv, "w", encoding="gb18030", errors="ignore", newline="\r\n") as f:
    f.write("\r\n".join(ps1_csv_lines) + "\r\n")
print(f"Rebuilt VPS1.csv with {len(ps1_csv_lines)} pure classic games!")

print("\n=== 2. CLEANING VPSP (Deleting 90 junk mini games, keeping Tekken 5 & Rumble Trucks) ===")
psp_roms = "E:/VPSP/roms"
psp_keep = ["Tekken 5.iso", "Rumble Trucks (USA).iso"]
psp_deleted = 0
for f in os.listdir(psp_roms):
    if f not in psp_keep and f != "name.txt":
        full_path = os.path.join(psp_roms, f)
        try:
            os.remove(full_path)
            psp_deleted += 1
        except Exception as e:
            print(f"Error deleting {f}: {e}")

print(f"Deleted {psp_deleted} junk PSP games! (Saved ~15 GB)")

# Rebuild VPSP.csv
vpsp_csv = "E:/VPSP/GUI/VPSP.csv"
vpsp_lines = [
    "Tekken 5.iso,Tekken 5 (PSP 3D),,tk5",
    "Rumble Trucks (USA).iso,Rumble Trucks - Fura (PSP),,truck"
]
with open(vpsp_csv, "w", encoding="gb18030", errors="ignore", newline="\r\n") as f:
    f.write("\r\n".join(vpsp_lines) + "\r\n")

print("\n=== 3. VERIFYING ALL CSV ENCODINGS & LINE ENDINGS ===")
for p in ["E:/VPS1/GUI/VPS1.csv", "E:/VPSP/GUI/VPSP.csv", "E:/VGEN/GUI/VGEN.csv", "E:/VGBA/GUI/VGBA.csv", "E:/VNES/GUI/VNES.csv"]:
    if os.path.exists(p):
        with open(p, "rb") as fp:
            raw = fp.read()
        fixed = raw.replace(b"\r\r\n", b"\r\n")
        if fixed != raw:
            with open(p, "wb") as fp:
                fp.write(fixed)
            print(f"Normalized line endings in {p}")
        else:
            print(f"Line endings already clean in {p}")

print("\n=== CLEANUP AND OPTIMIZATION FINISHED! ===")
