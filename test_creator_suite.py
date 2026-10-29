import subprocess
import pytest

ADB_PATH = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"
TABLET_SERIAL = "R9WN606KYZJ"

def run_adb(cmd):
    full_cmd = [ADB_PATH, "-s", TABLET_SERIAL] + cmd
    res = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
    return res.stdout.strip()

def test_ram_booster_installed():
    """Verify CapCut Boost (1-Click RAM Booster) is installed on Galaxy Tab A."""
    output = run_adb(["shell", "pm", "list", "packages", "com.muzaffar.capcutboost"])
    assert "package:com.muzaffar.capcutboost" in output

def test_capcut_pad_installed():
    """Verify CapCut Pad Pro is installed."""
    output = run_adb(["shell", "pm", "list", "packages", "com.lemon.ccpadpro"])
    assert "package:com.lemon.ccpadpro" in output

def test_all_25_sound_effects():
    """Verify all 25 creator sound effects are deployed to tablet."""
    output = run_adb(["shell", "ls", "/sdcard/Music/Creator_SFX/"])
    lines = [line.strip() for line in output.splitlines() if line.strip().endswith(".wav")]
    assert len(lines) == 25
    assert "11_Meme_Laugh.wav" in lines
    assert "18_Telegram_Notification.wav" in lines
    assert "21_Cinematic_Sub_Drop.wav" in lines
    assert "25_Swoosh_High.wav" in lines

def test_all_8_green_screen_overlays():
    """Verify all 8 creator green screen overlay videos exist on tablet."""
    output = run_adb(["shell", "ls", "/sdcard/DCIM/Creator_Overlays/"])
    lines = [line.strip() for line in output.splitlines() if line.strip().endswith(".mp4")]
    assert len(lines) == 8
    assert "01_Subscribe_Bell_Button.mp4" in lines
    assert "02_Like_ThumbsUp_Pop.mp4" in lines
    assert "03_Red_Arrow_Pointer.mp4" in lines
    assert "04_Countdown_5s.mp4" in lines
    assert "05_Question_Marks.mp4" in lines
    assert "06_Money_Cash_Rain.mp4" in lines
    assert "07_Fire_Energy_Flame.mp4" in lines
    assert "08_Heart_Love_Reactions.mp4" in lines

def test_creator_fonts_installed():
    """Verify creator fonts are installed in /sdcard/Fonts/."""
    output = run_adb(["shell", "ls", "/sdcard/Fonts/"])
    assert "Montserrat-Bold.ttf" in output
    assert "BebasNeue-Regular.ttf" in output
    assert "Oswald-Bold.ttf" in output
