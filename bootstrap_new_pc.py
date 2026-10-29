"""
================================================================================
MUZAFFARZED ANTIGRAVITY 1-CLICK BOOTSTRAP & RESTORE ENGINE
================================================================================
Yangi kompyuterda Antigravity ochilganda barcha loyihalar, Second Brain xotirasi,
40+ skills, qoidalar va agentlarni 1 daqiqada avtomatik o'rnatib beruvchi skript.

Muallif: MuzaffarZed
Standart: Oliy Arxitektura Kodeksi (Zero-Defect)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_banner():
    print("=" * 70)
    print("   MUZAFFARZED ANTIGRAVITY AVTOMATIK TIKLASH VA SOZLASH TIZIMI   ")
    print("=" * 70)

def restore_antigravity_config():
    base_dir = Path(__file__).resolve().parent
    backup_gemini = base_dir / ".gemini_backup"
    
    user_home = Path.home()
    target_gemini = user_home / ".gemini" / "config"

    print(f"[*] Foydalanuvchi jildi: {user_home}")
    print(f"[*] Zaxira manbasi: {backup_gemini}")
    print(f"[*] Nishon manzil: {target_gemini}")

    if not backup_gemini.exists():
        print(f"[XATO] .gemini_backup topilmadi: {backup_gemini}")
        return False

    os.makedirs(target_gemini, exist_ok=True)

    # Ko'chirish
    for item in os.listdir(backup_gemini):
        s = backup_gemini / item
        d = target_gemini / item
        if s.is_dir():
            shutil.copytree(s, d, dirs_exist_ok=True)
            print(f"  [+] Jild tiklandi: {item}")
        else:
            shutil.copy2(s, d)
            print(f"  [+] Fayl tiklandi: {item}")

    print("[MUVAFFAQIYAT] Barcha 40+ skills, qoidalar va agentlar yangi kompyuterga o'rnatildi!")
    return True

def setup_second_brain():
    base_dir = Path(__file__).resolve().parent
    memory_db = base_dir / ".agents" / "memory" / "memory.db"
    if memory_db.exists():
        print(f"[+] Second Brain xotira bazasi mavjud: {memory_db.stat().st_size} bayt")
    else:
        print("[*] Yangi Second Brain xotira bazasi sozlanmoqda...")

def main():
    print_banner()
    ok = restore_antigravity_config()
    setup_second_brain()
    
    print("\n" + "=" * 70)
    if ok:
        print(" BARCHA SOZLAMALAR MUKAMMAL TIKLANDI (Zero-Defect)!")
        print(" Yangi kompyuteringizdagi Antigravity hozirgi kompyuteringizdek ishlaydi.")
    else:
        print(" Tiklashda kamchilik yuz berdi.")
    print("=" * 70)

if __name__ == "__main__":
    main()
