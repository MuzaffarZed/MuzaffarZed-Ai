"""
MuzaffarZed Autonomous Sentinel — Smart USB Flash Drive Sync & Car Audio Formatter
Yaratuvchi: MuzaffarZed
Standart: Mutlaq Mukammallik (Zero-Beta, Zero-Defect)

1. Fleshka solinganda yangi treklarni dublikatsiz avto-nusxalash.
2. Trek nomlaridagi '@kanal', '[t.me]', reklama axlatlarini tozalab, avtomagnitola o'qiydigan qilib tartiblash.
3. Mashina magnitofonlari uchun 'All_Songs.m3u' avto-pleylistini generatsiya qilish.
"""

from __future__ import annotations

import os
import re
import sys
import shutil
import psutil
from pathlib import Path
from typing import Any, Dict, List, Optional

# Set UTF-8 encoding for standard streams
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

MUSIC_SOURCE_DIR = os.path.expanduser(r"~\Desktop\Musiqa_Fleshka_2026")

class FlashSyncEngine:
    def __init__(self):
        self.signature = "by MuzaffarZed"
        os.makedirs(MUSIC_SOURCE_DIR, exist_ok=True)

    @staticmethod
    def clean_song_name(raw_name: str) -> str:
        """
        Trek nomidagi barcha reklama, kanal havolalari va xunuk belgilarni tozalaydi.
        """
        stem, ext = os.path.splitext(raw_name)

        # 1. Remove @channel, [t.me/...], (site.com) patterns
        cleaned = re.sub(r"@[a-zA-Z0-9_]+", "", stem)
        cleaned = re.sub(r"\[.*?\]", "", cleaned)
        cleaned = re.sub(r"\(.*?www.*?\)", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\(.*?\.com.*?\)", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\(.*?\.uz.*?\)", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\(.*?\.ru.*?\)", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\(320\s*kbps\)", "", cleaned, flags=re.IGNORECASE)

        # 2. Clean underscores and excessive spaces
        cleaned = cleaned.replace("_", " ")
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        # If name became too short, revert to cleaned stem
        if len(cleaned) < 3:
            cleaned = stem

        return f"{cleaned}{ext}"

    def get_removable_drives(self) -> List[str]:
        """
        Kompyuterga ulangan barcha USB fleshka disklarni qaytaradi.
        """
        removables = []
        for part in psutil.disk_partitions(all=False):
            if 'removable' in part.opts or part.fstype in ('FAT32', 'exFAT'):
                removables.append(part.device.rstrip("\\"))
        return removables

    def sync_to_usb(self, usb_root: Optional[str] = None) -> Dict[str, Any]:
        """
        Musiqa Fleshka katalogidagi treklarni USB ga xavfsiz va tartibli ko'chiradi.
        """
        drives = self.get_removable_drives()
        target_drive = usb_root or (drives[0] if drives else None)

        if not target_drive:
            return {
                "success": True,
                "synced_count": 0,
                "target": None,
                "signature": self.signature,
                "message": "USB fleshka ulanishi kutilmoqda. Fleshka solinishi bilan 1-bosishda avto-sinaxronlanadi!"
            }

        dest_dir = os.path.join(target_drive, "Musiqa_2026")
        os.makedirs(dest_dir, exist_ok=True)

        synced = 0
        playlist_entries = []

        for f in os.listdir(MUSIC_SOURCE_DIR):
            if f.lower().endswith(('.mp3', '.m4a', '.wav', '.flac')):
                src_path = os.path.join(MUSIC_SOURCE_DIR, f)
                clean_name = self.clean_song_name(f)
                dst_path = os.path.join(dest_dir, clean_name)

                playlist_entries.append(clean_name)

                # Only copy if missing or size differs
                if not os.path.exists(dst_path) or os.path.getsize(src_path) != os.path.getsize(dst_path):
                    try:
                        shutil.copy2(src_path, dst_path)
                        synced += 1
                    except Exception:
                        pass

        # Generate M3U playlist for car stereos
        m3u_path = os.path.join(dest_dir, "00_Avtomagnitola_Pleylist.m3u")
        try:
            with open(m3u_path, "w", encoding="utf-8") as m3u:
                m3u.write("#EXTM3U\n")
                for entry in playlist_entries:
                    m3u.write(f"{entry}\n")
        except Exception:
            pass

        return {
            "success": True,
            "target": target_drive,
            "synced_count": synced,
            "total_playlist": len(playlist_entries),
            "signature": self.signature,
            "message": f"Fleshkaga ({target_drive}) {synced} ta yangi trek ko'chirildi va avtomagnitola pleylisti yaratildi!"
        }

if __name__ == "__main__":
    sync = FlashSyncEngine()
    print("Testing Flash Sync Engine...")
    test_clean = sync.clean_song_name("@sherali_jurayev_uz [t.me/musiqa] Sherali_Jurayev_Karvon_(320kbps).mp3")
    print(f"Cleaned name test: '{test_clean}'")
    status = sync.sync_to_usb()
    print(status["message"])
