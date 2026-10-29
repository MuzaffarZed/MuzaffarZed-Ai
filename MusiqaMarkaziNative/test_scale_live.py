import os
import time
import subprocess
import requests
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

def main():
    exe_path = r"C:\Users\MuzaffarZed\Desktop\Musiqa_Markazi_Pro.exe"
    port_file = os.path.expandvars(r"%LOCALAPPDATA%\UzbekMusiqaMarkaziPro\running_port.txt")
    
    port = None
    if os.path.exists(port_file):
        try:
            with open(port_file, "r") as f:
                p = int(f.read().strip())
            r = requests.post(f"http://127.0.0.1:{p}/api/native/action", json={"action": "evalJs", "code": "1+1"}, timeout=2)
            if r.status_code == 200:
                port = p
                print(f"[Port {port}] Using active Musiqa Markazi Pro instance.")
        except Exception:
            pass

    if port is None:
        subprocess.run(["powershell", "-NoProfile", "-Command", "Stop-Process -Name 'Musiqa_Markazi_Pro' -Force -ErrorAction SilentlyContinue"], capture_output=True)
        if os.path.exists(port_file):
            try: os.remove(port_file)
            except: pass
        print("Launching updated Musiqa_Markazi_Pro.exe...")
        proc = subprocess.Popen([exe_path])
        time.sleep(4)
        assert os.path.exists(port_file), "running_port.txt not found!"
        with open(port_file, "r") as f:
            port = int(f.read().strip())
        print(f"[Port {port}] App active and ready.")

    def eval_js(code):
        url = f"http://127.0.0.1:{port}/api/native/action"
        payload = {"action": "evalJs", "code": code}
        res = requests.post(url, json=payload, timeout=5)
        raw = res.json().get("result", "")
        try:
            return json.loads(raw)
        except Exception:
            return raw

    def capture_screenshot(filename):
        artifact_dir = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0"
        target_path = os.path.join(artifact_dir, filename)
        url = f"http://127.0.0.1:{port}/api/native/action"
        payload = {"action": "capturePreview", "path": target_path}
        res = requests.post(url, json=payload, timeout=6)
        print(f"Captured {filename}: {res.json()}")
    print("Waiting for WebView2 DOM and state initialization...")
    for i in range(15):
        try:
            ready = eval_js("typeof state !== 'undefined' && !!document.getElementById('btnScaleManager')")
            if ready is True:
                print(f"DOM & state ready at attempt {i+1}!")
                break
        except Exception:
            pass
        time.sleep(1)

    print("\n--- [TEST 1: Universal Scale Settings Initialization] ---")
    init_state = eval_js("""
    (() => {
        return {
            hasScaleSettings: !!state.scaleSettings,
            zoom: state.scaleSettings ? state.scaleSettings.zoom : 0,
            cardWidth: state.scaleSettings ? state.scaleSettings.cardWidth : 0,
            sidebarWidth: state.scaleSettings ? state.scaleSettings.sidebarWidth : 0,
            tableDensity: state.scaleSettings ? state.scaleSettings.tableDensity : '',
            deckSize: state.scaleSettings ? state.scaleSettings.deckSize : '',
            btnScaleManager: !!document.getElementById('btnScaleManager'),
            scaleSettingsModal: !!document.getElementById('scaleSettingsModal')
        };
    })()
    """)
    print("Initial Scale State:", init_state)
    assert init_state["hasScaleSettings"], "state.scaleSettings is missing!"
    assert init_state["btnScaleManager"], "#btnScaleManager is missing from topbar!"
    assert init_state["scaleSettingsModal"], "#scaleSettingsModal is missing from DOM!"
    print("=> TEST 1 PASSED: Scale engine initialized perfectly.")

    print("\n--- [TEST 2: Open Scale Settings Modal & Capture] ---")
    eval_js("openScaleSettingsModal();")
    time.sleep(0.5)
    modal_check = eval_js("""
    (() => {
        const m = document.getElementById('scaleSettingsModal');
        return {
            isOpen: m ? m.classList.contains('open') : false,
            zoomValText: document.getElementById('lblScaleZoomVal')?.textContent,
            fontValText: document.getElementById('lblScaleFontVal')?.textContent,
            cardValText: document.getElementById('lblScaleCardVal')?.textContent,
            densityValText: document.getElementById('lblScaleDensityVal')?.textContent
        };
    })()
    """)
    print("Modal Check:", modal_check)
    assert modal_check["isOpen"], "Modal did not open!"
    capture_screenshot("live_scale_modal_open.png")
    print("=> TEST 2 PASSED: Scale Settings Modal verified and captured.")

    print("\n--- [TEST 3: Dynamic Grid Cards Scaling (140px .. 290px)] ---")
    eval_js("closeScaleSettingsModal(); switchTab('artists');")
    time.sleep(0.3)
    eval_js("applyScalePreset('card', 260);")
    time.sleep(0.3)
    card_check = eval_js("""
    (() => {
        const root = document.documentElement;
        return {
            cardMinVar: root.style.getPropertyValue('--card-min-width'),
            gridCols: window.getComputedStyle(document.getElementById('artistsGrid') || document.body).gridTemplateColumns
        };
    })()
    """)
    print("Card Check (260px):", card_check)
    assert "260px" in card_check["cardMinVar"], "Card min-width variable not updated!"
    capture_screenshot("live_card_zoom_large.png")
    print("=> TEST 3 PASSED: Grid cards scaled dynamically.")

    print("\n--- [TEST 4: Table Density Modes (Compact vs Comfortable)] ---")
    eval_js("switchTab('aimp');")
    time.sleep(0.3)
    eval_js("applyScalePreset('density', 'compact');")
    time.sleep(0.3)
    compact_check = eval_js("""
    (() => {
        return {
            hasDensityCompact: document.body.classList.contains('density-compact')
        };
    })()
    """)
    print("Compact Check:", compact_check)
    assert compact_check["hasDensityCompact"], "body should have density-compact class!"
    capture_screenshot("live_density_compact.png")

    eval_js("applyScalePreset('density', 'comfortable');")
    time.sleep(0.3)
    comfortable_check = eval_js("""
    (() => {
        return {
            hasDensityComfortable: document.body.classList.contains('density-comfortable')
        };
    })()
    """)
    print("Comfortable Check:", comfortable_check)
    assert comfortable_check["hasDensityComfortable"], "body should have density-comfortable class!"
    capture_screenshot("live_density_comfortable.png")
    print("=> TEST 4 PASSED: Table density modes verified.")

    print("\n--- [TEST 5: Sidebar Icon Rail Mode (62px)] ---")
    eval_js("applyScalePreset('sidebar', 'rail');")
    time.sleep(0.3)
    rail_check = eval_js("""
    (() => {
        const sb = document.querySelector('.app-sidebar');
        return {
            hasSidebarRailClass: document.body.classList.contains('sidebar-rail'),
            sbWidth: sb ? sb.getBoundingClientRect().width : 0
        };
    })()
    """)
    print("Sidebar Rail Check:", rail_check)
    assert rail_check["hasSidebarRailClass"], "body should have sidebar-rail class!"
    assert rail_check["sbWidth"] <= 65, f"Sidebar width should be <= 65px in rail mode, got {rail_check['sbWidth']}"
    capture_screenshot("live_sidebar_rail_mode.png")
    print("=> TEST 5 PASSED: Sidebar rail mode verified.")

    print("\n--- [TEST 6: Large Studio Player Deck (104px)] ---")
    eval_js("applyScalePreset('sidebar', 232);")
    eval_js("applyScalePreset('deck', 'large');")
    eval_js("playRandomSurpriseTrack();")
    time.sleep(0.5)
    deck_check = eval_js("""
    (() => {
        const deck = document.querySelector('.master-deck');
        return {
            hasDeckLargeClass: document.body.classList.contains('deck-large'),
            deckHeight: deck ? deck.getBoundingClientRect().height : 0,
            hasTrack: !!state.currentTrack
        };
    })()
    """)
    print("Deck Large Check:", deck_check)
    assert deck_check["hasDeckLargeClass"], "body should have deck-large class!"
    assert deck_check["deckHeight"] >= 95, f"Deck height should be >= 95px in large mode, got {deck_check['deckHeight']}"
    capture_screenshot("live_deck_large_mode.png")
    print("=> TEST 6 PASSED: Large Studio deck verified.")

    print("\n--- [TEST 7: Reset All to Defaults] ---")
    eval_js("resetScaleSettingsToDefault();")
    time.sleep(0.3)
    reset_check = eval_js("""
    (() => {
        const root = document.documentElement;
        return {
            zoom: state.scaleSettings.zoom,
            fontScale: state.scaleSettings.fontScale,
            cardWidth: state.scaleSettings.cardWidth,
            sidebarWidth: state.scaleSettings.sidebarWidth,
            deckSize: state.scaleSettings.deckSize,
            tableDensity: state.scaleSettings.tableDensity,
            hasRail: document.body.classList.contains('sidebar-rail'),
            hasCompact: document.body.classList.contains('density-compact')
        };
    })()
    """)
    print("Reset Check:", reset_check)
    assert reset_check["zoom"] == 1.0
    assert reset_check["cardWidth"] == 210
    assert reset_check["sidebarWidth"] == 216
    assert not reset_check["hasRail"]
    assert not reset_check["hasCompact"]
    capture_screenshot("live_scale_defaults_perfect.png")
    print("=> TEST 7 PASSED: Reset to defaults verified.")

    print("\n========================================================")
    print(" ALL 7 UNIVERSAL SCALE AND CUSTOMIZER TESTS PASSED 100%! ")
    print("========================================================")

if __name__ == "__main__":
    main()
