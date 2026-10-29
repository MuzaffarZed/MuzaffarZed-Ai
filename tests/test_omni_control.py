"""tests/test_omni_control.py - Unit tests for 3-layer OmniControl system."""

import pytest
from actions.omni_control import OmniControl, get_omni_controller, ActionResult


def test_omni_control_singleton():
    omni1 = get_omni_controller()
    omni2 = get_omni_controller()
    assert omni1 is omni2
    assert isinstance(omni1, OmniControl)


def test_omni_control_powershell_safe_execution():
    omni = OmniControl(failsafe=True)
    res = omni.run_powershell("Write-Output 'Salom Jarvis'")
    assert res.success is True
    assert "Salom Jarvis" in res.data.get("stdout", "")
    assert res.layer == "powershell"


def test_omni_control_powershell_dangerous_command_blocked():
    omni = OmniControl()
    res = omni.run_powershell("Format-Volume -DriveLetter D")
    assert res.success is False
    assert "bloklandi" in res.message.lower()


def test_omni_control_unicode_safe_typing():
    omni = OmniControl()
    text = "O‘zbekiston — buyuk kelajak sari intilmoqda! G‘oliblik, sharaf va cho‘qqilar."
    res = omni.type_unicode_safe(text)
    assert res.success is True
    assert res.layer == "keyboard"


def test_omni_control_hotkey_dispatch():
    omni = OmniControl()
    res = omni.send_hotkey("ctrl")
    assert res.success is True
    assert res.layer == "keyboard"


def test_omni_control_process_and_drives():
    omni = OmniControl()
    procs = omni.list_processes("python")
    assert isinstance(procs, list)
    drives = omni.get_removable_drives()
    assert isinstance(drives, list)


def test_omni_control_dispatch():
    omni = OmniControl()
    res1 = omni.dispatch("powershell", command="Write-Output 'Dispatch OK'")
    assert res1.get("status") == "success"

    res2 = omni.dispatch("type_text", text="Salom")
    assert res2.get("status") == "success"

    res3 = omni.dispatch("hotkey", keys=["ctrl"])
    assert res3.get("status") == "success"
