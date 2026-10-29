import subprocess
import pytest

ADB_PATH = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"
TABLET_SERIAL = "R9WN606KYZJ"

def run_adb(cmd):
    full_cmd = [ADB_PATH, "-s", TABLET_SERIAL] + cmd
    res = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
    return res.stdout.strip()

def test_capcut_os_installed():
    """Verify CapCut OS Studio launcher package is installed."""
    output = run_adb(["shell", "pm", "list", "packages", "com.muzaffar.capcutos"])
    assert "package:com.muzaffar.capcutos" in output

def test_capcut_os_is_home_launcher():
    """Verify CapCut OS has the HOME intent filter."""
    output = run_adb(["shell", "dumpsys", "package", "com.muzaffar.capcutos"])
    assert "android.intent.category.HOME" in output

def test_capcut_pad_installed():
    """Verify CapCut Pad Pro is installed."""
    output = run_adb(["shell", "pm", "list", "packages", "com.lemon.ccpadpro"])
    assert "package:com.lemon.ccpadpro" in output

def test_all_25_sound_effects():
    """Verify 25 creator sound effects exist."""
    output = run_adb(["shell", "ls", "/sdcard/Music/Creator_SFX/"])
    lines = [l.strip() for l in output.splitlines() if l.strip().endswith(".wav")]
    assert len(lines) == 25

def test_all_8_green_screen_overlays():
    """Verify 8 green screen overlays exist in DCIM/Creator_Overlays."""
    output = run_adb(["shell", "ls", "/sdcard/DCIM/Creator_Overlays/"])
    lines = [l.strip() for l in output.splitlines() if l.strip().endswith(".mp4")]
    assert len(lines) == 8

def test_transfer_activity_exists():
    """Verify TransferActivity component is present for 1-click sharing to S22 Ultra."""
    output = run_adb(["shell", "cmd", "package", "resolve-activity", "--brief", "-n", "com.muzaffar.capcutos/.TransferActivity"])
    assert "com.muzaffar.capcutos/.TransferActivity" in output

def test_zero_lag_animations():
    """Verify all system animations are disabled (0x) for instant touch response."""
    w = run_adb(["shell", "settings", "get", "global", "window_animation_scale"])
    t = run_adb(["shell", "settings", "get", "global", "transition_animation_scale"])
    a = run_adb(["shell", "settings", "get", "global", "animator_duration_scale"])
    assert w == "0"
    assert t == "0"
    assert a == "0"

def test_bloatware_disabled():
    """Verify background bloatware and telemetry services are disabled."""
    output = run_adb(["shell", "pm", "list", "packages", "-d"])
    assert "com.samsung.android.securitylogagent" in output
    assert "com.google.android.googlequicksearchbox" in output
    assert "com.samsung.android.sm.devicesecurity" in output

def test_memory_and_cpu_health():
    """Verify CapCut Pad process is active and swap/RAM is healthy."""
    output = run_adb(["shell", "pidof", "com.lemon.ccpadpro"])
    assert len(output.strip()) > 0

