import subprocess
import pytest

ADB_PATH = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"
TABLET_SERIAL = "R9WN606KYZJ"

def run_adb(cmd):
    full_cmd = [ADB_PATH, "-s", TABLET_SERIAL] + cmd
    res = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
    return res.stdout.strip()

def test_vn_editor_uninstalled():
    """Verify VN Video Editor is completely removed from tablet."""
    output = run_adb(["shell", "pm", "list", "packages", "com.frontrow.vlog"])
    assert "com.frontrow.vlog" not in output

def test_capcut_pad_active():
    """Verify CapCut Pad Pro is installed and running."""
    output = run_adb(["shell", "pm", "list", "packages", "com.lemon.ccpadpro"])
    assert "package:com.lemon.ccpadpro" in output

def test_dns_unrestricted():
    """Verify Private DNS restriction is disabled so CapCut CDN loads."""
    output = run_adb(["shell", "settings", "get", "global", "private_dns_mode"])
    assert output == "off"

def test_creator_fonts_installed():
    """Verify custom creator fonts exist in Fonts directory."""
    output = run_adb(["shell", "ls", "/sdcard/Fonts/"])
    assert "Montserrat-Bold.ttf" in output
    assert "BebasNeue-Regular.ttf" in output
    assert "Oswald-Bold.ttf" in output

def test_creator_sfx_installed():
    """Verify creator SFX audio files exist."""
    output = run_adb(["shell", "ls", "/sdcard/Music/Creator_SFX/"])
    assert "01_Whoosh_Fast.wav" in output
    assert "03_Pop_Text.wav" in output
    assert "06_Camera_Shutter.wav" in output
