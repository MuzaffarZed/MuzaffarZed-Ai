import subprocess
import shutil
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class VideoFile:
    filename: str
    path: str
    size_bytes: int
    size_human: str
    modified_date: str
    is_transferred: bool = False

class VideoScanner:
    def __init__(self, adb_path: str, sender_serial: str, receiver_serial: Optional[str] = None):
        self.adb = adb_path
        self.sender_serial = sender_serial
        self.receiver_serial = receiver_serial
        self.camera_path = "/sdcard/DCIM/Camera"
        self.tablet_dest_path = "/sdcard/Movies/S22_Ultra"

    def _run_adb(self, *args, serial: str) -> str:
        cmd = [self.adb, "-s", serial] + list(args)
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=15)
            return res.stdout.strip()
        except Exception:
            return ""

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

    def get_tablet_existing_files(self) -> set:
        if not self.receiver_serial:
            return set()
        out = self._run_adb("shell", f"ls -1 {self.tablet_dest_path} 2>/dev/null", serial=self.receiver_serial)
        if not out:
            return set()
        return set(line.strip() for line in out.splitlines() if line.strip())

    def scan_camera_videos(self) -> List[VideoFile]:
        existing_on_tab = self.get_tablet_existing_files()
        out = self._run_adb(
            "shell",
            f"ls -l {self.camera_path}/*.mp4 2>/dev/null",
            serial=self.sender_serial
        )
        videos = []

        for line in out.splitlines():
            line = line.strip()
            if not line or not line.endswith(".mp4"):
                continue
            parts = line.split()
            # Standard ls -l formats:
            # Format A: -rw-rw---- 1 u0_a307 media_rw 104857600 2026-09-12_23:25 /path/file.mp4
            # Format B: -rw-rw---- 2 u0_a307 media_rw 104857600 2026-09-12 23:25 /path/file.mp4
            if len(parts) >= 6:
                try:
                    full_path = parts[-1]
                    filename = full_path.split("/")[-1]
                    
                    # Find size (usually parts[4])
                    size_bytes = 0
                    for p in parts[3:6]:
                        if p.isdigit():
                            size_bytes = int(p)
                            break
                    
                    mod_date = parts[5] if len(parts) > 5 else "Noma'lum"
                    is_already_sent = filename in existing_on_tab

                    videos.append(VideoFile(
                        filename=filename,
                        path=full_path,
                        size_bytes=size_bytes,
                        size_human=self._format_size(size_bytes),
                        modified_date=mod_date,
                        is_transferred=is_already_sent
                    ))
                except (ValueError, IndexError):
                    continue

        videos.sort(key=lambda x: x.modified_date, reverse=True)
        return videos
