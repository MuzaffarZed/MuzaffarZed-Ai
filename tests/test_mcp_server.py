"""
tests/test_mcp_server.py — Unit Tests for JARVIS Windows Controller MCP Server
Validates registration and execution of all 17 MCP tools.
"""

import os
import pytest
import asyncio

# Ensure test mode is active
os.environ["JARVIS_TEST_MODE"] = "1"

from bridge.mcp_server import (
    app,
    windows_list_windows,
    windows_get_active_window,
    windows_focus_window,
    windows_close_window,
    windows_launch_app,
    windows_kill_process,
    windows_inspect_ui,
    windows_click_ui_element,
    windows_set_control_text,
    windows_type_text,
    windows_press_hotkey,
    windows_mouse_click,
    windows_mouse_move,
    windows_mouse_scroll,
    windows_capture_screen,
    windows_system_telemetry,
    windows_run_powershell,
)


def test_mcp_tools_registration():
    tools = asyncio.run(app.list_tools())
    assert len(tools) == 17
    tool_names = [t.name for t in tools]
    expected_tools = [
        "windows_list_windows",
        "windows_get_active_window",
        "windows_focus_window",
        "windows_close_window",
        "windows_launch_app",
        "windows_kill_process",
        "windows_inspect_ui",
        "windows_click_ui_element",
        "windows_set_control_text",
        "windows_type_text",
        "windows_press_hotkey",
        "windows_mouse_click",
        "windows_mouse_move",
        "windows_mouse_scroll",
        "windows_capture_screen",
        "windows_system_telemetry",
        "windows_run_powershell",
    ]
    for exp in expected_tools:
        assert exp in tool_names


def test_mcp_tools_execution():
    # Window management
    wins = windows_list_windows()
    assert len(wins) >= 1

    active = windows_get_active_window()
    assert active["success"] is True

    foc = windows_focus_window("Code")
    assert foc["success"] is True

    cls = windows_close_window("Code")
    assert cls["success"] is True

    # App orchestration
    launch = windows_launch_app("notepad")
    assert launch["success"] is True

    kill = windows_kill_process("notepad.exe")
    assert kill["success"] is True

    # UI Automation
    ui = windows_inspect_ui()
    assert len(ui) >= 1

    click_el = windows_click_ui_element("Save")
    assert click_el["success"] is True

    set_txt = windows_set_control_text("EditBox", "Test text")
    assert set_txt["success"] is True

    # Inputs
    typed = windows_type_text("Test Unicode")
    assert typed["success"] is True

    hotkey = windows_press_hotkey(["ctrl", "c"])
    assert hotkey["success"] is True

    m_click = windows_mouse_click(100, 100)
    assert m_click["success"] is True

    m_move = windows_mouse_move(200, 200)
    assert m_move["success"] is True

    m_scroll = windows_mouse_scroll(2)
    assert m_scroll["success"] is True

    # Perception & Telemetry
    sc = windows_capture_screen()
    assert sc["success"] is True

    tel = windows_system_telemetry()
    assert "cpu_percent" in tel

    ps = windows_run_powershell("Get-Process")
    assert ps["success"] is True
