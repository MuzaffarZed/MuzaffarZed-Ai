import os
import time
import subprocess
import tempfile
from typing import Callable, Optional
from dataclasses import dataclass

@dataclass
class TransferResult:
    filename: str
    size_bytes: int
    duration_sec: float
    speed_mb_s: float
    success: bool
    error_message: Optional[str] = None

class TransferEngine:
    def __init__(self, adb_path: str, sender_serial: str, receiver_serial: str, dest_dir: str = "/sdcard/Movies/S22_Ultra"):
        self.adb = adb_path
        self.sender = sender_serial
        self.receiver = receiver_serial
        self.dest_dir = dest_dir

    def ensure_dest_dir(self) -> bool:
        cmd = [self.adb, "-s", self.receiver, "shell", "mkdir", "-p", self.dest_dir]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.returncode == 0

    def transfer_video(
        self,
        remote_src_path: str,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> TransferResult:
        filename = os.path.basename(remote_src_path)
        dest_file_path = f"{self.dest_dir}/{filename}"

        if progress_callback:
            progress_callback(filename, 0.0)

        start_time = time.time()
        temp_dir = tempfile.gettempdir()
        local_temp_file = os.path.join(temp_dir, f"galaxy_bridge_{filename}")

        try:
            # 1. Pull from S22 Ultra
            pull_cmd = [self.adb, "-s", self.sender, "pull", remote_src_path, local_temp_file]
            pull_proc = subprocess.run(pull_cmd, capture_output=True, text=True, check=True)

            if not os.path.exists(local_temp_file):
                return TransferResult(
                    filename=filename,
                    size_bytes=0,
                    duration_sec=0,
                    speed_mb_s=0,
                    success=False,
                    error_message="Telefondan fayl yuklab olinmadi."
                )

            file_size = os.path.getsize(local_temp_file)

            if progress_callback:
                progress_callback(filename, 50.0)

            # 2. Push to Galaxy Tab A
            self.ensure_dest_dir()
            push_cmd = [self.adb, "-s", self.receiver, "push", local_temp_file, dest_file_path]
            push_proc = subprocess.run(push_cmd, capture_output=True, text=True, check=True)

            # 3. Notify Android MediaScanner so it instantly shows in Samsung Gallery
            scan_cmd = [
                self.adb, "-s", self.receiver, "shell",
                "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
                "-d", f"file://{dest_file_path}"
            ]
            subprocess.run(scan_cmd, capture_output=True, text=True)

            duration = max(time.time() - start_time, 0.001)
            speed_mb_s = (file_size / (1024 * 1024)) / duration

            if progress_callback:
                progress_callback(filename, 100.0)

            return TransferResult(
                filename=filename,
                size_bytes=file_size,
                duration_sec=duration,
                speed_mb_s=speed_mb_s,
                success=True
            )

        except Exception as e:
            return TransferResult(
                filename=filename,
                size_bytes=0,
                duration_sec=time.time() - start_time,
                speed_mb_s=0,
                success=False,
                error_message=str(e)
            )
        finally:
            if os.path.exists(local_temp_file):
                try:
                    os.remove(local_temp_file)
                except Exception:
                    pass
