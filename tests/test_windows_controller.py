"""
tests/test_windows_controller.py — Comprehensive Unit Tests for WindowsController
Validates Deep UI Automation, Window Management, Perception, and System Controls.
"""

import os
import pytest
from bridge.windows_controller import WindowsController, WindowInfo, UIControlInfo, get_windows_controller


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    monkeypatch.setenv("JARVIS_TEST_MODE", "1")


def test_controller_singleton():
    c1 = get_windows_controller()
    c2 = get_windows_controller()
    assert c1 is c2
    assert isinstance(c1, WindowsController)


def test_list_windows():
    c = WindowsController()
    windows = c.list_windows()
    assert len(windows) >= 1
    assert all(isinstance(w, WindowInfo) for w in windows)
    assert any("Code" in w.process_name or "Visual Studio" in w.title for w in windows)


def test_get_active_window():
    c = WindowsController()
    active = c.get_active_window()
    assert active is not None
    assert isinstance(active, WindowInfo)
    assert active.is_active is True


def test_focus_and_close_window():
    c = WindowsController()
    assert c.focus_window("Code") is True
    assert c.close_window("Code") is True


def test_inspect_ui():
    c = WindowsController()
    ui_elements = c.inspect_ui(max_depth=2)
    assert len(ui_elements) >= 1
    assert all(isinstance(e, UIControlInfo) for e in ui_elements)
    assert ui_elements[0].depth >= 1


def test_click_ui_element_and_type():
    c = WindowsController()
    assert c.click_ui_element("Save") is True
    assert c.type_text("Salom O'zbekiston!") is True
    assert c.set_control_text("SearchBox", "Telegram") is True


def test_mouse_and_hotkey_actions():
    c = WindowsController()
    assert c.mouse_click(500, 500, button="left") is True
    assert c.mouse_move(600, 600) is True
    assert c.mouse_scroll(-5) is True
    assert c.press_hotkey("ctrl", "c") is True
    assert c.press_hotkey("alt", "f4") is True


def test_launch_app_and_kill():
    c = WindowsController()
    assert c.launch_app("notepad") is True
    assert c.launch_app("https://google.com") is True
    assert c.kill_process("notepad.exe") is True


def test_capture_screen_and_window():
    c = WindowsController()
    res = c.capture_screen()
    assert res["success"] is True
    assert res["width"] > 0
    assert res["height"] > 0
    assert len(res["base64"]) > 10

    win_img = c.capture_window()
    assert win_img is not None


def test_system_telemetry():
    c = WindowsController()
    t = c.get_system_telemetry()
    assert "cpu_percent" in t
    assert "ram_percent" in t
    assert "ram_used_gb" in t
    assert "disk_free_gb" in t


def test_run_powershell():
    c = WindowsController()
    res = c.run_powershell("Get-Date")
    assert res["success"] is True
    assert res["exit_code"] == 0
