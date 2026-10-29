import sys
import os
import argparse

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from galaxy_bridge.core.detector import DeviceDetector
from galaxy_bridge.core.video_scanner import VideoScanner
from galaxy_bridge.core.transfer_engine import TransferEngine

def run_cli_sync():
    print("=" * 60)
    print("⚡ Galaxy Video Bridge — CLI Tezkor Sinxronizatsiya")
    print("=" * 60)
    detector = DeviceDetector()
    pair = detector.detect_pair()
    sender = pair["sender"]
    receiver = pair["receiver"]

    if not sender or not receiver:
        print("❌ Xatolik: Ikkala qurilma (S22 Ultra va Planshet) ham ulangan bo'lishi lozim.")
        sys.exit(1)

    print(f"📱 Telefon : {sender.device_name} ({sender.serial})")
    print(f"📟 Planshet: {receiver.device_name} ({receiver.serial})")
    print("-" * 60)

    scanner = VideoScanner(detector.adb, sender.serial, receiver.serial)
    engine = TransferEngine(detector.adb, sender.serial, receiver.serial)

    videos = scanner.scan_camera_videos()
    new_videos = [v for v in videos if not v.is_transferred]

    print(f"Jami videolar: {len(videos)} | Yangi o'tkazilmagan: {len(new_videos)}")
    if not new_videos:
        print("✅ Barcha videolar allaqachon planshetda mavjud!")
        return

    for idx, v in enumerate(new_videos, 1):
        print(f"[{idx}/{len(new_videos)}] O'tkazilmoqda: {v.filename} ({v.size_human})...")
        res = engine.transfer_video(v.path)
        if res.success:
            print(f"   -> Muvaffaqiyatli! Tezlik: {res.speed_mb_s:.1f} MB/s ({res.duration_sec:.1f}s)")
        else:
            print(f"   -> Xatolik: {res.error_message}")

    print("=" * 60)
    print("🎉 Barcha yangi videolar planshet Galereyasiga o'tkazildi!")

def main():
    parser = argparse.ArgumentParser(description="Galaxy Video Bridge")
    parser.add_argument("--cli", action="store_true", help="Konsol rejimi")
    parser.add_argument("--sync-all", action="store_true", help="Barcha yangi videolarni darhol o'tkazish")
    args = parser.parse_args()

    if args.cli or args.sync_all:
        run_cli_sync()
    else:
        from galaxy_bridge.gui.app import GalaxyBridgeApp
        app = GalaxyBridgeApp()
        app.mainloop()

if __name__ == "__main__":
    main()
