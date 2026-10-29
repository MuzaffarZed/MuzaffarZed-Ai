import os
import subprocess
import tempfile
import requests
import pytest


def get_running_server_url() -> str:
    local_app = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    port_file = os.path.join(local_app, "UzbekMusiqaMarkaziPro", "running_port.txt")
    assert os.path.exists(port_file), "running_port.txt topilmadi — Musiqa_Markazi_Pro.exe ishga tushmagan!"
    with open(port_file, "r", encoding="utf-8") as f:
        port = int(f.read().strip())
    return f"http://127.0.0.1:{port}"


def test_v10_ui_assets_served():
    """Verify embedded GPU Studio UI (index.html, styles.css, app.js) is served with HTTP 200 and includes Cinema & Mini-Dock Restore controls."""
    base = get_running_server_url()
    for path in ["/", "/styles.css", "/app.js"]:
        r = requests.get(base + path, timeout=5)
        assert r.status_code == 200, f"{path} status={r.status_code}"
        assert len(r.text) > 500

    html = requests.get(base + "/", timeout=5).text
    assert "cinemaSeekSlider" in html
    assert "floatingPipDock" in html
    assert "btnRestoreFullWindow" in html
    assert "cinemaPlaylistContainer" in html
    assert "app-sidebar" in html
    assert "stage-topbar" in html
    assert "studioDrawer" in html
    assert "settingsPopover" in html
    assert "waveformHoverTooltip" in html
    assert "btnLiveKaraoke" in html

    js = requests.get(base + "/app.js", timeout=5).text
    assert "videoSourceNode" in js
    assert "syncVideoDockPlacement" in js
    assert "toggleVideoFullscreen" in js
    assert "getArtistMonogram" in js
    assert "downloadArtistTop5" in js
    assert "toggleLiveKaraokeMode" in js



def test_v10_init_catalog_and_profiles():
    """Verify /api/init returns 50+ artists, 16+ collections, 8 car folders, 8 Studio FX, and 5 Car Cabin profiles."""
    base = get_running_server_url()
    r = requests.get(base + "/api/init", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert len(data["artists"]) >= 50
    assert len(data["artistCategories"]) == 6
    assert len(data["collections"]) >= 16
    assert len(data["carFolders"]) >= 8
    assert len(data["eqFreqs"]) == 10
    assert len(data["studioFxPresets"]) >= 8
    assert len(data["carCabinProfiles"]) >= 5


def test_v10_library_and_usb_doctor():
    """Verify /api/library and /api/usb/doctor endpoints."""
    base = get_running_server_url()
    init_data = requests.get(base + "/api/init", timeout=5).json()
    base_dir = init_data["baseDir"]

    r_lib = requests.get(f"{base}/api/library?baseDir={base_dir}&folder=01_YANGI_XITLAR_2026&scope=all", timeout=5)
    assert r_lib.status_code == 200
    lib_data = r_lib.json()
    assert "items" in lib_data
    assert "storage" in lib_data

    r_doc = requests.post(
        base + "/api/usb/doctor",
        json={"baseDir": base_dir, "folder": "01_YANGI_XITLAR_2026"},
        timeout=10
    )
    assert r_doc.status_code == 200
    assert r_doc.json()["ok"] is True


def test_v10_live_trim_fx_mixtape_and_status_video():
    """Verify real C# FFmpeg execution of A-B Trim, Studio FX Bake, Non-Stop DJ Mixtape, and MP4 Status Video."""
    base = get_running_server_url()
    with tempfile.TemporaryDirectory() as tmp_dir:
        mp3_a = os.path.join(tmp_dir, "01 - Test One.mp3")
        mp3_b = os.path.join(tmp_dir, "02 - Test Two.mp3")

        # Generate two 4-second stereo MP3 files
        for p, freq in [(mp3_a, 440), (mp3_b, 554)]:
            subprocess.run(
                ["ffmpeg", "-y", "-f", "lavfi", "-i", f"sine=frequency={freq}:duration=4", "-ac", "2", "-ar", "44100", "-b:a", "192k", p],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )

        # 1. Test HTTP 206 Byte-Range Media Streaming
        r_stream = requests.get(
            f"{base}/stream?path={requests.utils.quote(mp3_a)}",
            headers={"Range": "bytes=0-1023"},
            timeout=5
        )
        assert r_stream.status_code == 206
        assert len(r_stream.content) == 1024

        # 2. Test A-B Audio Trimmer
        r_trim = requests.post(
            base + "/api/studio/trim",
            json={"path": mp3_a, "startSec": 0.5, "endSec": 2.5},
            timeout=15
        ).json()
        assert r_trim["ok"] is True
        assert os.path.exists(r_trim["outPath"])

        # 3. Test Studio FX Bake (Slowed + Reverb)
        r_fx = requests.post(
            base + "/api/studio/bake-fx",
            json={"path": mp3_a, "fxName": "🌊 Slowed + Reverb (Tungi Atmosfera)", "saveAsCopy": True},
            timeout=15
        ).json()
        assert r_fx["ok"] is True
        assert os.path.exists(r_fx["outPath"])

        # 4. Test Non-Stop DJ Mixtape Creator
        r_mix = requests.post(
            base + "/api/studio/mixtape",
            json={"paths": [mp3_a, mp3_b], "outDir": tmp_dir},
            timeout=20
        ).json()
        assert r_mix["ok"] is True
        assert os.path.exists(r_mix["outPath"])

        # 5. Test Instagram/Telegram Status Video MP4 Creator
        r_vid = requests.post(
            base + "/api/studio/status-video",
            json={"path": mp3_a, "startSec": 0.0, "durationSec": 3.0},
            timeout=20
        ).json()
        assert r_vid["ok"] is True
        assert os.path.exists(r_vid["outPath"])
        assert r_vid["outPath"].endswith(".mp4")
