import os
import re
import subprocess
import pytest

SCRIPT_DESKTOP = r"C:\Users\MuzaffarZed\Desktop\Musiqa_Yuklovchi.bat"
SCRIPT_WORKSPACE = r"C:\Users\MuzaffarZed\ai_workspace\Musiqa_Yuklovchi.bat"

def test_script_files_exist():
    """Verify script exists on Desktop and Workspace."""
    assert os.path.exists(SCRIPT_DESKTOP), f"Missing: {SCRIPT_DESKTOP}"
    assert os.path.exists(SCRIPT_WORKSPACE), f"Missing: {SCRIPT_WORKSPACE}"

def test_script_encoding_and_markers():
    """Verify polyglot batch/powershell structure and encoding."""
    with open(SCRIPT_DESKTOP, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "@echo off" in content
    assert "chcp 65001" in content
    assert "::POWERSHELL_BEGIN::" in content
    assert "Format-CleanTitle" in content
    assert "Select-AudioDSPProfile" in content
    assert "Format-UsbDriveToFat32" in content
    assert "Speak-Notification" in content
    assert "Generate-PlaylistsAndIndex" in content
    assert "Invoke-LocalFolderCleaner" in content

def test_dsp_audio_and_bypass_args():
    """Verify presence of EBU R128 (-14 LUFS), balanced exciter and anti-bot bypass args."""
    with open(SCRIPT_DESKTOP, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "ejs:github" in content
    assert "player_client=mweb,android" in content
    assert "treble=g=1.5:f=11000" in content
    assert "bass=g=0.5:f=70" in content
    assert "alimiter=limit=-1.2dB" in content
    assert "loudnorm=I=-14:LRA=7:TP=-1.5" in content
    assert "--embed-thumbnail" in content
    assert "256K" in content
    assert "-N" in content
    assert "--concurrent-fragments" in content
    assert "--http-chunk-size" in content

def test_catalog_and_features():
    """Verify extended 2026 catalog, voice notification and new categories."""
    with open(SCRIPT_DESKTOP, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "Jaloliddin Ahmadaliyev" in content
    assert "Konsta" in content
    assert "Yangi_Xitlar_2026" in content
    assert "Tungi_Safar_va_Karvon" in content
    assert "Toyona_va_Shox_Lazgi" in content
    assert "Retro_Oltin_Fond" in content
    assert "Avto_VIP_Bass_Remix" in content
    assert "Choyxona_va_Diltortar" in content
    assert "SAPI.SpVoice" in content

def test_powershell_syntax_integrity():
    """Verify PowerShell parser reports 0 syntax errors on the embedded code."""
    ps_cmd = (
        f"$raw = [System.IO.File]::ReadAllText('{SCRIPT_DESKTOP}', [System.Text.Encoding]::UTF8); "
        "$marker = '::POWER' + 'SHELL_BEGIN::'; "
        "$idx = $raw.IndexOf($marker); "
        "if ($idx -ge 0) { "
        "    $psCode = $raw.Substring($idx + $marker.Length); "
        "    $tokens = $null; $errors = $null; "
        "    $null = [System.Management.Automation.Language.Parser]::ParseInput($psCode, [ref]$tokens, [ref]$errors); "
        "    if ($errors.Count -gt 0) { exit 1 } else { exit 0 } "
        "} else { exit 2 }"
    )
    result = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    assert result.returncode == 0, f"PowerShell syntax validation failed with code {result.returncode}"

def test_title_cleaning_logic():
    """Test simulated title cleaning regex against dirty YouTube titles."""
    sample_titles = [
        "Jaloliddin Ahmadaliyev - Janon (Official Music Video 2026)",
        "Jaloliddin Ahmadaliyev — Chaqirsam | Жалолиддин Ахмадалиев — Чакирсам",
        "Konsta & Timur - O'tadi kunlar [Premyera HD 1080p RizaNova]",
        "Yulduz Usmonova - Muhabbat | Юлдуз Усмонова - Мухаббат (Konsert 2024)",
        "Shohruhxon - Yurak | Panterra Studio (Official Audio)"
    ]
    
    for raw in sample_titles:
        part = re.split(r'\s*\|\s*|\s*//\s*', raw)[0]
        c = re.sub(r'[\(\[\{][^\)\]\}]*[\)\]\}]', ' ', part)
        c = re.sub(r'(?i)\b(official|music|video|audio|klip|clip|premyera|premiere|konsert|concert|rizanova|nevomusic|nevo|tarona|navouz|navo|panterra|shou-biznes|gita|milliy|zortv|sevimli|hd|4k|1080p|720p|mp3|lyric|lyrics|cover|soundtrack|ost|parodiya|jonli ijro|live|remix|full album|202\d|201\d)\b', ' ', c)
        c = re.sub(r'[ʻʼ`‘’“”…–—]', '', c)
        c = re.sub(r'[\'"]', '', c)
        c = re.sub(r'[^\w\s\.-]', ' ', c)
        clean = re.sub(r'\s+', ' ', c).strip(' -_.,')
        
        assert "Official" not in clean
        assert "RizaNova" not in clean
        assert "NevoMusic" not in clean
        assert "2026" not in clean
        assert len(clean) > 3
        # Ensure song title was NOT truncated to just artist
        if "Chaqirsam" in raw:
            assert "Chaqirsam" in clean
        if "Janon" in raw:
            assert "Janon" in clean
        if "Otadi" in clean or "tadi" in clean:
            assert "kunlar" in clean
