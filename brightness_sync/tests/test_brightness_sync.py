"""
Comprehensive Unit Tests for Brightness Sync Module.
Barcha asosiy komponentlar, sozlamalar va chegaraviy holatlarni tekshirish.
"""

import os
import time
import pytest
from unittest.mock import MagicMock, patch
from core.controller import BrightnessController
from core.sync_daemon import BrightnessSyncDaemon
from core.config import ConfigManager


class TestConfigManager:
    """ConfigManager klassi uchun testlar."""

    def test_default_config_loading(self, tmp_path):
        cfg_file = str(tmp_path / "test_config.json")
        cfg = ConfigManager(cfg_file)
        assert cfg.get("sync_enabled") is True
        assert cfg.get("mode") == "mirror"
        assert cfg.get("scale") == 1.0

    def test_calculate_external_remapped_monotonic(self, tmp_path):
        cfg_file = str(tmp_path / "test_config.json")
        cfg = ConfigManager(cfg_file)
        cfg.set("remap_range", True)
        cfg.set("min_brightness", 20)
        cfg.set("max_brightness", 100)

        assert cfg.calculate_external(0) == 20
        assert cfg.calculate_external(100) == 100

        # Monotonik pasayish kafolati: 100 dan 0 gacha hech qachon ko'tarilmasligi kerak!
        prev = cfg.calculate_external(100)
        for lvl in range(99, -1, -1):
            cur = cfg.calculate_external(lvl)
            assert cur <= prev, f"Inversion found at {lvl}%: {cur} > {prev}"
            prev = cur

    def test_calculate_external_offset_without_remap(self, tmp_path):
        cfg_file = str(tmp_path / "test_config.json")
        cfg = ConfigManager(cfg_file)
        cfg.set("remap_range", False)
        cfg.set("mode", "offset")
        cfg.set("min_brightness", 0)
        cfg.set("offset", 10)
        assert cfg.calculate_external(50) == 60

    def test_calculate_external_clamping_without_remap(self, tmp_path):
        cfg_file = str(tmp_path / "test_config.json")
        cfg = ConfigManager(cfg_file)
        cfg.set("remap_range", False)
        cfg.set("mode", "offset")
        cfg.set("min_brightness", 0)
        cfg.set("offset", 50)
        assert cfg.calculate_external(80) == 100

        cfg.set("offset", -80)
        assert cfg.calculate_external(50) == 0

    def test_mirror_1_to_1(self, tmp_path):
        cfg_file = str(tmp_path / "test_config.json")
        cfg = ConfigManager(cfg_file)
        cfg.set("remap_range", False)
        cfg.set("mode", "mirror")
        for lvl in [0, 10, 25, 50, 75, 100]:
            assert cfg.calculate_external(lvl) == lvl

    def test_deep_dimming_contrast(self, tmp_path):
        cfg_file = str(tmp_path / "test_config.json")
        cfg = ConfigManager(cfg_file)
        cfg.set("deep_dimming", True)
        assert cfg.calculate_contrast(100) == 50
        assert cfg.calculate_contrast(50) == 50
        assert cfg.calculate_contrast(40) == 50
        assert cfg.calculate_contrast(20) == 30
        assert cfg.calculate_contrast(0) == 10


class TestBrightnessController:
    """BrightnessController uchun testlar."""

    def test_controller_initialization(self):
        controller = BrightnessController()
        assert controller._user32 is not None
        assert controller._dxva2 is not None
        controller.close()

    def test_get_laptop_brightness_bounds(self):
        controller = BrightnessController()
        val = controller.get_laptop_brightness()
        if val is not None:
            assert 0 <= val <= 100
        controller.close()

    def test_get_external_monitors_info_format(self):
        controller = BrightnessController()
        info = controller.get_external_monitors_info()
        assert isinstance(info, list)
        for mon in info:
            assert "current" in mon
            assert "min" in mon
            assert "max" in mon
            assert mon["min"] <= mon["current"] <= mon["max"]
        controller.close()

    def test_bounds_clamping_on_set_brightness(self):
        controller = BrightnessController()
        with patch.object(controller, "_init_physical_monitors"):
            with patch.object(controller, "_cached_monitors", []):
                res_neg = controller.set_external_brightness(-50)
                assert res_neg == 0

                res_pos = controller.set_external_brightness(150)
                assert res_pos == 0
        controller.close()

    def test_get_status_structure(self):
        controller = BrightnessController()
        status = controller.get_status()
        assert "laptop_brightness" in status
        assert "external_monitors" in status
        assert "in_sync" in status
        assert isinstance(status["in_sync"], bool)
        controller.close()


class TestBrightnessSyncDaemon:
    """BrightnessSyncDaemon uchun testlar."""

    def test_daemon_sync_once_with_mock(self, tmp_path):
        cfg_file = str(tmp_path / "test_config.json")
        cfg = ConfigManager(cfg_file)

        mock_controller = MagicMock()
        mock_controller.get_laptop_brightness.return_value = 85

        daemon = BrightnessSyncDaemon(
            config=cfg,
            controller=mock_controller,
        )

        res = daemon.sync_once()
        assert res == 85
        mock_controller.get_laptop_brightness.assert_called_once()
        assert daemon._target_brightness == 85

    def test_daemon_lifecycle_start_and_stop(self, tmp_path):
        cfg_file = str(tmp_path / "test_config.json")
        cfg = ConfigManager(cfg_file)

        mock_controller = MagicMock()
        mock_controller.get_laptop_brightness.return_value = 50
        mock_controller.set_external_brightness.return_value = 1

        daemon = BrightnessSyncDaemon(
            config=cfg,
            controller=mock_controller,
        )

        daemon.start(non_blocking=True)
        assert daemon._running is True
        assert daemon._worker_thread is not None
        assert daemon._worker_thread.is_alive()
        assert daemon._listener_thread is not None

        time.sleep(0.1)
        daemon.stop()
        assert daemon._running is False
        assert daemon._worker_thread is None
        assert daemon._listener_thread is None
