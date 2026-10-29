"""
tests/test_stress_and_chaos.py — High-Intensity Stress & Chaos Engineering Test Suite
Subjects the J.A.R.V.I.S Windows Controller, MCP Server, and Daemon to extreme edge cases:
1. Concurrency Hammer: 20 parallel threads slamming OS queries and telemetry simultaneously.
2. Unicode Torture: Massive strings, emojis, Arabic, Cyrillic, zero-width joiners, and Uzbek diacritics.
3. Coordinate & Geometry Bounds: Negative, zero, floating, massive, and NaN coordinates.
4. Phantom & Dead Windows: Operations on non-existent titles, handles, and processes.
5. Fault Injection: Corrupt PowerShell scripts, command timeouts, and invalid UIA traversal depths.
6. Resource Leak & Lifecycle Endurance: Rapid start/stop cycles of daemons, threads, and listeners.
"""

from __future__ import annotations

import concurrent.futures
import os
import sys
import threading
import time
from typing import Any

import pytest
from starlette.testclient import TestClient

# Ensure test mode is active for safe hermetic chaos testing
os.environ["JARVIS_TEST_MODE"] = "1"

from bridge.windows_controller import WindowsController, get_windows_controller
from bridge.mcp_server import (
    app,
    windows_capture_screen,
    windows_click_ui_element,
    windows_focus_window,
    windows_inspect_ui,
    windows_list_windows,
    windows_mouse_click,
    windows_press_hotkey,
    windows_run_powershell,
    windows_system_telemetry,
    windows_type_text,
)
from daemon.elevated_server import app as daemon_app
from senses.wake_listener import WakeListener


@pytest.fixture
def controller() -> WindowsController:
    return WindowsController()


@pytest.fixture
def daemon_client() -> TestClient:
    return TestClient(daemon_app)


# =============================================================================
# 1. UNICODE & STRING TORTURE TESTS
# =============================================================================

def test_unicode_and_diacritic_torture(controller: WindowsController):
    """Feeds extreme Unicode, Uzbek diacritics, Cyrillic, RTL Arabic, and emoji sequences."""
    torture_strings = [
        # Uzbek specific diacritics & grammar
        "O‘zbekiston Respublikasi — kelajagi buyuk davlat! G‘alaba, qo‘zg‘olon, shiddat, cho‘l.",
        # Multilingual & mixed scripts
        "English + O‘zbekcha + Русский текст + 中文测试 + العربية (Al-Arabiyya)",
        # Emoji and modifier sequences
        "🚀🎯🔥🤖💻🛡️👑⚡🌟🎉👨‍💻👩‍💻🏳️‍🌈",
        # Special symbols, quotes, control characters
        "\"Quote' 'single' `backtick` ~!@#$%^&*()_+=-{}[]|:;<>?,./\n\t\r",
        # Massive repeating string (10,000 characters)
        "J.A.R.V.I.S " * 800,
        # Empty and whitespace variations
        "",
        "   ",
        "\t\n\r",
    ]

    for s in torture_strings:
        assert controller.type_text(s) is True
        assert controller.set_control_text("SearchField", s) is True


# =============================================================================
# 2. COORDINATE & GEOMETRY BOUNDARY CHAOS
# =============================================================================

def test_extreme_coordinate_chaos(controller: WindowsController):
    """Tests extreme negative, out-of-screen, and zero coordinates."""
    coordinates = [
        (-1, -1),
        (-99999, -99999),
        (0, 0),
        (1920, 1080),
        (99999, 99999),
        (1000000, 1000000),
    ]

    for x, y in coordinates:
        # Must clamp or handle safely without throwing unhandled exceptions
        assert controller.mouse_click(x, y, button="left") is True
        assert controller.mouse_click(x, y, button="right", clicks=2) is True
        assert controller.mouse_move(x, y) is True

    # Test invalid mouse buttons
    assert controller.mouse_click(100, 100, button="middle") is True


def test_mouse_scroll_extremes(controller: WindowsController):
    """Tests extreme scroll deltas."""
    for clicks in [-1000, -10, 0, 10, 1000]:
        assert controller.mouse_scroll(clicks) is True


# =============================================================================
# 3. PHANTOM WINDOWS & PROCESS CHAOS
# =============================================================================

def test_phantom_window_management(controller: WindowsController):
    """Interacts with completely non-existent windows, empty queries, and garbage."""
    bogus_queries = [
        "NonExistent_Ghost_Window_XYZ_999999",
        "___!@#$%^&*()___",
        "",
        "   ",
        "\x00\x01\x02",
        "RandomTitleThatDoesNotExistAtAll_1234567890",
    ]

    for query in bogus_queries:
        # In test mode or live mode, must not crash
        res_focus = controller.focus_window(query)
        assert isinstance(res_focus, bool)

        res_close = controller.close_window(query)
        assert isinstance(res_close, bool)

        res_ui = controller.inspect_ui(window_query=query)
        assert isinstance(res_ui, list)


def test_phantom_process_kill(controller: WindowsController):
    """Attempts to kill imaginary process names and invalid PIDs."""
    phantom_processes = [
        "definitely_not_a_real_process_12345.exe",
        "-9999",
        "9999999",
        "",
        "   ",
    ]

    for p in phantom_processes:
        res = controller.kill_process(p)
        assert isinstance(res, bool)


# =============================================================================
# 4. DEEP UI AUTOMATION (UIA) STRESS & EDGE DEPTHS
# =============================================================================

def test_uia_inspection_depth_extremes(controller: WindowsController):
    """Tests extreme hierarchy depths for UIA traversal."""
    for depth in [-5, 0, 1, 5, 20]:
        elements = controller.inspect_ui(max_depth=depth)
        assert isinstance(elements, list)
        for el in elements:
            assert hasattr(el, "name")
            assert hasattr(el, "control_type")
            assert hasattr(el, "automation_id")
            assert hasattr(el, "rect")


def test_uia_click_and_set_text_edge_cases(controller: WindowsController):
    """Tests clicking and typing on edge-case element names."""
    bogus_elements = [
        "NonExistentButton_123",
        "",
        "   ",
        "Button With Spaces And Specials !@#$%",
    ]

    for el in bogus_elements:
        res_click = controller.click_ui_element(el)
        assert isinstance(res_click, bool)

        res_txt = controller.set_control_text(el, "Some text")
        assert isinstance(res_txt, bool)


# =============================================================================
# 5. CONCURRENCY & MULTI-THREADING HAMMER (20 PARALLEL WORKERS)
# =============================================================================

def test_concurrency_hammer_on_windows_controller(controller: WindowsController):
    """
    Sits 20 worker threads in a thread pool and hammers controller methods simultaneously:
    list_windows, get_active_window, telemetry, screen capture, hotkeys.
    Ensures zero deadlocks and zero race conditions.
    """
    num_workers = 20
    iterations_per_worker = 5

    def worker_task(worker_id: int) -> bool:
        for _ in range(iterations_per_worker):
            wins = controller.list_windows()
            assert len(wins) >= 1

            act = controller.get_active_window()
            assert act is not None

            tel = controller.get_system_telemetry()
            assert "cpu_percent" in tel

            sc = controller.capture_screen()
            assert sc["success"] is True

            hk = controller.press_hotkey("ctrl", "shift", "a")
            assert hk is True

            mv = controller.mouse_move(100 + worker_id, 200 + worker_id)
            assert mv is True
        return True

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker_task, i) for i in range(num_workers)]
        for f in concurrent.futures.as_completed(futures):
            assert f.result() is True


# =============================================================================
# 6. FAULT INJECTION & POWERSHELL RESILIENCE
# =============================================================================

def test_powershell_fault_injection(controller: WindowsController):
    """Tests malformed syntax, non-existent cmdlets, and commands."""
    commands = [
        "ThisIsNotAValidPowerShellCommandAtAll -ErrorAction Stop",
        "Get-ChildItem -Path 'C:\\Path\\That\\Definitely\\Does\\Not\\Exist_9999'",
        "Write-Output 'Hello from test'; exit 0",
        "",
        "   ",
    ]

    for cmd in commands:
        res = controller.run_powershell(cmd)
        assert isinstance(res, dict)
        assert "success" in res
        assert "exit_code" in res


# =============================================================================
# 7. MCP SERVER HIGH-SPEED BURST TESTING
# =============================================================================

def test_mcp_burst_execution():
    """Rapidly bursts through all MCP tool calls in sequence."""
    for i in range(5):
        assert len(windows_list_windows()) >= 1
        assert windows_system_telemetry()["cpu_percent"] >= 0.0
        assert windows_focus_window(f"App_{i}")["success"] is True
        assert windows_type_text(f"Text burst iteration {i}")["success"] is True
        assert windows_mouse_click(50 * i, 50 * i)["success"] is True
        assert windows_press_hotkey(["ctrl", "c"])["success"] is True
        assert windows_click_ui_element(f"Button_{i}")["success"] is True
        assert windows_capture_screen()["success"] is True


# =============================================================================
# 8. REST DAEMON TORTURE & ERROR HANDLING
# =============================================================================

def test_daemon_rest_api_torture(daemon_client: TestClient):
    """Hammers daemon API with invalid payloads, high-frequency requests, and edge data."""
    # 1. Health & Telemetry bursts
    for _ in range(10):
        h = daemon_client.get("/health")
        assert h.status_code == 200
        assert h.json()["status"] == "online"

        t = daemon_client.get("/telemetry")
        assert t.status_code == 200

        w = daemon_client.get("/windows")
        assert w.status_code == 200

    # 2. Malformed / Missing payloads
    bad_payload = daemon_client.post("/exec", json={})
    assert bad_payload.status_code == 422  # Pydantic validation error

    bad_click = daemon_client.post("/click", json={"x": "invalid_number", "y": 100})
    assert bad_click.status_code == 422

    # 3. Extreme values in valid payload
    extreme_click = daemon_client.post("/click", json={"x": -9999, "y": 9999, "button": "left", "clicks": 10})
    assert extreme_click.status_code == 200
    assert extreme_click.json()["success"] is True

    # 4. Long text payload
    long_type = daemon_client.post("/type", json={"text": "A" * 5000})
    assert long_type.status_code == 200
    assert long_type.json()["success"] is True


# =============================================================================
# 9. WAKE-WORD LISTENER RAPID LIFECYCLE STRESS
# =============================================================================

def test_wake_listener_rapid_cycling():
    """Rapidly starts and stops WakeListener 10 times to detect thread leakage or hangs."""
    for i in range(10):
        listener = WakeListener(on_wake=lambda _: None)
        assert listener.running is False
        listener.start_listening()
        assert listener.running is True
        listener.play_wake_chime()
        listener.stop_listening()
        assert listener.running is False
