import subprocess
import os
import pytest

ADB_PATH = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"
TABLET_SERIAL = "R9WN606KYZJ"

def run_adb(cmd):
    full_cmd = [ADB_PATH, "-s", TABLET_SERIAL] + cmd
    res = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
    return res.stdout.strip()

def test_vn_editor_installed():
    """Verify VN Video Editor is installed on Galaxy Tab A."""
    output = run_adb(["shell", "pm", "list", "packages", "com.frontrow.vlog"])
    assert "package:com.frontrow.vlog" in output

def test_vn_editor_version():
    """Verify VN Video Editor version is 2.17.0."""
    output = run_adb(["shell", "dumpsys", "package", "com.frontrow.vlog"])
    assert "versionName=2.17.0" in output

def test_vn_battery_whitelist():
    """Verify VN Video Editor is whitelisted from Doze / battery saver."""
    output = run_adb(["shell", "dumpsys", "deviceidle", "whitelist"])
    assert "com.frontrow.vlog" in output

def test_vn_exported_video():
    """Verify exported video exists and is in DCIM/VN."""
    output = run_adb(["shell", "ls", "-la", "/sdcard/DCIM/VN/"])
    assert ".mp4" in output

def test_capcut_pad_installed():
    """Verify CapCut Pad Pro is also installed and healthy."""
    output = run_adb(["shell", "pm", "list", "packages", "com.lemon.ccpadpro"])
    assert "package:com.lemon.ccpadpro" in output
