import time
import threading
from typing import Callable, Optional
from galaxy_bridge.core.video_scanner import VideoScanner
from galaxy_bridge.core.transfer_engine import TransferEngine, TransferResult

class AutoSyncManager:
    def __init__(
        self,
        scanner: VideoScanner,
        engine: TransferEngine,
        on_video_synced: Optional[Callable[[TransferResult], None]] = None,
        on_status_change: Optional[Callable[[str], None]] = None,
        poll_interval_sec: float = 3.0
    ):
        self.scanner = scanner
        self.engine = engine
        self.on_video_synced = on_video_synced
        self.on_status_change = on_status_change
        self.poll_interval = poll_interval_sec
        self.is_running = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        if self.on_status_change:
            self.on_status_change("Avtomatik sinxronizatsiya faol. Yangi videolar kutilmoqda...")

    def stop(self):
        self.is_running = False
        if self.on_status_change:
            self.on_status_change("Avtomatik sinxronizatsiya to'xtatildi.")

    def _run_loop(self):
        while self.is_running:
            try:
                videos = self.scanner.scan_camera_videos()
                # Transfer only untransferred videos
                new_videos = [v for v in videos if not v.is_transferred]
                for v in new_videos:
                    if not self.is_running:
                        break
                    if self.on_status_change:
                        self.on_status_change(f"Yangi video topildi: {v.filename}. O'tkazilmoqda...")
                    res = self.engine.transfer_video(v.path)
                    if self.on_video_synced:
                        self.on_video_synced(res)
            except Exception as e:
                if self.on_status_change:
                    self.on_status_change(f"Kuzatuvda xatolik: {e}")
            time.sleep(self.poll_interval)
