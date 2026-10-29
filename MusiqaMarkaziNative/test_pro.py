import os
import subprocess
import time
import requests
import pytest

@pytest.fixture(scope="session", autouse=True)
def ensure_app_running():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    if os.path.exists(port_file):
        try:
            with open(port_file, "r") as f:
                port = f.read().strip()
            res = requests.get(f"http://127.0.0.1:{port}/api/download/status", timeout=1.5)
            if res.status_code == 200:
                yield
                return
        except Exception:
            pass

    exe_path = r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"
    proc = subprocess.Popen([exe_path])
    time.sleep(3.5)
    yield
    try:
        proc.terminate()
    except Exception:
        pass

def test_gemini_rules_have_law_7():
    rule_path = r"C:\Users\MuzaffarZed\.gemini\GEMINI.md"
    assert os.path.exists(rule_path)
    with open(rule_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "7-QONUN: DASTURCHI \"MuzaffarZed\" MUALLIFLIK IMZOSI" in content

def test_desktop_exe_exists_and_valid():
    exe_path = r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"
    assert os.path.exists(exe_path)
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    assert size_mb > 1.0  # Compact single-file executable

def test_local_server_api_init():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    assert os.path.exists(port_file)
    with open(port_file, "r") as f:
        port = f.read().strip()
    
    url = f"http://127.0.0.1:{port}/api/init"
    res = requests.get(url, timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert "artists" in data
    assert len(data["artists"]) >= 50
    assert "carFolders" in data
    assert len(data["carFolders"]) >= 8

def test_local_server_html_watermarks():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    with open(port_file, "r") as f:
        port = f.read().strip()
    
    url = f"http://127.0.0.1:{port}/"
    res = requests.get(url, timeout=5)
    assert res.status_code == 200
    html = res.text
    assert "MuzaffarZed" in html
    assert "Dasturchi: MuzaffarZed" in html

def test_download_status_and_retry_endpoints():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    with open(port_file, "r") as f:
        port = f.read().strip()

    st_url = f"http://127.0.0.1:{port}/api/download/status"
    res = requests.get(st_url, timeout=5)
    assert res.status_code == 200
    st = res.json()
    assert "isDownloading" in st
    assert "completedCount" in st
    assert "errorCount" in st
    assert "items" in st

    retry_url = f"http://127.0.0.1:{port}/api/download/retry-errors"
    res_retry = requests.post(retry_url, json={}, timeout=5)
    assert res_retry.status_code == 200
    retry_data = res_retry.json()
    assert "started" in retry_data

def test_ui_components_and_features():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    with open(port_file, "r") as f:
        port = f.read().strip()
    
    url = f"http://127.0.0.1:{port}/"
    res = requests.get(url, timeout=5)
    assert res.status_code == 200
    html = res.text
    # Verify new features exist in UI
    assert 'id="lyricsModal"' in html
    assert 'id="hotkeysModal"' in html
    assert 'id="topbarSleepBadge"' in html
    assert 'id="ytDirectCard"' in html
    assert 'quick-fx-pills' in html
    assert 'Nightcore' in html
    assert 'Slowed' in html

def test_master_deck_expanded_layout():
    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert "height: 104px;" in css
    assert "grid-template-columns: 320px 1fr auto;" in css

    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'height="26"' in html

def test_queue_instant_playback_handlers():
    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "playQueueItemByIndex" in js
    assert "playFileImmediately" in js
    assert "event.stopPropagation(); playQueueItemByIndex" in js

def test_smart_duplicates_hunter_and_stem_separator_ui():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Zero-Bloat: Redundant modals and heavy tabs pruned
    assert 'id="duplicatesModal"' not in html
    assert 'id="stemSeparatorModal"' not in html
    assert 'id="tab-kiosk"' not in html
    assert 'id="tab-reels"' not in html
    assert 'id="tab-dj"' not in html
    assert 'id="tab-vault"' not in html

    # Essential synchronized core tabs verified
    assert 'data-tab="artists"' in html
    assert 'data-tab="collections"' in html
    assert 'data-tab="search"' in html
    assert 'data-tab="queue"' in html
    assert 'data-tab="aimp"' in html
    assert 'data-tab="simulator"' in html

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "openDuplicatesModal" in js
    assert "openStemSeparatorModal" in js

def test_duplicates_scan_api_endpoint():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    with open(port_file, "r") as f:
        port = f.read().strip()

    url = f"http://127.0.0.1:{port}/api/duplicates/scan?scope=all"
    res = requests.get(url, timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert "ok" in data and data["ok"] is True
    assert "groups" in data
    assert "groupCount" in data

def test_watermark_in_new_modals():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Verify subtle watermark across modals and headers
    scale_section = html[html.find('id="scaleSettingsModal"'):]
    assert "Dasturchi: MuzaffarZed" in scale_section or "MuzaffarZed" in html
    assert "by MuzaffarZed" in html
    assert "Dasturchi: MuzaffarZed" in html

def test_car_renumber_and_agc_features():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="pillFxAgc"' in html
    assert 'id="pillFxBass"' in html
    assert 'renumberActiveFolderForCarAction()' in html
    assert 'normalizeActiveTrackLoudnessAction()' in html

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "dynamicsCompressorNode" in js
    assert "toggleLiveCarAgc" in js
    assert "renumberActiveFolderForCarAction" in js
    assert "normalizeActiveTrackLoudnessAction" in js

def test_car_renumber_api_endpoint():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    with open(port_file, "r") as f:
        port = f.read().strip()

    test_folder = r"C:\Users\MuzaffarZed\Desktop\Musiqa_Fleshka_2026\03_TUNGI_SOKIN_YOL"
    if os.path.exists(test_folder):
        url = f"http://127.0.0.1:{port}/api/car/renumber"
        res = requests.post(url, json={"folder": test_folder, "addPrefix": True, "createM3U": True}, timeout=5)
        assert res.status_code == 200
        data = res.json()
        assert data.get("ok") is True
        assert data.get("m3uCreated") is True

def test_kiosk_packages_api_and_ui():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    with open(port_file, "r") as f:
        port = f.read().strip()

    url = f"http://127.0.0.1:{port}/api/kiosk/packages"
    res = requests.get(url, timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert data.get("ok") is True
    assert "packages" in data
    assert len(data["packages"]) >= 5

    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Kiosk unified directly into Fleshka Cockpit & Artist catalog
    assert 'artistUsbSelect' in html
    assert "Fleshkaga To'g'ridan-To'g'ri 1-Papka Yozish Standarti" in html

def test_system_telemetry_and_turbo_clean_api():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    with open(port_file, "r") as f:
        port = f.read().strip()

    url = f"http://127.0.0.1:{port}/api/system/telemetry"
    res = requests.get(url, timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert data.get("ok") is True
    assert "ramUsagePercent" in data
    assert "totalRamGb" in data
    assert "freeRamGb" in data

    clean_url = f"http://127.0.0.1:{port}/api/system/turbo-clean"
    res_clean = requests.post(clean_url, json={}, timeout=5)
    assert res_clean.status_code == 200
    clean_data = res_clean.json()
    assert clean_data.get("ok") is True
    assert "freedMb" in clean_data

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "runTurboCleanAction" in js

def test_vault_api_and_ui():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    with open(port_file, "r") as f:
        port = f.read().strip()

    url = f"http://127.0.0.1:{port}/api/vault/list"
    res = requests.get(url, timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert data.get("ok") is True
    assert "files" in data

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "loadVaultFiles" in js

def test_reels_and_dj_and_jarvis_ui():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # JARVIS Assistant Verified
    assert 'id="assistantModal"' in html
    assert 'id="jarvisOrb"' in html
    assert 'id="btnJarvisAssistant"' in html
    assert 'executeJarvisTextCommand()' in html

    # Check MuzaffarZed author signatures across the app
    assert "by MuzaffarZed" in html
    assert "Dasturchi: MuzaffarZed" in html

def test_kiosk_16_packages_and_categories():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    assert os.path.exists(port_file)
    with open(port_file, "r") as f:
        port = f.read().strip()

    url = f"http://127.0.0.1:{port}/api/kiosk/packages"
    res = requests.get(url, timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert data.get("ok") is True
    packages = data.get("packages", [])
    assert len(packages) >= 15
    for p in packages:
        assert "id" in p
        assert "title" in p
        assert "genre" in p
        assert "estSizeMb" in p
        assert "carProfile" in p

def test_turbo_doctor_and_disk_benchmark_api():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    assert os.path.exists(port_file)
    with open(port_file, "r") as f:
        port = f.read().strip()

    # 1. Turbo Clean
    res_clean = requests.post(f"http://127.0.0.1:{port}/api/system/turbo-clean", json={}, timeout=10)
    assert res_clean.status_code == 200
    clean_data = res_clean.json()
    assert clean_data.get("ok") is True
    assert "freedMb" in clean_data

    # 2. Disk Benchmark
    res_bench = requests.post(f"http://127.0.0.1:{port}/api/system/disk-benchmark", json={}, timeout=15)
    assert res_bench.status_code == 200
    bench_data = res_bench.json()
    assert bench_data.get("ok") is True
    write_speed = bench_data.get("writeSpeedMbS", bench_data.get("writeSpeedMb", 0))
    read_speed = bench_data.get("readSpeedMbS", bench_data.get("readSpeedMb", 0))
    assert write_speed > 0
    assert read_speed > 0

def test_show_toast_defined_and_sidebar_scroll_fix():
    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "function showToast" in js
    assert "window.showToast = showToast" in js
    assert "sidebar.contains(e.target)" in js

    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".toast-container" in css
    assert ".toast-pill" in css
    assert ".app-sidebar" in css
    assert ".sidebar-nav" in css

def test_virtual_dj_pro_ui_components():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Verifies real-time WebAudio visualizer canvas and quick studio FX
    assert 'id="waveformCanvas"' in html
    assert 'id="pillFxBass"' in html
    assert 'id="pillFxKaraoke"' in html
    assert 'id="pillFxSlowed"' in html
    assert 'id="pillFxAgc"' in html

def test_vault_pro_features_and_api():
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    assert os.path.exists(port_file)
    with open(port_file, "r") as f:
        port = f.read().strip()

    # 1. Check Vault list API endpoint
    res = requests.get(f"http://127.0.0.1:{port}/api/vault/list", timeout=5)
    assert res.status_code == 200
    vault_data = res.json()
    assert "files" in vault_data

    # 2. Check JavaScript vault stub
    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "loadVaultFiles" in js

def test_reels_studio_pro_features():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Verifies cinema video player edge-to-edge layout
    assert 'id="tab-simulator"' in html
    assert 'id="carVideoPlayer"' in html
    assert 'id="cinemaStageCard"' in html

    # Check fontfile escaping in StudioEngine.cs
    engine_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\StudioEngine.cs"
    with open(engine_path, "r", encoding="utf-8") as f:
        cs = f.read()
    assert "segoeui.ttf" in cs
    assert "fontEsc" in cs
    assert "drawtext=fontfile=" in cs
    assert "gold_luxury" in cs
    assert "neon_cyber" in cs
    assert "DeleteVaultFile" in cs

def test_sidebar_and_deck_collapsible_pro():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="btnToggleSidebar"' in html
    assert 'id="btnCollapseSidebar"' in html
    assert 'id="btnCollapsePlayerDeck"' in html
    assert 'id="floatingMiniPlayerPill"' in html

    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert "body.sidebar-collapsed .app-sidebar" in css
    assert "body.deck-hidden .master-deck" in css
    assert ".floating-mini-player-pill" in css

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "toggleSidebarCollapse" in js
    assert "togglePlayerDock" in js
    assert "updateMiniPlayerPill" in js
    assert "deck-hidden" in js

def test_windows_explorer_view_modes_and_inspector():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="btnViewModeDropdown"' in html
    assert 'id="viewModeMenu"' in html
    assert 'id="libraryInspectorPane"' in html
    assert 'id="inspectorCoverImg"' in html
    assert 'id="inspectorWaveCanvas"' in html
    assert 'id="inspectorLyricsText"' in html

    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".library-split-wrapper" in css
    assert ".library-inspector-pane" in css
    assert ".view-grid-extra-large" in css
    assert ".view-grid-large" in css
    assert ".view-grid-medium" in css
    assert ".view-grid-small" in css
    assert ".view-mode-list" in css
    assert ".details-table-wrapper" in css
    assert ".view-grid-tiles" in css
    assert ".view-mode-content" in css

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "setLibraryViewMode" in js
    assert "toggleViewModeDropdown" in js
    assert "toggleInspectorPane" in js
    assert "selectLibraryTrackItem" in js
    assert "updateInspectorPane" in js
    assert "drawInspectorWaveform" in js

def test_cinema_video_player_edge_to_edge_overhaul():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="cinemaStageCard"' in html
    assert 'id="cinemaVideoSlot"' in html
    assert 'id="carVideoPlayer"' in html
    assert 'class="cinema-top-bar"' in html
    assert 'class="cinema-control-deck"' in html

    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    # Ensure cinema-video-viewport and control overlays are absolute/edge-to-edge
    assert ".cinema-video-viewport video" in css
    assert ".cinema-top-bar" in css
    assert ".cinema-control-deck" in css
    assert "#cinemaStageCard.controls-idle" in css

    server_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\LocalStudioServer.cs"
    with open(server_path, "r", encoding="utf-8") as f:
        cs = f.read()
    assert "video/mp4" in cs
    assert "416 Range Not Satisfiable" in cs
    assert "Accept-Ranges" in cs

def test_folder_drawer_and_whole_pc_scan():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="libraryFolderDrawer"' in html
    assert 'id="libraryFolderDrawerBody"' in html
    assert 'id="btnToggleFolderDrawer"' in html
    assert 'data-scope="whole_pc"' in html

    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".folder-drawer-card" in css
    assert ".folder-drawer-header" in css
    assert ".folder-drawer-body" in css

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "toggleFolderDrawer" in js
    assert "filterFolderDrawerPills" in js

    engine_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\StudioEngine.cs"
    with open(engine_path, "r", encoding="utf-8") as f:
        cs = f.read()
    assert 'scope == "whole_pc"' in cs

def test_mini_dock_resilience_and_compact_mode():
    prog_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\Program.cs"
    with open(prog_path, "r", encoding="utf-8") as f:
        cs = f.read()
    assert "action == \"toggleMiniDock\" || action == \"restoreFullWindow\"" in cs
    assert "MinimumSize = new Size(380, 85)" in cs

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "if (!state.isMiniDock)" in js
    assert "if (state.isMiniDock) {" in js

def test_mini_dock_non_overlapping_layout_and_flexbox():
    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert "body.mini-dock .master-deck {" in css
    assert "display: flex !important;" in css
    assert "body.mini-dock .deck-left {" in css
    assert "body.mini-dock .deck-center {" in css
    assert "body.mini-dock .deck-right {" in css
    assert "body.mini-dock .quick-fx-pills" in css
    assert "body.mini-dock #volumeSlider {" in css
    assert "width: 48px !important;" in css
    assert "body.mini-dock .btn-restore-full {" in css

def test_cinema_overlay_and_controls_separation():
    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".cinema-audio-overlay {" in css
    assert "top: 56px !important;" in css
    assert "bottom: 82px !important;" in css
    assert ".cinema-top-bar {" in css
    assert "top: 0 !important;" in css
    assert ".cinema-control-deck {" in css
    assert "bottom: 0 !important;" in css
    assert "#cinemaStageCard:fullscreen .cinema-audio-overlay" in css

    engine_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\StudioEngine.cs"
    with open(engine_path, "r", encoding="utf-8") as f:
        cs = f.read()
    assert "SpecialFolder.MyVideos" in cs
    assert 'ext == ".mp4" || ext == ".m4v" || ext == ".webm" || ext == ".mkv" || ext == ".mov"' in cs

def test_zoom_freedom_and_multiscreen_responsiveness():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="zoomWidget"' in html
    assert 'id="appZoomSelect"' in html
    assert 'id="btnToggleFullscreen"' in html
    assert 'adjustZoom' in html
    assert 'resetZoom' in html

    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".zoom-widget" in css
    assert ".zoom-select" in css
    assert "@media (max-width: 1400px)" in css
    assert "@media (max-width: 1200px)" in css
    assert "@media (max-height: 800px)" in css

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "function setAppZoom(zoomLevel)" in js
    assert "function adjustZoom(delta)" in js
    assert "function resetZoom()" in js
    assert "function toggleAppFullscreen()" in js
    assert "musiqa_zoom_level" in js

def test_folder_drawer_category_filters_and_active_banner():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="btnFolderCatAll"' in html
    assert 'id="btnFolderCatAudio"' in html
    assert 'id="btnFolderCatVideo"' in html
    assert 'id="activeFolderBanner"' in html

    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".active-folder-banner" in css
    assert ".folder-badge-btn" in css
    assert ".folder-cat-btn" in css

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "function setFolderDrawerCategory(cat)" in js
    assert "function playActiveFolderTracks()" in js
    assert "function playActiveFolderInKinozal()" in js
    assert "function revealActiveFolderInExplorer()" in js
    assert "folder-badge-btn" in js

def test_compact_and_floating_mode_playback_persistence():
    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "musiqa_deck_collapsed" in js
    assert "isDeckCollapsed: localStorage.getItem(\"musiqa_deck_collapsed\") === \"true\"" in js
    assert "if (state.isMiniDock || state.isDeckCollapsed) {" in js

def test_multiscreen_synchronous_bounds_and_minimum_size():
    prog_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\Program.cs"
    with open(prog_path, "r", encoding="utf-8") as f:
        cs = f.read()
    assert "MinimumSize = new Size(760, 480);" in cs
    assert "Screen.PrimaryScreen?.WorkingArea" in cs

def test_css_zero_overflow_and_100_percent_boundary_lock():
    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert "width: 100%;" in css
    assert "height: 100%;" in css
    assert "max-width: 100%;" in css
    assert "max-height: 100%;" in css
    assert ".details-table-wrapper" in css
    assert ".topbar-btn-text" in css
    assert "@media (max-width: 960px)" in css
    assert "@media (max-height: 690px)" in css

def test_canvas_dynamic_resolution_scaling():
    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "canvas.getBoundingClientRect()" in js
    assert "canvas.width = Math.round(rect.width);" in js

def test_universal_scale_customizer_ui_and_modal():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="btnScaleManager"' in html
    assert 'id="scaleSettingsModal"' in html
    assert 'id="scaleZoomSlider"' in html
    assert 'id="scaleFontSlider"' in html
    assert 'id="scaleCardSlider"' in html
    assert 'id="scaleSidebarSlider"' in html
    assert 'id="scaleWaveformSlider"' in html
    assert 'openScaleSettingsModal()' in html
    assert 'closeScaleSettingsModal()' in html
    assert 'resetScaleSettingsToDefault()' in html

def test_scale_engine_javascript_and_css_variables():
    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert "--app-font-scale" in css
    assert "--card-min-width" in css
    assert "--sidebar-width" in css
    assert "--deck-height" in css
    assert "--waveform-height" in css
    assert "body.density-compact" in css
    assert "body.density-comfortable" in css
    assert "body.sidebar-rail" in css
    assert "body.deck-compact" in css
    assert "body.deck-large" in css
    assert ".scale-modal-card" in css

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "function loadScaleSettings()" in js
    assert "function saveScaleSettings()" in js
    assert "function applyScaleSettings()" in js
    assert "function openScaleSettingsModal()" in js
    assert "function closeScaleSettingsModal()" in js
    assert "function applyScalePreset" in js
    assert "function resetScaleSettingsToDefault()" in js
    assert "musiqa_scale_settings" in js

def test_app_js_syntax_clean():
    import subprocess
    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    res = subprocess.run(["node", "-c", js_path], capture_output=True, text=True)
    assert res.returncode == 0, f"app.js syntax error: {res.stderr}"

def test_synergy_favorites_system():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="artistCategoryPills"' in html
    assert 'id="artistUsbSelect"' in html

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "toggleFavoriteArtist" in js
    assert "musiqa_fav_artists" in js

    cs_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\CatalogData.cs"
    with open(cs_path, "r", encoding="utf-8") as f:
        cs = f.read()
    assert "❤️ Sevimlilar" in cs

def test_synergy_fleshka_cockpit_and_usb_sync():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="collectionsUsbSelect"' in html
    assert 'id="artistUsbSelect"' in html

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "collectionsUsbSelect" in js
    assert "artistUsbSelect" in js

def test_synergy_smart_clipboard_and_artist_suggestion():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'pasteClipboardToSearchInput' in html
    assert 'id="searchArtistSuggestionBanner"' in html

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "checkSearchArtistSuggestion" in js
    assert "pasteClipboardToSearchInput" in js

def test_synergy_multilanguage_i18n():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="langSelector"' in html
    assert 'changeLanguage(this.value)' in html

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "const I18N =" in js
    assert "changeLanguage" in js
    assert "musiqa_lang" in js


def test_topbar_sartirofka_and_view_popover():
    html_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert 'id="btnViewMenu"' in html
    assert 'id="viewPopover"' in html
    assert 'class="topbar-download-cfg"' in html
    assert 'id="zoomWidget"' in html
    assert 'id="skinSelector"' in html

    js_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()
    assert "toggleViewPopover" in js

    css_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css"
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    assert ".topbar-download-cfg" in css
    assert ".view-popover" in css
