import pytest
from unittest.mock import MagicMock, patch
from galaxy_bridge.core.detector import DeviceDetector, AndroidDevice
from galaxy_bridge.core.video_scanner import VideoScanner, VideoFile
from galaxy_bridge.core.transfer_engine import TransferEngine, TransferResult
from galaxy_bridge.core.auto_sync import AutoSyncManager

def test_device_detector_parsing():
    detector = DeviceDetector(adb_path="mock_adb")
    
    with patch.object(detector, "_run_adb") as mock_adb:
        mock_adb.side_effect = [
            "List of devices attached\nR3CT902NQAN\tdevice\nR9WN606KYZJ\tdevice\n",
            "SM-S908N",  # model
            "16",        # android ver
            "/dev/fuse 223G 129G 94G 58% /sdcard",  # df
            "level: 85\n",  # battery
            "SM-T295",   # model
            "11",        # android ver
            "/dev/fuse 22G 5G 17G 26% /sdcard",    # df
            "level: 90\n"   # battery
        ]
        
        pair = detector.detect_pair()
        assert pair["sender"] is not None
        assert pair["receiver"] is not None
        assert pair["sender"].role == "sender"
        assert "S22" in pair["sender"].device_name
        assert pair["receiver"].role == "receiver"
        assert "Tab A" in pair["receiver"].device_name
        assert pair["sender"].battery_level == 85
        assert pair["receiver"].battery_level == 90

def test_video_scanner_parsing():
    scanner = VideoScanner(adb_path="mock_adb", sender_serial="S22_SERIAL", receiver_serial="TAB_SERIAL")
    
    sample_ls_out = (
        "-rw-rw---- 1 u0_a307 media_rw 104857600 2026-09-12_23:25 /sdcard/DCIM/Camera/video1.mp4\n"
        "-rw-rw---- 1 u0_a307 media_rw 52428800 2026-09-10_12:00 /sdcard/DCIM/Camera/video2.mp4\n"
    )
    
    with patch.object(scanner, "_run_adb") as mock_adb:
        mock_adb.side_effect = [
            "video1.mp4\n",  # existing on tablet
            sample_ls_out     # camera videos
        ]
        
        videos = scanner.scan_camera_videos()
        assert len(videos) == 2
        assert videos[0].filename == "video1.mp4"
        assert videos[0].size_bytes == 104857600
        assert videos[0].size_human == "100.0 MB"
        assert videos[0].is_transferred is True
        
        assert videos[1].filename == "video2.mp4"
        assert videos[1].size_bytes == 52428800
        assert videos[1].size_human == "50.0 MB"
        assert videos[1].is_transferred is False

def test_transfer_engine_mock():
    engine = TransferEngine("mock_adb", "S22_SERIAL", "TAB_SERIAL")
    
    with patch("subprocess.run") as mock_subproc, \
         patch("os.path.exists", return_value=True), \
         patch("os.path.getsize", return_value=10485760), \
         patch("os.remove") as mock_rm:
        
        mock_subproc.return_value = MagicMock(returncode=0, stdout="")
        res = engine.transfer_video("/sdcard/DCIM/Camera/my_video.mp4")
        
        assert res.success is True
        assert res.filename == "my_video.mp4"
        assert res.size_bytes == 10485760
        assert res.speed_mb_s > 0
        assert mock_subproc.call_count >= 3  # pull, mkdir/push, media_scanner broadcast

def test_auto_sync_loop_once():
    scanner = MagicMock()
    engine = MagicMock()
    
    scanner.scan_camera_videos.return_value = [
        VideoFile("vid1.mp4", "/sdcard/DCIM/Camera/vid1.mp4", 1000, "1 KB", "2026-01-01", is_transferred=False)
    ]
    engine.transfer_video.return_value = TransferResult("vid1.mp4", 1000, 0.5, 2.0, True)
    
    synced_results = []
    def on_synced(res):
        synced_results.append(res)
        
    auto_sync = AutoSyncManager(scanner, engine, on_video_synced=on_synced, poll_interval_sec=0.1)
    
    # Run one pass manually
    videos = scanner.scan_camera_videos()
    new_videos = [v for v in videos if not v.is_transferred]
    assert len(new_videos) == 1
    res = engine.transfer_video(new_videos[0].path)
    assert res.success is True
