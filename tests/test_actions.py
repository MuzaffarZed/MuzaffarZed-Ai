"""
Unit tests for Actions Subsystem (SystemActions)
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

os.environ["JARVIS_TEST_MODE"] = "1"

from actions.system_actions import SystemActions, get_system_actions


def test_system_actions_telemetry():
    actions = SystemActions()
    telemetry = actions.get_telemetry()
    assert "CPU:" in telemetry
    assert "RAM:" in telemetry
    assert "Disk:" in telemetry
    assert "janob" in telemetry


def test_system_actions_volume_and_media():
    actions = SystemActions()
    # In test mode, these execute safely without error
    assert actions.volume_up() is True
    assert actions.volume_down() is True
    assert actions.volume_mute() is True
    assert actions.media_play_pause() is True
    assert actions.media_next() is True


def test_system_actions_launchers():
    actions = SystemActions()

    with patch("subprocess.Popen") as mock_popen:
        assert actions.open_notepad() is True
        mock_popen.assert_called_with(["notepad.exe"])

    with patch("subprocess.Popen") as mock_popen:
        assert actions.open_taskmgr() is True
        mock_popen.assert_called_with(["taskmgr.exe"])

    with patch("webbrowser.open") as mock_browser:
        assert actions.search_google("sun'iy intellekt") is True
        mock_browser.assert_called_once()
        assert "q=sun%27iy+intellekt" in mock_browser.call_args[0][0]


def test_system_actions_clipboard():
    actions = SystemActions()
    actions.copy_to_clipboard("JARVIS Test")
    read_text = actions.read_clipboard()
    assert "JARVIS Test" in read_text


def test_system_actions_singleton():
    a1 = get_system_actions()
    a2 = get_system_actions()
    assert a1 is a2
